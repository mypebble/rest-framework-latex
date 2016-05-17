from unittest import TestCase

from mock import patch

from django.core.exceptions import ImproperlyConfigured
from rest_framework_latex.templatetags import rest_framework_latex as tags


class TemplateTagTestCase(TestCase):
    """Test the LaTeX-specific template tags
    """

    @patch('rest_framework_latex.templatetags.rest_framework_latex.settings')
    def test_latex_resources(self, settings):
        """Test the latex_resources templatetag
        """
        settings.LATEX_RESOURCES = '/home/test_value/'
        self.assertEqual(tags.latex_resources(), '/home/test_value/')

    @patch('rest_framework_latex.templatetags.rest_framework_latex.settings')
    def test_latex_resources_trailing_slash(self, settings):
        """The template tag appends a trailing /
        """
        settings.LATEX_RESOURCES = '/home/test_value'
        self.assertEqual(tags.latex_resources(), '/home/test_value/')

    def test_latex_improperly_configured(self):
        """If LATEX_RESOURCES isn't set, raise an exception
        """
        try:
            tags.latex_resources()
        except ImproperlyConfigured as e:
            self.assertEqual(
                e.message, 'LATEX_RESOURCES is not defined in settings')

    def test_escape_tags(self):
        """Escape the latex tags in a user-entered string.
        """
        simple_replace = ('#', '$', '%', '^', '_', '{', '}')
        for character in simple_replace:
            escaped_char = u'\\{}'.format(character)
            self.assertEqual(tags.latex_safe(character), escaped_char)

        self.assertEqual(tags.latex_safe('\\'), '\\textbackslash{}')
        self.assertEqual(tags.latex_safe('~'), '\\textasciitidle{}')

    def test_escape_collected(self):
        """Collect the tags and escape in one go.
        """
        simple_replace = ('#', '$', '%', '^', '_', '{', '}')
        escaped_backslash = '\\textbackslash{}'
        escaped_tilde = '\\textasciitidle{}'

        entry_string = ''.join(simple_replace + ('\\', '~'))
        escaped_string = ''.join(
            tuple('\\{}'.format(c) for c in simple_replace) +
            (escaped_backslash, escaped_tilde))

        self.assertEqual(tags.latex_safe(entry_string), escaped_string)
