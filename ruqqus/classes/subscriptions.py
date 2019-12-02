from ruqqus.helpers.base36 import *
from ruqqus.helpers.security import *
from sqlalchemy import *
from ruqqus.__main__ import Base, db, cache
import time

class Subscriptions(Base):
    __tablename__ = "subscriptions"
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger, ForeignKey("users.id"))
    subscribed_to_uid = Column(BigInteger, ForeignKey("users.id"))
    is_banned = Column(Integer, default=0)
    created_utc = Column(BigInteger, default=0)

    def __init__(self, *args, **kwargs):
        if "created_utc" not in kwargs:
            kwargs["created_utc"] = int(time.time())

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Subscriptions(id={self.id})>"