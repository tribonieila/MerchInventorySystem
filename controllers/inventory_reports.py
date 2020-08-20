
##########          R E P O R T S           ##########

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, A3,landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time
import datetime

import locale
locale.setlocale(locale.LC_ALL,'')
from time import gmtime, strftime


today = datetime.datetime.now()

MaxWidth_Content = 530
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
# styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle(name='BodyText', fontSize=7)
_courier = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=80, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
a3 = SimpleDocTemplate(tmpfilename,pagesize=A3, topMargin=80, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
logo_path = request.folder + '/static/images/Merch.jpg'
img = Image(logo_path)
img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'


merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])

def _landscape_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage],['PRICE LIST REPORT']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .2 * cm)

    # Footer
    today = date.today()
    footer = Table([[merch],[today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ('LINEABOVE',(0,1),(0,1),0.25, colors.gray)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

def _stock_value_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage],['STOCK VALUE REPORT']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .2 * cm)

    # Footer
    today = date.today()
    footer = Table([[merch],[today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ('LINEABOVE',(0,1),(0,1),0.25, colors.gray)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

def _transfer_header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Footer
    # today = date.today()
    _trn = db(db.Stock_Request.id == request.args(0)).select().first()

    footer = Table([
        # [str(_trn.stock_transfer_approved_by.first_name.upper() + ' ' + _trn.stock_transfer_approved_by.last_name.upper()),'',''],
        # ['Issued by','Receive by', 'Delivered by'],
        # ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))],
        # # ['','- - WAREHOUSE COPY - -',''],
        [merch,''],['',request.now.strftime("%A %d. %B %Y, %I:%M%p ")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(1,1),8),
        ('ALIGN',(1,1),(1,1),'RIGHT'),        
        ('LINEABOVE',(0,1),(1,1),1, colors.Color(0, 0, 0, 0.55))
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

def _header_footer_stock_receipt(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        # ('LINEBELOW',(0,0),(0, 0),0.10, colors.gray),
        # ('BOTTOMPADDING',(0,0),(0, 1),10)
        # ('TOPPADDING',(0,2),(1,2),6)
        ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .6 * inch)


    # Footer
    # today = date.today()
    _stk_req = db(db.Stock_Receipt.id == request.args(0)).select().first()
    if _stk_req.stock_receipt_approved_by == None:
        _approved_by = 'None'
    else:
        _approved_by = str(_stk_req.stock_receipt_approved_by.first_name.upper() + ' ' + _stk_req.stock_receipt_approved_by.last_name.upper())
    
    footer = Table([
        ['','Received by:','','Delivered by:',''],
        ['',_approved_by,'','',''],
        ['','Name and Signature','','Name and Signature',''],
        [merch,'','','',''],
        [today.strftime("Printed on %A %d. %B %Y, %I:%M%p "),'','','','']], colWidths=[50,'*',50,'*',50])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('ALIGN',(0,0),(-1,2),'CENTER'),        
        ('FONTNAME',(0,0),(-1,-2),'Courier'),
        ('TOPPADDING',(0,0),(-1,1),0),
        ('BOTTOMPADDING',(0,0),(-1,1),0),        
        ('SPAN',(0,-2),(4,-2)),        
        ('SPAN',(0,-1),(4,-1)),
        ('BOTTOMPADDING',(0,0),(-1,0),30),
        ('LINEBELOW',(1,1),(1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW',(3,1),(3,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE',(0,-1),(-1,-1),0.25, colors.black),        
        ('ALIGN',(0,-1),(4,-1),'RIGHT'),
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

def _header_footer_stock_adjustment(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .1 * inch)


    # Footer
    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()    
    if _stk_adj.approved_by:
        _approved_or_not = str(_stk_adj.approved_by.first_name.upper()) + ' ' + str(_stk_adj.approved_by.last_name.upper())
    else:
        _approved_or_not = ''

    footer = Table([
        [str(_stk_adj.created_by.first_name.upper() + ' ' + _stk_adj.created_by.last_name.upper()), _approved_or_not],        
        
        ['Requested by:','Approved by:'],
        ['',''],
        [merch,''],['',today.strftime("%A %d. %B %Y, %I:%M%p ")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('TEXTCOLOR',(0,0),(0,0), colors.gray),

        ('FONTSIZE',(0,0),(-1,1),8),
        ('FONTSIZE',(0,4),(1,4),8),
        ('ALIGN',(0,0),(-1,1),'CENTER'),
        ('ALIGN',(0,4),(1,4),'RIGHT'),
        ('LINEABOVE',(0,4),(1,4),0.25, colors.black)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

import inflect 
from decimal import Decimal
w=inflect.engine()

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        # ('LINEBELOW',(0,0),(0, 0),0.10, colors.gray),
        # ('BOTTOMPADDING',(0,0),(0, 1),10)
        # ('TOPPADDING',(0,2),(1,2),6)
        ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .6 * inch)


    # Footer
    
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    if _stk_req.srn_status_id != 2:
        _approved_by = None
    else:
        _approved_by = str(_stk_req.stock_request_approved_by.first_name.upper() + ' ' + _stk_req.stock_request_approved_by.last_name.upper())
    footer = Table([
        [merch,''],['',today.strftime("%A %d. %B %Y, %I:%M%p ")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,1),8),
        ('ALIGN',(0,1),(1,1),'RIGHT'),
        ('LINEABOVE',(0,1),(1,1),0.25, colors.black)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_rpt():    
    _grand_total = 0
    ctr = 0
    _total = 0
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK REQUEST'],               
            ['Stock Request No:',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stcok Request Date:',':',s.Stock_Request.stock_request_date.strftime('%d-%m-%Y')],
            ['Stock Request From:',':',s.Stock_Request.stock_source_id.location_name,'','Stock Request To:',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department:',':',s.Stock_Request.dept_code_id.dept_name,'','Remarks',':',s.Stock_Request.remarks]]

    # stk_tbl = Table(stk_req_no, colWidths=[120, 150,120,150 ])
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,0),(0,0),5),        
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTSIZE',(0,1),(-1,-1),8)]))
    
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)]):
        _query = db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock).first()
        if _query:
            _closing_stock = card(i.Stock_Request_Transaction.item_code_id, _query.closing_stock,i.Stock_Request_Transaction.uom)
        else:
            _closing_stock = 0        
        ctr += 1
        _total = i.Stock_Request_Transaction.total_amount
        _grand_total += _total            
        # _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, i.Stock_File.closing_stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str('Remarks: ')+str(i.Stock_Request_Transaction.remarks),        
        i.Item_Master.uom_id.description,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Stock_Request_Transaction.item_code_id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.unit_price,
        # _closing_stock,
        locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))

    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])


    # stk_trn.append(['','', '','', '','','','','TOTAL AMOUNT:',locale.format('%.2F',_grand_total or 0, grouping = True)])


    trn_tbl = Table(stk_trn, colWidths = [25,55,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)
    # stock_transaction_table()
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    if _stk_req.srn_status_id != 2:
        _approved_by = None
    else:
        _approved_by = str(_stk_req.stock_request_approved_by.first_name.upper() + ' ' + _stk_req.stock_request_approved_by.last_name.upper())

    signatory = [[str(_stk_req.created_by.first_name.upper() + ' ' + _stk_req.created_by.last_name.upper()),_approved_by],['Requested by:','Approved by:']]
    signatory_table = Table(signatory, colWidths='*')
    signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,1),8),     
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),   
        ('ALIGN',(0,0),(-1,1),'CENTER')]))
    row.append(Spacer(1,.9*cm))
    row.append(signatory_table)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data   

