"""
Console debugging service.
"""

from analytical.services.base import AnalyticalService


DEBUG_CODE = """
    <script type="text/javascript">
      if(typeof(console) !== 'undefined' && console != null) {
        console.log('Analytical: rendering analytical_%(location)s tag');
      }
    </script>
"""


class ConsoleService(AnalyticalService):
    KEY = 'console'

    def render_head_top(self, context):
        return DEBUG_CODE % {'location': 'head_top'}

    def render_head_bottom(self, context):
        return DEBUG_CODE % {'location': 'head_bottom'}

    def render_body_top(self, context):
        return DEBUG_CODE % {'location': 'body_top'}

    def render_body_bottom(self, context):
        return DEBUG_CODE % {'location': 'body_bottom'}
