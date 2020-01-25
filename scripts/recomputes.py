import time
import threading

from ruqqus.__main__ import db

from ruqqus import classes

def recompute():

    while True:

        db.begin(subtransactions=True)

        now=int(time.time())

        cutoff=now-(60860*24*180)

        print("Beginning score recompute")

        total=db.query(classes.submission.Submission
                       ).filter_by(is_banned=False, is_deleted=False
                                   ).filter(classes.submission.Submission.created_utc>cutoff
                                            ).count()

        print(f"{total} submissions to score")

        i=0
        for post in db.query(classes.submission.Submission
                       ).filter_by(is_banned=False, is_deleted=False
                                   ).filter(classes.submission.Submission.created_utc>cutoff
                                            ).all():
            i+=1

            post.score_hot = post.rank_hot
            post.score_disputed=post.rank_fiery
            post.score_top=post.score
            post.score_activity=post.rank_activity

            db.add(post)
            db.commit()

            #print(f"{i}/{total} - {post.base36id}")

        print("Done. Sleeping 10min")

        time.sleep(600)


recompute()
