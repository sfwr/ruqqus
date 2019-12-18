from urllib.parse import urlparse
import mistletoe
import re

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from ruqqus.helpers.sanitize import *
from ruqqus.helpers.filters import *
from ruqqus.helpers.markdown import *
from ruqqus.helpers.get import *
from ruqqus.classes import *
from flask import *
from ruqqus.__main__ import app, db, limiter, cache

valid_board_regex=re.compile("^\w{3,25}$")
fa_icon_regex=re.compile("(fas|far|fal|fad) fa-([a-z0-9-]+)")

@app.route("/create_guild", methods=["GET"])
@is_not_banned
def create_board_get(v):
    if not v.is_activated:
        return render_template("message.html", title="Unable to make board", text="You need to verify your email adress first.")
    if v.karma<100:
        return render_template("message.html", title="Unable to make board", text="You need more rep to do that.")

        
    return render_template("make_board.html", v=v)

@app.route("/api/board_available/<name>", methods=["GET"])
def api_board_available(name):
    if db.query(Board).filter(Board.name.ilike(name)).first():
        return jsonify({"board":name, "available":False})
    else:
        return jsonify({"board":name, "available":True})

@app.route("/create_guild", methods=["POST"])
@is_not_banned
@validate_formkey
def create_board_post(v):

    board_name=request.form.get("name")
    board_name=board_name.lstrip("+")

    if not re.match(valid_board_regex, board_name):
        return render_template("message.html", title="Unable to make board", text="Valid board names are 3-25 letters or numbers.")

    if not v.is_activated:
        return render_template("message.html", title="Unable to make board", text="Please verify your email first")

    if v.karma<100:
        return render_template("message.html", title="Unable to make board", text="You need more rep to do that")


    #check name
    if db.query(Board).filter(Board.name.ilike(board_name)).first():
        abort(409)

    #check # recent boards made by user
    cutoff=int(time.time())-60*60*24
    recent=db.query(Board).filter(Board.creator_id==v.id, Board.created_utc >= cutoff).all()
    if len([x for x in recent])>=2:
        abort(429)

    description = request.form.get("description")

    with CustomRenderer() as renderer:
        description_md=renderer.render(mistletoe.Document(description))
    description_html=sanitize(description_md, linkgen=True)

    #make the board

    new_board=Board(name=board_name,
                    description=description,
                    description_html=description_html,
                    over_18=bool(request.form.get("over_18","")),
                    creator_id=v.id
                    )

    db.add(new_board)
    db.commit()

    #add user as mod
    mod=ModRelationship(user_id=v.id,
                        board_id=new_board.id,
                        accepted=True)
    db.add(mod)

    #add subscription for user
    sub=Subscription(user_id=v.id,
                     board_id=new_board.id)
    db.add(sub)
    db.commit()

    return redirect(new_board.permalink)

@app.route("/board/<name>", methods=["GET"])
@app.route("/+<name>", methods=["GET"])
@auth_desired
def board_name(name, v):

    board=db.query(Board).filter(Board.name.ilike(name)).first()

    if not board:
        abort(404)

    if not board.name==name:
        return redirect(board.permalink)

    if board.over_18 and not (v and v.over_18):
        abort(451)

    sort=request.args.get("sort","hot")
    page=int(request.args.get("page", 1))
             
    return board.rendered_board_page(v=v,
                                     sort=sort,
                                     page=page)

@app.route("/mod/kick/<bid>/<pid>", methods=["POST"])
@auth_required
@validate_formkey
def mod_kick_bid_pid(bid,pid, v):

    board=get_board(bid)

    post = get_post(pid)

    if not post.board_id==board.id:
        abort(422)

    if not board.has_mod(v):
        abort(403)

    post.board_id=1
    db.add(post)
    db.commit()

    cache.delete_memoized(Board.idlist, board)

    return "", 204

@app.route("/mod/ban/<bid>/<username>", methods=["POST"])
@auth_required
@validate_formkey
def mod_ban_bid_user(bid, username, v):

    user=get_user(username)
    board=get_board(bid)

    if not board.has_mod(v):
        abort(403)

    if board.has_ban(user):
        abort(409)

    if board.has_mod(user):
        abort(409)

    new_ban=BanRelationship(user_id=user.id,
                            board_id=board.id,
                            banning_mod_id=v.id)

    db.add(new_ban)
    db.commit()

    return "", 204
    
