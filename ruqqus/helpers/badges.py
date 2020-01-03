import time
import threading

from ruqqus.classes import *
from ruqqus.__main__ import db

def badge_monitor():

    while True:

        print("starting badge check thread")

        badge_types=[x for x in db.query(BadgeDef).filter(BadgeDef.qualification_expr.isnot(None)).all()]

        for user in db.query(User).filter_by(is_banned=False).all():

            for badge in badge_types:
                
                if eval(badge.qualification_expr, {}, {'v':user}):
                    
                    if not user.has_badge(badge.id):
                        new_badge=Badge(user_id=user.id,
                                        badge_id=badge.id,
                                        created_utc=int(time.time())
                                        )
                        db.add(new_badge)
                        db.commit()
                        print(f"added {badge.name} to @{user.username}")
                else:
                    bad_badge=user.has_badge(badge.id)
                    if bad_badge:
                        db.delete(bad_badge)
                        db.commit()
                        print(f"removed {badge.name} from @{user.username}")

        print("thread sleeping 1hr")
        time.sleep(3600)

badge_thread=threading.Thread(target=badge_monitor)
badge_thread.start()
    
