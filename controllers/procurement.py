# ------------------------------------------------------------------------------------------
# -------------------------  P R O C U R E M E N T   S Y S T E M  --------------------------
# ------------------------------------------------------------------------------------------
from babel.numbers import format_number, format_decimal, format_percent, format_currency
import string, random, locale
from datetime import date
locale.setlocale(locale.LC_ALL, '')

@auth.requires_login()
def insurance_proposal():
    form = SQLFORM(db.Insurance_Master)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def validate_ins_pro(form):
    form.vars.purchase_request_no_id = request.args(0)

@auth.requires_login()
def insurance_proposal_details():
    # _om = db.Outgoing_Mail(request.args(0)) or redirect(URL('procurement','insurance_proposal_details_new', args = request.args(0)))
    _om = db(db.Outgoing_Mail.purchase_request_no_id == request.args(0)).select().first()
    if not _om:
        redirect(URL('procurement','insurance_proposal_details_new', args = request.args(0)))
    else:
        redirect(URL('procurement','insurance_proposal_details_view', args = request.args(0)))
    _id = db(db.Insurance_Details.id == request.args(0)).select().first()
    form1 = SQLFORM(db.Outgoing_Mail, _om, showid = False)
    if form1.process().accepted:
        response.flash = 'FORM SAVE'
        # redirect(URL('procurement','insurance_proposal_reports', args = request.args(0)))
    elif form1.errors:
        response.flash = 'FORM HAS ERROR'
    
    return dict(form1 = form1, _id = _id)

@auth.requires_login()
def insurance_proposal_details_view():
    _om = db(db.Outgoing_Mail.purchase_request_no_id == request.args(0)).select().first()
    form1 = SQLFORM(db.Outgoing_Mail, _om, showid = False)
    if form1.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form1.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form1 = form1)

@auth.requires_login()
def validate_outgoing_mail(form):
    _ip = db(db.Insurance_Master.id == request.vars.insurance_master_id).select().first()
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.outgoing_mail_no = _ckey
    form.vars.mail_prefix_no_id = _pre.id    
    form.vars.mail_addressee = _ip.insurance_name

@auth.requires_login()
def insurance_proposal_details_new():        
    _po = db(db.Purchase_Order.purchase_request_no_id == request.args(0)).select().first()
    _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()            
    _pur = db(db.Purchase_Request.id == request.args(0)).select().first()
    # _po = db(db.Purchase_Order.id == request.args(0)).select().first()    
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    _subject = 'Insurance Proposal for ' + str(_po.purchase_order_no_prefix_id.prefix) + str(_po.purchase_order_no)        
    form = SQLFORM.factory(
        Field('insurance_master_id','reference Insurance_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Insurance_Master.id, '%(insurance_name)s', zero = 'Choose Insurance')),
        Field('mail_subject','string', length = 50, default = _subject),
        Field('description', 'string', length = 50),
        Field('payment_terms', 'string', length = 50),
        Field('partial_shipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Partial Shipment')),
        Field('transhipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Transhipment')))
    if form.process(onvalidation = validate_outgoing_mail).accepted:        
        response.flash = 'FORM SAVE'
        _pre.update_record(serial_key = _skey) 
        _po.update_record(status_id = 17, insurance_letter_reference = _ckey)     
        _pur.update_record(status_id = 17)
        db.Outgoing_Mail.insert(
            purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            mail_prefix_no_id = form.vars.mail_prefix_no_id,
            outgoing_mail_no = form.vars.outgoing_mail_no,            
            mail_subject = form.vars.mail_subject,
            mail_sender = 'The Management',
            mail_addressee = form.vars.mail_addressee,
            print_process = True)
        db.Insurance_Details.insert(
            purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            subject = form.vars.mail_subject,
            description = form.vars.description,
            payment_terms = form.vars.payment_terms,
            partial_shipment = form.vars.partial_shipment,
            transhipment = form.vars.transhipment)        
        redirect(URL('procurement','insurance_proposal_reports', args = _po.id))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    
    return dict(form = form, _ckey = _ckey,_om = _om)

@auth.requires_login()
def insurance_proposal_details_on_hold():
    _po = db(db.Purchase_Order.id == request.args(0)).select().first()
    _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()            
    _pur = db(db.Purchase_Request.id == request.args(0)).select().first()    
    
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    _subject = 'Insurance Proposal for ' + str(_po.purchase_order_no_prefix_id.prefix) + str(_po.purchase_order_no)        
    form = SQLFORM.factory(
        Field('insurance_master_id','reference Insurance_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Insurance_Master.id, '%(insurance_name)s', zero = 'Choose Insurance')),
        Field('mail_subject','string', length = 50, default = _subject),
        Field('description', 'string', length = 50),
        Field('payment_terms', 'string', length = 50),
        Field('partial_shipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Partial Shipment')),
        Field('transhipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Transhipment')))
    if form.process(onvalidation = validate_outgoing_mail).accepted:        
        response.flash = 'FORM SAVE'
        _pre.update_record(serial_key = _skey) 
        _po.update_record(status_id = 17, insurance_letter_reference = _ckey)     
        _pur.update_record(status_id = 17)
        db.Outgoing_Mail.insert(
            purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            mail_prefix_no_id = form.vars.mail_prefix_no_id,
            outgoing_mail_no = form.vars.outgoing_mail_no,            
            mail_subject = form.vars.mail_subject,
            mail_sender = 'The Management',
            mail_addressee = form.vars.mail_addressee,
            print_process = True)
        db.Insurance_Details.insert(
            purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            subject = form.vars.mail_subject,
            description = form.vars.description,
            payment_terms = form.vars.payment_terms,
            partial_shipment = form.vars.partial_shipment,
            transhipment = form.vars.transhipment)        
        redirect(URL('procurement','insurance_proposal_reports', args = _po.id))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    
    return dict(form = form, _ckey = _ckey)
# -----------------------  ACCOUNT GRID  -----------------------------
@auth.requires_login()
def puchase_receipt_account_grid(): # manoj
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location Source'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    
    for n in db((db.Purchase_Receipt_Warehouse_Consolidated.status_id == 18) & (db.Purchase_Receipt_Warehouse_Consolidated.draft == False)).select(db.Purchase_Receipt_Warehouse_Consolidated.ALL , orderby = ~db.Purchase_Receipt_Warehouse_Consolidated.id):

        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view', args = n.id, extension = False))        
        insu_lnk = A(I(_class='fas fa-car-crash'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)        
        
        _rw = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()
        _ow = db(db.Purchase_Order.id == _rw.purchase_order_no_id).select().first()
        session.dept_code_id = _ow.dept_code_id
        session.supplier_code_id = _ow.supplier_code_id
        session.location_code_id = _ow.location_code_id         
        row.append(TR(
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
            TD(_ow.dept_code_id.dept_name),
            TD(_ow.supplier_code_id.supp_name),
            TD(_ow.location_code_id.location_name),
            TD(_ow.status_id.description),
            TD(_ow.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

def purchase_receipt_account_grid_view():
    _id = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True)).select().first()
    if _id:
        redirect(URL('procurement','purchase_receipt_account_grid_new_item', args = request.args(0)))
    else:
        row = []
        ctr = 0        
        head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),_class='bg-primary'))
        for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
            ctr += 1
            _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()        
            _po = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()
            # print 'Purchase Order', _po.purchase_order_no
            session.dept_code_id = _po.dept_code_id
            session.supplier_code_id = _po.supplier_code_id
            session.location_code_id = _po.location_code_id 
            row.append(TR(TD(ctr),TD(n.purchase_receipt_date_approved),TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),TD(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no_id.purchase_order_no)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id = 'POtbl')     
        return dict(table = table)

@auth.requires_login()
def purchase_receipt_account_grid_view_transaction(): # .load
    form3 = SQLFORM.factory(
        Field('landed_cost','decimal(10,2)', default = 0.0),
        Field('other_charges','decimal(10,2)', default = 0.0),    
        Field('custom_duty_charges','decimal(10,2)', default = 0.0),
        Field('other_discount','decimal(10,2)', default = 0.0),
        Field('exchange_rate','decimal(10,2)', default = 0.0),
        Field('selective_tax','decimal(10,2)', default = 0.0, label = 'Selective Tax'),
        Field('supplier_invoice','string', length = 25))
    if form3.accepts(request, session):
        response.flash = 'RECORD SAVE'
    elif form3.errors:
        response.flash = 'FORM HAS ERROR'
    
    _id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    row = []
    ctr = 0
    _total_amount = _price_cost = _pieces = _total_net_amount = _total_amount_rec_new = _net_amount = 0
    _net_amount_1 = _net_amount_2 = 0
    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Invoice Qty'),TH('Warehouse Receipt Qty'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-success'))        
    for n in db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')          
        btn_lnk = DIV(dele_lnk)
        _pot = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id).select().first()
        _po = db(db.Purchase_Order.id == _pot.purchase_order_no_id).select().first()
        _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
        _pcs = n.Purchase_Receipt_Transaction_Consolidated.quantity - n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.uom
        _pieces = n.Purchase_Receipt_Transaction_Consolidated.quantity * n.Purchase_Receipt_Transaction_Consolidated.uom + _pieces
        _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction_Consolidated.quantity
        _net_amount_1 += _total_amount        
        # print 'total_amount 1: ', _net_amount_1
        _qty = INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= _qty)
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)            
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = _pcs)
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')          
        btn_lnk = DIV(dele_lnk)                
        row.append(TR(            
            TD(ctr),
            TD(n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code, INPUT(_type='numbers', _id='item_code_id', _name='item_code_id', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.item_code_id)),
            TD(n.Item_Master.item_description),
            TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='numbers', _id='uom', _name='uom', _hidden=True, _value=n.Purchase_Receipt_Transaction_Consolidated.uom)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.category_id.mnemonic,INPUT(_type='numbers', _id = 'category_id', _name='category_id', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.category_id)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='numbers', _id = 'purchase_ordered_quantity', _name='purchase_ordered_quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='numbers', _id = '_cquantity', _name='_cquantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.quantity)),
            TD(_qty, _align = 'right', _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(INPUT(_class='form-control', _type='numbers', _id = 'price_cost', _style="text-align:right;", _name='price_cost', _value= locale.format('%.2F',_pot.price_cost or 0, grouping = True)),  _style="width:120px;"),
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_style="text-align:right;"),TD(),TD(btn_lnk)))        
        for x in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id)).select():                        
            if x.quantity != n.Purchase_Receipt_Transaction_Consolidated.quantity:
                ctr += 1                      
                _price_cost = float(x.price_cost) / int(x.uom)
                _total_amount = float(_price_cost) * int(x.quantity)              
                _net_amount_2 += _total_amount                

                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')          
                btn_lnk = DIV(dele_lnk)
                # print 'total amount 2: ', _net_amount_2
                _qty = x.quantity / x.uom                
                _pcs = x.quantity - x.quantity / x.uom * x.uom
                row.append(TR(
                    TD(ctr),
                    TD(x.item_code_id.item_code),
                    TD(n.Item_Master.item_description),
                    TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='numbers', _id = 'uom', _name='uom', _hidden = True, _value= x.uom)),
                    TD(x.category_id.mnemonic),
                    TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom)),
                    TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom)),                                        
                    TD(card(x.quantity, x.uom), INPUT(_type='numbers', _id = 'quantity', _name='quantity', _hidden = True, _value= _qty)),
                    TD(INPUT(_type='numbers', _id = 'pieces', _name='pieces', _hidden = True, _value = _pcs)),
                    TD(locale.format('%.2F',x.price_cost or 0, grouping = True),INPUT(_type='numbers', _id = 'price_cost', _name='price_cost', _hidden = True, _value = x.price_cost),_align = 'right'),
                    TD(locale.format('%.2F',_total_amount or 0, grouping = True), _align = 'right'),
                    TD(str(x.remarks) + '  ' + str('{:,d}'.format(abs(x.difference_quantity)))),TD(btn_lnk),_class='text-danger'))                                    
    
        _total_net_amount = float(_net_amount_1) + float(_net_amount_2)        
        _total_amount = float(_total_net_amount) * int((100 - n.Purchase_Receipt_Transaction_Consolidated.discount_percentage)) / 100    
        _cur = db(db.Currency_Exchange.id == _po.currency_id).select().first()
        _local_amount = float(_total_amount) * float(_cur.exchange_rate_value)
        # Currency_Exchange
        # print 'total net amount: ',     _net_amount_1, _net_amount_2
    body = TBODY(*row)        
    foot  = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(INPUT(_id='btnSubmit', _type='submit', _value='submit',_class='btn btn-success'),TD(INPUT(_type='button', _value='abort', _class='btn btn-danger'),TD()))))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD(_po.currency_id.mnemonic,' ', locale.format('%.2F',_total_net_amount or 0, grouping = True),_align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(locale.format('%.2F', n.Purchase_Receipt_Transaction_Consolidated.discount_percentage or 0, grouping = True), align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(_po.currency_id.mnemonic,' ',locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount (QR)'),TD(locale.format('%.2F',_local_amount or 0, grouping = True), _align = 'right'),TD(),TD()))

    form = FORM(TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl'))
    if form.accepts(request, session):
        response.flash = 'RECORD UPDATED'
        for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
            _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()            
            _id = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()  
            session._po = _id.id # get the purchase order from changing receipt transaction                 
            db.Purchase_Receipt.update_or_insert(
                purchase_receipt_no_id_consolidated = request.args(0),
                purchase_receipt_no_prefix_id = n.purchase_receipt_no_prefix_id,
                purchase_receipt_no = n.purchase_receipt_no,
                purchase_receipt_approved_by = n.purchase_receipt_approved_by,
                purchase_receipt_date_approved = n.purchase_receipt_date_approved,
                dept_code_id = _id.dept_code_id,
                supplier_code_id = _id.supplier_code_id,
                mode_of_shipment = _id.mode_of_shipment,
                location_code_id = _id.location_code_id,
                supplier_reference_order = _id.supplier_reference_order,
                estimated_time_of_arrival = _id.estimated_time_of_arrival,
                total_amount = _id.total_amount,
                total_amount_after_discount = _id.total_amount_after_discount,
                insured = _id.insured,
                foreign_currency_value = _id.foreign_currency_value,
                local_currency_value = _id.local_currency_value,
                exchange_rate = _id.exchange_rate,
                trade_terms_id = _id.trade_terms_id,
                discount_percentage = _id.discount_percentage,
                currency_id = _id.currency_id,
                remarks = _id.remarks,
                status_id = n.status_id)
        _pr = db(db.Purchase_Receipt.purchase_receipt_no == n.purchase_receipt_no).select().first()
        for x in xrange(ctr):          
            _total_pcs = int(request.vars['quantity'][x]) * int(request.vars['uom'][x]) + int(request.vars['pieces'][x])
            _price_per_piece = float(request.vars['price_cost'][x].replace(',','')) / int(request.vars['uom'][x])
            if int(request.vars['_cquantity'][x]) != int(_total_pcs): # updated or insert to purchase receipt transaction                            
                if int(request.vars['_cquantity'][x]) > int(_total_pcs):
                    _category_id = 5
                    _remarks = 'Short by'
                else:
                    _category_id = 2
                    _remarks = 'Excess by'
                db.Purchase_Receipt_Transaction.update_or_insert(
                    purchase_receipt_no_id_consolidated = request.args(0),
                    purchase_receipt_no_id = _pr.id,
                    item_code_id = request.vars['item_code_id'][x],
                    # category_id = request.vars['category_id'][x],                    
                    category_id = _category_id,
                    uom = request.vars['uom'][x],
                    quantity = _total_pcs,
                    price_cost = float(request.vars['price_cost'][x].replace(',','')),
                    difference_quantity = int(_total_pcs) - int(request.vars['_cquantity'][x]),
                    total_amount = _price_per_piece * _total_pcs,
                    remarks = _remarks,
                    partial = True)
            
                _id = db((db.Purchase_Receipt_Transaction.item_code_id == request.vars['item_code_id'][x]) & (db.Purchase_Receipt_Transaction.purchase_receipt_no_id == _pr.id)).select().first()
                _pot = db(db.Purchase_Order.id == session._po).select().first()
                _prt = db((db.Purchase_Order_Transaction.purchase_order_no_id == _pot.id) & (db.Purchase_Order_Transaction.item_code_id == request.vars['item_code_id'][x])).select().last()                            
                _diff = int(request.vars['_cquantity'][x]) - int(_total_pcs)
                _prt.update_record(difference_quantity = _diff, selected = False, consolidated = False, status_id = 17, partial = True)
            db.Purchase_Receipt_Transaction.update_or_insert(
                purchase_receipt_no_id_consolidated = request.args(0),
                purchase_receipt_no_id = _pr.id,
                item_code_id = request.vars['item_code_id'][x],
                category_id = request.vars['category_id'][x],
                uom = request.vars['uom'][x],
                quantity = request.vars['_cquantity'][x],
                # purchase_ordered_quantity = request.vars['_cquantity'][x],
                price_cost = float(request.vars['price_cost'][x].replace(',','')),
                consolidated = True, 
                total_amount = _price_per_piece * int(request.vars['_cquantity'][x]),
                received = True)                
    elif form.errors:
        response.flash = 'FORM HAS ERROR'       

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt).accepted:
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(
            purchase_receipt_no_id = request.args(0),
            item_code_id = form2.vars.item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            uom = form2.vars.uom,
            price_cost = float(request.vars.most_recent_cost.replace(',','')),
            total_amount = form2.vars.total_amount)    
        response.flash = 'RECORD SAVE'
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'        

    _row = []
    _head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Purchase Ordered'),TH('Warehouse Quantity'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Remarks'),_class='bg-danger'))        
    for z in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).select():
        ctr += 1
        _qty = z.quantity * z.uom + z.pieces
        _qty = str(z.quantity) + ' - ' + str(z.pieces) + '/' + str(z.uom)
        _row.append(TR(TD(ctr),TD(z.item_code),TD(z.item_description),TD(z.uom),TD(z.category_id.mnemonic),TD('0 - 0/0'),TD(_qty),TD(I(_class='fas fa-exclamation-triangle'),' NEED TO UPDATE STOCK FILES', _colspan = '3'),TD(),_class='text-danger'))          
    _body = TBODY(*_row)
    _table = TABLE(*[_head, _body], _class='table')
    return dict(form = form, form2 = form2, form3 = form3, _table = _table)    

