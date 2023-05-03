from django.template import Library, Node

from analytical.utils import is_internal_ip, disable_html

LIVEINTERNET_WITH_IMAGE = """
<a href="https://www.liveinternet.ru/click"
target="_blank"><img id="licnt515E" width="31" height="31" style="border:0" 
title="LiveInternet"
src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7"
alt=""/></a><script>(function(d,s){d.getElementById("licnt515E").src=
"https://counter.yadro.ru/hit?t50.6;r"+escape(d.referrer)+
((typeof(s)=="undefined")?"":";s"+s.width+"*"+s.height+"*"+
(s.colorDepth?s.colorDepth:s.pixelDepth))+";u"+escape(d.URL)+
";h"+escape(d.title.substring(0,150))+";"+Math.random()})
(document,screen)</script>
"""

LIVEINTERNET_CODE = """
<script>
new Image().src = "https://counter.yadro.ru/hit?r"+
escape(document.referrer)+((typeof(screen)=="undefined")?"":
";s"+screen.width+"*"+screen.height+"*"+(screen.colorDepth?
screen.colorDepth:screen.pixelDepth))+";u"+escape(document.URL)+
";h"+escape(document.title.substring(0,150))+
";"+Math.random();
</script>
"""
LIVEINTERNET_IMAGE = """
<a href="https://www.liveinternet.ru/click"
target="_blank"><img src="https://counter.yadro.ru/logo?50.6"
title="LiveInternet"
alt="" style="border:0" width="31" height="31"/>
</a>
"""

register = Library()


@register.tag
def liveinternet(parser, token):
    """
    Body Liveinternet, full image and code template tag.

    Render the body Javascript code and image for Liveinternet.
    """
    return LiveInternetNode(LIVEINTERNET_WITH_IMAGE, 'liveinternet_with_image')


@register.tag
def liveinternet_code(parser, token):
    """
    Top Liveinternet,code template tag.

    Render the top Javascript code for Liveinternet.
    """
    return LiveInternetNode(LIVEINTERNET_CODE, 'liveinternet_code')


@register.tag
def liveinternet_img(parser, token):
    """
    Body Liveinternet image template tag.

    Render the body Javascript code for Liveinternet.
    """
    return LiveInternetNode(LIVEINTERNET_IMAGE, 'liveinternet_image')


class LiveInternetNode(Node):
    def __init__(self, key, name):
        self.key = key
        self.name = name

    def render(self, context):
        if is_internal_ip(context):
            return disable_html(self.key, self.name)
        return LIVEINTERNET_CODE