@app.route("/mod/unban/<bid>/<username>", methods=["POST"])
@auth_required
@validate_formkey
def mod_unban_bid_user(bid, username, v):

    user=get_user(username)
    board=get_board(bid)

    if not board.has_mod(v):
        abort(403)

    x= board.has_ban(user)
    if not x:
        abort(409)

    db.delete(x)
    db.commit()
    
    return "", 204

@app.route("/user/kick/<pid>", methods=["POST"])
@auth_required
@validate_formkey
def user_kick_pid(pid, v):

    #allows a user to yank their content back to +general if it was there previously
    
    post=get_post(pid)

    current_board=post.board

    if not post.author_id==v.id:
        abort(403)

    if post.board_id==post.original_board_id:
        abort(403)

    if post.board_id==1:
        abort(400)

    #block further yanks to the same board
    new_rel=PostRelationship(post_id=post.id,
                             board_id=post.board.id)
    db.add(new_rel)

    post.board_id=1
    
    db.add(post)
    db.commit()
    
    #clear board's listing caches
    cache.delete_memoized(Board.idlist, current_board)
    
    return "", 204

@app.route("/mod/take/<pid>", methods=["POST"])
@auth_required
@validate_formkey
def mod_take_bid_pid(bid, v):

    board=get_board(request.form("board_id"))

    post = get_post(pid)

    if not post.board_id==1:
        abort(422)

    if board.has_ban(post.author):
        abort(403)

    if not board.has_mod(v):
        abort(403)

    if not board.can_take(post):
        abort(403)

    post.board_id=board.id
    db.add(post)
    db.commit()

    #clear board's listing caches
    cache.delete_memoized(Board.idlist, board)
    
    return "", 204

@app.route("/mod/invite_mod/<bid>", methods=["POST"])
@auth_required
@validate_formkey
def mod_invite_username(bid,v):


    board = get_board(bid)

    if not board.has_mod(v):
        abort(403)

    username=request.form.get("username")
    user=get_user(username)

    if not board.can_invite_mod(user):
        abort(409)

    if not board.has_rescinded_invite(user):

        #notification

        text=f"You have been invited to join +{board.name} as a guildmaster. You can [click here]({board.permalink}/mod/mods) and accept this invitation. Or, if you weren't expecting this, you can ignore it."
        with CustomRenderer() as renderer:
            text_html=renderer.render(mistletoe.Document(text))

        
        new_comment=Comment(author_id=1,
                            body=text,
                            body_html=text_html,
                            parent_submission=None)
        db.add(new_comment)
        notif=Notification(comment_id=new_comment.id,
                           user_id=user.id)
        db.add(Notification)

    new_mod=ModRelationship(user_id=user.id,
                            board_id=board.id,
                            accepted=False)
    db.add(new_mod)
    db.commit()
    return redirect(f"/+{board.name}/mod/mods")

@app.route("/mod/<bid>/rescind/<username>", methods=["POST"])
@auth_required
@validate_formkey
def mod_rescind_bid_username(bid, username, v):

    board=get_board(bid)

    if not board.has_mod(v):
        abort(403)
        
    user=get_user(username)

    invitation = db.query(ModRelationship).filter_by(board_id=board.id,
                                                     user_id=user.id,
                                                     accepted=False).first()
    if not invitation:
        abort(404)

    invitation.invite_rescinded=True

    db.add(invitation)
    db.commit()
    

@app.route("/mod/accept/<bid>", methods=["POST"])
@auth_required
@validate_formkey
def mod_accept_board(bid, v):

    board=get_board(bid)

    x=board.has_invite(v)
    if not x:
        abort(404)

    x.accepted=True
    db.add(x)
    db.commit()
    return "", 204
    

@app.route("/mod/<bid>/remove/<username>", methods=["POST"])
@auth_required
@validate_formkey
def mod_remove_username(bid, username,v):

    user=get_user(username)

    board = get_board(bid)

    v_mod=board.has_mod(v)
    u_mod=board.has_mod(user)

    if not v_mod:
        abort(403)
    if not u_mod:
        abort(422)
    if v_mod.id > u_mod.id:
        abort(403)

    del v_mod
    db.delete(u_mod)
    db.commit()
    return "", 204

