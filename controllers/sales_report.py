
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

arabic_text = u'إذا أخذنا بعين'
arabic_text = arabic_reshaper.reshape(arabic_text) # join characters
arabic_text = get_display(arabic_text) # change orientation by using bidi   
# canvas.setFont('Arabic', 32)
# canvas.drawString(x - 100, y, ar)


def print_arabic_2():
    arabic_text = u'إذا أخذنا بعين الإعتبار طبيعة تقلب المناخ و المتغيرات البينية السنوية و تلك على المدى الطويل إضافة إلى عدم دقة القياسات والحسابات المتبعة'
    arabic_text = arabic_reshaper.reshape(arabic_text) # join characters
    # arabic_text = get_display(arabic_text) # change orientation by using bidi
    print arabic_text
    pdf_file=open('disclaimer.pdf','w')
    pdf_doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    pdfmetrics.registerFont(TTFont('Arabic-normal', '/home/larry/Workspace/web2py/applications/mtc_inv/static/fonts/ae_Arab.ttf'))
    style = ParagraphStyle(name='Normal', fontName='Arabic-normal', fontSize=12, leading=12. * 1.2)
    style.alignment=TA_RIGHT
    pdf_doc.build([Paragraph(arabic_text, style)])
    pdf_file.close()    

def print_arabic():
    print 'arabic_text: ', arabic_text    
    doc.build([Paragraph(arabic_text, heading_style)])    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data