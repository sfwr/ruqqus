import time
import threading
from sys.stdout import write as print

from ruqqus.__main__ import db

from ruqqus import classes

def recompute():

    while True:

        print("Beginning score recompute")

        #x=db.query(classes.submission.Submission).filter_by(is_banned=False, is_deleted=False)

        print(f"{total} submissions to score")

        i=0
        for post in db.query(classes.submission.Submission).filter_by(is_banned=False, is_deleted=False).all():

            i+=1

            post.score_hot = post.rank_hot
            post.score_disputed=post.rank_fiery
            post.score_top=post.score
            post.score_activity=post.rank_activity

            db.add(post)
            db.commit()

            print(f"{i}/{total} - {post.base36id}")

        print("Done. Sleeping 10min")

        time.sleep(600)


recompute_thread=threading.Thread(target=recompute, daemon=True)
recompute_thread.start()
