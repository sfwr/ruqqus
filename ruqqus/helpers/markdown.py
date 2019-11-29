from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
import re

# add token/rendering for @username mentions

class UserMention(SpanToken):

    pattern=re.compile("(^|\s)@(\w{3,25})")
    
    def __init__(self, match_obj):
        self.target = (match_obj.group(1), match_obj.group(2))

class BoardMention(SpanToken):

    pattern=re.compile("(^|\s)\+(\w{3,25})")

    def __init__(self, match_obj):

        self.target=(match_obj.group(1), match_obj.group(2))

class CustomRenderer(HTMLRenderer):

    def __init__(self):
        super().__init__(UserMention)
        super().__init__(BoardMention)

    def render_user_mention(self, token):
        template = '{space}<a href="/u/{target}">@{target}</a>'
        space = token.target[0]
        target = token.target[1]
        #inner = self.render_inner(token)
        return template.format(space=space, target=target)

    def render_board_mention(self, token):

        template='{space}<a href="/board/{target}">+{target}</a>'
        space=token.target[0]
        target=token.target[1]
        #inner=self.render_inner(token)
        return template.format(space=space, target=target)
        