def stock_transaction_table():
    ctr = _grand_total= 0
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','SOH','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL,
    left = [
        db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),         
        db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)
        ]):
        for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
            ctr += 1
            _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
            _grand_total += _total
            _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, l.closing_stock, i.Stock_Request_Transaction.uom)
            stk_trn.append([ctr,
            i.Stock_Request_Transaction.item_code_id.item_code,        
            str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks),        
            i.Item_Master.uom_id.mnemonic,
            i.Stock_Request_Transaction.category_id.mnemonic,
            i.Stock_Request_Transaction.uom,
            card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
            i.Stock_Request_Transaction.retail_price,
            _stock_on_hand,
            locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))

    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])


    trn_tbl = Table(stk_trn, colWidths = [25,55,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    return row.append(trn_tbl)

# @auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_transaction_report():
    _id = request.args(0)
    _grand_total = 0    
    ctr = 0
    _total = 0
    for s in db(db.Stock_Transfer.id == _id).select(db.Stock_Transfer.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Transfer.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK TRANSFER'],               
            ['Stock Transfer No',':', str(s.Stock_Transfer.stock_transfer_no_id.prefix)+str(s.Stock_Transfer.stock_transfer_no),'', 'Stock Transaction Date',':',str(s.Stock_Transfer.stock_transfer_date_approved.strftime('%d-%m-%Y,%H:%M %p'))],
            ['Stock Request No',':',str(s.Stock_Transfer.stock_request_no_id.prefix)+str(s.Stock_Transfer.stock_request_no),'', 'Stock Request Date',':',str(s.Stock_Transfer.stock_request_date_approved.strftime('%d-%m-%Y,%H:%M %p'))],
            ['Stock Transfer From',':',s.Stock_Transfer.stock_source_id.location_name,'','Stock Transfer To',':',s.Stock_Transfer.stock_destination_id.location_name],
            ['Department',':',s.Stock_Transfer.dept_code_id.dept_name,'','','','']]        
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,0),(0,0),5),        
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTSIZE',(0,1),(-1,-1),8)]))

    ctr = _grand_total= 0
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Transfer.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Stock_Transfer.on(db.Stock_Transfer.id == db.Stock_Request_Transaction.stock_request_id)]):
        # for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Transfer.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
        _soh = db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Transfer.stock_destination_id)).select().first()
        if not _soh:
            _stock = 0
        else:
            _stock = _soh.closing_stock
        ctr += 1
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total        
        _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, _stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        Paragraph(i.Stock_Request_Transaction.item_code_id.item_code, style=_style),        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks)+str('\n')+str('SOH: ')+str(_stock_on_hand),        
        i.Item_Master.uom_id,
        # i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.retail_price,
        # _stock_on_hand,
        locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))

    _pc = db(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0)).select().first()
    if not _pc:
        _ctr = 1
        db.Stock_Request_Transaction_Report_Counter.insert(stock_transfer_no_id = request.args(0), printer_counter = _ctr)
    else:
        _pc.printer_counter += 1
        _ctr = _pc.printer_counter
        db.Stock_Request_Transaction_Report_Counter.update_or_insert(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0), printer_counter = _ctr,updated_on = request.now,updated_by = auth.user_id)

    _trn = db(db.Stock_Transfer.id == request.args(0)).select().first()
    signatory = [
        [str(_trn.stock_transfer_approved_by.first_name.upper() + ' ' + _trn.stock_transfer_approved_by.last_name.upper()),'',''],
        ['Issued by','Receive by', 'Delivered by'],
        ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))]]

    signatory_table = Table(signatory, colWidths='*')
    signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),      
    ]))
    _printer = [['PRINT COUNT: ' + str(_ctr)]]
    _warehouse = [['- - WAREHOUSE COPY - -']]
    _accounts = [['- - ACCOUNTS COPY - -']]
    _pos = [['- - POS COPY - -']]

    
    _w_tbl = Table(_warehouse, colWidths='*')
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')
    _c_tbl = Table(_printer, colWidths='*')

    _w_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'),('FONTNAME', (0, 0), (-1, -1), 'Courier'),('FONTSIZE',(0,0),(-1,-1),8)]))
    _a_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _p_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _c_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_w_tbl)
    row.append(_c_tbl)
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_a_tbl)
    row.append(_c_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_p_tbl)
    row.append(_c_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    doc.build(row, onFirstPage=_transfer_header_footer, onLaterPages=_transfer_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data   

def get_stock_transfer_report_id():    # final report 
    _id = db(db.Stock_Transfer.id == request.args(0)).select().first()
    _grand_total = 0    
    ctr = 0
    _total = 0    
    
    
    for s in db(db.Stock_Transfer.id == request.args(0)).select():        
        stk_req_no = [
            ['STOCK TRANSFER VOUCHER'],               
            ['Stock Transfer No',':', str(s.stock_transfer_no_id.prefix)+str(s.stock_transfer_no),'', 'Stock Transaction Date',':',str(s.stock_transfer_date_approved.strftime('%d-%m-%Y,%H:%M %p'))],
            ['Stock Request No',':',str(s.stock_request_no_id.prefix)+str(s.stock_request_no),'', 'Stock Request Date',':',str(s.stock_request_date_approved.strftime('%d-%m-%Y,%H:%M %p'))],
            ['Stock Transfer From',':',s.stock_source_id.location_name,'','Stock Transfer To',':',s.stock_destination_id.location_name],
            ['Department',':',s.dept_code_id.dept_name,'','','','']]        
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,0),(0,0),5),        
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTSIZE',(0,1),(-1,-1),8)]))

    ctr = _grand_total= 0
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for i in db((db.Stock_Transfer_Transaction.stock_transfer_no_id == request.args(0)) & (db.Stock_Transfer_Transaction.delete == False)).select(db.Stock_Transfer_Transaction.ALL, db.Item_Master.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Transfer_Transaction.item_code_id)):
        # for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
        _soh = db((db.Stock_File.item_code_id == i.Stock_Transfer_Transaction.item_code_id) & (db.Stock_File.location_code_id == _id.stock_destination_id)).select().first()
        if not _soh:
            _stock = 0
        else:
            _stock = _soh.closing_stock
        ctr += 1
        # _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += i.Stock_Transfer_Transaction.total_amount        
        _stock_on_hand = card(i.Stock_Transfer_Transaction.item_code_id, _stock, i.Stock_Transfer_Transaction.uom)
        if i.Item_Master.uom_id == None:
            _uom = ''
        else:
            _uom = i.Item_Master.uom_id.mnemonic
        stk_trn.append([ctr,
        Paragraph(i.Stock_Transfer_Transaction.item_code_id.item_code, style=_style),        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+
        str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Transfer_Transaction.remarks)+str('\n')+str('SOH: ')+str(_stock_on_hand),        
        _uom,
        # i.Item_Master.uom_id.mnemonic,
        i.Stock_Transfer_Transaction.category_id.mnemonic,
        i.Stock_Transfer_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Transfer_Transaction.quantity, i.Stock_Transfer_Transaction.uom),        
        i.Stock_Transfer_Transaction.unit_price,
        # _stock_on_hand,
        locale.format('%.2F',i.Stock_Transfer_Transaction.total_amount or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))

    # _pc = db(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0)).select().first()
    # if not _pc:
    #     _ctr = 1
    #     db.Stock_Request_Transaction_Report_Counter.insert(stock_transfer_no_id = request.args(0), printer_counter = _ctr)
    # else:
    #     _pc.printer_counter += 1
    #     _ctr = _pc.printer_counter
    #     db.Stock_Request_Transaction_Report_Counter.update_or_insert(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0), printer_counter = _ctr,updated_on = request.now,updated_by = auth.user_id)

    _trn = db(db.Stock_Request.id == request.args(0)).select().first()
    signatory = [
        [str(_trn.stock_transfer_approved_by.first_name.upper() + ' ' + _trn.stock_transfer_approved_by.last_name.upper()),'',''],
        ['Issued by','Receive by', 'Delivered by'],
        ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))]]

    signatory_table = Table(signatory, colWidths='*')
    signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),      
    ]))
    _printer = [['PRINT COUNT: ' + str(0)]]
    _warehouse = [['- - WAREHOUSE COPY - -']]
    _accounts = [['- - ACCOUNTS COPY - -']]
    _pos = [['- - POS COPY - -']]

    
    _w_tbl = Table(_warehouse, colWidths='*')
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')
    _c_tbl = Table(_printer, colWidths='*')

    _w_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'),('FONTNAME', (0, 0), (-1, -1), 'Courier'),('FONTSIZE',(0,0),(-1,-1),8)]))
    _a_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _p_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _c_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_w_tbl)
    # row.append(_c_tbl)
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_a_tbl)
    # row.append(_c_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_p_tbl)
    # row.append(_c_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    doc.build(row, onFirstPage=_transfer_header_footer, onLaterPages=_transfer_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

