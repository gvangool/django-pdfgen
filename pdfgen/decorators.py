from django.conf import settings
from django.shortcuts import render_to_response
from django.template import loader, TemplateDoesNotExist
from django.template import RequestContext
from django.http import HttpResponse

from functools import wraps

from pdfgen.parser import Parser
from pdfgen.shortcuts import render_to_pdf_download, multiple_templates_to_pdf_download


def pdf_download(default_template_name, default_file_name=None, default_context=None):
    """
    Based on templatable_view from Jonathan Slenders

    Creates a decorator which
    - Extracts the `context` and `template_name` params from the view.
    - Call the view without those parameters
    - Render the template. Use the default template if none was passed to the view.
    - Convert the template to PDF and return as download.

    The decorated view should return either:
    - a context dictionary; or
    - a tuple (template_name, context dictionary); or
    - a HttpResponse
    """
    # Create decorator
    def decorator(view_func):
        # Check whether this template exists
        if settings.DEBUG:
            try:
                loader.get_template(default_template_name)
            except TemplateDoesNotExist:
                print '\n=== ERROR: pdf_download detected missing template:'
                print '            Template: %s' % default_template_name
                try:
                    print '            From:     %s   def %s\n' % (view_func.func_code.co_filename, view_func.func_code.co_name)
                except:
                    print '            From:     %s\n' % unicode(view_func)

        @wraps(view_func)
        def decorate(request, *args, **kwargs):
            """
            Wrapper around the view
            """
            # Start from the default context and update this one every step
            context = default_context or {}
            file_name = default_file_name or 'output.pdf'

            # Pop decorator parameters
            context.update(kwargs.pop('context', {}))
            template_name = kwargs.pop('template_name', default_template_name)

            # Call original view function
            view_result = view_func(request, *args, **kwargs)

            if isinstance(view_result, dict):
                context.update(view_result)

                # Make sure templates are rendered in strict mode.
                # see: cl_utils/django_patches/patch_resolve_to_not_fail_silently.py
                context.update({'strict': True})
            elif isinstance(view_result, tuple):
                template_name, view_result_file_name, view_result_context = view_result
                context.update(view_result_context)
                file_name = view_result_file_name
            else:
                # otherwise, just return the HttpResponseRedirect or whatever the view returned
                return view_result

            if isinstance(template_name, list):
                response = multiple_templates_to_pdf_download(template_name, context, context_instance=RequestContext(request), filename=file_name)
            else:
                response = render_to_pdf_download(template_name, context, context_instance=RequestContext(request), filename=file_name)

            return response

        return decorate
    return decorator
