# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

try:
    from unittest import mock, TestCase
except ImportError:
    import mock
import six

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

    @mock.patch('rest_framework_latex.renderers.shutil')
    @mock.patch('rest_framework_latex.renderers.settings')
    @mock.patch('rest_framework_latex.renderers.open')
    @mock.patch('rest_framework_latex.renderers.Popen')
    def test_successful_render(self, Popen, open_util, settings, shutil):
        """Assume a render was successful.
        """
        request = mock.MagicMock()
        response = mock.MagicMock()
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

    @mock.patch('rest_framework_latex.renderers.shutil')
    @mock.patch('rest_framework_latex.renderers.settings')
    @mock.patch('rest_framework_latex.renderers.open')
    @mock.patch('rest_framework_latex.renderers.Popen')
    @mock.patch('rest_framework.renderers.template_render')
    def test_write_unicode(self, render, Popen, open_util, settings, shutil):
        """Writing Unicode characters shouldn't error.
        """
        request = mock.MagicMock()
        response = mock.MagicMock()
        render.return_value = u'£ü'

        file_handle = mock.MagicMock()
        open_util.return_value.__enter__.return_value = file_handle
        settings.LATEX_RESOURCES = 'output'
        self.mock_output(open_util, u'£ü')
        Popen.return_value = self.get_proc()

        output = self.renderer.render(
            {'key': 'value'},
            renderer_context={
                'view': self.view,
                'request': request,
                'response': response,
            }
        )
        self.assertEqual(output, '£ü')

        test_val = '£ü'.encode('utf-8') if six.PY2 else '£ü'
        file_handle.write.assert_called_with(test_val)

    @mock.patch('rest_framework_latex.renderers.shutil')
    @mock.patch('rest_framework_latex.renderers.settings')
    @mock.patch('rest_framework_latex.renderers.open')
    @mock.patch('rest_framework_latex.renderers.Popen')
    def test_latex_error(self, Popen, open_util, settings, shutil):
        """Raise an error if the latex command failed.
        """
        request = mock.MagicMock()
        response = mock.MagicMock()
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
            if six.PY2:
                self.assertEqual(
                    err.message,
                    'LaTeX returned nonzero response `1` with msg: '
                    '`Test error`')
            else:
                self.assertEqual(
                    str(err),
                    'LaTeX returned nonzero response `1` with msg: '
                    '`Test error`')
        else:
            self.fail('Runtime error not raised')

    @mock.patch('rest_framework_latex.renderers.shutil')
    @mock.patch('rest_framework_latex.renderers.open')
    @mock.patch('rest_framework_latex.renderers.Popen')
    def test_missing_latex_setting(self, Popen, open_util, shutil):
        """Not setting LATEX_RESOURCES is an error
        """
        request = mock.MagicMock()
        response = mock.MagicMock()
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
            if six.PY2:
                self.assertEqual(err.message, 'LATEX_RESOURCES not set')
            else:
                self.assertEqual(str(err), 'LATEX_RESOURCES not set')
        else:
            self.fail('ImproperlyConfigured error not raised')

    def get_communicate(self, stdout='', stderr=''):
        """Get a Communicate method with pre-defined out/err
        """
        return stdout, stderr

    def get_proc(self, return_value=0, stdout='', stderr=''):
        """Return a proc object to attach to the output of Popen
        """
        proc = mock.MagicMock()
        proc.communicate.return_value = self.get_communicate(stdout, stderr)
        proc.returncode = return_value
        return proc

    def mock_output(self, open, return_string):
        """Set the return_string to the output of the read file.
        """
        open.return_value.__enter__.return_value.read.return_value = (
            return_string)


class _FakeView(object):
    """
    """
    latex_name = 'output.tex'