@app.route("/mod/is_banned/<bid>/<username>", methods=["GET"])
@auth_required
@validate_formkey
def mod_is_banned_board_username(bid, username, v):
    board=get_board(bid)
    user=get_user(username)

    result={"board":board.name,
            "user":user.username}

    if board.has_ban(user):
        result["is_banned"]=True
    else:
        result["is_banned"]=False

    return jsonify(result)
        
@app.route("/mod/<bid>/settings", methods=["POST"])
@auth_required
@validate_formkey
def mod_bid_settings(bid, v):

    board=get_board(bid)

    if not board.has_mod(v):
        abort(403)

    #name capitalization
    new_name=request.form.get("name","").lstrip("+")

    if new_name.lower()==board.name.lower():
        board.name=new_name

    #board description
    description = request.form.get("description")
    with CustomRenderer() as renderer:
        description_md=renderer.render(mistletoe.Document(description))
    description_html=sanitize(description_md, linkgen=True)


    board.description = description
    board.description_html=description_html

    #nsfw
    board.over_18=bool(request.form.get("over_18",False))

    #fontawesome
    fa_raw=request.form.get("fa_icon","")
    if not fa_raw:
        board.fa_icon=""
    else:
        try:
            if fa_raw.startswith("http"):
                parsed_link=urlparse(fa_raw)
                icon=parsed_link.path.split("/")[-1]
                style=parsed_link.query.split("=")[-1]
                styles={"duotone":"fad",
                        "light":"fal",
                        "regular":"far",
                        "solid":"fas"}
                style=styles[style]
            else:

                regex=re.search(fa_icon_regex, fa_raw)
                style=regex.group(1)
                icon=regex.group(2)
                
            board.fa_icon=f"{style} fa-{icon}"
        except Exception as e:
            pass
        
    
    db.add(board)
    db.commit()

    return redirect(board.permalink)

@app.route("/+<boardname>/mod/settings", methods=["GET"])
@auth_required
def board_about_settings(boardname, v):

    board=db.query(Board).filter(Board.name.ilike(boardname)).first()
    if not board:
        abort(404)

    if not board.has_mod(v):
        abort(403)

    return render_template("guild/settings.html", v=v, b=board)

@app.route("/+<boardname>/mod/mods", methods=["GET"])
@auth_desired
def board_about_mods(boardname, v):

    board=db.query(Board).filter(Board.name.ilike(boardname)).first()
    if not board:
        abort(404)

    me=board.has_mod(v)

    return render_template("guild/mods.html", v=v, b=board, me=me)


@app.route("/+<boardname>/mod/exiled", methods=["GET"])
@auth_required
def board_about_exiled(boardname, v):

    board=db.query(Board).filter(Board.name.ilike(boardname)).first()
    if not board:
        abort(404)

    if not board.has_mod(v):
        abort(403)

    username=request.args.get("user","")
    if username:
        users=db.query(User).filter_by(is_banned=0).filter(func.lower(User.username).contains(username.lower())).limit(25)
    else:
        users=[]
                                    

    return render_template("guild/bans.html", v=v, b=board, users=users)

@app.route("/api/subscribe/<boardname>", methods=["POST"])
@auth_required
def subscribe_board(boardname, v):

    board=get_guild(boardname)

    #check for existing subscription, canceled or otherwise
    sub= db.query(Subscription).filter_by(user_id=v.id, board_id=board.id).first()
    if sub:
        if sub.is_active:
            abort(409)
        else:
            #reactivate canceled sub
            sub.is_active=True
            db.add(sub)
            db.commit()
            return "", 204

    
    new_sub=Subscription(user_id=v.id,
                         board_id=board.id)

    db.add(new_sub)
    db.commit()

    #clear your cached guild listings
    cache.delete_memoized(User.idlist, v, kind="board")

    return "", 204


@app.route("/api/unsubscribe/<boardname>", methods=["POST"])
@auth_required
def unsubscribe_board(boardname, v):

    board=get_guild(boardname)

    #check for existing subscription
    sub= db.query(Subscription).filter_by(user_id=v.id, board_id=board.id).first()

    if not sub:
        abort(409)
    elif not sub.is_active:
        abort(409)

    sub.is_active=False

    db.add(sub)
    db.commit()

    #clear your cached guild listings
    cache.delete_memoized(User.idlist, v, kind="board")

    return "", 204
