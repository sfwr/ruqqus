from ruqqus.helpers.base36 import *
from ruqqus.helpers.security import *
from .submission import *
from ruqqus.__main__ import Base, db, cache

class Board(Base):

    __tablename__="boards"

    id=Column(Integer, primary_key=True)
    name=Column(String)
    created_utc=Column(Integer)

    @property
    def permalink(self):

        return f"/board/{self.name}"

    @cache.memoize(timeout=30)
    def idlist(self, sort="hot", page=1):

        posts=db.query(Submission).filter_by(is_banned=False,
                                             is_deleted=False,
                                             stickied=False,
                                             board=self.id)

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
        
        ids=self.idlist(sort=sort, page=page)

        next_exists=(len(ids)==26)
        ids=ids[25]

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
                                select submissions.*, submission.ups, submission.downs
                                from submissions
                                join (values {tups}) as x(id, n) on submissions.id=x.id
                                order by x.n"""
                               )).all()
        else:
            posts=[]

        return render_template("board.html", v=v, listin=posts, next_exists=next_exists, sort_method=sort, page=page)        
