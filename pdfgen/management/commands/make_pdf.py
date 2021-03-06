from django.conf import settings
from django.core.management.base import NoArgsCommand

from optparse import make_option
import codecs

class Command(NoArgsCommand):
    help = u'Generate pdf'
    option_list = NoArgsCommand.option_list + (
        make_option('--source', dest='source', action='store', default=None, help='The source file in the City Live Template for ReportLab (CLTR) language.'),
    )

    def handle_noargs(self, **options):
        source_file = options['source']

        print(u'Reading file "%s"...' % source_file)

        fh = codecs.open(source_file, 'rt', 'utf-8')
        buffer = fh.read()
        fh.close()
        
        from pdfgen.parser import Parser
        p = Parser()
        output = p.parse(buffer)
        
        fh = open(source_file + '.pdf', 'wb')
        fh.write(output)
        fh.close()
