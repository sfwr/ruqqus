import time
import threading

from ruqqus.__main__ import db

def recompute():

    while True:

        for post in db.query(ruqqus.classes.submission.Submission).filter(is_banned=False, is_deleted=False).all():

            post.score_hot = post.rank_hot
            post.score_disputed=post.rank_fiery
            post.score_top=post.score
            post.score_activity=post.rank_activity

            db.add(post)
            db.commit()


        time.sleep(600)


recompute_thread=threading.Thread(target=recompute)
recompute_thread.start()