def purchase_receipt_account_grid_new_item():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Action'),_class='bg-danger'))        
    for n in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True)).select():        
        ctr += 1
        newi_lnk = A(I(_class='fas fa-tasks'), _title='Process Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_new_item_form', args = n.id))
        btn_lnk = DIV(newi_lnk)
        row.append(TR(TD(ctr),TD(n.item_code),TD(n.item_description),TD(n.uom),TD(n.category_id.mnemonic),TD(card(n.total_pieces, n.uom)),TD(btn_lnk),_class='text-danger'))          
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table) 
def validate_accounts_new_item(form):
    print 'form here: ', request.vars.item_code
    _id = db(db.Item_Master.item_code == request.vars.item_code).select(db.Item_Master.item_code).first()
    if _id:
        form.errors.item_code = 'already exist'
    else:
        form.vars.item_code = _id

def purchase_receipt_account_new_item_form():
    _id = db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).select().first()
    _dp = db(db.Department.id == session.dept_code_id).select().first()
    _dv = db(db.Division.id == _dp.div_code_id).select().first()
    # print 'session', session.dept_code_id, session.supplier_code_id,session.location_code_id    
    form = SQLFORM.factory(
        Field('item_description', 'string', length = 50, label = 'Description', default = _id.item_description, requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('item_description_ar', 'string', length = 50, label = 'Arabic Name', requires = [IS_LENGTH(50), IS_UPPER()]),
        Field('supplier_item_ref', 'string', length = 20, requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
        Field('int_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
        Field('loc_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
        Field('purchase_point', 'integer', default = 40),
        Field('ib', 'decimal(10,2)', default = 0),
        Field('uom_value', 'integer', default = int(_id.uom)),    
        Field('uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose UOM Pack Size')),
        Field('supplier_uom_value', 'integer'),
        Field('supplier_uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose UOM Pack Size')),
        Field('weight_value', 'integer'),
        Field('weight_id', 'reference Weight', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Weight.id, '%(mnemonic)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Item_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), # saleable/non-saleable => item_type_id    
        Field('selectivetax','decimal(10,2)', default = 0, label = 'Selective Tax'),    
        Field('vatpercentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),    
        Field('division_id', 'reference Division', ondelete = 'NO ACTION',default = int(_dv.id), requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',default = int(session.dept_code_id), requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', default = int(session.supplier_code_id), requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', ondelete = 'NO ACTION',label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', ondelete = 'NO ACTION',label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Size.id, '%(description)s', zero = 'Choose Size')),    
        Field('gender_code_id','reference Gender', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Gender.id,'%(description)s', zero = 'Choose Gender')),
        Field('fragrance_code_id','reference Fragrance_Type',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(description)s', zero = 'Choose Fragrance Code')),
        Field('color_code_id','reference Color_Code',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = 'Choose Color')),
        Field('collection_code_id','reference Item_Collection', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Collection.id, '%(description)s', zero = 'Choose Collection')),
        Field('made_in_id','reference Made_In', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Made_In.id, '%(description)s', zero = 'Choose Country')),
        Field('item_status_code_id','reference Status',ondelete = 'NO ACTION', default = 1, requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        # db.Item_Master.insert(
        #     item_code = request.vars.item_code
        # )
        # fnd = db(db.Supplier_Master.id == request.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()
        # itm_code = fnd.supp_code[-5:]+ctr
        # print 'request: ', request.vars.item_code, form.vars.item_description,form.vars.item_description_ar,form.vars.supplier_item_ref,
        # form.vars.int_barcode,form.vars.loc_barcode,form.vars.purchase_point,
        # form.vars.ib,form.vars.uom_value,form.vars.uom_id,form.vars.supplier_uom_value,form.vars.supplier_uom_id,form.vars.weight_value,form.vars.weight_id,form.vars.type_id,form.vars.selective_tax,form.vars.vat_percentage,  

        # print 'item code ', request.vars.item_code, request.vars.item_description
        # db.Item_Master.insert(item_code = itm_code,
        # print 'error'
        #     item_description = request.vars.item_description
            # item_description_ar = form.vars.item_description_ar)
            # supplier_item_ref = form.vars.supplier_item_ref,
            # int_barcode = form.vars.int_barcode,
            # loc_barcode = form.vars.loc_barcode,
            # purchase_point = form.vars.purchase_point,

            # ib = form.vars.ib,

            # uom_value = form.vars.uom_value,
            # uom_id = form.vars.uom_id,
            # supplier_uom_value = form.vars.supplier_uom_value,
            # supplier_uom_id = form.vars.supplier_uom_id,
            # weight_value = form.vars.weight_value,
            # weight_id = form.vars.weight_id,
            # type_id = form.vars.type_id,
            # selective_tax = form.vars.selective_tax,
            # vat_percentage = form.vars.vat_percentage)

            # division_id = form.vars.division_id, 
            # dept_code_id = form.vars.dept_code_id,             
            # supplier_code_id = form.vars.supplier_code_id)
            # product_code_id = form.vars.product_code_id,
            # subproduct_code_id = form.vars.subproduct_code_id,
            # group_line_id = form.vars.group_line_id,
            # brand_line_code_id = form.vars.brand_line_code_id,
            # brand_cls_code_id = form.vars.brand_cls_code_id,            
            # section_code_id = form.vars.section_code_id,
            # size_code_id = form.vars.size_code_id,
            # gender_code_id = form.vars.gender_code_id,
            # fragrance_code_id = form.vars.fragrance_code_id,
            # color_code_id = form.vars.color_code_id,
            # collection_code_id = form.vars.collection_code_id,
            # made_in_id = form.vars.made_in_id,
            # item_status_code_id = form.vars.item_status_code_id)
        
        # _item_code = db(db.Item_Master.item_code == str(request.vars.item_code)).select(db.Item_Master.ALL).first()
        # print 'item code > ', _item_code.id
        
        # session._item_code = _item_code.id       
        redirect(URL('procurement','purchase_receipt_account_new_item_prices_form'))
        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)

def purchase_receipt_account_new_item_prices_form():
    form = SQLFORM.factory(
        Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
        Field('most_recent_cost', 'decimal(10,4)', default = 0),
        Field('average_cost', 'decimal(10,4)', default = 0),
        Field('most_recent_landed_cost', 'decimal(10,4)', default =0),
        Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('opening_average_cost', 'decimal(10,4)', default = 0),
        Field('last_issued_date', 'date', default = request.now),
        Field('wholesale_price', 'decimal(10,2)', default = 0),
        Field('retail_price', 'decimal(10,2)',default = 0),
        Field('vansale_price', 'decimal(10,2)',default =0),
        Field('reorder_qty', 'integer', default = 0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def other_charges():    
    _id = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()    
    _id.update_record(landed_cost = request.vars.landed_cost, other_charges = request.vars.other_charges, custom_duty_charges = request.vars.custom_duty_charges, other_discount = request.vars.other_discount)
    # print ':',request.vars.landed_cost,request.vars.other_charges,request.vars.custom_duty_charges,request.vars.other_discount
def validate_purchase_receipt(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' is zero in stock file.'
    else:
        _exist = db((db.Purchase_Receipt_Transaction_Consolidated.item_code_id == _id.id) & (db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0))).select().first()
        if _exist:
            form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        else:    
            _qty = int(request.vars.quantity) * _id.uom_value + int(request.vars.pieces)
            if _qty <= 0:
                form.errors.quantity = 'Quantity should not less than to zero.'
            _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
            _pc = float(_pu) * int(_qty)
            form2.vars.item_code = _id.id
            form2.vars.quantity = _qty
            form2.vars.uom = _id.uom_value
            form2.vars.total_amount = _pc
   

@auth.requires_login()
def purchase_request_archived():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _id.update_record(archives = True, updated_on = request.now, updated_by = auth.user_id)
    response.flahs = 'RECORD CLEARED'


@auth.requires_login()
def puchase_request_transaction_grid_view_accounts_(): # db.Purchase_Request_Transaction_Accounts
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    _id = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select(orderby = db.Purchase_Request_Transaction.id)    
    _query = db(db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == request.args(0)).select().first()
    if not _query:
        for x in _id:
            db.Purchase_Request_Transaction_Ordered.insert(
                purchase_request_no_id = request.args(0),
                item_code_id = x.item_code_id,
                category_id = x.category_id,                
                uom = x.uom,
                price_cost = x.price_cost)            
    row = []
    ctr = grand_total = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Req.Qty.'),TH('Whs.Qty.'),TH('Quantity'),TH('Pieces'),TH('Most Recent Cost'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    _query = db((db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Ordered.delete != True)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Ordered.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction_Ordered.id, 
        left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Ordered.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction_Ordered.item_code_id)])
    for n in _query:
        ctr += 1
        _total_amount = float(float(n.Purchase_Request_Transaction_Ordered.price_cost) /  int(n.Purchase_Request_Transaction_Ordered.uom)) * int(n.Purchase_Request_Transaction_Ordered.total_pieces)
        grand_total += _total_amount
        
        _req = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.item_code_id == n.
        _Ordered.item_code_id)).select().first()
        if not _req:
            _requested = '0 - 0/' + str(n.Purchase_Request_Transaction_Ordered.uom)
        else:
            _requested = card(_req.quantity, _req.uom)

        _rec = db((db.Purchase_Request_Transaction_Received.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Received.item_code_id == n.Purchase_Request_Transaction_Ordered.item_code_id)).select().first()
        if not _rec:
            _received = '0 - 0/' + str(n.Purchase_Request_Transaction_Ordered.uom)
        else:
            _received = card(_rec.total_pieces, _rec.uom)

        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_browse_view_edit',args = n.Purchase_Request_Transaction_Ordered.id, extension = False))
        if _pr.status_id == 18:
            _save_btn = INPUT(_type='submit',_value='save', _disabled = True)
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            _save_btn = INPUT(_type='submit',_value='save')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction_Ordered.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction_Ordered.id)})
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Ordered.item_code_id.item_code, INPUT(_type='text', _id='item_code_id', _name='item_code_id', _hidden = True, _value = n.Purchase_Request_Transaction_Ordered.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction_Ordered.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction_Ordered.uom),            
            TD(_requested),     
            TD(_received),     
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _style='text-align:right;', _value= n.Purchase_Request_Transaction_Ordered.quantity), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',  _style='text-align:right;',_value= n.Purchase_Request_Transaction_Ordered.pieces), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control', _id = 'price_cost', _name='price_cost', _style='text-align:right;', _value= locale.format('%.2F',n.Purchase_Request_Transaction_Ordered.price_cost or 0, grouping = True)), _style='width:150px;'),
            # TD(locale.format('%.2F',n.Purchase_Request_Transaction_Ordered.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),
            TD(locale.currency(_total_amount, grouping = True), _align = 'right', _style="width:120px;"),
            TD(btn_lnk))) 
    body = TBODY(*row)
    # foot = TFOOT(TR(TD(_colspan='8'),TD(INPUT(_type='submit'))))
    
    foot = TFOOT(TR(TD(H4('TOTAL AMOUNT'), _align = 'right', _colspan='10'),TD(H4(locale.currency(grand_total, grouping = True)), _align = 'right'),TD(_save_btn)))
    # table = TABLE(*[head, body, foot], _class='table table-bordered', _id = 'tblTA')
    form = FORM(TABLE(*[head, body, foot], _class='table table-bordered', _id = 'tblTA'))
    if form.accepts(request, session):
        _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _upd = db((db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Ordered.item_code_id == _item_code_id)).select().first()            
            _total_amount = float(request.vars['price_cost'][x]) / int(_upd.uom) * int(_upd.quantity) 
            _total_pieces = int(request.vars['quantity'][x]) * int(_upd.uom) + int(request.vars['pieces'][x])
            _upd.update_record(quantity = request.vars['quantity'][x],pieces = request.vars['pieces'][x],price_cost = request.vars['price_cost'][x], total_amount = _total_amount, total_pieces = _total_pieces)    
        _pr.update_record(total_amount = grand_total)
        response.flash = 'RECORD UPDATED'
        response.js = "$('#tblTA').get(0).reload()"
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_Purchase_Request_Transaction_Ordered).accepted:
        db.Purchase_Request_Transaction_Ordered.insert(
            purchase_request_no_id = request.args(0),
            item_code_id = form2.vars.item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            pieces = form2.vars.pieces,
            total_pieces = form2.vars.total_pieces,
            price_cost = form2.vars.price_cost,
            uom = form2.vars.uom,
            total_amount = form2.vars.total_amount)    
        response.flash = 'RECORD SAVE'
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    return dict(table = form, form2 = form2, _id = _id, _pr = _pr)