def stock_request_report():    
    _grand_total = ctr = 0
    # ctr = 00,0
    _total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK REQUEST'],               
            ['Stock Request No',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stock Request Date:',':',s.Stock_Request.stock_request_date], #.strftime('%d-%m-%Y, %-I:%M %p')],
            ['Stock Request From', ':',s.Stock_Request.stock_source_id.location_name,'','Stock Request To',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department', ':',s.Stock_Request.dept_code_id.dept_name,'','','','']]
        
    # stk_tbl = Table(stk_req_no, colWidths=[120, 150,150,120 ])
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),    
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('FONTSIZE',(0,1),(-1,-1),8)]))
        
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select():
        ctr += 1
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        # _price_cost = n.quantity * n.price_cost
        _grand_total +=n.total_amount
        stk_trn.append([ctr,Paragraph(n.item_code_id.item_code, style=_style),str(_i.brand_line_code_id.brand_line_name) + str('\n') + str(_i.item_description),
        _i.uom_id,n.category_id.mnemonic,n.uom,card(_i.id,n.quantity,n.uom),locale.format('%.2F',n.price_cost or 0, grouping = True),locale.format('%.2F',n.total_amount or 0, grouping = True)])
        # _i.uom_id.mnemonic,n.category_id.mnemonic,n.uom,card(_i.id,n.quantity,n.uom),locale.format('%.2F',n.price_cost or 0, grouping = True),locale.format('%.2F',n.total_amount or 0, grouping = True)])
    # for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL,
    # left = [
    #     db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),         
    #     db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)
    #     ]):
    #     for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
    #         ctr += 1
    #         _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
    #         _grand_total += _total
    #         _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, l.closing_stock, i.Stock_Request_Transaction.uom)
    #         stk_trn.append([ctr,
    #         Paragraph(i.Stock_Request_Transaction.item_code_id.item_code, style=_style),
    #         str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks),        
    #         i.Item_Master.uom_id.mnemonic,
    #         i.Stock_Request_Transaction.category_id.mnemonic,
    #         i.Stock_Request_Transaction.uom,
    #         card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
    #         i.Stock_Request_Transaction.retail_price,
    #         # _stock_on_hand,
    #         locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])    
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    
    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths = [75,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier')]))    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_remarks_table)

    doc.build(row, onFirstPage=_header_footer_stock_receipt, onLaterPages=_header_footer_stock_receipt)
    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

# @auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def get_stock_receipt_report_id():    # final report 
    _grand_total = ctr = 0
    # ctr = 00,0
    _total = 0
    _id = db(db.Stock_Receipt.id == request.args(0)).select().first()
    for s in db(db.Stock_Receipt.id == request.args(0)).select():        
        stk_req_no = [
            ['STOCK RECEIPT'],               
            ['Stock Receipt No',':',str(s.stock_receipt_no_id.prefix)+str(s.stock_receipt_no), '','Stock Receipt Date:',':',s.stock_receipt_date_approved],# .strftime('%d-%m-%Y, %-I:%M %p') [today.strftime("Printed on %A %d. %B %Y, %I:%M%p "),'','','','']], colWidths=[50,'*',50,'*',50])
            ['Stock Transfer No',':',str(s.stock_transfer_no_id.prefix)+str(s.stock_transfer_no), '','Stock Transfer Date:',':',s.stock_transfer_date_approved], #.strftime('%d-%m-%Y, %-I:%M %p')
            ['Stock Request No',':',str(s.stock_request_no_id.prefix)+str(s.stock_request_no),'', 'Stock Request Date:',':',s.stock_request_date_approved], #.strftime('%d-%m-%Y, %-I:%M %p')
            ['Stock Request From', ':',s.stock_source_id.location_name,'','Stock Request To',':',s.stock_destination_id.location_name],
            ['Department', ':',s.dept_code_id.dept_name,'','','','']]
        
    # stk_tbl = Table(stk_req_no, colWidths=[120, 150,150,120 ])
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),    
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('FONTSIZE',(0,1),(-1,-1),8)]))
        
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for n in db((db.Stock_Receipt_Transaction.stock_receipt_no_id == request.args(0)) & (db.Stock_Receipt_Transaction.delete == False)).select():
        ctr += 1
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        # _price_cost = n.quantity * n.price_cost
        _grand_total +=n.total_amount
        stk_trn.append([ctr,Paragraph(n.item_code_id.item_code, style=_style),str(_i.brand_line_code_id.brand_line_name) + str('\n') + str(_i.item_description),
        _i.uom_id.mnemonic,n.category_id.mnemonic,n.uom,card(_i.id,n.quantity,n.uom),locale.format('%.2F',n.unit_price or 0, grouping = True),locale.format('%.2F',n.total_amount or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])    
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    
    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths = [75,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier')]))    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_remarks_table)

    doc.build(row, onFirstPage=_header_footer_stock_receipt, onLaterPages=_header_footer_stock_receipt)
    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

def stock_adjustment_report():
    ctr = 0
    _grand_total = _selective_tax = 0
    _id = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    for r in db(db.Stock_Adjustment.id == request.args(0)).select():
        stk_adj = [
            ['STOCK ADJUSTMENT'],
            ['Stock Adjustment',':', str(r.stock_adjustment_no_id.prefix)+str(r.stock_adjustment_no),'','Stock Adjustment Date',':',r.date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Transaction No.',':', str(r.transaction_no)+'/'+str(r.transaction_date.strftime('%d-%m-%Y')),'','Location',':',r.location_code_id.location_name],
            ['Department',':', r.dept_code_id.dept_name,'','Stock Adjustment Code',':',r.stock_adjustment_code],
            ['Adjustment Type',':', r.adjustment_type.description,'','Status',':', r.srn_status_id.description]]
    stk_adj_tbl = Table(stk_adj, colWidths=['*',15,'*',15,'*',15,'*'])
    stk_adj_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('BACKGROUND',(0,1),(3,1),colors.gray),
        ('BOTTOMPADDING',(0,0),(3,0),15),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'), 
        ('ALIGN',(0,0),(3,0),'CENTER'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        # ('FONTSIZE',(0,1),(3,1),9),
        ('FONTSIZE',(0,0),(3,0),15),
        ('FONTNAME',(0,0),(3,0),'Courier-Bold',12),
        ('SPAN',(0,0),(6,0)),
    ]))
    

    stk_adj_trnx = [['#','Item Code','Item Description','Cat.','UOM','Qty','Price','Total']]
    for r in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(orderby = db.Stock_Adjustment_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        
        ctr += 1
        # _total = r.Stock_Adjustment_Transaction.quantity * r.Stock_Adjustment_Transaction.price_cost
        _grand_total += r.Stock_Adjustment_Transaction.total_amount
        # _selective_tax += r.Stock_Adjustment_Transaction.selective_tax

        stk_adj_trnx.append([
            ctr,
            r.Stock_Adjustment_Transaction.item_code_id.item_code,
            str(r.Item_Master.brand_line_code_id.brand_line_name) +str('\n') +str(r.Item_Master.item_description),
            r.Stock_Adjustment_Transaction.category_id.mnemonic,
            r.Stock_Adjustment_Transaction.uom,
            # r.Stock_Adjustment_Transaction.quantity,
            card(r.Stock_Adjustment_Transaction.item_code_id, r.Stock_Adjustment_Transaction.quantity,r.Stock_Adjustment_Transaction.uom),
            locale.format('%.2F',r.Stock_Adjustment_Transaction.average_cost or 0, grouping = True),
            locale.format('%.2F',r.Stock_Adjustment_Transaction.total_amount or 0, grouping = True)
        ])
    stk_adj_trnx.append(['','','','','','','GRAND TOTAL:',locale.format('%.2F',_grand_total or 0, grouping = True)])
    stk_adj_trnx.append(['------- nothing to follows -------'])
    stk_adj_trnx_tbl = Table(stk_adj_trnx, colWidths=[25,60,'*',40,40,50,50,50])
    stk_adj_trnx_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        # ('BACKGROUND',(0,0),(-1,0),colors.gray),
        # ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN', (0,1), (-1,-1), 'TOP'),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
        ('LINEABOVE', (0,0), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.black,None, (2,2)),
        # ('LINEABOVE', (0,-1), (-1,-1), .5, colors.black),
        ('SPAN',(0,-1),(-1,-1)),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,-1),(-1,-1),20),   
        
    ]))
    if _id.srn_status_id == 15:
        _approved_by = str(_id.approved_by.first_name.upper()) + ' ' + str(_id.approved_by.last_name.upper())                
    else:
        _approved_by = ''
    _sign = [['',str(_id.created_by.first_name.upper()) + ' ' + str(_id.created_by.last_name.upper()),'',_approved_by,''],
    ['','Requested by:','','Approved/Posted by:','']]
    _sign_tbl = Table(_sign,colWidths=[50,'*',50,'*',50])
    _sign_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('LINEABOVE', (1,1), (1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (3,1), (3,1), 0.25, colors.black,None, (2,2)),
    ]))

    row.append(stk_adj_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(stk_adj_trnx_tbl)
    row.append(Spacer(1,3*cm))
    row.append(_sign_tbl)
    doc.build(row)#, onFirstPage=_header_footer_stock_adjustment, onLaterPages=_header_footer_stock_adjustment)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data 

def stock_adjustment_store_report():
    ctr = 0
    _grand_total = 0
    for r in db(db.Stock_Adjustment.id == request.args(0)).select():
        stk_adj = [
            ['STOCK ADJUSTMENT','','',''],
            ['STOCK ADJUSTMENT:', str(r.stock_adjustment_no_id.prefix)+str(r.stock_adjustment_no),'STOCK ADJUSTMENT DATE:',r.date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Department:', r.dept_code_id.dept_name,'Location:',r.location_code_id.location_name],
            ['Adjustment Type:', r.adjustment_type.description,'Stock Adjustment Code:',r.stock_adjustment_code],
            ['Status:', r.srn_status_id.description,'',''],
        ]
    stk_adj_tbl = Table(stk_adj, colWidths='*')
    stk_adj_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('BACKGROUND',(0,1),(3,1),colors.gray),
        ('BOTTOMPADDING',(0,0),(3,0),15),
        ('ALIGN',(0,0),(3,0),'CENTER'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTSIZE',(0,1),(3,1),9),
        ('FONTSIZE',(0,0),(3,0),12),
        ('SPAN',(0,0),(3,0)),
    ]))
    row.append(stk_adj_tbl)

    stk_adj_trnx = [['#','ITEM CODE','ITEM DESCRIPTION','CAT.','QTY']]
    for r in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        
        ctr += 1
        _total = r.Stock_Adjustment_Transaction.quantity * r.Stock_Adjustment_Transaction.average_cost
        _grand_total += _total
        stk_adj_trnx.append([
            ctr,
            r.Stock_Adjustment_Transaction.item_code_id.item_code,
            str(r.Item_Master.brand_line_code_id.brand_line_name) +str('\n') +str(r.Item_Master.item_description),
            r.Stock_Adjustment_Transaction.category_id.mnemonic,
            # r.Stock_Adjustment_Transaction.uom,
            # r.Stock_Adjustment_Transaction.quantity,
            card(r.Stock_Adjustment_Transaction.item_code_id, r.Stock_Adjustment_Transaction.quantity,r.Stock_Adjustment_Transaction.uom),
            # locale.format('%.4F',r.Stock_Adjustment_Transaction.average_cost or 0, grouping = True),
            # locale.format('%.4F',_total or 0, grouping = True)
        ])
    # stk_adj_trnx.append(['','','','','','','GRAND TOTAL:',locale.format('%.4F',_grand_total or 0, grouping = True)])
    stk_adj_trnx_tbl = Table(stk_adj_trnx, colWidths=[25,60,'*',40,40])
    stk_adj_trnx_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('BACKGROUND',(0,0),(-1,0),colors.gray),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN', (0,1), (-1,-1), 'TOP'),
        # ('ALIGN',(6,1),(7,-1),'RIGHT'),
        # ('LINEABOVE', (0,-1), (-1,-1), .5, colors.black),
        # ('SPAN',(0,-1),(6,-1)),
        
    ]))
    row.append(Spacer(1,.5*cm))
    row.append(stk_adj_trnx_tbl)

    doc.build(row, onFirstPage=_header_footer_stock_adjustment, onLaterPages=_header_footer_stock_adjustment)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data     

