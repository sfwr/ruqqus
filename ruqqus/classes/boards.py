from sqlalchemy import *
from sqlalchemy.orm import relationship
import time

from ruqqus.helpers.base36 import *
from ruqqus.helpers.security import *
from ruqqus.helpers.lazy import *
from .submission import *
from .board_relationships import *
from ruqqus.__main__ import Base, db, cache

class Board(Base):

    __tablename__="boards"

    id=Column(Integer, primary_key=True)
    name=Column(String)
    created_utc=Column(Integer)
    description = Column(String)
    description_html=Column(String)
    over_18=Column(Boolean, default=False)
    
    submissions=relationship("Submission", lazy="dynamic", backref="board", primaryjoin="Board.id==Submission.board_id")
    original_submissions=relationship("Submission", lazy="dynamic", backref="original_board", primaryjoin="Board.id==Submission.original_board_id")

    moderators = relationship("ModRelationship", lazy="dynamic", backref="board")
    bans = relationship("BanRelationship", lazy="dynamic", backref="board")
    postrels=relationship("PostRelationship", lazy="dynamic", backref="board")
    subscribers=relationship("Subscription", lazy="dynamic", backref="board")
    
    def __init__(self, **kwargs):

        kwargs["created_utc"]=int(time.time())

        super().__init__(**kwargs)

    @property
    @lazy
    def base36id(self):
        return base36encode(self.id)

    @property
    @cache.memoize(timeout=30)
    def mods(self):

        return self.moderators.filter_by(accepted=True).order_by(text("id")).all()

    @property
    @cache.memoize(timeout=30)
    def invited_mods(self):
        return self.moderators.filter_by(accepted=False).order_by(text("id")).all()

    @property
    def permalink(self):

        return f"/+{self.name}"

    def can_take(self, post):
        return self.postrels.filter_by(post_id=post.id).first()

    @cache.memoize(timeout=30)
    def idlist(self, sort="hot", page=1, nsfw=False):

        posts=db.query(Submission).filter_by(is_banned=False,
                                             is_deleted=False,
                                             stickied=False,
                                             board_id=self.id
                                             )

        if not nsfw:
            posts=posts.filter_by(over_18=False)

        if sort=="hot":
            posts=posts.order_by(text("submissions.rank_hot desc"))
        elif sort=="new":
            posts=posts.order_by(Submission.created_utc.desc())
        elif sort=="disputed":
            posts=posts.order_by(text("submissions.rank_fiery desc"))
        elif sort=="top":
            posts=posts.order_by(text("submissions.score desc"))
        elif sort=="activity":
            posts=posts.order_by(text("submissions.rank_activity desc"))
        else:
            abort(422)

        posts=[x.id for x in posts.offset(25*(page-1)).limit(26).all()]

        return posts

    def rendered_board_page(self, v, sort="hot", page=1):
        
        ids=self.idlist(sort=sort, page=page, nsfw=(v and v.over_18))

        next_exists=(len(ids)==26)
        ids=ids[0:25]

        if ids:

            #assemble list of tuples
            i=1
            tups=[]
            for x in ids:
                tups.append((x,i))
                i+=1

            tups=str(tups).lstrip("[").rstrip("]")

            #hit db for entries
            posts=db.query(Submission
                           ).from_statement(
                               text(
                               f"""
                                select submissions.*, submissions.ups, submissions.downs
                                from submissions
                                join (values {tups}) as x(id, n) on submissions.id=x.id
                                order by x.n"""
                               )).all()
        else:
            posts=[]

        return render_template("board.html", b=self, v=v, listing=posts, next_exists=next_exists, sort_method=sort, page=page)        


    @property
    def age_string(self):

        age=int(time.time()) - self.created_utc

        if age<60:
            return "just now"
        elif age<3600:
            minutes=int(age/60)
            return f"{minutes} minute{'s' if minutes>1 else ''} ago"
        elif age<86400:
            hours=int(age/3600)
            return f"{hours} hour{'s' if hours>1 else ''} ago"
        elif age<2592000:
            days=int(age/86400)
            return f"{days} day{'s' if days>1 else ''} ago"

        now=time.gmtime()
        ctd=time.gmtime(self.created_utc)
        months=now.tm_mon-ctd.tm_mon+12*(now.tm_year-ctd.tm_year)

        if months < 12:
            return f"{months} month{'s' if months>1 else ''} ago"
        else:
            years=int(months/12)
            return f"{years} year{'s' if years>1 else ''} ago"

    @cache.memoize(timeout=60)
    def has_mod(self, user):

        if user is None:
            return None

        return self.moderators.filter_by(user_id=user.id, accepted=True).first()


    @cache.memoize(timeout=60)
    def can_invite_mod(self, user):

        return user.id not in [x.user_id for x in self.moderators.all()]

    @cache.memoize(timeout=60)
    def has_invite(self, user):

        return self.moderators.filter_by(user_id=user.id, accepted=False).first()
        
    @cache.memoize(timeout=60)
    def has_ban(self, user):

        return db.query(BanRelationship).filter_by(board_id=self.id, user_id=user.id).first()