@auth.requires_login()
def purchase_receipt_transaction_grid_view_accounts():
    row = []
    ctr = grand_total = 0   
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('On-Hand'),TH('On-Transit'),TH('Quantity'),TH('Pieces'),_class='bg-success'))        
    for n in db((db.Purchase_Request_Transaction_Ordered.selected == True) & (db.Purchase_Request_Transaction_Ordered.consolidated == False)).select(        
        db.Purchase_Request_Transaction_Ordered.item_code_id, 
        db.Item_Master.item_description,
        db.Purchase_Request_Transaction_Ordered.uom, 
        db.Purchase_Request_Transaction_Ordered.category_id, 
        db.Purchase_Request_Transaction_Ordered.quantity,
        db.Purchase_Request_Transaction_Ordered.pieces,        
        groupby = db.Purchase_Request_Transaction_Ordered.item_code_id | 
        db.Item_Master.item_description |
        db.Purchase_Request_Transaction_Ordered.uom |
        db.Purchase_Request_Transaction_Ordered.category_id |
        db.Purchase_Request_Transaction_Ordered.quantity |
        db.Purchase_Request_Transaction_Ordered.pieces,
        left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Ordered.item_code_id)):
        ctr += 1      
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')          
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Ordered.item_code_id.item_code, INPUT(_type='text', _id = 'item_code_id', _name='item_code_id', _hidden = True, _value= n.Purchase_Request_Transaction_Ordered.item_code_id)),
            TD(n.Item_Master.item_description.upper()),            
            TD(n.Purchase_Request_Transaction_Ordered.uom,INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= n.Purchase_Request_Transaction_Ordered.uom)),
            TD(n.Purchase_Request_Transaction_Ordered.category_id.mnemonic),
            TD(stock_on_hand_all_location(n.Purchase_Request_Transaction_Ordered.item_code_id), _align = 'right', _style="width:120px;"),
            TD(stock_in_transit_all_location(n.Purchase_Request_Transaction_Ordered.item_code_id), _align = 'right', _style="width:120px;"),
            TD(card(n.Purchase_Request_Transaction_Ordered.total_pieces, n.Purchase_Request_Transaction_Ordered.uom), _align = 'right', _style="width:120px;"),
            # TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= n.Purchase_Request_Transaction_Ordered.quantity, _align = 'right'), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = n.Purchase_Request_Transaction_Ordered.pieces), _align = 'right', _style="width:120px;")))    
    row.append(TR(TD(),TD(),TD(),TD(),TD(),TD(INPUT(_type='button', _value='abort', _class='btn btn-danger')),TD(INPUT(_type='submit', _value='save',_class='btn btn-success'), _colspan='3')))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table', _id = 'tblPr'))
    if form.accepts(request, session):
        # response.flash = 'RECORD UPDATED'
        # generate purchase receipt
        
        # _id = db(db.Purchase_Request.id == ).select().first()
        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
        # _id.update_record(status_id = 18, purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)                
        db.Purchase_Receipt_Consolidated.insert(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)
        _pr = db(db.Purchase_Receipt_Consolidated.purchase_receipt_no == _skey).select().first()

        _proc = db((db.Purchase_Request_Transaction_Ordered.selected == True) & (db.Purchase_Request_Transaction_Ordered.consolidated == False)).select(db.Purchase_Request_Transaction_Ordered.purchase_request_no_id, groupby = db.Purchase_Request_Transaction_Ordered.purchase_request_no_id)
        for p in _proc:
            # print 'purchase order :', p.purchase_request_no_id
            db.Purchase_Receipt_Ordered_Consolidated.insert(purchase_receipt_consolidated_id = _pr.id , purchase_ordered_no_id = p.purchase_request_no_id)            

        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _total_pieces = int(request.vars['quantity'][x]) * int(request.vars['uom'][x]) + int(request.vars['pieces'][x])            
            _upd = db((db.Purchase_Request_Transaction_Ordered.item_code_id == _item_code_id) & (db.Purchase_Request_Transaction_Ordered.selected == True) & (db.Purchase_Request_Transaction_Ordered.consolidated == False)).select(db.Purchase_Request_Transaction_Ordered.ALL)
            
            for u in _upd:                                                
                _u = db((db.Purchase_Request_Transaction_Ordered.item_code_id == u.item_code_id) & (db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == u.purchase_request_no_id)).select().first()                
                _u.update_record(quantity = request.vars['quantity'][x],pieces = request.vars['pieces'][x], total_pieces = _total_pieces, consolidated = True)            
        response.flash = 'PURCHASE RECEIPT GENERATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'   
    return dict(form = form) 
    
def validate_Purchase_Request_Transaction_Ordered(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    
    _ex = db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction.item_code_id == _id.id)).select().first()    
    _tp = int(request.vars.quantity or 0) * int(_id.uom_value) + int(request.vars.pieces or 0)    
    if _ex:        
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'    
    _pu = float(request.vars.most_recent_cost or 0) / int(_id.uom_value)
    _pc = float(_pu) * int(_tp)
    form2.vars.item_code = _id.id
    form2.vars.price_cost = request.vars.most_recent_cost
    form2.vars.total_amount = _pc
    form2.vars.total_pieces = _tp
    form2.vars.uom = _id.uom_value

