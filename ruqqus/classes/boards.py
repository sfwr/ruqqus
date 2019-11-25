from ruqqus.helpers.base36 import *
from ruqqus.helpers.security import *
from .submissions import *
from ruqqus.__main__ import Base, db, cache

class Board(Base):

    __tablename__="boards"

    id=Column(Integer, primary_key=True)
    name=Column(String)

    @property
    def permalink(self):

        return f"/board/{self.name}"

    @cache.memoize(timeout=30)
    def idlist(sort="hot", page=1):

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

        posts=[x.id for x in posts.offset(25*(page-1)).limit(26).all()]

        return posts
