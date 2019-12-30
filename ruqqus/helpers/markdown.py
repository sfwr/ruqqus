from .get import *

from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
import re

# add token/rendering for @username mentions

class UserMention(SpanToken):

    pattern=re.compile("(^|\s)@(\w{3,25})")
    parse_inner=False
    
    def __init__(self, match_obj):
        self.target = (match_obj.group(1), match_obj.group(2))

class BoardMention(SpanToken):

    pattern=re.compile("(^|\s)\+(\w{3,25})")
    parse_inner=False

    def __init__(self, match_obj):

        self.target=(match_obj.group(1), match_obj.group(2))

class CustomRenderer(HTMLRenderer):

    def __init__(self):
        super().__init__(UserMention,
                         BoardMention)

    def render_user_mention(self, token):
        space = token.target[0]
        target = token.target[1]

        user=get_user(target, graceful=True)
        if not user or user.reserved:
            return f"{space}@{target}"
        
        return f'{space}<a href="{user.permalink}">@{user.username}</a>'

    def render_board_mention(self, token):


        icon_template='<i class="{icon} fa-width-rem"></i>'
        space=token.target[0]
        target=token.target[1]

        board=get_guild(target, graceful=True)

        if not board:
            return f"{space}+{target}"
        if board and board.fa_icon:
            icon=icon_template.format(icon=board.fa_icon)
        else:
            icon=""
        return f'{space}<a href="{board.permalink}">{icon}+{board.name}</a>'
        