# ----------------------------- PURCHASE REQUEST ----------------------
@auth.requires_login()
def purchase_request_form():
    session.currency_id = 5
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = 0
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),        
        Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
        Field('supplier_reference_order','string', length = 25),
        Field('estimated_time_of_arrival', 'date', default = request.now),
        Field('trade_terms_id', 'reference Supplier_Trade_Terms', default = 1, ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  
        Field('remarks', 'string'),
        Field('status_id','reference Stock_Status',default = 19, ondelete = 'NO ACTION', requires = IS_IN_DB(db(db.Stock_Status.id == 19), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:
        ctr = db((db.Transaction_Prefix.prefix_key == 'POR') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)         
        db.Purchase_Request.insert(
            purchase_request_no_prefix_id = ctr.id,
            purchase_request_no = ctr.current_year_serial_key,
            purchase_request_date = request.now,
            dept_code_id = form.vars.dept_code_id,
            supplier_code_id = form.vars.supplier_code_id,
            mode_of_shipment = form.vars.mode_of_shipment,
            location_code_id = form.vars.location_code_id,
            supplier_reference_order = form.vars.supplier_reference_order,
            estimated_time_of_arrival = form.vars.estimated_time_of_arrival,
            trade_terms_id = form.vars.trade_terms_id,
            # total_amount = form.vars.total_amount,
            # total_amount_after_discount = form.vars.total_amount_after_discount,
            discount_percentage = session.discount,
            currency_id = session.currency_id,
            remarks = form.vars.remarks, 
            status_id = form.vars.status_id)
        _id = db(db.Purchase_Request.purchase_request_no == ctr.current_year_serial_key).select().first()
        _foc = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()    
        _query = db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _query:
            _im = db(db.Item_Master.id == n.item_code_id).select().first()
            _ip = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            db.Purchase_Request_Transaction.insert(
                purchase_request_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = n.uom,
                price_cost = n.price_cost,
                total_amount = n.total_amount,
                average_cost = _ip.average_cost,                
                wholesale_price = _ip.wholesale_price,
                retail_price = _ip.retail_price,
                vansale_price = _ip.vansale_price,
                discount_percentage = n.discount_percentage,
                net_price = n.net_price,
                selective_tax = n.selective_tax,
                selective_tax_foc = n.selective_tax_foc,
                vat_percentage = n.vat_percentage)
            _grand_total += n.total_amount or 0
        _discount = session.discount or 0        
        _discount = float(_grand_total) * float(_discount) / 100
        _after_discount = float(_grand_total) - float(_discount)
        _local_amount = float(_after_discount) * float(_foc.exchange_rate_value)        
        _id.update_record(
            total_amount = _grand_total,            
            foreign_currency_value = _after_discount,
            local_currency_value = _local_amount,
            exchange_rate = _foc.exchange_rate_value,
            total_amount_after_discount = _after_discount)
        session.discount = 0
        db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        session.flash = 'SAVE PURCHASE REQUEST NO ' + str(_skey) + '.'
        redirect(URL('procurement','purchase_request'))
    elif form.errors:
        response.flash = 'FORM HAS ERRROS'    
    # session.forget(response)
    return dict(form = form, ticket_no_id = ticket_no_id)

def purchase_request_view():
    
    return dict()
def payment_details():      
    # print 'session', session.supplier_code_id  
    i = 'Empty'
    for x in db(db.Supplier_Payment_Mode_Details.supplier_id == session.supplier_code_id).select():
        i = TABLE(*[
            TR(TD('Trade Terms'),TD(':'),TD(x.trade_terms_id)),
            TR(TD('Payment Mode'),TD(':'),TD(x.payment_mode_id)),
            TR(TD('Payment Terms'),TD(':'),TD(x.payment_terms_id)),
            TR(TD('Currency'),TD(':'),TD(x.currency_id)),
            TR(TD('Forwarder'),TD(':'),TD(x.forwarder_id))], _id = 'details')
    table = str(XML(i, sanitize=False))
    return table

@auth.requires_login()
def validate_purchase_request_transaction(form):
    # print session.pieces, session.category_id
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    if not _id:
        form.errors.item_code ='Item code does not exist or empty.'
    # elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
    #     form.errors.item_code = 'Item code does not exist in stock file.'

    else:
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
    
        _pr = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _ex = db((db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Purchase_Request_Transaction_Temporary.item_code_id == _id.id) & (db.Purchase_Request_Transaction_Temporary.category_id == session.category_id)).select().first()
        _tp = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)
        _pu = _pc = 0

        if not _pr:
            form.errors.item_code = 'Item code does\'nt have price'
        
        if _ex:
            # response.js = "$('#btnadd').attr('disabled','disabled')"
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        else:
            # response.js = "$('#btnadd').removeAttr('disabled')"  
            if int(session.category_id) == 3:
                _pu = 0                
            else:
                # _pu =  float(request.vars.average_cost.replace(',','')) / int(_id.uom_value)                
                _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                    
        if _id.uom_value == 1:            
            form.vars.pieces = 0
        
        if int(form.vars.pieces) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value'

        if _tp == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
        
        # if int(request.vars.pieces or 0) >= int(_id.uom_value):
        #     form.errors.pieces = 'Pieces should not be more than UOM value.'                

        _pc = float(_pu) * int(_tp)
        form.vars.item_code_id = _id.id    
        form.vars.price_cost = float(request.vars.most_recent_cost.replace(',',''))
        form.vars.total_amount = _pc
        form.vars.total_pieces = _tp
        form.vars.uom = _id.uom_value
        form.vars.category_id = session.category_id
            
@auth.requires_login()
def purchase_request_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0))
        # Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_request_transaction).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'        
        db.Purchase_Request_Transaction_Temporary.insert(
            item_code = form.vars.item_code,
            item_code_id = form.vars.item_code_id,
            quantity = form.vars.quantity,
            uom = form.vars.uom,
            pieces = form.vars.pieces,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            category_id = form.vars.category_id,            
            total_amount = form.vars.total_amount,
            ticket_no_id = session.ticket_no_id)
        if db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    ctr = net_amount = local_amount = foreign_amount = 0    
    _foc = db(db.Currency_Exchange.currency_id == int(session.currency_id)).select().first()    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('PCs'),TH('Most Recent Cost'),TH('Total Amount'),TH('Action'),_class='bg-success'))
    _query = db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1
        net_amount += n.Purchase_Request_Transaction_Temporary.total_amount                  
        local_amount = float(net_amount) * float(_foc.exchange_rate_value)
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Purchase_Request_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Purchase_Request_Transaction_Temporary.id),'_data-qt':(n.Purchase_Request_Transaction_Temporary.quantity), '_data-pc':(n.Purchase_Request_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction_Temporary.id)})
        btn_lnk = DIV( dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),            
            TD(n.Item_Master.uom_value),
            TD(n.Purchase_Request_Transaction_Temporary.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction_Temporary.quantity),
            TD(n.Purchase_Request_Transaction_Temporary.pieces),
            TD(locale.format('%.2F',n.Purchase_Request_Transaction_Temporary.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
            TD(locale.format('%.2F',n.Purchase_Request_Transaction_Temporary.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Total Amount (QR)'), _align = 'right', _colspan='2'),TD(INPUT(_class='form-control',_type='text', _name = 'local_amount', _id='local_amount', _disabled = True, _value = locale.format('%.2F',local_amount or 0, grouping = True))),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control',_type='text', _name = 'net_amount', _id='net_amount', _disabled = True , _value = locale.format('%.2F',net_amount or 0, grouping = True))),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount %', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _value = 0), _align = 'right'),TD(P(_id='error'))))
    foot +=  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control', _type='text', _name = 'foreign_amount', _id='foreign_amount', _disabled = True,  _value = locale.format('%.2F',net_amount or 0, grouping = True))),TD()))    
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblPrt')
    return dict(form = form, table = table, net_amount = net_amount, _foc = _foc)

@auth.requires_login()
def procurement_request_form_abort():     
    db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()

@auth.requires_login()
def discount_session():
    session.discount = request.vars.discount
    # print 'discount session', session.discount

@auth.requires_login()
def purchase_request_transaction_temporary_delete():        
    db(db.Purchase_Request_Transaction_Temporary.id == request.args(0)).delete()
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblPrt').get(0).reload()"

@auth.requires_login()
def purchase_request_item_code_description():
    response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    _icode = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == session.dept_code_id) & (db.Item_Master.supplier_code_id == session.supplier_code_id)).select().first()        
    if not _icode:
        # response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belongs to the selected supplier. ", _class='alert alert-warning',_role='alert'))       
    else:           
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()        
        if _sfile:                           
            if _icode.uom_value == 1:                
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                session.pieces = 0
                _on_balanced = _sfile.probational_balance
                _on_transit = _sfile.stock_in_transit
                _on_hand = _sfile.closing_stock                      
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_sfile.probational_balance, _icode.uom_value)
                _on_transit = card(_sfile.stock_in_transit, _icode.uom_value)
                _on_hand = card(_sfile.closing_stock, _icode.uom_value)     
            
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax'),TH('Retail Price'),TH('Unit Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(_icode.selectivetax),
                TD(_iprice.retail_price),
                TD(locale.format('%.4F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit)),_class="bg-info"),_class='table'))
            response.js = "$('#btnadd').removeAttr('disabled')"         
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

@auth.requires_login()
def purchase_request(): # purchase request grid
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    for n in db((db.Purchase_Request.created_by == auth.user.id) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id):
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))        
        if n.status_id ==18:            
            # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')
        elif n.status_id == 11:            
            if n.supplier_code_id == 4:            
                purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _id='generate', _target='_blank', _href = URL('procurement','generate_purchase_order_no', args = n.id, extension = False))            
        elif (n.status_id == 11) or (n.status_id == 17) or (n.status_id == 19) or (n.status_id == 20):
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))        
                # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', 
                # if n.purchase_order_no_prefix_id > 0:
                #     _om = db(db.Outgoing_Mail.purchase_request_no_id == n.id).select().first()
                #     if not _om:
                #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('procurement','insurance_proposal_details', args = n.id, extension = False))            
                #     else: 
                #         if _om.print_process == False:
                #             insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('procurement','insurance_proposal_details', args = n.id, extension = False))            
                #         else:
                #             purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
                #             prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                        
                #             insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
                # else:
                #     insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
            # else:
            #     insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
                # purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
                # prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
            # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        
        if not n.purchase_request_no_prefix_id:
            _pr = 'None'
        else:
            _pr = str(n.purchase_request_no_prefix_id.prefix) + str(n.purchase_request_no)
        
        if not n.purchase_order_no_prefix_id:
            _po = 'None'
        else:
            _po = str(n.purchase_order_no_prefix_id.prefix) + str(n.purchase_order_no)
        
        if not n.purchase_receipt_no_prefix_id:
            _px = 'None'
        else:
            _px = str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)
        row.append(TR(
            TD(n.purchase_request_date),
            TD(_pr),
            # TD(_po),
            # TD(_px),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic,' ', locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

@auth.requires_login()
def purchase_request_transaction_view():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    db.Purchase_Request.discount_percentage.writable = False
    db.Purchase_Request.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Purchase_Request.status_id.default = 19 
    db.Purchase_Request.mode_of_shipment.writable = False
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def puchase_request_transaction_view_details():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    row = body = foot = []
    ctr = grand_total = 0
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty.'),TH('Closing Stock'),TH('Order In Transit'),TH('Unit Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    else:
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty.'),TH('MRS Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
    for n in _query:
        ctr += 1
        grand_total += n.Purchase_Request_Transaction.total_amount
        _foc = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()
        _foc_amount = _id.total_amount_after_discount * _foc.exchange_rate_value
        if auth.user_id != n.Purchase_Request_Transaction.created_by or _id.status_id != 19:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, dele_lnk)
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_view_edit',args = n.Purchase_Request_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction.id)})
            btn_lnk = DIV(edit_lnk, dele_lnk)
        if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Request_Transaction.item_code_id.item_code),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Request_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.mnemonic, _style="width:100px;"),            
                TD(card(n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                TD(stock_on_hand_all_location(n.Purchase_Request_Transaction.item_code_id), _align = 'right', _style="width:120px;"),
                TD(stock_in_transit_all_location(n.Purchase_Request_Transaction.item_code_id), _align = 'right', _style="width:120px;"),    
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot =  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT (QR)'), _align = 'right'), TD(H4(locale.format('%.2F',_foc_amount or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('NET AMOUNT '), _align = 'right'),       TD(H4(_id.currency_id.mnemonic, ' ' ,locale.format('%.2F',grand_total or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT % '), _align = 'right'),       TD(H4(locale.format('%d',_id.discount_percentage or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),      TD(H4(_id.currency_id.mnemonic, ' ' ,locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True), _align = 'right')),TD()))            
        else:
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Request_Transaction.item_code_id.item_code),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Request_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.mnemonic, _style="width:100px;"),            
                TD(card(n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT (QR)'), _align = 'right'),TD(H4(locale.format('%.2F',_foc_amount or 0, grouping = True), _align = 'right')),TD()))            
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('NET AMOUNT '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ',locale.format('%.2F',grand_total or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT % '), _align = 'right'),TD(H4(locale.format('%.2F',_id.discount_percentage or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ',locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True), _align = 'right')),TD()))
            
            
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblPr')
    return dict(table = table)    

def puchase_request_transaction_browse_view_delete():        
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()      
    # print 'delete', _id.id  
    # _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()    
    # _chk_empty = db((db.Purchase_Request_Transaction.purchase_request_no_id == _pr.id) & (db.Purchase_Request_Transaction.delete == False)).count()
    # if _chk_empty == 1:
    #     response.flash = 'RECORD SHOULD NOT EMPTY'
    # else:
    # _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    # _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    # response.flash = 'RECORD DELETED'
    # response.js = "$('#tblPr').get(0).reload()"

def puchase_request_transaction_edit(form):
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    form.vars.quantity = _qty

def puchase_request_transaction_view_edit():
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()
    _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom
    _total = 0    
    form = SQLFORM.factory(
        Field('quantity', 'integer', default = _qty),
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = puchase_request_transaction_edit).accepted:
        _price_per_piece = _id.price_cost / _id.uom
        _total_amount = form.vars.quantity * _price_per_piece
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id, total_amount = _total_amount)
        for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == _pr.id) & (db.Purchase_Request_Transaction.delete == False)).select():
            _total += n.total_amount        
        _total_amount_after_discount = (float(_total) * (int(100) - float(_pr.discount_percentage))) / 100
        _pr.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount)
        session.flash = 'RECORD UPDATED'
        redirect(URL('procurement','purchase_request_transaction_view', args = _pr.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('purchase_request_transaction_view', args = _pr.id))
    return dict(form = form, btn_back = btn_back)   

@auth.requires_login()
def purchase_request_grid():
    row = []
    _query = db(db.Purchase_Request).select(orderby = ~db.Purchase_Request.id) 
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'): # wael approval
        _query = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    elif auth.has_membership(role = 'INVENTORY'):  # john approval
        _query = db((db.Purchase_Request.status_id == 20) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'): # hakim approval
        _query = db((db.Purchase_Request.status_id == 17) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    elif auth.has_membership(role = 'ACCOUNT USERS'): # manoj approval
        _query = db((db.Purchase_Request.status_id == 18) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Requested by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    for n in _query:
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'): # wael approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_sales_view', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        elif auth.has_membership(role = 'INVENTORY'): # john approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_inventory_manager', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)            
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'): # hakim approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_store_keeper', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        elif auth.has_membership(role = 'ACCOUNT USERS'): # manoj approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_accounts', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        else:
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)

        if not n.purchase_request_no_prefix_id:
            _pr = 'None'
        else:
            _pr = str(n.purchase_request_no_prefix_id.prefix) + str(n.purchase_request_no)
        
        if not n.purchase_order_no_prefix_id:
            _po = 'None'
        else:
            _po = str(n.purchase_order_no_prefix_id.prefix) + str(n.purchase_order_no)
        
        if not n.purchase_receipt_no_prefix_id:
            _px = 'None'
        else:
            _px = str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)
        row.append(TR(
            TD(n.purchase_request_date),
            TD(_pr),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ',locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.created_by.first_name.upper()),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)    

@auth.requires_login()
def purchase_order_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    for n in db(db.Purchase_Order.archives == False).select(orderby = ~db.Purchase_Order.id):    
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))        
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        if auth.has_membership(role = 'INVENTORY'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_manager_view', args = n.id, extension = False))        
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='POtbl')    
    return dict(table = table)

def purchase_request_form_writable_false():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    db.Purchase_Request.discount_percentage.writable = False
    db.Purchase_Request.currency_id.writable = False
    db.Purchase_Request.status_id.writable = False
    db.Purchase_Request.mode_of_shipment.writable = False
    
@auth.requires_login()
def purchase_request_sales_view(): # wael form
    purchase_request_form_writable_false()
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process(onvalidation = validate_empty).accepted:
        _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)    
        session.flash = 'PURCHASE REQUEST REJECTED'
        # redirect(URL('inventory','mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'    
    return dict(form = form, _id = _id)

@auth.requires_login() # john forms
def purchase_request_grid_view_inventory_manager():
    purchase_request_form_writable_false()
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process(onvalidation = validate_empty).accepted:
        session.flash = 'PURCHASE REQUEST REJECTED'
        _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)            
        redirect(URL('inventory','inventory_manager'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def purchase_history():
    row = []
    ctr = _grand_total = _on_balanced = 0
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    if not _pr:
        session.flash = 'Some error'
        redirect(URL('default','index'))   

    _sm = db(db.Supplier_Master.id == _pr.supplier_code_id).select().first() 
    if not _sm.purchase_budget:
        session.flash = 'Empty Supplier Budget'
        redirect(URL('default','index'))

    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),TH('Amount'),_class='bg-primary'))
    for n in db(db.Purchase_Receipt.supplier_code_id == _sm.id).select(db.Purchase_Receipt.ALL, orderby = ~db.Purchase_Receipt.id):
        ctr += 1
        _grand_total += n.total_amount_after_discount
        _po = db(db.Purchase_Receipt_Warehouse_Consolidated.purchase_receipt_no == n.purchase_receipt_no).select().first()        
        _pt = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == _po.id).select().first()
        if not _pt:
            _pur_ord = 'None'
        else:
            _pur_ord = str(_pt.purchase_order_no_id.purchase_order_no_prefix_id.prefix) +str(_pt.purchase_order_no_id.purchase_order_no)
        row.append(TR(TD(ctr),TD(n.purchase_receipt_date_approved),TD(str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)),TD(_pur_ord),TD(str(n.currency_id.mnemonic) +' '+ str(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)))))
        # for z in db(db.Purchase_Order.purchase_receipt_no_id == n.id).select():
        #     row.append(TR(TD(),TD(),TD(),TD(z.purchase_order_no_id.purchase_order_no),TD()))
        # row.append(TR(TD(ctr),TD(n.purchase_request_date),TD(n.purchase_order_no_prefix_id.prefix+str(n.purchase_order_no)),TD(locale.format('%.2F',n.total_amount or 0, grouping = True))))
    row.append(TR(TD(),TD(),TD(),TD(B('GRAND TOTAL:')),TD(B(str(n.currency_id.mnemonic) ,' ', locale.format('%.2F',_grand_total or 0, grouping = True))),_class='active'))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')

    trow = []
    tctr = tgrand_total = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Order'),TH('Amount'),_class='bg-warning'))
    for y in db(db.Purchase_Order.status_id == 17).select(db.Purchase_Order.ALL):
        tctr += 1
        tgrand_total += y.total_amount_after_discount
        trow.append(TR(TD(tctr),TD(y.purchase_order_date_approved),TD(str(y.purchase_order_no_prefix_id.prefix), str(y.purchase_order_no)),TD(y.currency_id.mnemonic, ' ',locale.format('%.2F',y.total_amount_after_discount or 0, grouping = True))))
    trow.append(TR(TD(),TD(),TD(B('GRAND TOTAL:')),TD(B(y.currency_id.mnemonic, ' ',locale.format('%.2F',tgrand_total or 0, grouping = True))),_class='active'))
    tbody = TBODY(*trow)
    ttable = TABLE(*[thead, tbody], _class='table')
    _on_balanced = float(_sm.purchase_budget) - int(_grand_total or 0)  
    return dict(_pr = _pr, _sm = _sm, table = table, _grand_total = _grand_total, _on_balanced=_on_balanced, ttable = ttable)

# -------   warehouse session    ----------
def validate_purchase_request_grid_view_store_keeper(form):
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form.vars.status_id = 18

