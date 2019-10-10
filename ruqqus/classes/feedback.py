from flask import render_template, session, request
from time import strftime, time, gmtime
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred
from ruqqus.__main__ import Base, db, cache


class Feedback(Base):

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"), default=None)
    title = Column(VARCHAR, default=None)
    msg = Column(VARCHAR, default=None)
    created_utc = Column(BigInteger, default=0)

    def __init__(self, *args, **kwargs):
        if "created_utc" not in kwargs:
            kwargs["created_utc"] = int(time.time())
        super().__init__(*args, **kwargs)

    @property
    def url(self):
        return f"/feedback/admin/{self.id}"

    def __repr__(self):
        return f"<Feedback(id={self.id}, uid={self.uid})>"