def master_item_view():
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form.accepts(request): 
        if not request.vars.item_code_id:
            response.flash = 'NO ITEM CODE ENTERED'
        else:
            row = []
            i_row = []
            ctr = 0
            _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
            _stk_file = db(db.Stock_File.item_code_id == request.vars.item_code_id).select().first()
            _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()

            _outer = int(int(_stk_file.probational_balance) / int(_itm_code.uom_value))
            _pcs = int(_stk_file.probational_balance) - int(_outer * _itm_code.uom_value)    
            _on_hand = str(_outer) + ' ' + str(_pcs) + '/' +str(_itm_code.uom_value)

            _outer_transit = int(_stk_file.stock_in_transit) / int(_itm_code.uom_value)   
            _pcs_transit = int(_stk_file.stock_in_transit) - int(_outer * _itm_code.uom_value)
            _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_itm_code.uom_value)

            _outer_on_hand = int(_stk_file.closing_stock) / int(_itm_code.uom_value)
            _pcs_on_hand = int(_stk_file.closing_stock) - int(_outer_on_hand * _itm_code.uom_value) 
            _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_itm_code.uom_value)        
            
            i_head = THEAD(TR(TD('Item Code'),TD('Description'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Retail Price'),TD('Whole Sale Price'),TD('Van Sale Price')))
            
            i_row.append(TR(TD(_itm_code.item_code),TD(_itm_code.item_description),TD(_itm_code.group_line_id.group_line_name),
            TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),
            TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),
            TD(locale.format('%.2F',_item_price.wholesale_price or 0, grouping = True)),
            TD(locale.format('%.2F',_item_price.vansale_price or 0, grouping = True))))
            i_body = TBODY(*i_row)
            i_table = TABLE(*[i_head, i_body], _class = 'table')

            head = THEAD(TR(TD('#'),TD('Location Code'),TD('Opening Stock'),TD('Closing Stock'),TD('Stock In Transit'),TD('Provisional Balance'),TD('Free Stock'),TD('Damaged Stock'),TD('POS Stock')))
            
            for i in db().select(db.Stock_File.ALL, db.Location.ALL, orderby = db.Location.id, left = db.Stock_File.on((db.Stock_File.location_code_id == db.Location.id) & (db.Stock_File.item_code_id == request.vars.item_code_id))):
                ctr += 1
                _available_balanced = int(i.Stock_File.closing_stock or 0) - int(i.Stock_File.stock_in_transit or 0)
                if _itm_code.uom_value == 1:
                    _os = i.Stock_File.opening_stock or 0
                    _cl = i.Stock_File.closing_stock or 0
                    _st = i.Stock_File.stock_in_transit or 0
                    _av = i.Stock_File.probational_balance or 0#int(i.Stock_File.closing_stock or 0) + int(i.Stock_File.stock_in_transit or 0)
                    _fs = i.Stock_File.free_stock_qty or 0
                    _ds = i.Stock_File.damaged_stock_qty or 0
                else:
                    _os = card_view(i.Stock_File.item_code_id, i.Stock_File.opening_stock)
                    _cl = card_view(i.Stock_File.item_code_id, i.Stock_File.closing_stock)
                    _st = card_view(i.Stock_File.item_code_id, i.Stock_File.stock_in_transit)
                    # _av = card_view(i.Stock_File.item_code_id, _available_balanced)
                    _av = card_view(i.Stock_File.item_code_id, i.Stock_File.probational_balance)
                    _fs = card_view(i.Stock_File.item_code_id, i.Stock_File.free_stock_qty)
                    _ds = card_view(i.Stock_File.item_code_id, i.Stock_File.damaged_stock_qty)
                    _po = card_view(i.Stock_File.item_code_id, i.Stock_File.pos_stock)

                row.append(TR(TD(ctr),TD(i.Location.location_name),
                TD(_os),
                TD(_cl),
                TD(_st),
                TD(_av),
                TD(_fs),
                TD(_ds),
                TD(_po))) 
                # TD(i.Stock_File.opening_stock or 0, grouping = True),                
                # TD(i.Stock_File.closing_stock or 0, grouping = True),
                # TD(i.Stock_File.stock_in_transit or 0, grouping = True),
                # TD(_avl_bal or 0, grouping = True)))         
            body = TBODY(*row)
            table = TABLE(*[head, body], _class = 'table')
            return dict(form = form, i_table = i_table, table = table)
    return dict(form = form, table = '', i_table = '')

def stock_card_movement():
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('location_code_id', 'reference Location', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('start_date','date', default= request.now, requires = IS_DATE()),
        Field('end_date','date', default = request.now, requires = IS_DATE()))
    if form.accepts(request):
        # response.flash = 'ok'
        _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()
        _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
        i_row = []
        i_head = THEAD(TR(TD('Item Code'),TD('Description'),TD('Opening Stock'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Retail Price'),TD('Whole Sale Price'),TD('Van Sale Price')))
        i_row.append(TR(TD(_itm_code.item_code),TD(_itm_code.item_description),
        TD(card_view(_itm_code.id, _stk_file.opening_stock)),
        TD(_itm_code.group_line_id.group_line_name),
        TD(_itm_code.brand_line_code_id.brand_line_name),
        TD(_itm_code.uom_value),
        TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),
        TD(locale.format('%.2F',_item_price.wholesale_price or 0, grouping = True)),
        TD(locale.format('%.2F',_item_price.vansale_price or 0, grouping = True))))
        i_body = TBODY(*i_row)
        i_table = TABLE(*[i_head, i_body], _class = 'table')

        head = THEAD(TR(TH('#'),TH('Type'),TH('Voucher No'),TH('Date'),TH('Category'),TH('Qty In'),TH('Qty Out'),TH('Balance')))
        row = []
        ctr = 0
        
        _stv = db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id     
        _stv &= db.Stock_Request.stock_source_id == request.vars.location_code_id
        _stv &= db.Stock_Request.srn_status_id == 6
        _stv &= db.Stock_Request.stock_transfer_date_approved >= request.vars.start_date
        _stv &= db.Stock_Request.stock_transfer_date_approved <= request.vars.end_date



        # query = db(_pr).select(db.Purchase_Receipt.ALL, db.Purchase_Receipt_Transaction.ALL, db.Stock_Request_Transaction.ALL, db.Stock_Request.ALL, 
        # left = [db.Stock_Request_Transaction.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id), db.Purchase_Receipt_Transaction.on(db.Purchase_Receipt.id == db.Purchase_Receipt_Transaction.purchase_receipt_no_id)]) 
        _bal = 0
        _bal = _stk_file.opening_stock
        # print 'stv: ', _stv
        
        _total_qty = db.Merch_Stock_Transaction.quantity.sum().coalesce_zero()
        _query = db.Merch_Stock_Transaction.item_code == _itm_code.item_code
        _query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id
        _query &= db.Merch_Stock_Transaction.transaction_date >= request.vars.start_date
        _query &= db.Merch_Stock_Transaction.transaction_date <= request.vars.end_date
        _qty = db().select(_total_qty).first()[_total_qty]
        print _itm_code.item_code, request.vars.location_code_id,request.vars.start_date,request.vars.end_date
        for n in db(_query).select(_total_qty, db.Merch_Stock_Transaction.voucher_no, db.Merch_Stock_Transaction.transaction_type, db.Merch_Stock_Transaction.transaction_date, db.Merch_Stock_Transaction.category_id, groupby = db.Merch_Stock_Transaction.voucher_no | db.Merch_Stock_Transaction.transaction_type | db.Merch_Stock_Transaction.transaction_date | db.Merch_Stock_Transaction.category_id, orderby = db.Merch_Stock_Transaction.voucher_no , left = db.Merch_Stock_Header.on(db.Merch_Stock_Header.id == db.Merch_Stock_Transaction.merch_stock_header_id)):
            # _qty += n.quantity
            print 'voucher no:: ', n._extra[_total_qty], _qty, n.Merch_Stock_Transaction.transaction_type
            # db.Merch_Stock_Transaction.transaction_type, 
            # db.Merch_Stock_Transaction.voucher_no,
            # db.Merch_Stock_Transaction.transaction_date,
            # db.Merch_Stock_Transaction.category_id,
            # db.Merch_Stock_Transaction.quantity, 
            # groupby=db.Merch_Stock_Transaction.voucher_no):
            # groupby=db.Merch_Stock_Transaction.transaction_type|db.Merch_Stock_Transaction.voucher_no|db.Merch_Stock_Transaction.transaction_date|db.Merch_Stock_Transaction.category_id|db.Merch_Stock_Transaction.quantity):
            
            ctr += 1            

            _type = n.Merch_Stock_Transaction.transaction_type
            _no = n.Merch_Stock_Transaction.voucher_no
            _date = n.Merch_Stock_Transaction.transaction_date
            _category = n.Merch_Stock_Transaction.category_id
            _quantity_in = 0 
            _quantity_out = 0
            _balanced = 0

            if _type == 1:
                _quantity_in = 1
                _quantity_out = 0 #card_view(_itm_code.id, n.quantity)
                _balanced = _quantity_out - _quantity_in
            elif _type == 2:
                _quantity_in = 0
                _quantity_out = n._extra[_total_qty]
                _balanced = _quantity_out - _quantity_in
            elif _type == 3:
                _quantity_in = 1
                _quantity_out = 0
                _balanced = 0
            elif _type == 4:
                _quantity_in = 1
                _quantity_out = 0
                _balanced = 0
            elif _type == 5:
                _quantity_in = 1
                _quantity_out = 0
                _balanced = 0
            elif _type == 6:
                _quantity_in = 1
                _quantity_out = 0
                _balanced = 0
            elif _type == 7:
                _quantity_in = 1
                _quantity_out = 0
                _balanced = 0
            elif _type == 8:
                _quantity_in = 1
                _quantity_out = 0
                _balanced = 0


            row.append(TR(TD(ctr),
            TD(_type),
            TD(_no),
            TD(_date),                                        
            TD(_category),
            TD(_quantity_in), 
            TD(_quantity_out),
            TD(_balanced)))

        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD('CLOSING STOCK AS PER MASTER STOCK',_colspan = '3'),TD(card_view(_itm_code.id, _stk_file.closing_stock))))
        table = TABLE(*[head, body, foot], _class = 'table table-bordered')
        return dict(form = form, i_table = i_table, table = table)
    else:
        return dict(form = form, table = '', i_table = '')


def stock_card_movement_():
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('location_code_id', 'reference Location', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('start_date','date', default= request.now, requires = IS_DATE()),
        Field('end_date','date', default = request.now, requires = IS_DATE()))
    if form.accepts(request):
        # response.flash = 'ok'
        _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()
        _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
        i_row = []
        i_head = THEAD(TR(TD('Item Code'),TD('Description'),TD('Opening Stock'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Retail Price'),TD('Whole Sale Price'),TD('Van Sale Price')))
        i_row.append(TR(TD(_itm_code.item_code),TD(_itm_code.item_description),
        TD(card_view(_itm_code.id, _stk_file.opening_stock)),
        TD(_itm_code.group_line_id.group_line_name),
        TD(_itm_code.brand_line_code_id.brand_line_name),
        TD(_itm_code.uom_value),
        TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),
        TD(locale.format('%.2F',_item_price.wholesale_price or 0, grouping = True)),
        TD(locale.format('%.2F',_item_price.vansale_price or 0, grouping = True))))
        i_body = TBODY(*i_row)
        i_table = TABLE(*[i_head, i_body], _class = 'table')

        head = THEAD(TR(TH('#'),TH('Type'),TH('No'),TH('Date'),TH('Category'),TH('Qty In'),TH('Qty Out'),TH('Balance')))
        row = []
        ctr = 0
        
        _stv = db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id     
        _stv &= db.Stock_Request.stock_source_id == request.vars.location_code_id
        _stv &= db.Stock_Request.srn_status_id == 6
        _stv &= db.Stock_Request.stock_transfer_date_approved >= request.vars.start_date
        _stv &= db.Stock_Request.stock_transfer_date_approved <= request.vars.end_date



        # query = db(_pr).select(db.Purchase_Receipt.ALL, db.Purchase_Receipt_Transaction.ALL, db.Stock_Request_Transaction.ALL, db.Stock_Request.ALL, 
        # left = [db.Stock_Request_Transaction.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id), db.Purchase_Receipt_Transaction.on(db.Purchase_Receipt.id == db.Purchase_Receipt_Transaction.purchase_receipt_no_id)]) 
        _bal = 0
        _bal = _stk_file.opening_stock
        # print 'stv: ', _stv
  
        for n in db(db.Item_Master.id == request.vars.item_code_id).select():
            ctr += 1            
            _pr = db.Purchase_Receipt_Transaction.item_code_id == int(n.id)
            _pr &= db.Purchase_Receipt.posted == True
            _pr &= db.Purchase_Receipt.purchase_receipt_date_approved >= request.vars.start_date
            _pr &= db.Purchase_Receipt.purchase_receipt_date_approved <= request.vars.end_date
            _pr &= db.Purchase_Receipt.location_code_id == request.vars.location_code_id    
            _type = 'None'
            _no = 'None'
            _date = 'None'
            _category = 'None'
            _quantity_in = 'None'
            _quantity_out = 'None'
            _balanced = 'None'

            for i in db(_pr).select(db.Purchase_Receipt.ALL, db.Purchase_Receipt_Transaction.ALL):                                
                _type = i.Purchase_Receipt.purchase_receipt_no_prefix_id.prefix
                _no = i.Purchase_Receipt.purchase_receipt_no
                _date = i.Purchase_Receipt.purchase_receipt_date_approved
                _category = i.Purchase_Receipt_Transaction.category_id.description
                _quantity_in = card_view(i.Purchase_Receipt_Transaction.item_code_id, i.Purchase_Receipt_Transaction.quantity)
                _quantity_out = 0
                _balanced = card_view(i.Purchase_Receipt_Transaction.item_code_id, i.Purchase_Receipt_Transaction.quantity)
                
            for g in db(_stv).select(db.Stock_Request.ALL, db.Stock_Request_Transaction.ALL):                                  
                _type = g.Stock_Request.stock_transfer_no_id.prefix
                _no = g.Stock_Request.stock_transfer_no
                _date = g.Stock_Request.stock_transfer_date_approved
                _category = g.Stock_Request_Transaction.category_id.description
                _quantity_in = card_view(g.Stock_Request_Transaction.item_code_id, g.Stock_Request_Transaction.quantity)
                _quantity_out = 0
                _balanced = card_view(g.Stock_Request_Transaction.item_code_id, g.Stock_Request_Transaction.quantity)
                

            row.append(TR(TD(ctr),
            TD(_type),
            TD(_no),
            TD(_date),                                        
            TD(_category),
            TD(_quantity_in), 
            TD(_quantity_out),
            TD(_balanced)))

        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD('CLOSING STOCK AS PER MASTER STOCK',_colspan = '3'),TD(card_view(_itm_code.id, _stk_file.closing_stock))))
        table = TABLE(*[head, body, foot], _class = 'table table-bordered')
        return dict(form = form, i_table = i_table, table = table)
    else:
        return dict(form = form, table = '', i_table = '')

def price_list_report_print():
    ctr = 0
    _rep = [['#','Item Code','Supplier Ref.','Product','Subproduct','Group Line','Brand Line','Brand Classification','Description','UOM','Unit','Whole Price','Retail Price']]
    for n in db(db.Item_Master.supplier_code_id == request.args(0)).select(db.Item_Master.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.product_code_id | db.Item_Master.subproduct_code_id | db.Item_Master.group_line_id | db.Item_Master.brand_line_code_id | db.Item_Master.brand_cls_code_id ,  left = db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)):
        ctr += 1
        if n.Item_Master.product_code_id == None:
            _product = 'None'
        else:
            _product = n.Item_Master.product_code_id.product_name
        if n.Item_Master.uom_id == None:
            _uom = 'None'
        else:
            _uom = n.Item_Master.uom_id.mnemonic
        _rep.append([ctr,
        Paragraph(n.Item_Master.item_code,style=_courier),
        n.Item_Master.supplier_item_ref,        
        Paragraph(_product,style=_courier),    
        Paragraph(n.Item_Master.subproduct_code_id.subproduct_name,style=_courier),
        n.Item_Master.group_line_id.group_line_name,
        Paragraph(n.Item_Master.brand_line_code_id.brand_line_name,style=_courier),
        Paragraph(n.Item_Master.brand_cls_code_id.brand_cls_name, style = _courier),            
        Paragraph(n.Item_Master.item_description, style = _courier),            
        n.Item_Master.uom_value,
        _uom,
        locale.format('%.2F',n.Item_Prices.wholesale_price or 0, grouping = True),
        locale.format('%.2F',n.Item_Prices.retail_price or 0, grouping = True)])
    _rep_tbl = Table(_rep, colWidths=[20,'*','*','*','*','*','*','*','*',30,30,'*','*'], repeatRows=1)
    # _rep_tbl = Table(_rep, colWidths=(50*mm, 50*mm), rowHeights=(10*mm, 250*mm))
    _rep_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 1)),
        # ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(-1,-1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('ALIGN', (9,1), (12,-1), 'RIGHT'),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
    ]))
    row.append(_rep_tbl)
    a3.pagesize = landscape(A3)
    a3.build(row, onFirstPage=_landscape_header, onLaterPages= _landscape_header)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def price_list_report_option():
    row = []    
    _query = db(db.Item_Master.supplier_code_id == request.vars.supplier_code_id).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Product'),TH('Subproduct'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('Description'),TH('UOM'),TH('Type'),TH('Whole Price'),TH('Retail Price')))
        ctr = 0
        for n in db(db.Item_Master.supplier_code_id == request.vars.supplier_code_id).select(db.Item_Master.ALL, db.Item_Prices.ALL, 
        orderby = db.Item_Master.product_code_id | db.Item_Master.subproduct_code_id | db.Item_Master.group_line_id | db.Item_Master.brand_line_code_id | db.Item_Master.brand_cls_code_id ,  left = db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)):
            ctr += 1
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(n.Item_Master.product_code_id.product_name),                
                TD(n.Item_Master.subproduct_code_id.subproduct_name),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.brand_cls_code_id.brand_cls_name),                                
                TD(n.Item_Master.item_description),
                TD(n.Item_Master.uom_value),
                TD(n.Item_Master.uom_id.mnemonic),
                TD(n.Item_Prices.wholesale_price),
                TD(n.Item_Prices.retail_price)))
        tbody = TBODY(*row)
        table = TABLE(*[thead, tbody], _class = 'table')
        return table
    else:
        return CENTER(DIV(B('INFO! '),'No item record yet.',_class='alert alert-info',_role='alert'))