@auth.requires_login()
def purchase_request_grid_view_store_keeper():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    db.Purchase_Request.discount_percentage.writable = False
    db.Purchase_Request.currency_id.writable = False
    db.Purchase_Request.status_id.writable = False
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process(onvalidation = validate_purchase_request_grid_view_store_keeper).accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory','str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def selected_po():
    from collections import Counter
    _po = db(db.Purchase_Order.id == request.args(0)).select().first()    
    for n in db(db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)).select():
        n.update_record(selected = True, updated_by = auth.user_id, updated_on = request.now)        
    session.dept_code_id = _po.dept_code_id
    session.supplier_code_id = _po.supplier_code_id
    session.location_code_id = _po.location_code_id
    
    # _supplier = session.supplier
    # _supplier.append(int(_po.supplier_code_id))    
    
    
    # counter = Counter(_supplier)
    
    # for values in counter.itervalues():
    #     # print 'add', values
    #     if values > 1:
    #         session.flag = 1
    # if not session.flag:        
    #     response.js = "$('#btnCon').Attr('disabled', 'disabled');"        
    # else:
    #     response.js = "$('#btnCon').removeAttr('disabled');"
    # _supplier = session.supplier
    # print _supplier, counter

@auth.requires_login()
def deselected_po():
    # from collections import Counter
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    _query = db(db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)).select()
    for n in _query:
        n.update_record(selected = False, updated_by = auth.user_id, updated_on = request.now)

    # _supplier = session.supplier
    # _supplier.remove(int(_pr.supplier_code_id))    
        
    # counter = Counter(_supplier)
    
    # for values in counter.itervalues():        
    #     # print 'remove', values
    #     if values == 1:
    #         session.flag = 0

    # if not session.flag:        
    #     response.js = "$('#btnCon').removeAttr('disabled');"                              
    # else:
    #     response.js = "$('#btnCon').Attr('disabled', 'disabled');"  
    # _supplier = session.supplier
    # print _supplier

@auth.requires_login()
def consolidate_purchase_received():
    response.js = "$('#tblPr').get(0).reload()"
    _query = db(db.Purchase_Request.supplier_code_id == int(session.supplier_code_id)).select().first()
    # if not _query:
    #     print 'error', _query.supplier_code_id
    # else:
    #     print 'success', _query.supplier_code_id
    return locals()


@auth.requires_login()
def purchase_receipt_warehouse_grid_consolidate():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id 
    row = []
    ctr = grand_total = 0   
    _qty = db.Purchase_Order_Transaction.quantity.sum()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('WQty'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-success'))        
    for n in db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(                
        db.Purchase_Order_Transaction.item_code_id, 
        db.Item_Master.item_description,
        db.Purchase_Order_Transaction.uom, 
        db.Purchase_Order_Transaction.category_id,    
        _qty,
        groupby = db.Purchase_Order_Transaction.item_code_id | 
        db.Item_Master.item_description |
        db.Purchase_Order_Transaction.uom |
        db.Purchase_Order_Transaction.category_id,        
        left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id)):
        ctr += 1              
        _cls = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Order_Transaction.item_code_id).select().first()
        cut_lnk = A(I(_class='fas fa-cut'), _title='Cut Row', _type='button  ', _role='button', _class='btn btn-icon-toggle cut', callback=URL( args = [_cls.item_code_id,_cls.purchase_request_no_id]), **{'_data-id':(_cls.item_code_id), '_data-pr':(_cls.purchase_request_no_id)})
        btn_lnk = DIV(cut_lnk)
        if n.Purchase_Order_Transaction.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)           
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0)            
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Order_Transaction.item_code_id.item_code, INPUT(_type='text', _id = 'item_code_id', _name='item_code_id', _hidden = True, _value= n.Purchase_Order_Transaction.item_code_id)),
            TD(n.Item_Master.item_description.upper(),INPUT(_type='text', _id = 'qty', _name='qty', _hidden = True, _value= n[_qty])),            
            TD(n.Purchase_Order_Transaction.uom,INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= n.Purchase_Order_Transaction.uom)),
            TD(n.Purchase_Order_Transaction.category_id.mnemonic,INPUT(_type='number', _id = 'category_id', _name='category_id', _hidden = True, _value= n.Purchase_Order_Transaction.category_id)),
            TD(card(n[_qty],n.Purchase_Order_Transaction.uom)),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= 0, _align = 'right'), _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(cut_lnk))) 
    session.ctr = ctr  
    row.append(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(INPUT(_type='submit', _value='save & generate',_class='btn btn-success'), _colspan='2')))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table', _id = 'tblPr'))
    if form.accepts(request, session):        
        # GENERATE PURCHASE RECEIPT        
        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key        
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)                   
        db.Purchase_Receipt_Ordered_Consolidated.insert(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now, status_id = 18)        
        _pr = db(db.Purchase_Receipt_Ordered_Consolidated.purchase_receipt_no == int(_skey)).select().first()

        # UPDATE ADDTIONAL ITEMS
        db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id == str(session.ticket_no)).update(purchase_receipt_no_id = _pr.id)
        
        # GENERATE PURCHASE ORDER DETAILS
        _proc = db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(db.Purchase_Order_Transaction.purchase_request_no_id, groupby = db.Purchase_Order_Transaction.purchase_request_no_id)
        for p in _proc:            
            db.Purchase_Order.insert(purchase_order_no_id = int(p.purchase_request_no_id), purchase_receipt_no_id = int(_pr.id))
            for x in db(db.Purchase_Order_Transaction.purchase_request_no_id == int(p.purchase_request_no_id)).select():
                x.update_record(consolidated = True)            
            y = db(db.Purchase_Request.id == p.purchase_request_no_id).select().first()
            y.update_record(status_id = 18)
            
        # GENERATE PURCHASE RECEIPT TRANSACTION CONSOLIDATION        
        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _total_pieces = int(request.vars['quantity'][x]) * int(request.vars['uom'][x]) + int(request.vars['pieces'][x])     
            if int(_total_pieces) == 0:
                _prt = db(db.Purchase_Order_Transaction.item_code_id == _item_code_id).select().first()
                _prt.update_record(consolidated = False, selected = False)    
                _prq = db(db.Purchase_Request.id == _prt.purchase_request_no_id).select().first()
                _prq.update_record(status_id = 17)
            else:                
                db.Purchase_Receipt_Transaction_Consolidated.insert(                    
                    purchase_receipt_no_id = _pr.id,
                    item_code_id = int(request.vars['item_code_id'][x]),
                    category_id = int(request.vars['category_id'][x]),
                    uom = int(request.vars['uom'][x]),
                    quantity = _total_pieces,
                    purchase_ordered_quantity = int(request.vars['qty'][x]))                    

        session.flash = 'PURCHASE RECEIPT GENERATED'  
    
        # redirect(URL('inventory','str_kpr_grid'))      
    elif form.errors:
        response.flash = 'FORM HAS ERROR'     
    db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id != session.ticket_no_id) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.consolidated == True)).delete()
    # print 'session front:', session.ticket_no_id
    return dict(form = form, ticket_no_id= ticket_no_id) 

@auth.requires_login()
def purchase_receipt_warehouse_grid_process():
    _id = db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select().first()
    if not _id:
        redirect(URL('default','index'))
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id 
    row = []
    ctr = grand_total = 0   
    _qty = db.Purchase_Order_Transaction.quantity.sum()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-success'))        
    for n in db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(                
        db.Purchase_Order_Transaction.item_code_id, 
        db.Item_Master.item_description,
        db.Purchase_Order_Transaction.uom, 
        db.Purchase_Order_Transaction.category_id,    
        _qty,
        groupby = db.Purchase_Order_Transaction.item_code_id | 
        db.Item_Master.item_description |
        db.Purchase_Order_Transaction.uom |
        db.Purchase_Order_Transaction.category_id,        
        left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id)):
        ctr += 1              
        _cls = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Order_Transaction.item_code_id).select().first()
        cut_lnk = A(I(_class='fas fa-cut'), _title='Cut Row', _type='button  ', _role='button', _class='btn btn-icon-toggle cut', callback=URL( args = [_cls.item_code_id,_cls.purchase_order_no_id]), **{'_data-id':(_cls.item_code_id), '_data-pr':(_cls.purchase_order_no_id)})
        btn_lnk = DIV(cut_lnk)
        if n.Purchase_Order_Transaction.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)           
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0)            
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Order_Transaction.item_code_id.item_code, INPUT(_type='text', _id = 'item_code_id', _name='item_code_id', _hidden = True, _value= n.Purchase_Order_Transaction.item_code_id)),
            TD(n.Item_Master.item_description.upper(),INPUT(_type='text', _id = 'qty', _name='qty', _hidden = True, _value= n[_qty])),            
            TD(n.Purchase_Order_Transaction.uom,INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= n.Purchase_Order_Transaction.uom)),
            TD(n.Purchase_Order_Transaction.category_id.mnemonic,INPUT(_type='number', _id = 'category_id', _name='category_id', _hidden = True, _value= n.Purchase_Order_Transaction.category_id)),
            # TD(card(n[_qty],n.Purchase_Order_Transaction.uom)),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= 0, _align = 'right'), _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(cut_lnk))) 
    session.ctr = ctr  
    row.append(TR(TD(),TD(DIV(LABEL('Location:'),DIV(SELECT(_name='location_code_id', _class='form-control', *[OPTION(i.location_name, _value=i.id) for i in db().select(db.Location.ALL, orderby = db.Location.id)])),_class='form-group'),_colspan='2'),TD(),TD(),TD(),TD(),TD(INPUT(_type='submit', _value='submit',_class='btn btn-success'))))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table', _id = 'tblPr'))
    if form.accepts(request, session):        
        # GENERATE PURCHASE RECEIPT CONSOLIDATION      
        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key        
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)                   
        db.Purchase_Receipt_Warehouse_Consolidated.insert(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now, status_id = 18, location_code_id = form.vars.location_code_id)        
        _pr = db(db.Purchase_Receipt_Warehouse_Consolidated.purchase_receipt_no == int(_skey)).select().first()

        # UPDATE ADDTIONAL ITEMS
        db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id == str(session.ticket_no)).update(purchase_receipt_no_id = _pr.id)
        
        # GENERATE PURCHASE ORDER DETAILS CONSOLIDATION
        _proc = db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(db.Purchase_Order_Transaction.purchase_order_no_id, groupby = db.Purchase_Order_Transaction.purchase_order_no_id)
        # _proc = db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(db.Purchase_Order_Transaction.ALL)
        for p in _proc:                                    
            db.Purchase_Receipt_Ordered_Warehouse_Consolidated.insert(
                purchase_receipt_no_id = int(_pr.id),
                purchase_order_no_id = int(p.purchase_order_no_id),   

                status_id = 18)
            for x in db(db.Purchase_Order_Transaction.purchase_order_no_id == int(p.purchase_order_no_id)).select():
                x.update_record(consolidated = True)            
            y = db(db.Purchase_Order.id == p.purchase_order_no_id).select().first()
            y.update_record(status_id = 18)
        

        # GENERATE PURCHASE RECEIPT TRANSACTION CONSOLIDATION        
        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _total_pieces = int(request.vars['quantity'][x]) * int(request.vars['uom'][x]) + int(request.vars['pieces'][x])     
            if int(_total_pieces) == 0:
                _prt = db(db.Purchase_Order_Transaction.item_code_id == _item_code_id).select().first()
                _prt.update_record(consolidated = False, selected = False)    
                _prq = db(db.Purchase_Request.id == _prt.purchase_request_no_id).select().first()
                _prq.update_record(status_id = 17)
            else:                
                _prt = db(db.Purchase_Order_Transaction.item_code_id == _item_code_id).select().first()
                db.Purchase_Receipt_Transaction_Consolidated.insert(                    
                    purchase_receipt_no_id = _pr.id,
                    item_code_id = int(request.vars['item_code_id'][x]),
                    category_id = int(request.vars['category_id'][x]),
                    uom = int(request.vars['uom'][x]),
                    quantity = _total_pieces,
                    price_cost = _prt.price_cost,
                    purchase_ordered_quantity = int(request.vars['qty'][x]),
                    total_amount = _prt.total_amount)

        session.flash = 'PURCHASE RECEIPT GENERATED'  
    
        redirect(URL('inventory','str_kpr_grid'))      
    elif form.errors:
        response.flash = 'FORM HAS ERROR'     
    db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id != session.ticket_no) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.consolidated == True)).delete()    
    return dict(form = form, ticket_no_id= ticket_no_id)     


@auth.requires_login()
def cut_purchase_order_transaction():    
    db((db.Purchase_Order_Transaction.item_code_id == request.args(0)) & (db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).update(selected = False)    
    return locals()

def validate_purchase_receipt_add_new(form):
    _not_exist = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _not_exist:
        _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
        if request.vars.item_description == '':
            form.errors.item_description = 'Item description should not empty.'                
        if _qty <= 0:
            form.errors.quantity = 'UOM and Quantity should not equal to zero'    
        form.vars.new_item = True    
        form.vars.total_pieces = _qty
    else:   
        _exist = db((db.Purchase_Order_Transaction.item_code_id == _not_exist.id) & (db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select().first()      
        _qty = int(request.vars.quantity) * int(_not_exist.uom_value) + int(request.vars.pieces)
        if _exist:
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        if _qty <= 0:
            form.errors.quantity = 'UOM and Quantity should not equal to zero'        
        form.vars.item_code_id = _not_exist.id
        form.vars.item_description = _not_exist.item_description
        form.vars.uom = _not_exist.uom_value
        form.vars.total_pieces = _qty
        form.vars.new_item = False
    

def purchase_receipt_warehouse_grid_consolidate_add_new():
    form = SQLFORM.factory(
        Field('item_code','string', length = 25),
        Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('uom','integer', default = 0),   
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_receipt_add_new).accepted: #onvalidation = validate_purchase_receipt_add_new
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(            
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            category_id = form.vars.category_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            uom = form.vars.uom,
            total_pieces = form.vars.total_pieces,
            item_description = form.vars.item_description,
            ticket_no_id = session.ticket_no_id, 
            new_item = form.vars.new_item           
        )    
        response.flash = 'RECORD SAVE'
        session.ticket_no = session.ticket_no_id
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-warning'))
    for n in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id == session.ticket_no_id).select(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ALL, orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
        session.ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle del', callback=URL(args = n.id, extension = False), **{'_data-2id':(n.id)})        
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(session.ctr),
            TD(n.item_code),
            TD(n.item_description),
            TD(n.uom),
            TD(n.category_id.mnemonic),            
            TD(n.quantity),
            TD(n.pieces),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return dict(form = form, table = table)     

def consolidated_remove():
    _id = db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).delete()

def consolidated_remove_new_item():
    _id = db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).select().first()
    _id.update_record(delete = True)

def warehouse_new_item():
    _icode = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if _icode:
        response.js = "$('#no_table_item_description').attr('disabled','disabled'), $('#no_table_uom').attr('disabled','disabled')"
        return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'))),
        TBODY(TR(
            TD(_icode.item_code),
            TD(_icode.item_description.upper()),
            TD(_icode.group_line_id.group_line_name),
            TD(_icode.brand_line_code_id.brand_line_name),
            TD(_icode.uom_value)),_class="bg-info"),_class='table'))
    else:
        response.js = "$('#no_table_item_description').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled')"
        return CENTER(DIV('Item Code ', B(str(request.vars.item_code)), ' is new item.'), _class='alert alert-danger',_role='alert')

