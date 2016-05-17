from unittest import TestCase

from rest_framework_latex import renderers


class RendererTestCase(TestCase):
    """Test the LatexRenderer
    """
    def setUp(self):
        """Reset the renderer for testing
        """
        self.renderer = renderers.LatexRenderer()

    def test_successful_render(self):
        """Assume a render was successful.
        """

    def test_latex_error(self):
        """Raise an error if the latex command failed.
        """

    def test_missing_latex_setting(self):
        """
        """