def price_list_report():
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')))
    if form.process().accepted:
        response.flash = 'SUCCESS'
        redirect(URL('price_list_report_print', args = form.vars.supplier_code_id))
    elif form.errors:
        response.flash = 'ERROR'
    return dict(form = form)

def stock_value_report():
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s',zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master',label='Supplier Code',requires=IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'All Supplier'))),
        Field('location_code_id', 'reference Location', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'All Location'))))
    if form.process().accepted:
        response.flash = 'SUCCESS'        
        # redirect(URL('inventory','get_stock_value_report', args =[form.vars.dept_code_id,form.vars.supplier_code_id, form.vars.location_code_id]))
    elif form.errors:
        response.flash = 'ERROR'        
        print form.errors
    return dict(form = form)

def get_stock_value_view_():
    print 'get_stock_value_view', request.vars.dept_code_id, request.vars.supplier_code_id, request.vars.location_code_id
    if request.vars.supplier_code_id == "" and request.vars.location_code_id == "":
        
        print 'ALL'
        
    else:
        print 'SELECTED'
       
def get_stock_value_view():
    # response.js = "jQuery($('#btnSubmit').attr)"
    row = []
    ctr = _total = 0
    session.dept_code_id = request.vars.dept_code_id
    session.supplier_code_id = request.vars.supplier_code_id
    session.location_code_id = request.vars.location_code_id
    
    if request.vars.supplier_code_id == "" and request.vars.location_code_id == "":
        _query_supplier = db.Item_Master.supplier_code_id > 0
        _query_location = db.Stock_File.location_code_id > 0        
        response.js = 'jQuery($("#btnPrint").removeAttr("disabled"))'
        head = THEAD(TR(TH('#'),TH('Supplier Name'),TH('Total Stock Value')))
        _query = db((db.Item_Master.dept_code_id == request.vars.dept_code_id) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id,left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (int(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            row.append(TR(
                TD(ctr),                
                TD(n.Item_Master.supplier_code_id.supp_name,', ', n.Item_Master.supplier_code_id.supp_code ),
                TD(locale.format('%.2F',_stock_value or 0, grouping = True))))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD('TOTAL:'),TD(locale.format('%.2F',_total or 0, grouping = True))))
        table = TABLE(*[head, body, foot],_class='table')
        return XML(table)
        
    else:
        _query_supplier = db.Item_Master.supplier_code_id == request.vars.supplier_code_id
        _query_location = db.Stock_File.location_code_id == request.vars.location_code_id
        
        _query = db((db.Item_Master.dept_code_id == request.vars.dept_code_id) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id, left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('Description'),TH('UOM'),TH('Type'),TH('Unit Price'),TH('Closing Stock'),TH('Closing Stock Value')))    
        response.js = 'jQuery($("#btnPrint").removeAttr("disabled"))'
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (int(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            if n.Item_Master.uom_id == None:
                _uom_id = 'None'
            else:
                _uom_id = n.Item_Master.uom_id.mnemonic
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.brand_cls_code_id.brand_cls_name),                                
                TD(n.Item_Master.item_description),
                TD(n.Item_Master.uom_value),
                TD(_uom_id),                
                # TD(n.Item_Master.uom_id),                
                TD(n.Item_Prices.average_cost),
                TD(n.Stock_File.closing_stock),
                TD(locale.format('%.2F',_stock_value or 0, grouping = True))))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('TOTAL: '),TD(locale.format('%.2F',_total or 0, grouping = True))))
        table = TABLE(*[head, body, foot],_class='table')
        return XML(table)

    
    response.js = 'jQuery($("#btnPrint").attr("disabled","disabled"))'
        # <div class="alert alert-warning" role="alert">...</div>
        # return XML(DIV('No records found.',_class="alert alert-warning"))
    # redirect(URL('inventory','get_stock_value_report_print', args=request.vars.dept_code_id), client_side=True)


