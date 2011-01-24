"""
Console debugging service.
"""

from analytical.services.base import AnalyticalService


DEBUG_CODE = """
    <script type="text/javascript">
      if(typeof(console) !== 'undefined' && console != null) {
        %s
      }
    </script>
"""
LOG_CODE_ANONYMOUS = """
    console.log('Analytical: rendering analytical_%(location)s tag');
"""
LOG_CODE_IDENTIFIED = """
    console.log('Analytical: rendering analytical_%(location)s tag for user %(identity)s');
"""


class ConsoleService(AnalyticalService):
    def render_head_top(self, context):
        return self._render_code('head_top', context)

    def render_head_bottom(self, context):
        return self._render_code('head_bottom', context)

    def render_body_top(self, context):
        return self._render_code('body_top', context)

    def render_body_bottom(self, context):
        return self._render_code('body_bottom', context)

    def _render_code(self, location, context):
        vars = {'location': location, 'identity': self.get_identity(context)}
        if vars['identity'] is None:
            debug_code = DEBUG_CODE % LOG_CODE_ANONYMOUS
        else:
            debug_code = DEBUG_CODE % LOG_CODE_IDENTIFIED
        return debug_code % vars
