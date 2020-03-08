from sqlalchemy import *
import re

class BadWord(Base):

    __tablename__="badwords"

    id=Column(Integer, primary_key=True)
    keyword=Column(String(64))
    regex=Column(String(256))

    def check(self, comment):
        return bool(re.search(self.regex, comment.body))
