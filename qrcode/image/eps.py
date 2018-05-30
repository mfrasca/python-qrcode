from decimal import Decimal

import qrcode.image.base


class EpsImage(qrcode.image.base.BaseImage):
    """
    EPS image builder

    Creates a QR-code image as a Encapsulated PostScript document fragment.
    """

    _header = '''\
%!PS-Adobe-3.0
%%BoundingBox: 0 0 595 842
%%Creator: (Ghini)
%%For: (ghini)
%%CreationDate: (2016-01-15 21:34:45 )
%%Title: (Untitled1)
%%LanguageLevel: 2
%%DocumentData: Clean7Bit
%%Pages: (atend)
%%Orientation: Portrait
%%PageOrder: Ascend
%%EndComments
%%BeginProlog
%%EndProlog
%%BeginSetup
%%EndSetup
/SCALE { 0.45 0.45 scale 0 0 translate } bind def
%%Page: 1 1
%%BeginPageSetup
%%EndPageSetup
grestore

/M { moveto } bind def
/m { rmoveto } bind def
/l { rlineto } bind def

gsave
SCALE
0 1700 translate
0 0 0 setrgbcolor
1 setlinewidth
gsave
10 -200 translate
16 16 scale
newpath
'''
    _trailer = '''\
stroke

grestore
showpage

%%PageTrailer


%%Trailer
%%Pages: 1
%%EOF
'''
    
    def __init__(self, *args, **kwargs):
        super(EpsImage, self).__init__(*args, **kwargs)
        # Save the unit size, for example the default box_size of 10 is '1mm'.
        self.unit_size = self.units(self.box_size)
        self._rectangles = []

    def units(self, pixels, text=True):
        """
        A box_size of 10 (default) equals 1mm.
        """
        units = Decimal(pixels) / 10
        if not text:
            return units
        return '%smm' % units

    def drawrect(self, row, col):
        self._rectangles.append((row, col))

    def save(self, stream, kind=None):
        self.check_kind(kind=kind)
        stream.write(self._header.encode())
        for rect in self._rectangles:
            stream.write(('%s %s M 1 0 l' % rect).encode())
            stream.write(b'\n')
        stream.write(self._trailer.encode())