def get_stock_value_report_():
    ctr = 0
    if int(request.vars.supplier_code_id) == 0:        
        _query = db.Item_Master.dept_code_id == request.vars.dept_code_id            
    else:           
        _query = (db.Item_Master.dept_code_id == request.vars.dept_code_id) & (db.Item_Master.supplier_code_id == request.vars.supplier_code_id)
    if request.vars.location_code_id == "":
        _query_stock = db.Item_Master.id == db.Stock_File.item_code_id        
    else:
        _query_stock = db.Stock_File.location_code_id == request.vars.location_code_id
            
    _row = [['#','Item Code','Supplier Ref.','Product','SubProduct','Group Line','Brand Line','Brand Classification','Description','UOM','Type','Whole Price','Retail Price','Amount Cost','Stock Qty','Stock Value']]
    _query = db((_query) & (_query_stock)).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)])
    for n in _query:
        ctr += 1       
        if n.Item_Master.product_code_id == None:
            _product = 'None'
        else:
            _product = n.Item_Master.product_code_id.product_name
        if n.Item_Master.subproduct_code_id == None:
            _subprod = 'None'
        else:
            _subprod = n.Item_Master.subproduct_code_id.subproduct_name
        if n.Item_Master.group_line_id == None:
            _groupln = 'None'
        else:
            _groupln = n.Item_Master.group_line_id.group_line_name
        if n.Item_Master.brand_line_code_id == None:
            _brandln = 'None'
        else:
            _brandln = n.Item_Master.brand_line_code_id.brand_line_name
        if n.Item_Master.brand_cls_code_id == None:
            _brandcl = 'None'
        else:
            _brandcl = n.Item_Master.brand_cls_code_id.brand_cls_name
        if n.Item_Master.uom_id == None:
            _uom = 'None'
        else:
            _uom = n.Item_Master.uom_id.mnemonic            
        _row.append([
            ctr,n.Item_Master.item_code,n.Item_Master.supplier_item_ref,_product,_subprod,_groupln,_brandln,_brandcl,n.Item_Master.item_description,
                n.Item_Master.uom_value,_uom,n.Item_Prices.wholesale_price,n.Item_Prices.retail_price,n.Item_Prices.most_recent_landed_cost,n.Stock_File.closing_stock])
    _row_tbl = Table(_row,colWidths='*')
    _row_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))])) 
    row.append(_row_tbl)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data         

