from unittest import TestCase

from mock import MagicMock, patch

from django.core.exceptions import ImproperlyConfigured

from rest_framework_latex import renderers


class RendererTestCase(TestCase):
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
    def test_successful_render(self, Popen, open_util, settings, shutil):
        """Assume a render was successful.
        """
        request = MagicMock()
        response = MagicMock()
        settings.LATEX_RESOURCES = 'output'
        self.mock_output(open_util, 'Output')

        Popen.return_value = self.get_proc()

        output = self.renderer.render(
            {'key': 'value'},
            renderer_context={
                'view': self.view,
                'request': request,
                'response': response,
            }
        )
        self.assertEqual(output, 'Output')

    @patch('rest_framework_latex.renderers.shutil')
    @patch('rest_framework_latex.renderers.settings')
    @patch('rest_framework_latex.renderers.open')
    @patch('rest_framework_latex.renderers.Popen')
    def test_latex_error(self, Popen, open_util, settings, shutil):
        """Raise an error if the latex command failed.
        """
        request = MagicMock()
        response = MagicMock()
        settings.LATEX_RESOURCES = 'output'

        Popen.return_value = self.get_proc(
            return_value=1, stdout='Test error')

        try:
            self.renderer.render(
                {'key': 'value'},
                renderer_context={
                    'view': self.view,
                    'request': request,
                    'response': response,
                }
            )
        except RuntimeError as err:
            self.assertEqual(
                err.message,
                'LaTeX returned nonzero response `1` with msg: `Test error`')
        else:
            self.fail('Runtime error not raised')

    @patch('rest_framework_latex.renderers.shutil')
    @patch('rest_framework_latex.renderers.open')
    @patch('rest_framework_latex.renderers.Popen')
    def test_missing_latex_setting(self, Popen, open_util, shutil):
        """Not setting LATEX_RESOURCES is an error
        """
        request = MagicMock()
        response = MagicMock()
        Popen.return_value = self.get_proc()

        try:
            self.renderer.render(
                {'key': 'value'},
                renderer_context={
                    'view': self.view,
                    'request': request,
                    'response': response,
                }
            )
        except ImproperlyConfigured as err:
            self.assertEqual(err.message, 'LATEX_RESOURCES not set')
        else:
            self.fail('ImproperlyConfigured error not raised')

    def get_communicate(self, stdout='', stderr=''):
        """Get a Communicate method with pre-defined out/err
        """
        return stdout, stderr

    def get_proc(self, return_value=0, stdout='', stderr=''):
        """Return a proc object to attach to the output of Popen
        """
        proc = MagicMock()
        proc.communicate.return_value = self.get_communicate(stdout, stderr)
        proc.returncode = return_value
        return proc

    def mock_output(self, open, return_string):
        """Set the return_string to the output of the read file.
        """
        open.return_value.__enter__.return_value.read.return_value = 'Output'


class _FakeView(object):
    """
    """
    latex_name = 'output.tex'
