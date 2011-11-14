from reportlab.platypus.flowables import Flowable


class Barcode(Flowable):
    def __init__(self, library, width, height, data, scale=1, type='datamatrix', align='left'):
        '''
        Creates a Barcode Flowable

        * width and height define the size in ReportLab points (for example 2*cm x 2*cm)
        * data will be encoded as the barcode
        * scale allows you to resize the barcode (default 1)
        * type is the type of the barcode (default 'datamatrix').
          Other types can be found in media/common/pdf_img/barcode.ps
        '''

        Flowable.__init__(self)

        self.width = width
        self.height = height
        self.scale = scale
        self.data = data
        self.resolution_factor = 8
        self.type = type
        self.hAlign = 'CENTER'
        self.library = library
        self.align = align

    def draw(self):
        import subprocess
        import tempfile
        import os

        # create a unique temporary file and keep it open to reserve the name, so we can create
        # another file with the same name plus a suffix. This is to guarantee that there will
        # be no race conditions forrandom file names.
        placeholder = tempfile.NamedTemporaryFile()

        temp_png = placeholder.name + '.png'

        # this is where our fancy postscript file is
        barcode_path = self.library

        # the arguments for ghostscript
        data = self.data
        res = 72 * self.resolution_factor * self.scale  # DPI resolution
        type = self.type

        bbox_proc = subprocess.Popen(['gs',
                                      '-sDEVICE=bbox',
                                      '-sBARCODEDATA=%(data)s' % locals(),
                                      '-dBARCODETYPE=/%(type)s' % locals(),
                                      '-q',
                                      '-dNOPAUSE',
                                      '-dBATCH',
                                      '-dSAFER',
                                      '-r%(res)d' % locals(),
                                      barcode_path],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      )

        raw_bbox = bbox_proc.communicate()
        if not len(raw_bbox[0]) and len(raw_bbox[1]):
            bbox = (float(i) for i in raw_bbox[1].splitlines()[1].split()[3:])
            pw, ph = bbox

            bbox_w = pw * self.scale
            bbox_h = ph * self.scale

            temp_w = pw * self.scale * self.resolution_factor
            temp_h = ph * self.scale * self.resolution_factor

            result = subprocess.call(['gs',
                                      '-sDEVICE=pngalpha',
                                      '-sOutputFile=%(temp_png)s' % locals(),
                                      '-sBARCODEDATA=%(data)s' % locals(),
                                      '-dBARCODETYPE=/%(type)s' % locals(),
                                      '-g%(temp_w)dx%(temp_h)d' % locals(),
                                      '-q',
                                      '-dNOPAUSE',
                                      '-dBATCH',
                                      '-dSAFER',
                                      '-r%(res)d' % locals(),
                                      barcode_path])

            if os.path.exists(temp_png):
                if self.align == 'left':
                    x = 0
                elif self.align == 'center':
                    x = (self.width - bbox_w) / 2.0
                else:
                    x = self.width - bbox_w
                y = self.height - bbox_h
                if y < 0:
                    y = 0
                self.canv.drawImage(temp_png, x, y, width=bbox_w, height=bbox_h if bbox_h < self.height else self.height)
                os.unlink(temp_png)

            else:
                self.canv.line(0, 0, self.width, self.height)
        else:
            self.canv.line(0, 0, self.width, self.height)

        placeholder.close()
