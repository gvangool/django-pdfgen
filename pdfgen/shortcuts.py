from reportlab.platypus.flowables import PageBreak

from django.conf import settings
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import translation

from pdfgen.parser import Parser, XmlParser, find


def get_parser(template_name):
    """
    Get the correct parser based on the file extension
    """
    import os

    if template_name[-4:] == '.xml':
        parser = XmlParser()
        # set the barcode file
        parser.barcode_library = find('common/pdf_img/barcode.ps')
        return parser
    else:
        return Parser()


def render_to_pdf_data(template_name, context, context_instance=None):
    """
    Parse the template into binary PDF data
    """
    context_instance = context_instance or Context()

    input = render_to_string(template_name, context, context_instance)
    parser = get_parser(template_name)

    return parser.parse(input)


def render_to_pdf_download(template_name, context, context_instance=None, filename=None):
    """
    Parse the template into a download
    """
    context_instance = context_instance or Context()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = u'attachment; filename="%s"' % (filename or u'document.pdf')

    input = render_to_string(template_name, context, context_instance)

    parser = get_parser(template_name)
    output = parser.parse(input)

    response.write(output)

    return response


def multiple_templates_to_pdf_download(template_names, context, context_instance=None, filename=None):
    """
    Render multiple templates with the same context into a single download
    """
    context_instance = context_instance or Context()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = u'attachment; filename="%s"' % (filename or u'document.pdf')

    all_parts = []

    for template_name in template_names:
        parser = get_parser(template_name)
        input = render_to_string(template_name, context, context_instance)
        parts = parser.parse_parts(input)
        all_parts += parts
        all_parts.append(PageBreak())

    output = parser.merge_parts(all_parts)

    response.write(output)

    return response


def multiple_contexts_to_pdf_data(template_name, contexts, context_instance):
    """
    Render multiple templates with the same context into a single data bundle
    """
    all_parts = []
    parser = get_parser(template_name)

    old_lang = translation.get_language()

    for context in contexts:
        if 'language' in context:
            translation.activate(context['language'])
        input = render_to_string(template_name, context, context_instance)
        parts = parser.parse_parts(input)
        all_parts += parts
        all_parts.append(PageBreak())

    output = parser.merge_parts(all_parts)

    translation.activate(old_lang)

    return output


def multiple_contexts_to_pdf_download(template_name, contexts, context_instance=None, filename=None):
    """
    Render a single template with multiple contexts into a single download
    """
    context_instance = context_instance or Context()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = u'attachment; filename="%s"' % (filename or u'document.pdf')

    output = multiple_contexts_to_pdf_data(template_name, contexts, context_instance)

    response.write(output)

    return response


def multiple_contexts_and_templates_to_pdf_download(contexts_templates, context_instance=None, filename=None):
    """
    Render multiple templates with multiple contexts into a single download
    """
    context_instance = context_instance or Context()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = u'attachment; filename="%s"' % (filename or u'document.pdf')

    all_parts = []

    old_lang = translation.get_language()

    for context, template_name in contexts_templates:
        parser = get_parser(template_name)
        if 'language' in context:
            translation.activate(context['language'])
        input = render_to_string(template_name, context, context_instance)
        parts = parser.parse_parts(input)
        all_parts += parts
        all_parts.append(PageBreak())

    output = parser.merge_parts(all_parts)

    translation.activate(old_lang)

    response.write(output)

    return response
