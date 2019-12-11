from ruqqus.helpers.base36 import *
from ruqqus.helpers.security import *
from sqlalchemy import *
from ruqqus.__main__ import Base, db, cache
import time

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    board_id = Column(BigInteger, ForeignKey("board.id"))
    created_utc = Column(BigInteger, default=0)

    def __init__(self, *args, **kwargs):
        if "created_utc" not in kwargs:
            kwargs["created_utc"] = int(time.time())

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Subscription(id={self.id}, user)>"
