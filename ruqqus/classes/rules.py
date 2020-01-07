from .mix_ins import *
from flask import *
import time
from sqlalchemy import *
from sqlalchemy.orm import relationship, deferred
from ruqqus.helpers.base36 import *
from ruqqus.helpers.lazy import lazy
from ruqqus.__main__ import Base, db, cache

class Rules(Base, Stndrd):

    __tablename__="rules"
    id = Column(BigInteger, primary_key=True)
    board_id = Column(Integer, ForeignKey("boards.id"))
    rule_body = Column(String(256))
    rule_html = Column(String)
    created_utc = Column(BigInteger, default=0)

    def __repr__(self):
        return f"<Rule(id={self.id}, board_id={self.board_id})>"