def restart():
    db(db.Purchase_Order_Transaction).update(consolidated = False)
    return locals()        

# -----------------------------------------------------------------------
# ----------------------------- PURCHASE ORDER TOP ----------------------
# -----------------------------------------------------------------------
@auth.requires_login()
def purchase_order(): # purchase_order_table
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    for n in db((db.Purchase_Order.created_by == auth.user.id) & (db.Purchase_Order.archives == False)).select(orderby = ~db.Purchase_Order.id):
    # for n in db().select(db.Purchase_Order.ALL):
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_view', args = n.id, extension = False))        
        if n.supplier_code_id == 4:
            _om = db(db.Outgoing_Mail.purchase_order_no_id == n.id).select().first()
            if not _om:
                insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','insurance_proposal_details_on_hold', args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

@auth.requires_login()
def purchase_order_transaction_view():
    db.Purchase_Order.dept_code_id.writable = False
    db.Purchase_Order.supplier_code_id.writable = False
    db.Purchase_Order.location_code_id.writable = False
    db.Purchase_Order.supplier_reference_order.writable = False
    db.Purchase_Order.estimated_time_of_arrival.writable = False
    db.Purchase_Order.total_amount.writable = False
    db.Purchase_Order.total_amount_after_discount.writable = False
    db.Purchase_Order.discount_percentage.writable = False
    db.Purchase_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Purchase_Order.status_id.default = 19 
    db.Purchase_Order.mode_of_shipment.writable = False
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)        

@auth.requires_login()
def purchase_order_transaction_manager_view():
    db.Purchase_Order.dept_code_id.writable = False
    db.Purchase_Order.supplier_code_id.writable = False
    db.Purchase_Order.location_code_id.writable = False
    db.Purchase_Order.supplier_reference_order.writable = False
    db.Purchase_Order.estimated_time_of_arrival.writable = False
    db.Purchase_Order.total_amount.writable = False
    db.Purchase_Order.total_amount_after_discount.writable = False
    db.Purchase_Order.discount_percentage.writable = False
    db.Purchase_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Purchase_Order.status_id.default = 19 
    db.Purchase_Order.mode_of_shipment.writable = False
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)        

@auth.requires_login()
def puchase_order_transaction_view_details():
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    row = body = foot = []
    ctr = grand_total = 0
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Closing Stock'),TH('Order In Transit'),TH('MRS Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    else:
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Action'),_class='bg-success'))    
    _query = db((db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)) & (db.Purchase_Order_Transaction.delete != True)).select(db.Item_Master.ALL, db.Purchase_Order_Transaction.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1
        grand_total += n.Purchase_Order_Transaction.total_amount
        _foc = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()
        _foc_amount = _id.total_amount_after_discount * _foc.exchange_rate_value        
        if auth.user_id != n.Purchase_Order_Transaction.created_by or _id.status_id != 19:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, dele_lnk)
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_view_edit',args = n.Purchase_Order_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Order_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Order_Transaction.id)})
            btn_lnk = DIV(edit_lnk, dele_lnk)
        if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Order_Transaction.item_code_id.item_code),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Order_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Order_Transaction.category_id.mnemonic, _style="width:100px;"),            
                TD(card(n.Purchase_Order_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                TD(stock_on_hand_all_location(n.Purchase_Order_Transaction.item_code_id), _align = 'right', _style="width:120px;"),
                TD(stock_in_transit_all_location(n.Purchase_Order_Transaction.item_code_id), _align = 'right', _style="width:120px;"),    
                TD(locale.format('%.2F',n.Purchase_Order_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
                TD(locale.format('%.2F',n.Purchase_Order_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2F',grand_total or 0, grouping = True)), _align = 'right'),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT %'), _align = 'right'),TD(H4('0', _align = 'right')),TD(P(_id='error'))))
        else:
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Order_Transaction.item_code_id.item_code),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Order_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Order_Transaction.category_id.mnemonic, _style="width:100px;"),            
                TD(card(n.Purchase_Order_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                # TD(locale.format('%.2F',n.Purchase_Order_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
                # TD(locale.format('%.2F',n.Purchase_Order_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            # foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT (QR)'), _align = 'right'),TD(H4(locale.format('%.2F',_foc_amount or 0, grouping = True)), _align = 'right'),TD()))            
            # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('NET AMOUNT '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ', locale.format('%.2F',grand_total or 0, grouping = True), _align = 'right')),TD()))
            # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT % '), _align = 'right'),TD(H4(locale.format('%d',_id.discount_percentage or 0, grouping = True), _align = 'right')),TD()))
            # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ',locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body], _class='table', _id = 'tblPr')
    return dict(table = table)   

def u_list():
    # Python code to demonstrate 
    # to test all elements in list are unique 
    # using Counter.itervalues() 
    from collections import Counter 

    # initializing list 
    test_list = [1, 1, 1, 1, 1] 

    # printing original list 
    print ("The original list is : " + str(test_list)) 

    flag = 0

    # using Counter.itervalues() 
    # to check all unique list elements 
    counter = Counter(test_list) 
    for values in counter.itervalues(): 
            if values > 1: 
                flag = 1


    # printing result 
    if(not flag) : 
        print ("List contains all unique elements") 
    else : 
        print ("List contains does not contains all unique elements") 

    return locals()
# ----------------------------- HAKIM'S WORLD ----------------------
@auth.requires_login()
def purchase_receipt_warehouse_grid(): # hakim's form
    session.flag = 0
    session.supplier = []
    row = []
    head = THEAD(TR(TH(),TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    for n in db((db.Purchase_Order.status_id == 17) & (db.Purchase_Order.archives == False)).select(orderby = ~db.Purchase_Order.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))        
        insu_lnk = A(I(_class='fas fa-car-crash'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)                
        row.append(TR(
            TD(INPUT(_type="checkbox", _id='selected', _name='selected', _class="checkbox", _value = n.id)),
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),        
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic,' ',locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

def purchase_receipt_warehouse_grid_view():
    db.Purchase_Order.dept_code_id.writable = False
    db.Purchase_Order.supplier_code_id.writable = False
    db.Purchase_Order.mode_of_shipment.writable = False
    db.Purchase_Order.location_code_id.writable = False
    db.Purchase_Order.supplier_reference_order.writable = False
    db.Purchase_Order.estimated_time_of_arrival.writable = False
    db.Purchase_Order.total_amount.writable = False
    db.Purchase_Order.total_amount_after_discount.writable = False
    db.Purchase_Order.insured.writable = False
    db.Purchase_Order.insurance_letter_reference.writable = False
    db.Purchase_Order.foreign_currency_value.writable = False
    db.Purchase_Order.local_currency_value.writable = False
    db.Purchase_Order.exchange_rate.writable = False
    db.Purchase_Order.trade_terms_id.writable = False
    db.Purchase_Order.discount_percentage.writable = False
    db.Purchase_Order.currency_id.writable = False
    # db.Purchase_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    # db.Purchase_Order.status_id.default = 19 
    db.Purchase_Order.status_id.writable = False
    
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Order, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory','str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def purchase_receipt_warehouse_grid_view_():
    POrow = []
    POctr = 0
    _id = db(db.Purchase_Receipt_Ordered_Consolidated.id == request.args(0)).select().first()
    
    POhead = THEAD(TR(TH('#'),TH('Purchase Receipt'),TH('Purchase Order'),_class='bg-primary'))
    for o in db(db.Purchase_Order.purchase_receipt_no_id == request.args(0)).select():
        POctr += 1
        POrow.append(TR(TD(POctr),TD(o.purchase_receipt_no_id.purchase_receipt_no_prefix_id.prefix,o.purchase_receipt_no_id.purchase_receipt_no),TD(o.purchase_order_no_id.purchase_order_no_prefix_id.prefix,o.purchase_order_no_id.purchase_order_no)))
    PObody = TBODY(*POrow)
    PO_table = TABLE(*[POhead, PObody], _class='table', _id = 'POtbl')

    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('On-Hand'),TH('On-Transit'),TH('Quantity'),TH('Action'),_class='bg-success'))        
    for n in db(db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Order_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id)):
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')          
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description),
            TD(n.Purchase_Order_Transaction.uom),
            TD(n.Purchase_Order_Transaction.category_id.mnemonic),
            TD(stock_on_hand_all_location(n.Purchase_Order_Transaction.item_code_id)),
            TD(stock_in_transit_all_location(n.Purchase_Order_Transaction.item_code_id)),
            TD(card(n.Purchase_Order_Transaction.quantity,n.Purchase_Order_Transaction.uom)),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table', _id = 'POTtbl')
    return dict(_id = _id,  PO_table = PO_table, table = table)

def purchase_receipt_warehouse_grid_consolidated():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Status'),TH('Action'),_class='bg-success'))
    for n in db().select(db.Purchase_Receipt_Warehouse_Consolidated.ALL, orderby = ~db.Purchase_Receipt_Warehouse_Consolidated.id):
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href = URL('procurement','warehouse_receipt_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_consolidated_view', args = n.id, extension = False))        
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,'',n.purchase_receipt_no),
            TD(n.status_id.description),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id='PCtbl')
    return dict(table = table)

def purchase_receipt_warehouse_grid_consolidated_view():
    row =  []
    trow = []
    ctr = _after_discount = _total_amount = grand_total = discount_percentage = _foc_amount = _loc_amount = _total_row_amount =  0
    _wc = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.id == request.args(0)).select().first()
    _id = db(db.Purchase_Order.id == _wc.purchase_order_no_id).select().first()    
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Purchase Order No.'),TH('Purchase Request No.'),_class='bg-success'))
    for n in db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select():        
        _po = db(db.Purchase_Order.id == n.purchase_order_no_id).select().first()
        _foc = db(db.Currency_Exchange.currency_id == _po.currency_id).select().first()
        _after_discount += _po.total_amount_after_discount
        _total_amount += _po.total_amount
        _loc_amount += _po.total_amount_after_discount * _foc.exchange_rate_value
        _pr = db(n.purchase_order_no_id == db.Purchase_Order.id).select().first()
        row.append(TR(
            TD(n.purchase_receipt_no_id.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_id.purchase_receipt_no_prefix_id.prefix,'',n.purchase_receipt_no_id.purchase_receipt_no),
            TD(n.purchase_order_no_id.purchase_order_no_prefix_id.prefix,'',n.purchase_order_no_id.purchase_order_no),
            TD(_pr.purchase_request_no_id.purchase_request_no_prefix_id.prefix,_pr.purchase_request_no_id.purchase_request_no)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id='PCtbl')
    
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-success'))    
    for t in db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):
        ctr += 1
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(edit_lnk, dele_lnk)  
        _pcs = t.Purchase_Receipt_Transaction_Consolidated.quantity - t.Purchase_Receipt_Transaction_Consolidated.quantity / t.Purchase_Receipt_Transaction_Consolidated.uom * t.Purchase_Receipt_Transaction_Consolidated.uom      
        if t.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)           
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = _pcs)        
        
        _qty = t.Purchase_Receipt_Transaction_Consolidated.quantity / t.Purchase_Receipt_Transaction_Consolidated.uom
        trow.append(TR(
            TD(ctr),
            TD(t.Item_Master.item_code, INPUT(_type='text', _name='item_code', _value=t.Item_Master.item_code, _hidden=True)),
            TD(t.Item_Master.item_description),
            TD(t.Purchase_Receipt_Transaction_Consolidated.uom),
            TD(t.Purchase_Receipt_Transaction_Consolidated.category_id.mnemonic),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= _qty, _align = 'right'), _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(btn_lnk)))
    for m in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).select():
        ctr += 1
        if m.uom == 1:
            _mpcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)           
        else:
            _mpcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = m.pieces)        
        _mqty = m.total_pieces / m.uom
        if m.new_item == True:
            trow.append(TR(
                TD(ctr),
                TD(m.item_code, INPUT(_type='text', _name='item_code', _value=m.item_code, _hidden=True)),
                TD(m.item_description),
                TD(m.uom),
                TD(m.category_id.mnemonic),
                TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= m.quantity, _align = 'right'), _style="width:120px;"),
                TD(_mpcs, _align = 'right', _style="width:120px;"),
                TD(btn_lnk),_class='text-danger danger'))     
        else:
            trow.append(TR(
                TD(ctr),
                TD(m.item_code, INPUT(_type='text', _name='item_code', _value=m.item_code, _hidden=True)),
                TD(m.item_description),
                TD(m.uom),
                TD(m.category_id.mnemonic),
                TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= m.quantity, _align = 'right'), _style="width:120px;"),
                TD(_mpcs, _align = 'right', _style="width:120px;"),
                TD(btn_lnk),_class='text-danger'))     

    trow.append(TR(TD(),TD(),TD(),TD(INPUT(_id='btnDraft', _type='button', _value='save as draft',_class='btn btn-primary')),TD(INPUT(_id='btnRefresh', _type='button', _value='refresh',_class='btn btn-primary')),TD(INPUT(_id='btnSubmit', _type='submit', _value='submit',_class='btn btn-success')),TD(INPUT(_type='button', _value='abort', _class='btn btn-danger')),TD(INPUT(_type='button', _value='print', _class='btn btn-warning'))))                   
    tbody = TBODY(*trow)
    form = FORM(TABLE(*[thead, tbody], _class= 'table', _id='PTtbl'))
    if form.accepts(request, session):
        _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
        _prwc.update_record(draft = False)
        # print _prwc.id
        for x in xrange(ctr):
            _i = db(db.Item_Master.item_code == request.vars['item_code'][x]).select().first()            
            try:                
                _prc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == _i.id)).select().first()
                _npc = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code == request.vars['item_code'][x])).select().first()
                if _prc:
                    _qty = int(request.vars['quantity'][x]) * int(_prc.uom) + int(request.vars['pieces'][x])
                    _prc.update_record(quantity = _qty)
                else:                                
                    _total_pieces = int(request.vars['quantity'][x]) * int(_npc.uom) + int(request.vars['pieces'][x])
                    _npc.update_record(quantity = int(request.vars['quantity'][x]),pieces = int(request.vars['pieces'][x]), total_pieces = _total_pieces)
            except:
                _npc = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code == request.vars['item_code'][x])).select().first()
                _total_pieces = int(request.vars['quantity'][x]) * int(_npc.uom) + int(request.vars['pieces'][x])
                _npc.update_record(quantity = int(request.vars['quantity'][x]),pieces = int(request.vars['pieces'][x]), total_pieces = _total_pieces)
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory','str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(table = table, form = form)