def get_stock_value_print():
    ctr = _total= 0    
    if session.supplier_code_id == "" and session.location_code_id == "":
        _query_supplier = db.Item_Master.supplier_code_id > 0        
        _query_location = db.Stock_File.location_code_id > 0       
        _row = [['#','Supplier Name','Cl. STK Val.']]
        _query = db((db.Item_Master.dept_code_id == int(session.dept_code_id)) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id, left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])  
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (int(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            if n.Item_Master.uom_id == None:
                _uom_id = 'None'
            else:
                _uom_id = n.Item_Master.uom_id.mnemonic
            _row.append([
                ctr,
                str(n.Item_Master.supplier_code_id.supp_name) + ', ' + str(n.Item_Master.supplier_code_id.supp_code),                
                locale.format('%.2F',_stock_value or 0, grouping = True)])
        _row.append(['','TOTAL',locale.format('%.2F',_total or 0, grouping = True)])
        _row_tbl = Table(_row,colWidths=[25,'*',100], repeatRows=1)             
    else:        
        _query_supplier = db.Item_Master.supplier_code_id == int(session.supplier_code_id)        
        _query_location = db.Stock_File.location_code_id == int(session.location_code_id)

        _row = [['#','Item Code','Supplier Ref.','Group Line','Brand Line','Brand Classfication','Description','UOM','Type','Ave. Cost','Cl. STK','Cl. STK Val.']]
        _query = db((db.Item_Master.dept_code_id == int(session.dept_code_id)) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id, left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])  
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (int(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            if n.Item_Master.uom_id == None:
                _uom_id = 'None'
            else:
                _uom_id = n.Item_Master.uom_id.mnemonic
            _row.append([
                ctr,
                n.Item_Master.item_code,
                n.Item_Master.supplier_item_ref,
                n.Item_Master.group_line_id.group_line_name,
                n.Item_Master.brand_line_code_id.brand_line_name,
                n.Item_Master.brand_cls_code_id.brand_cls_name,
                n.Item_Master.item_description,
                n.Item_Master.uom_value,
                _uom_id,            
                n.Item_Prices.average_cost,
                n.Stock_File.closing_stock,
                locale.format('%.2F',_stock_value or 0, grouping = True)])
        _row.append(['','','','','','','','','','','TOTAL',locale.format('%.2F',_total or 0, grouping = True)])
        _row_tbl = Table(_row,colWidths=[25,70,'*',80,'*','*','*',30,30,70,70,70], repeatRows=1)
    _row_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0,0,0,0.2)),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(-1,-1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),        
    ]))
    row.append(_row_tbl)
    a3.pagesize = landscape(A3)
    a3.build(row, onFirstPage=_stock_value_header, onLaterPages= _stock_value_header)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data


