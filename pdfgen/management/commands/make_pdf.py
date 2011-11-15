import codecs
from optparse import make_option

from django.conf import settings
from django.core.management.base import NoArgsCommand

from pdfgen.parser import Parser


class Command(NoArgsCommand):
    """
    Management command to create a pdf
    """

    help = u'Generate pdf'
    option_list = NoArgsCommand.option_list + (
        make_option('--source', dest='source', action='store', default=None,
                    help='The source file in the City Live Template for '
                         'ReportLab (CLTR) language.'),
    )

    def handle_noargs(self, **options):
        source_file = options['source']

        print(u'Reading file "%s"...' % source_file)

        fh = codecs.open(source_file, 'rt', 'utf-8')
        buffer = fh.read()
        fh.close()

        p = Parser()
        output = p.parse(buffer)

        fh = open(source_file + '.pdf', 'wb')
        fh.write(output)
        fh.close()
