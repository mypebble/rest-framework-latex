from __future__ import absolute_import, print_function, unicode_literals

try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import MagicMock, patch

from rest_framework_latex import renderers
from tests.testrenderers.tests.test_latex import RendererTestCase


class CallbackTestCase(RendererTestCase):
    """Test the LatexRenderer
    """

    def setUp(self):
        """Reset the renderer for testing
        """
        self.renderer = renderers.LatexRenderer()
        self.view = _FakeView()

    @patch('rest_framework_latex.renderers.shutil')
    @patch('rest_framework_latex.renderers.settings')
    @patch('rest_framework_latex.renderers.open')
    @patch('rest_framework_latex.renderers.Popen')
    def test_callbacks(self, Popen, open_util, settings, shutil):
        """Assume a render was successful.
        """
        request = MagicMock()
        response = MagicMock()
        settings.LATEX_RESOURCES = 'output'
        self.mock_output(open_util, 'Output')

        Popen.return_value = self.get_proc()

        self.renderer.render(
            {'key': 'value'},
            renderer_context={
                'view': self.view,
                'request': request,
                'response': response,
            }
        )

        self.assertTrue(self.view.called_pre_latex)
        self.assertTrue(self.view.called_post_latex)


class _FakeView(object):
    """
    """
    latex_name = 'output.tex'

    def __init__(self):
        self.called_pre_latex = False
        self.called_post_latex = False

    def pre_latex(self, t_dir, context):
        assert context['key'] == 'value'
        self.called_pre_latex = True

    def post_latex(self, t_dir, context):
        assert context['key'] == 'value'
        self.called_post_latex = True
