
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
import locale
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.5 * inch,bottomMargin=1.5 * inch)#, showBoundary=1)
style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=15)
style.alignment=TA_CENTER
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)

item_style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=8)
item_style.alignment=TA_RIGHT

heading_style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=20)
heading_style.alignment=TA_CENTER

arabic_text = u'إذا أخذنا بعين'
arabic_text = arabic_reshaper.reshape(arabic_text) # join characters
arabic_text = get_display(arabic_text) # change orientation by using bidi   
# canvas.setFont('Arabic', 32)
# canvas.drawString(x - 100, y, ar)


def sales_return_canvas(canvas, doc_invoice):     
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Return.id == request.args(0)).select().first()    
        
    _customer = _id.customer_code_id.account_name#.upper() + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
    _so = [
        ['SALES RETURN DRAFT'],                         
        ['Sales No. ', ':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_return_no),'','Sales Return Date ',':',_id.sales_return_date.strftime('%d-%m-%Y')],
        ['Customer Code',':',_id.customer_code_id.account_code,'','Transaction Type',':','Credit'],             
        [_customer,'','','','Department',':',_id.dept_code_id.dept_name],
        ['','','','', 'Location', ':',_id.location_code_id.location_name],       
        ['','','','', 'Sales Man',':',str(_id.sales_man_id.employee_id.first_name.upper()) + ' ' + str(_id.sales_man_id.employee_id.last_name.upper())],
        ['','','','','','','']]
    header = Table(_so, colWidths=['*',10,'*',10,'*',10,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),        
        ('SPAN',(0,3),(3,-1)),        
        ('ALIGN',(0,0),(0,0),'CENTER'),                
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(-1,1),8),                
        ('FONTSIZE',(0,2),(-1,-1),8),                
        ('VALIGN',(0,3),(3,-1),'TOP'),        
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,0),20),
        
        ]))
    header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .9 * inch)
    _page = [['']]
    footer = Table(_page, colWidths=['*',10,'*',10,'*',10,'*'])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def get_sales_return_reports_id():  
    row = []
    _id = db(db.Sales_Return.id == request.args(0)).select().first()

    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty']]
    
    for t in db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(orderby = db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id)):        
        ctr += 1        
        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Return_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Return_Transaction.quantity, t.Sales_Return_Transaction.uom)

        if t.Sales_Return_Transaction.category_id == 3:
            _net_price = 'FOC-Price'
        else:
            _net_price = locale.format('%.2F',t.Sales_Return_Transaction.net_price or 0, grouping = True)
        if t.Sales_Return_Transaction.category_id != 4:
            _category = t.Sales_Return_Transaction.category_id.mnemonic
        else:
            _category = ''

        _st.append([ctr,Paragraph(t.Item_Master.item_code,style = _style), t.Item_Master.brand_line_code_id.brand_line_name+ '\n' + t.Item_Master.item_description, 
            t.Sales_Return_Transaction.uom, _category,_qty])
    _st.append(['---* nothing to follows *---'])   
    
    _st_tbl = Table(_st, colWidths=[20,60,'*',50,50,50],repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),            
        ('SPAN',(0,-1),(-1,-1)),       
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),   
        ('ALIGN',(0,-1),(-1,-1),'CENTER'),            
        ('VALIGN',(0,0),(-1,-1),'TOP')]))    
 
    _sr_rem = Table([['Remarks: ', _id.remarks]], colWidths=[80,'*'])
    _sr_rem.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),           
        ('VALIGN',(0,0),(-1,-1),'TOP')]))
    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_sr_rem)
    doc.build(row, onFirstPage=sales_return_canvas, onLaterPages = sales_return_canvas)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

