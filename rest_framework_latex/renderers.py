import tempfile
from os.path import join
from subprocess import Popen
import shutil
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework import renderers


logger = logging.getLogger(__name__)


class LatexRenderer(renderers.TemplateHTMLRenderer):
    """Renders a PDF based on a LaTeX template
    """
    latex_name = None
    format = 'latex'
    media_type = 'application/pdf'

    def get_template_names(self, response, view):
        """Override with latex_name from DRF. This allows for you
        to still render HTML if you want
        """
        if hasattr(response, 'latex_name'):
            return [response.latex_name]
        elif self.latex_name:
            return [self.latex_name]
        elif hasattr(view, 'get_latex_names'):
            return view.get_latex_names()
        elif hasattr(view, 'latex_name'):
            return [view.latex_name]
        raise ImproperlyConfigured(
            u'Returned a template response with no `latex_name` attribute '
            u'set on either the view or response')

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Renders data to PDF using a LaTeX template
        """
        # Get latex
        tex = super(LatexRenderer, self).render(
            data, accepted_media_type, renderer_context)

        # Build tempoary directory
        t_dir = tempfile.mkdtemp(prefix='drf_latex_')

        ret = None
        try:
            ret = self.run_latex(tex, t_dir)
        finally:
            # Cleanup
            shutil.rmtree(t_dir)

        return ret

    def run_latex(self, tex, t_dir):
        # Copy over resources
        if not hasattr(settings, 'LATEX_RESOURCES'):
            raise ImproperlyConfigured('LATEX_RESOURCES not set')
        shutil.copytree(settings.LATEX_RESOURCES, join(t_dir, 'tex'))

        # Write tex file
        tex_file = join(t_dir, 'tex', 'file.tex')
        result_file = join(t_dir, 'tex', 'file.pdf')
        with open(tex_file, 'w') as f:
            f.write(tex)

        # Latex it!
        call_args = [
            'lualatex', '-interaction=nonstopmode', tex_file]
        proc = Popen(call_args, cwd=join(t_dir, 'tex'))
        out, err = proc.communicate()
        if proc.returncode != 0:
            err_msg = u'LaTeX returned nonzero response `{}` with msg: `{}`'
            raise RuntimeError(err_msg.format(proc.returncode, err))
        logger.info(err)

        # Read file
        with open(result_file) as f:
            r = f.read()

        # return
        return r