def get_stock_value_print_():    
    # print '--- * == * ---'
    row = []
    ctr = 0    
    if int(request.vars.supplier_code_id) == 0:        
        _query = db.Item_Master.dept_code_id == request.vars.dept_code_id    
        _supplier = 'All Supplier'
    else:   
        _supplier = 'Selected Supplier'
        _query = (db.Item_Master.dept_code_id == request.vars.dept_code_id) & (db.Item_Master.supplier_code_id == request.vars.supplier_code_id)

    if request.vars.location_code_id == "":
        _query_stock = db.Item_Master.id == db.Stock_File.item_code_id
        _location = 'All Location'
    else:
        _query_stock = db.Stock_File.location_code_id == request.vars.location_code_id
        _location = 'Selected Location'

    #### create to _query for all supplier and location or by supplier and location ### ----   
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Product'),TH('Subproduct'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('Description'),TH('UOM'),TH('Type'),TH('Whole Price'),TH('Retail Price'),TH('Amount Cost'),TH('Total Stock Qty'),TH('Total Stock Value')))        
    _query = db((_query) & (_query_stock)).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, 
    left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)])
    # print _supplier, _location
    if _query:
        for n in _query:        
            ctr += 1       
            # print ctr, n.Item_Master.item_code, n.Item_Prices.wholesale_price, n.Stock_File.closing_stock
            if n.Item_Master.product_code_id == None:
                _product = 'None'
            else:
                _product = n.Item_Master.product_code_id.product_name
            if n.Item_Master.subproduct_code_id == None:
                _subprod = 'None'
            else:
                _subprod = n.Item_Master.subproduct_code_id.subproduct_name
            if n.Item_Master.group_line_id == None:
                _groupln = 'None'
            else:
                _groupln = n.Item_Master.group_line_id.group_line_name
            if n.Item_Master.brand_line_code_id == None:
                _brandln = 'None'
            else:
                _brandln = n.Item_Master.brand_line_code_id.brand_line_name
            if n.Item_Master.brand_cls_code_id == None:
                _brandcl = 'None'
            else:
                _brandcl = n.Item_Master.brand_cls_code_id.brand_cls_name
            if n.Item_Master.uom_id == None:
                _uom = 'None'
            else:
                _uom = n.Item_Master.uom_id.mnemonic
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(_product),                
                TD(_subprod),
                TD(_groupln),
                TD(_brandln),
                TD(_brandcl), 
                TD(n.Item_Master.item_description),
                TD(n.Item_Master.uom_value),
                TD(_uom),
                TD(n.Item_Prices.wholesale_price),
                TD(n.Item_Prices.retail_price),            
                TD(n.Item_Prices.most_recent_landed_cost), # amount cost
                TD(n.Stock_File.closing_stock),
                TD())) # total stock value
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table',_id='tblSVR')
        return XML(DIV(table))
    else:
        # return 
        return CENTER(DIV(B('INFO! '),'No item record yet.',_class='alert alert-info',_role='alert'))


def reprint():
    _id = db(db.Stock_Request.id == 11).select().first()
    for r in db(db.Stock_Request_Transaction.stock_request_id == 11).select(left = db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)):
        # print 'Item Code::', r.Stock_Request_Transaction.item_code_id,r.Stock_Request.stock_destination_id
        for l in db((db.Stock_File.item_code_id == r.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == r.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
            print '<item code> ', r.Stock_Request_Transaction.item_code_id, '.location code', l.closing_stock
    return locals()


def test():    
    from reportlab.pdfbase import pdfdoc    
    pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:true,bShrinkToFit:true}\);)>>'
    import subprocess, sys, os    
    elements = []
    # Make heading for each column and start data list
    column1Heading = "COLUMN ONE HEADING"
    column2Heading = "COLUMN TWO HEADING"
    # Assemble data for each column using simple loop to append it into data list
    data = [[column1Heading,column2Heading]]
    for i in range(1,5):
        data.append([str(i),str(i)])

    tableThatSplitsOverPages = Table(data, [6 * cm, 6 * cm], repeatRows=1)
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),1,colors.black),('BOX',(0,0),(-1,-1),1,colors.black),('BOX',(0,0),(0,-1),1,colors.black)])
    tblStyle.add('BACKGROUND',(0,0),(1,0),colors.lightblue)
    tblStyle.add('BACKGROUND',(0,2),(1,2),colors.gray)
    tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
    tableThatSplitsOverPages.setStyle(tblStyle)
    elements.append(tableThatSplitsOverPages)
    # doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
    doc.build(elements)
    pdf_data = open(tmpfilename,"rb").read()
    response.headers['Content-Type']='application/pdf'
    os.unlink(tmpfilename)    
    return pdf_data 
    

def pdfprint():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("C:\\Temp\\Test.pdf", pagesize=A4, bottomup=0)    
    c.setFont('Helvetica', 14)
    c.drawString(10, 20, 'Hello World!')
    c.save()
    # /t <filename> <printername> <drivername> <portname> - Print the file the specified printer.
    # AcroRd32.exe /N /T PdfFile PrinterName [ PrinterDriver [ PrinterPort ] ]
    # Generic-PostScript: lpd://128.1.2.199:515/PASSTHRU    
    # os.system('"/usr/bin/acroread" /n/t/s/o/h/p "C:\\Temp\\test.pdf"')       # C:\web2py\applications\MerchERP\private
    os.system('"/usr/bin/acroread" /h/p "C:\\Temp\\Test.pdf"')       # C:\web2py\applications\MerchERP\private
    # os.system('"/usr/bin/acroread" /n/t/p/h /home/larry/Documents/test.pdf "Generic-PostScript[lpd://128.1.2.199:515/PASSTHRU[515]]"' )        
    # os.system('lpr -P Generic-PostScript /home/larry/Documents/test.pdf')
    # C:\web2py\applications\MerchERP\private

def pdfprint3():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("C:\Temp\Test.pdf", pagesize=A4, bottomup=0)    
    c.setFont('Helvetica', 14)
    c.drawString(10, 20, 'Hello World!')
    c.save()
    os.system('"C:\Program Files\Adobe\Reader 11.0\Reader\AcroRd32.exe" /t "C:\Temp\Test.pdf"')       # C:\web2py\applications\MerchERP\private

def pdfprint4():
    import subprocess
    tempfilename = "C:\Temp\Test.pdf"
    acrobatexe = "C:\Program Files\Adobe\Acrobat 11.0\Reader\AcroRd32.exe"
    subprocess.call([acrobatexe, "/t", tempfilename, "EPSON AL-M7000 Advanced"])
    os.unlink(tempfilename)

def pdfprint5():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("C:\\Temp\\Test.pdf", pagesize=A4, bottomup=0)    
    c.setFont('Helvetica', 14)
    c.drawString(10, 20, 'Hello World!')
    c.save()  
    os.system('"C:\\Program Files (x86)\\Google\Chrome\\Application\\chrome.exe" --kiosk --kiosk-printing --disable-print-preview C:\\Temp\\Test.pdf')


def pdfprint2():
    import requests
    from subprocess import Popen, PIPE

    message = 'print this...'

    cmd = '/usr/bin/lpr -P {}'.format(self.printer_name)
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    response = requests.get(html.unescape(message['body']), stream=True)
    for block in response.iter_content(1024):
        proc.stdin.write(block)
    stdout, stderr = proc.communicate()
    exit_code = proc.wait()
    print exit_code    

# Adobe acrobat has (or at least used to have) a parameter "/t", which made it open, print and exit. By using it, you can call acrobat reader and wait for it to exit, and then delete the file.

# Untested code:

# >>> import subprocess
# # You will have to figure out where your Acrobate reader is located, can be found in the registry:
# >>> acrobatexe = "C:\Program Files\Adobe\Acrobat 4.0\Reader\AcroRd32.exe"  
# >>> subprocess.call([acrobatexe, "/t", tempfilename, "My Windows Printer Name"])
# >>> os.unlink(tempfilename)

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
# ---- C A R D Function  -----