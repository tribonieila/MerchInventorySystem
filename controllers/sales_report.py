
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from textwrap import wrap
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas    
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# pdfmetrics.registerFont(TTFont('Arabic', '../fonts/ae_Arab.ttf'))
pdfmetrics.registerFont(TTFont('Arabic', '/home/larry/Workspace/web2py/applications/mtc_inv/static/fonts/ae_Arab.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/usr/share/fonts/truetype/fonts-arabeyes/ae_Arab.ttf'))
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.3 * inch,bottomMargin=1.5 * inch)#, showBoundary=1)
style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=15)
style.alignment=TA_CENTER

item_style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=8)
item_style.alignment=TA_RIGHT

heading_style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=20)
heading_style.alignment=TA_CENTER

_ar_sales_invoice = u'فاتورة المبيعات'
_ar_item_code = arabic_reshaper.reshape(_ar_sales_invoice)
arabic_text = Paragraph(get_display(_ar_item_code), item_style)

def print_arabic():
    # print 'arabic_text: ', arabic_text
    doc.build([['arabic_text']])
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data