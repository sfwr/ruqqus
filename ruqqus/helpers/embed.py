import re

youtube_regex=re.compile("^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*")

def youtube_embed(url):

    try:
        yt_id=re.match(youtube_regex, url).group(2)
    except AttributeError:
        return "error"

    if yt_id and len(yt_id)==11:
        return f"https://youtube.com/embed/{yt_id}"
    else:
        return "error"


ruqqus_regex=re.compile("post/(\w+)(/comment/(\w+))?")
def ruqqus_embed(url):

    matches=re.match(ruqqus_regex, url)

    post_id=matches.group(2)
    comment_id=matches.group(3)

    if comment_id:
        return f"https://beta.ruqqus.com/embed/comment/{comment_id}"
    else:
        return f"https://beta.ruqqus.com/embed/post/{post_id}:

    