def validate_purchase_receipt_add_new_item(form2):
    _not_exist = db(db.Item_Master.item_code == request.vars.new_item_code).select().first()
    if not _not_exist:        
        _query = db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code == str(request.vars.new_item_code)
        _query &= db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)
        _exist = db(_query).select().first()
        if _exist:
            # print 'exist new item in table',request.vars.new_item_code            
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
        else:
            _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
            if request.vars.item_description == '':
                form2.errors.item_description = 'Item description should not empty.'                
            if _qty <= 0:
                form2.errors.quantity = 'UOM and Quantity should not equal to zero'    
            form2.vars.new_item = True    
            form2.vars.total_pieces = _qty
    else:           
        # print 'old item', _not_exist.id
        _query = db.Purchase_Order_Transaction.item_code_id == _not_exist.id
        _query &= db.Purchase_Order_Transaction.selected == True
        _query &= db.Purchase_Order_Transaction.consolidated == False
        _query &= db.Purchase_Order_Transaction.delete == False
        _exist = db((_query) | (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code == str(request.vars.new_item_code))).select().first()      
        _qty = int(request.vars.quantity) * int(_not_exist.uom_value) + int(request.vars.pieces)
        if _exist:
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
        if _qty <= 0:
            form2.errors.quantity = 'UOM and Quantity should not equal to zero'        
        form2.vars.item_code_id = _not_exist.id
        form2.vars.item_description = _not_exist.item_description
        form2.vars.uom = _not_exist.uom_value
        form2.vars.total_pieces = _qty
        form2.vars.new_item = False

def purchase_receipt_warehouse_grid_consolidate_add_new_item():
    form2 = SQLFORM.factory(
        Field('new_item_code','string', length = 25),
        Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('uom','integer', default = 0),   
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt_add_new_item).accepted: #onvalidation = validate_purchase_receipt_add_new
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(            
            purchase_receipt_no_id = request.args(0),
            item_code_id = form2.vars.item_code_id,
            item_code = form2.vars.new_item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            pieces = form2.vars.pieces,
            uom = form2.vars.uom,
            total_pieces = form2.vars.total_pieces,
            item_description = form2.vars.item_description,
            # ticket_no_id = session.ticket_no_id, 
            new_item = form2.vars.new_item           
        )    
        response.flash = 'RECORD SAVE'
        session.ticket_no = session.ticket_no_id
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-warning'))
    for n in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).select(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ALL, orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle del', callback=URL(args = n.id, extension = False), **{'_data-2id':(n.id)})        
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(n.item_description),
            TD(n.uom),
            TD(n.category_id.mnemonic),            
            TD(n.quantity),
            TD(n.pieces),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table', _id = 'PRtbl')
    return dict(form2 = form2, table = table)     

def warehouse_add_new_item():
    _icode = db(db.Item_Master.item_code == request.vars.new_item_code).select().first()
    if _icode:
        response.js = "$('#no_table_item_description').attr('disabled','disabled'), $('#no_table_uom').attr('disabled','disabled')"
        return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'))),
        TBODY(TR(
            TD(_icode.item_code),
            TD(_icode.item_description.upper()),
            TD(_icode.group_line_id.group_line_name),
            TD(_icode.brand_line_code_id.brand_line_name),
            TD(_icode.uom_value)),_class="bg-info"),_class='table'))
    else:
        response.js = "$('#no_table_item_description').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled')"
        return CENTER(DIV('Item Code ', B(str(request.vars.new_item_code)), ' is new item.'), _class='alert alert-danger',_role='alert')

def save_as_draft_record():
    return locals()

@auth.requires_login()
def purchase_request_grid_view_accounts():
    _id = db(db.Purchase_Receipt_Consolidated.id == request.args(0)).select().first()       
    _id = db(db.Purchase_Receipt_Ordered_Consolidated.purchase_receipt_consolidated_id == _id.id).select().first()        
    _id = db(db.Purchase_Request.id == _id.purchase_ordered_no_id).select().first()
 
    # session.dept_code_id = _id.dept_code_id
    # session.supplier_code_id = _id.supplier_code_id
    # session.location_code_id = _id.location_code_id
    form = SQLFORM(db.Purchase_Receipt_Consolidated, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def purchase_request_approved():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _id.update_record(status_id = 20, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now, remarks = request.vars.remarks)        
        session.flash = 'PURCHASE REQUEST APPROVED'        
    elif auth.has_membership(role = 'INVENTORY'):
        _id.update_record(status_id = 11, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now, remarks = request.vars.remarks)
        session.flash = 'PURCHASE REQUEST APPROVED'
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)   
        _id.update_record(status_id = 17, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now, remarks = request.vars.remarks)
        session.flash = 'PURCHASE ORDER APPROVED'
    elif auth.has_membership(role = 'ACCOUNT USERS'):
        _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
        _id.update_record(status_id = 18, purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now, remarks = request.vars.remarks)
        session.flash = 'PURCHASE RECEIPT APPROVED'
    response.js = "$('#PRtbl').get(0).reload()"
    #ajax('{{=URL('generate_item_code_recent_cost')}}', ['item_code'], '_most_recent_cost'); 

@auth.requires_login()
def purchase_request_rejected():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY') | auth.has_membership(role = 'INVENTORY STORE KEEPER') | auth.has_membership(role = 'ACCOUNT USERS'):
        _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now, remarks=request.vars.remarks)    
        session.flash = 'PURCHASE REQUEST REJECTED'
    response.js = "$('#PRtbl').get(0).reload()"

@auth.requires_login()    
def generate_purchase_order_no():    
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
    _skey = _tp.current_year_serial_key
    _skey += 1
    _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)   
    _id.update_record(status_id = 17, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now)    
    
    for n in db(db.Purchase_Request.id == request.args(0)).select():
        db.Purchase_Order.insert(
            purchase_request_no_id = request.args(0),
            purchase_order_no_prefix_id = _tp.id,
            purchase_order_no = _skey,
            purchase_order_approved_by = auth.user_id,
            purchase_order_date_approved = request.now,
            dept_code_id = n.dept_code_id,
            supplier_code_id = n.supplier_code_id,
            mode_of_shipment = n.mode_of_shipment,
            location_code_id = n.location_code_id,
            supplier_reference_order = n.supplier_reference_order,
            estimated_time_of_arrival = n.estimated_time_of_arrival,
            total_amount = n.total_amount,
            total_amount_after_discount = n.total_amount_after_discount,
            insured = n.insured,
            foreign_currency_value = n.foreign_currency_value,
            local_currency_value = n.local_currency_value,
            exchange_rate = n.exchange_rate,
            trade_terms_id = n.trade_terms_id,
            discount_percentage = n.discount_percentage,
            currency_id = n.currency_id,
            remarks = n.remarks,
            status_id = 17)
    
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select()
    _po = db(db.Purchase_Order.purchase_request_no_id == request.args(0)).select().first()
    for n in _query:       
        db.Purchase_Order_Transaction.insert(            
            purchase_order_no_id = _po.id,
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            uom = n.uom,
            price_cost = n.price_cost,
            total_amount = n.total_amount,
            average_cost = n.average_cost,
            sale_cost = n.sale_cost,
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price)
    # session.po = _po.id
    response.flash = 'PURCHASE ORDER APPROVED'
    redirect(URL('procurement','insurance_proposal_details_new', args = request.args(0)))
    

def validate_empty(form):
    if request.vars.remarks == '':
        form.errors.remarks = 'Please indicate the reason.'

@auth.requires_login()
def generate_purchase_request_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'POR')).select().first()    
    _serial = _trans_prfx.current_year_serial_key + 1
    _val_purchase_request_no = str(_trans_prfx.prefix) + str(_serial)
    return XML(INPUT(_type="text", _class="form-control", _id='purchase_request_no', _name='purchase_request_no', _value=_val_purchase_request_no, _disabled = True))

@auth.requires_login()
def generate_supplier_code_currency():
    session.currency_id = 5    
    session.supplier_code_id = request.vars.supplier_code_id
    _s = db(db.Supplier_Master.id == request.vars.supplier_code_id).select().first()      
    if not _s:
        _currency = 1
    else:
        _currency = _s.currency_id
    _c = db(db.Currency.id == _currency).select().first() 
    if not _c:
        _value = 'None'        
        session.currency_id = 5        
        return XML(INPUT(_type="text", _class="form-control", _id='currency_id', _name='currency_id', _value=_value, _disabled = True))
    else:        
        _value = str(_c.description) 
        session.currency_id = _c.id        
        return XML(INPUT(_type="text", _class="form-control", _id='currency_id', _name='currency_id', _value=_value, _disabled = True))

@auth.requires_login()
def generate_supplier_trade_terms():
    _t = db(db.Supplier_Payment_Mode_Details.supplier_id == request.vars.supplier_code_id).select().first()
    if not _t:
        return XML(INPUT(_type="text", _class="form-control", _id='trade_terms', _name='trade_terms', _value='None', _disabled = True))
    else:
        return XML(INPUT(_type="text", _class="form-control", _id='trade_terms', _name='trade_terms', _value=_t.trade_terms_id.trade_terms, _disabled = True))
        # print 'supplier trade terms', _t.trade_terms_id.trade_terms

@auth.requires_login()
def generate_item_code_recent_cost():
    _i = db(db.Item_Master.item_code == request.vars.item_code).select().first()    
    if not _i:
        _value = 0
    else:
        _p = db(db.Item_Prices.item_code_id == _i.id).select().first()    
        _value = _p.most_recent_cost    
    return XML(INPUT(_type="text", _class="form-control", _id='most_recent_cost', _name='most_recent_cost', _value=locale.format('%.2F',_value or 0, grouping = True)))

@auth.requires_login()
def generate_category_id():
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()

    if not _id:
        return INPUT(_type="text", _class="form-control", _id='category_id', _name='category_id', _value = 'None', _readonly = True)                        
    else:
        # print 'if'
        
        if _id.type_id == 2 or _id.type_id == 3:
            _tx = db(db.Transaction_Item_Category.id == 4).select().first()
            session.category_id = _tx.id
            return INPUT(_type="text", _class="form-control", _id='category_id', _name='category_id', _value = _tx.description, _readonly = True) 
            # return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db(db.Transaction_Item_Category.id == 4).select(orderby=db.Transaction_Item_Category.id)])        
        if _id.type_id == 1:
            _tx = db(db.Transaction_Item_Category.id == 3).select().first()
            session.category_id = _tx.id
            return INPUT(_type="text", _class="form-control", _id='category_id', _name='category_id', _value = _tx.description, _readonly = True) 
        
        # if _id.type_id == 3 and _des.location_code_id == 1:
# -------   procurement session    ----------
@auth.requires_login()
def procurement_session():
    session.dept_code_id = request.vars.dept_code_id
    session.location_code_id = request.vars.location_code_id
    session.supplier_code_id = request.vars.supplier_code_id    
    
# -------   help request    ----------
@auth.requires_login()
def help_request():    
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Description'),TH('Department'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance')))    
    for n in db((db.Item_Master.dept_code_id == session.dept_code_id) & (db.Item_Master.supplier_code_id == session.supplier_code_id)).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
        for s in db((db.Stock_File.item_code_id == n.Item_Master.id) & (db.Stock_File.location_code_id == session.location_code_id)).select():
            row.append(TR(            
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.item_description),            
                TD(n.Item_Master.dept_code_id.dept_name),
                TD(n.Item_Master.supplier_code_id),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.uom_value),
                TD(n.Item_Prices.retail_price),
                TD(on_hand(n.Item_Master.id)),
                TD(on_transit(n.Item_Master.id)),
                TD(on_balance(n.Item_Master.id))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'display', _id = 'example', _style = "width:100%")
    return dict(table = table)

# ------- form id generator ----------
@auth.requires_login()
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# ---- C A R D Function  -----
@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

@auth.requires_login()
def on_hand(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _closing = db(db.Stock_File.item_code_id == _i.id).select().first()
        _on_hand = _closing.closing_stock
        return _on_hand
    else:
        _s = db(db.Stock_File.item_code_id == _i.id).select().first()
        _outer_on_hand = int(_s.closing_stock) / int(_i.uom_value)
        _pcs_on_hand = int(_s.closing_stock) - int(_outer_on_hand * _i.uom_value) 
        _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_i.uom_value)
        return _on_hand

@auth.requires_login()
def on_balance(e):    
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _balance = db(db.Stock_File.item_code_id == _i.id).select().first()
        _on_balance = _balance.probational_balance
        return _on_balance
    else:
        _s = db(db.Stock_File.item_code_id == _i.id).select().first()
        _outer = int(_s.probational_balance) / int(_i.uom_value)        
        _pcs = int(_s.probational_balance) - int(_outer * _i.uom_value)    
        _on_balance = str(_outer) + ' ' + str(_pcs) + '/' +str(_i.uom_value)
        return _on_balance

