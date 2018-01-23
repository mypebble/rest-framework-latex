"""The renderer.
"""
from __future__ import absolute_import, print_function, unicode_literals

from os.path import join
from subprocess import Popen, PIPE

import logging
import shutil
import six
import tempfile

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

    def pre_latex(self, view, t_dir, data):
        if hasattr(view, 'pre_latex'):
            view.pre_latex(t_dir, data)

    def post_latex(self, view, t_dir, data):
        if hasattr(view, 'post_latex'):
            view.post_latex(t_dir, data)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Renders data to PDF using a LaTeX template
        """
        # Get latex
        tex = super(LatexRenderer, self).render(
            data, accepted_media_type, renderer_context)

        # Build tempoary directory
        t_dir = tempfile.mkdtemp(prefix='drf_latex_')

        view = renderer_context['view']

        ret = None
        try:
            ret = self.run_latex(tex, t_dir, view, data)
        finally:
            # Cleanup
            shutil.rmtree(t_dir)

        self.post_latex(view, t_dir, data)

        return ret

    def run_latex(self, tex, t_dir, view, data):
        # Copy over resources
        if not hasattr(settings, 'LATEX_RESOURCES'):
            raise ImproperlyConfigured('LATEX_RESOURCES not set')

        tex_dir = join(t_dir, 'tex')

        shutil.copytree(settings.LATEX_RESOURCES, tex_dir)

        # Write tex file
        tex_file = join(tex_dir, 'file.tex')
        result_file = join(tex_dir, 'file.pdf')

        with open(tex_file, 'w') as f:
            output = tex.encode('utf-8') if six.PY2 else tex
            f.write(output)

        # Hook
        self.pre_latex(view, t_dir, data)

        # Latex it!
        call_args = [
            'lualatex', '-interaction=nonstopmode', tex_file]
        proc = Popen(
            call_args, cwd=tex_dir, stdout=PIPE, stderr=PIPE)

        out, err = proc.communicate()

        if proc.returncode != 0:
            err_msg = u'LaTeX returned nonzero response `{}` with msg: `{}`'

            # Errors appear on stdout
            raise RuntimeError(err_msg.format(proc.returncode, out))
        logger.info(out)
        logger.info(err)

        # Read file
        with open(result_file, 'rb') as f:
            r = f.read()

        # return
        return r