@auth.requires_login()
def on_transit(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _transit = db(db.Stock_File.item_code_id == _i.id).select().first()
        _on_transit = _transit.stock_in_transit
        return _on_transit
    else:
        _s = db(db.Stock_File.item_code_id == _i.id).select().first()
        _outer = int(_s.probational_balance) / int(_i.uom_value)
        _outer_transit = int(_s.stock_in_transit) / int(_i.uom_value)   
        _pcs_transit = int(_s.stock_in_transit) - int(_outer * _i.uom_value)
        _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_i.uom_value)
        return _on_transit

# ---- STOCK ON HAND ENTIRE LOCATION  -----
def stock_on_hand_all_location(e):
    _i = db(db.Purchase_Request_Transaction.item_code_id == e).select().first()
    _sum_on_hand = db.Stock_File.closing_stock.sum()
    _closing = db(db.Stock_File.item_code_id == e).select(_sum_on_hand).first()[_sum_on_hand]
    if _i.uom == 1:        
        return _closing
    else:
        _outer_on_hand = int(_closing) / int(_i.uom)
        _pcs_on_hand = int(_closing) - int(_outer_on_hand * _i.uom)
        _closing = str(_outer_on_hand) + ' - ' + str(_pcs_on_hand) + '/' + str(_i.uom)
        return _closing

def stock_in_transit_all_location(e):
    _i = db(db.Purchase_Request_Transaction.item_code_id == e).select().first()
    _sum_on_hand = db.Stock_File.stock_in_transit.sum()
    _in_transit = db(db.Stock_File.item_code_id == e).select(_sum_on_hand).first()[_sum_on_hand]
    if _i.uom == 1:        
        return _in_transit
    else:
        _outer_on_hand = int(_in_transit) / int(_i.uom)
        _pcs_on_hand = int(_in_transit) - int(_outer_on_hand * _i.uom)
        _in_transit = str(_outer_on_hand) + ' - ' + str(_pcs_on_hand) + '/' + str(_i.uom)
        return _in_transit

    
# ---------------------------------------------------------------
# -----------------     R  E  P  O  R  T  S     -----------------
# ---------------------------------------------------------------

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
from time import gmtime, strftime

today = datetime.datetime.now()
import inflect 
w=inflect.engine()
MaxWidth_Content = 530
styles = getSampleStyleSheet()
styles.leading = 24
styleB = styles["BodyText"]
styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch)
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch, showBoundary=1)
logo_path = request.folder + 'static/images/Merch.jpg'
text_path = request.folder + 'static/fonts/reports/'
img = Image(logo_path)
img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'

#  ['Remarks',':',Paragraph(_id.remarks, style = _style), '','Customer Sales Order Ref.',':',n.customer_order_reference]]
def insurance_proposal_reports():
    _id = db(db.Insurance_Details.purchase_order_no_id == request.args(0)).select().first()    
    _ip = db(db.Insurance_Master.id == _id.insurance_master_id).select().first()
    _po = db(db.Purchase_Order.id == request.args(0)).select().first()
    _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()
    _header = [
        ['INSURANCE PROPOSAL'],
        ['Ref: ' + str(_om.outgoing_mail_no)],
        [str(request.now.strftime("%B %d, %Y"))],
        [str(_ip.contact_person) + str('\n') + str(_ip.insurance_name) + str('\n') + str(_ip.address) + str('\n') +str(_ip.city) + str('\n') + str(_ip.country_id.description),''],
        ['Subject: ' + str(_om.mail_subject),''],        
        [Paragraph('Please make insurance for the following shipment which the details as the following to cover under our Open Insurance No. MTC/9/82:', style=_style)],
        ['DESCRIPTION',':',str(_id.description)],
        # ['VALUE',':',str(locale.format('%.2F',_po.total_amount_after_discount or 0, grouping = True))],
        ['VALUE',':',str(format_currency(_po.total_amount_after_discount, 'USD', locale='en_US'))],
        ['PAYMENT TERMS',':',str(_id.payment_terms)],
        ['MODE OF SHIPMENT',':',str(_po.mode_of_shipment)],
        ['PARTIAL SHIPMENT',':',str(_id.partial_shipment)],
        ['TRANSHIPMENT',':',str(_id.transhipment)],
        [Paragraph('Therefore, we appreciate to send us the insurance policy and the relevant debit advice.', style = _style),''],
        ['Expected date of arrival: ' + str(_po.estimated_time_of_arrival.strftime("%B %d, %Y")),''],
        ['Thanking You,',''],
        ['Yours faithfully,\nMERCH & PARTNERS CO.WLL',''],
        ['AUTHORIZED SIGNATURE',''],
        ['c.c: Order File(3133/2016C) Balancve\n:Home/amin/insurance proposal','']
    ]
    _header_table = Table(_header, colWidths=[155,20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('SPAN',(0,2),(-1,2)),
        ('SPAN',(0,3),(-1,3)),
        ('SPAN',(0,4),(-1,4)),
        ('SPAN',(0,5),(-1,5)),
        ('SPAN',(0,12),(-1,12)),
        ('SPAN',(0,13),(-1,13)),
        ('SPAN',(0,14),(-1,14)),
        ('SPAN',(0,15),(-1,15)),
        ('SPAN',(0,16),(-1,16)),
        ('SPAN',(0,17),(-1,17)),
        ('FONTSIZE',(0,0),(-1,0),15),        
        ('FONTNAME', (0, 3), (-1, 3), 'Courier-Bold'),
        ('FONTNAME', (0, 4), (-1, 4), 'Courier-Bold'),
        ('FONTNAME', (2, 6), (-1, 11), 'Courier-Bold'),
        ('ALIGN',(0,0),(0,0),'CENTER'),   
        ('ALIGN',(0,2),(-1,2),'RIGHT'),  
        ('BOTTOMPADDING',(0,0),(0,0),20), 
        ('TOPPADDING',(0,3),(0,3),20),
        ('BOTTOMPADDING',(0,3),(0,3),20), 
        ('TOPPADDING',(0,5),(-1,5),20),
        ('BOTTOMPADDING',(0,5),(-1,5),20), 
        ('TOPPADDING',(0,12),(-1,12),20),
        ('BOTTOMPADDING',(0,12),(-1,12),20), 
        ('TOPPADDING',(0,14),(-1,14),20),
        ('BOTTOMPADDING',(0,14),(-1,14),20), 
        ('TOPPADDING',(0,16),(-1,16),40),
        ('TOPPADDING',(0,17),(-1,17),40),
        ('TOPPADDING',(0,6),(-1,11),0),
        ('BOTTOMPADDING',(0,6),(-1,11),0),
    ]))
    row.append(_header_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def purchase_order_reports():
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    _header = [
        ['PURCHASE ORDER'],
        ['Purchase Order No',':',str(_id.purchase_order_no_prefix_id.prefix) + str(_id.purchase_order_no),'','Purchase Order Date',':',_id.purchase_order_date_approved.strftime('%d-%m-%Y')],
        ['Deparment',':',_id.dept_code_id.dept_name,'','Location',':',_id.location_code_id.location_name],
        ['Supplier Code',':',_id.supplier_code_id.supp_name,'','Proporma Invoice',':',_id.supplier_reference_order],
        ['Mode of Shipment',':',_id.mode_of_shipment,'','Trade Terms',':',_id.trade_terms_id.trade_terms],
        ['ETA',':',_id.estimated_time_of_arrival.strftime('%d-%m-%Y'),'','','',]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
    # head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Closing Stock'),TH('Order In Transit'),TH('MRS Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    ctr = _grand_total = 0
    _row = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Total Amount']]    
    for n in db(db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)).select(left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id)):
        ctr += 1
        _grand_total += n.Purchase_Order_Transaction.total_amount
        _row.append([            
            ctr,            
            n.Purchase_Order_Transaction.item_code_id.item_code,
            n.Item_Master.item_description,
            n.Purchase_Order_Transaction.uom,
            n.Purchase_Order_Transaction.category_id.mnemonic,
            card(n.Purchase_Order_Transaction.quantity,n.Purchase_Order_Transaction.uom),
            # stock_on_hand_all_location(n.Purchase_Order_Transaction.item_code_id),
            # stock_in_transit_all_location(n.Purchase_Order_Transaction.item_code_id),            
            locale.format('%.2F',n.Purchase_Order_Transaction.price_cost or 0, grouping = True),
            locale.format('%.2F',n.Purchase_Order_Transaction.total_amount or 0, grouping = True),
            ])
    _row.append(['','','','','','Net Amount',':',_id.currency_id.mnemonic+' ' + locale.format('%.2F',_grand_total or 0, grouping = True)])
    _row.append(['','','','','','Discount %',':',locale.format('%d',_id.discount_percentage or 0, grouping = True)])
    _row.append(['','','','','','Total Amount',':', _id.currency_id.mnemonic+' ' + locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True)])
    _row.append(['','','','','','Total Amount (QR)',':', locale.format('%.2F',_id.local_currency_value or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,60,'*',30,30,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
    ]))    

    _footer = [
        # ['Purchase Order No',':',str(_id.purchase_order_no_prefix_id.prefix) + str(_id.purchase_order_no),'','Purchase Order Date',':',_id.purchase_order_date_approved.strftime('%d-%m-%Y')],
        ['Purchase Request No',':',str(_id.purchase_request_no_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_no_id.purchase_request_date.strftime('%d-%m-%Y')],        
        ['Remarks',':',_id.remarks,'','','','']]
    _footer_table = Table(_footer, colWidths=['*',20,'*',20,'*',20,'*'])
    _footer_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
        
    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_footer_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def purchase_request_reports():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _header = [
        ['PURCHASE REQUEST'],
        ['Purchase Request No',':', str(_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_date],
        ['Deparment',':',_id.dept_code_id.dept_name,'','Location',':',_id.location_code_id.location_name],
        ['Supplier Code',':',_id.supplier_code_id.supp_name,'','Proporma Invoice',':',_id.supplier_reference_order],
        ['Mode of Shipment',':',_id.mode_of_shipment,'','Trade Terms',':',_id.trade_terms_id.trade_terms],
        ['ETA',':',_id.estimated_time_of_arrival.strftime('%d-%m-%Y'),'','','',]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    ctr = _grand_total = 0
    _row = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Total Amount']]
    for n in db(db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)).select(left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id)):
        ctr += 1
        _grand_total += n.Purchase_Request_Transaction.total_amount
        _row.append([            
            ctr,            
            n.Purchase_Request_Transaction.item_code_id.item_code,
            n.Item_Master.item_description,
            n.Purchase_Request_Transaction.uom,
            n.Purchase_Request_Transaction.category_id.mnemonic,
            card(n.Purchase_Request_Transaction.quantity,n.Purchase_Request_Transaction.uom),
            # stock_on_hand_all_location(n.Purchase_Request_Transaction.item_code_id),
            # stock_in_transit_all_location(n.Purchase_Request_Transaction.item_code_id),            
            locale.format('%.2F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True),
            locale.format('%.2F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True),
            ])
    _row.append(['','','','','','Net Amount',':',_id.currency_id.mnemonic+' ' + locale.format('%.2F',_grand_total or 0, grouping = True)])
    _row.append(['','','','','','Discount %',':',locale.format('%d',_id.discount_percentage or 0, grouping = True)])
    _row.append(['','','','','','Total Amount',':', _id.currency_id.mnemonic+' ' + locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True)])
    _row.append(['','','','','','Total Amount (QR)',':', locale.format('%.2F',_id.local_currency_value or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,60,'*',30,30,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
    ]))    

    _footer = [
        ['Remarks',':',_id.remarks,'','','','']]
    _footer_table = Table(_footer, colWidths=['*',20,'*',20,'*',20,'*'])
    _footer_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_footer_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def warehouse_receipt_reports():
    # _id = db(db.Purchase_Receipt_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    _list = ', '.join([str(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix)+str(i.purchase_order_no_id.purchase_order_no) for i in db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select()])
    _header = [
        ['WAREHOUSE PURCHASE RECEIPT'],
        ['Purchase Receipt No.',':',str(_id.purchase_receipt_no_id.purchase_receipt_no_prefix_id.prefix)+str(_id.purchase_receipt_no_id.purchase_receipt_no),'','Purchase Receipt Date',':',_id.purchase_receipt_no_id.purchase_receipt_date_approved],        
        ['Purchase Order No.',':',_list,'','','']
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    ctr = _after_discount = _discount = _total_amount = _total_amount_loc = 0

    for n in db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select():
        _after_discount += n.purchase_order_no_id.total_amount_after_discount
        _discount += int(n.purchase_order_no_id.discount_percentage or 0)
        _total_amount += n.purchase_order_no_id.total_amount
        _total_amount_loc += n.purchase_order_no_id.local_currency_value

    _row = [['#','Item Code','Item Description','UOM','Cat','Qty']]
    for n in db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select(left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):
        ctr += 1
        # _total_row_amount = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.price_cost
        _row.append([
            ctr,
            n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code,
            n.Item_Master.item_description,
            n.Purchase_Receipt_Transaction_Consolidated.uom,
            n.Purchase_Receipt_Transaction_Consolidated.category_id.mnemonic,
            card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),
            # locale.format('%.2F',n.Purchase_Receipt_Transaction_Consolidated.price_cost or 0, grouping = True),
            # locale.format('%.2F',_total_row_amount or 0, grouping = True)
            ])
    # _row.append(['','','','','','Net Amount',':', locale.format('%.2F', _after_discount or 0, grouping = True)])
    # _row.append(['','','','','','Discount %',':',locale.format('%d', _discount or 0, grouping = True)])
    # _row.append(['','','','','','Total Amount',':',  locale.format('%.2F', _total_amount or 0, grouping = True)])
    # _row.append(['','','','','','Total Amount (QR)',':', locale.format('%.2F', _total_amount_loc or 0, grouping = True)])
    for m in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).select():
        ctr += 1
        _row.append([
            ctr,
            m.item_code,
            m.item_description,
            m.uom,
            m.category_id.mnemonic,
            card(m.total_pieces,m.uom)
        ])
    _table = Table(_row, colWidths=[20,60,'*',30,30,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        # ('ALIGN',(6,1),(7,-1),'RIGHT'),
    ]))    
    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data