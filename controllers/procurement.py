# ------------------------------------------------------------------------------------------
# -------------------------  P R O C U R E M E N T   S Y S T E M  --------------------------
# ------------------------------------------------------------------------------------------

import string, random, locale
from datetime import date

@auth.requires_login()
def purchase_request_browse():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Purchase Order No.'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
    for n in db((db.Purchase_Request.created_by == auth.user.id) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id):
        if n.status_id ==18:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})                    
        else:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_browse_view', args = n.id, extension = False))        
        btn_lnk = DIV(view_lnk, clea_lnk)
        
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
            TD(_po),
            TD(_px),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

@auth.requires_login()
def purchase_request_archived():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _id.update_record(archives = True, updated_on = request.now, updated_by = auth.user_id)
    response.flahs = 'RECORD CLEARED'

@auth.requires_login()
def purchase_request_browse_view():
    db.Purchase_Request.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Purchase_Request.status_id.default = 19
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def puchase_request_transaction_browse_view():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    row = []
    ctr = grand_total = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Most Recent Cost'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
    for n in _query:
        ctr += 1
        grand_total += n.Purchase_Request_Transaction.total_amount
        if auth.user_id != n.Purchase_Request_Transaction.created_by or _id.status_id != 19:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_browse_view_edit',args = n.Purchase_Request_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction.id)})
        btn_lnk = DIV(edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction.uom),
            TD(card(n.Purchase_Request_Transaction.item_code_id,n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value)),            
            TD(locale.format('%.2F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
            TD(locale.format('%.2F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD('', _colspan= '2'),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2F',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD('', _colspan= '2'),TD(),TD(),TD(),TD(H4('DISCOUNT %'), _align = 'right'),TD(H4('0', _align = 'right')),TD(P(_id='error'))))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblPr')
    return dict(table = table)    

def puchase_request_transaction_browse_view_delete():        
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()        
    # _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()    
    # _chk_empty = db((db.Purchase_Request_Transaction.purchase_request_no_id == _pr.id) & (db.Purchase_Request_Transaction.delete == False)).count()
    # if _chk_empty == 1:
    #     response.flash = 'RECORD SHOULD NOT EMPTY'
    # else:
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblPr').get(0).reload()"

def puchase_request_transaction_edit(form):
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    form.vars.quantity = _qty

def puchase_request_transaction_browse_view_edit():
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
        _discount = float(_total) * int(_pr.discount_percentage or 0) / 100
        _total_amount_after_discount = float(_total) - int(_discount)
        _pr.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount)
        session.flash = 'RECORD UPDATED'
        redirect(URL('procurement','purchase_request_browse_view', args = _pr.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('purchase_request_browse_view', args = _pr.id))
    return dict(form = form, btn_back = btn_back)   

@auth.requires_login()
def puchase_request_transaction_grid_view_accounts(): # db.Purchase_Request_Transaction_Accounts
    _id = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select(orderby = ~db.Purchase_Request_Transaction.id)
    _query = db(db.Purchase_Request_Transaction_Accounts.purchase_request_no_id == request.args(0)).select().first()
    if not _query:
        for x in _id:
            db.Purchase_Request_Transaction_Accounts.insert(
                purchase_request_no_id = request.args(0),
                item_code_id = x.item_code_id,
                category_id = x.category_id,
                quantity = x.quantity,
                uom = x.uom,
                price_cost = x.price_cost)            
    row = []
    ctr = grand_total = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Most Recent Cost'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    _query = db((db.Purchase_Request_Transaction_Accounts.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Accounts.delete != True)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Accounts.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction_Accounts.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Accounts.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction_Accounts.item_code_id)])
    for n in _query:
        ctr += 1
        _total_amount = float(float(n.Purchase_Request_Transaction_Accounts.price_cost) /  int(n.Purchase_Request_Transaction_Accounts.uom)) * int(n.Purchase_Request_Transaction_Accounts.quantity)
        grand_total += _total_amount
        # print 'currency ', locale.currency(grand_total, grouping = True)
        if auth.user_id != n.Purchase_Request_Transaction_Accounts.created_by:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_browse_view_edit',args = n.Purchase_Request_Transaction_Accounts.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction_Accounts.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction_Accounts.id)})
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Accounts.item_code_id.item_code, INPUT(_type='text', _id='item_code_id', _name='item_code_id', _hidden = True, _value = n.Purchase_Request_Transaction_Accounts.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction_Accounts.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction_Accounts.uom),
            TD(card(n.Purchase_Request_Transaction_Accounts.item_code_id,n.Purchase_Request_Transaction_Accounts.quantity,n.Purchase_Request_Transaction_Accounts.uom)),     
            TD(INPUT(_type='number', _class='form-control', _id = 'price_cost', _name='price_cost', _style='text-align:right;', _value= locale.format('%.2F',n.Purchase_Request_Transaction_Accounts.price_cost or 0, grouping = True)), _style='width:150px;'),
            # TD(locale.format('%.2F',n.Purchase_Request_Transaction_Accounts.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),
            TD(locale.currency(_total_amount, grouping = True), _align = 'right', _style="width:120px;"),
            TD(btn_lnk)))
    body = TBODY(*row)
    # foot = TFOOT(TR(TD(_colspan='8'),TD(INPUT(_type='submit'))))
    foot = TFOOT(TR(TD(H4('TOTAL AMOUNT'), _align = 'right', _colspan='7'),TD(H4(locale.currency(grand_total, grouping = True)), _align = 'right'),TD(INPUT(_type='submit',_value='save'))))
    # table = TABLE(*[head, body, foot], _class='table table-bordered', _id = 'tblTA')
    form = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblTA'))
    if form.accepts(request, session):
        _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _upd = db((db.Purchase_Request_Transaction_Accounts.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Accounts.item_code_id == _item_code_id)).select().first()            
            _total_amount = float(request.vars['price_cost'][x]) / int(_upd.uom) * int(_upd.quantity) 
            _upd.update_record(price_cost = request.vars['price_cost'][x], total_amount = _total_amount)    
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
    if form2.process(onvalidation = validate_purchase_request_transaction_accounts).accepted:
        db.Purchase_Request_Transaction_Accounts.insert(
            purchase_request_no_id = request.args(0),
            item_code_id = form2.vars.item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            price_cost = form2.vars.price_cost,
            total_amount = form2.vars.total_amount)        
        response.flash = 'RECORD SAVE'
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(table = form, form2 = form2)

def validate_purchase_request_transaction_accounts(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    _ex = db((db.Purchase_Request_Transaction_Accounts.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Accounts.item_code_id == _id.id)).select().first()    
    _tp = int(request.vars.quantity or 0) * int(_id.uom_value) + int(request.vars.pieces or 0)    

    if _ex:        
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'    

    _pu = float(request.vars.most_recent_cost or 0) / int(_id.uom_value)
    _pc = float(_pu) * int(_tp)
    
    form2.vars.item_code = _id.id
    form2.vars.price_cost = request.vars.most_recent_cost
    form2.vars.total_amount = _pc
    form2.vars.quantity = _tp
    form2.vars.uom = _id.uom_value

@auth.requires_login()
def purchase_request_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = 0
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('supplier_reference_order','string', length = 25),
        Field('estimated_time_of_arrival', 'date', default = request.now),
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
            location_code_id = form.vars.location_code_id,
            supplier_reference_order = form.vars.supplier_reference_order,
            estimated_time_of_arrival = form.vars.estimated_time_of_arrival,
            total_amount = form.vars.total_amount,
            total_amount_after_discount = form.vars.total_amount_after_discount,
            discount_percentage = form.vars.discount_percentage,
            currency_id = session.currency_id,
            remarks = form.vars.remarks, 
            status_id = form.vars.status_id)
        _id = db(db.Purchase_Request.purchase_request_no == ctr.current_year_serial_key).select().first()
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
                # sale_cost = _ip.sale_cost,
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
            _id.update_record(
                total_amount = _grand_total,
                discount_percentage = _discount,
                total_amount_after_discount = _after_discount)
            session.discount = 0
            db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'SAVE PURCHASE REQUEST NO ' + str(_skey) + '.'
    elif form.errors:
        response.flash = 'FORM HAS ERRROS'

    
    # _details = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': payment_details(2)})
    # _details = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': payment_details(1)}) 
    return dict(form = form, ticket_no_id = ticket_no_id)

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
def validate_purchase_return_transaction(form):
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    if not _id:
        form.errors.item_code ='Item code does not exist or empty.'
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code = 'Item code does not exist in stock file.'
    else:
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        _pr = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _ex = db((db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Purchase_Request_Transaction_Temporary.item_code_id == _id.id) & (db.Purchase_Request_Transaction_Temporary.category_id == request.vars.category_id)).select().first()
        _tp = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)
        _pu = _pc = 0
        if not _pr:
            form.errors.item_code = 'Item code does\'nt have price'
        
        if _ex:
            response.js = "$('#btnadd).get(0).reload()"
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        else:
            if int(request.vars.category_id) == 3:
                _pu = 0                
            else:
                _pu = float(request.vars.most_recent_cost or 0) / int(_id.uom_value)
            
        
        if _id.uom_value == 1:
            form.vars.piece = 0
        
        if _tp == 0:
            form.vars.quantity = 'Zero quantity not accepted.'
        
        if int(request.vars.pieces) >= int(_id.uom_value):
            form.vars.pieces = 'Pieces should not be more than UOM value.'                

        _pc = float(_pu) * int(_tp)
        # print 'total amount', _pc, _pu, _tp, request.vars.most_recent_cost, _id.uom_value
    form.vars.item_code_id = _id.id
    form.vars.price_cost = request.vars.most_recent_cost
    form.vars.total_amount = _pc
    form.vars.total_pieces = _tp
    form.vars.uom = _id.uom_value
    
@auth.requires_login()
def purchase_request_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_return_transaction).accepted:
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
    ctr = grand_total = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Most Recent Cost'),TH('Total Amount'),TH('Action'),_class='bg-success'))
    _query = db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1
        grand_total += n.Purchase_Request_Transaction_Temporary.total_amount
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Purchase_Request_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Purchase_Request_Transaction_Temporary.id),'_data-qt':(n.Purchase_Request_Transaction_Temporary.quantity), '_data-pc':(n.Purchase_Request_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction_Temporary.id)})
        btn_lnk = DIV( dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction_Temporary.category_id.mnemonic),
            TD(n.Item_Master.uom_value),
            TD(n.Purchase_Request_Transaction_Temporary.quantity),
            TD(n.Purchase_Request_Transaction_Temporary.pieces),
            TD(locale.format('%.2F',n.Purchase_Request_Transaction_Temporary.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
            TD(locale.format('%.2F',n.Purchase_Request_Transaction_Temporary.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD('', _colspan= '2'),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(INPUT(_class='form-control', _name = 'grand_total', _id='grand_total', _disabled = True, _value = locale.format('%.2F',grand_total or 0, grouping = True))), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD('', _colspan= '2'),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT %'), _align = 'right'),TD(H4(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right')),TD(P(_id='error'))))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblPrt')
    return dict(form = form, table = table, grand = 0)

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
        response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:   
             
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()        
        if _sfile:               
            if _icode.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_balanced = _sfile.probational_balance
                _on_transit = _sfile.stock_in_transit
                _on_hand = _sfile.closing_stock      
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_icode.id, _sfile.probational_balance, _icode.uom_value)
                _on_transit = card(_icode.id, _sfile.stock_in_transit, _icode.uom_value)
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)     
            response.js = "$('#btnadd').removeAttr('disabled')"       
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax'),TH('Retail Price'),TH('Unit Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(_icode.selectivetax),
                TD(_iprice.retail_price),
                TD(locale.format('%.2F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_balanced)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

def test():
    return dict()
# ------------------- PURCHASE REQUEST ACTION REQUIRED -------------------
@auth.requires_login()
def purchase_request_grid():
    row = []
    _query = db(db.Purchase_Request).select(orderby = ~db.Purchase_Request.id) 
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _query = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    elif auth.has_membership(role = 'INVENTORY'):        
        _query = db((db.Purchase_Request.status_id == 20) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _query = db((db.Purchase_Request.status_id == 11) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
    elif auth.has_membership(role = 'ACCOUNT USERS'):
        _query = db((db.Purchase_Request.status_id == 17) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 

    head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Purchase Order No.'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Ref. Order'),TH('Location Source'),TH('Amount'),TH('Requested by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))

    for n in _query:
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_sales_manager', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        elif auth.has_membership(role = 'INVENTORY'):
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_inventory_manager', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)            
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_store_keeper', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        elif auth.has_membership(role = 'ACCOUNT USERS'):
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
            TD(_po),
            TD(_px),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.total_amount),TD(n.created_by.first_name.upper()),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)    

@auth.requires_login()
def purchase_request_grid_view_sales_manager():
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
    if form.process(onvalidation = validate_empty).accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('inventory','mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)


    # _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    # _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)
    # response.js = "$('#PRtbl').get(0).reload()"
    # session.flash = 'PURCHASE REQUEST REJECTED'

@auth.requires_login()
def purchase_request_grid_view_inventory_manager():
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
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

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
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def purchase_request_grid_transaction_store_keeper_():
    row = []
    ctr = grand_total = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),_class='bg-success'))    
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
    for n in _query:
        ctr += 1
        grand_total += n.Purchase_Request_Transaction.total_amount
        if auth.user_id != n.Purchase_Request_Transaction.created_by:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_browse_view_edit',args = n.Purchase_Request_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction.id)})
        btn_lnk = DIV(edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction.uom),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity')),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces'))))
    body = TBODY(*row)        
    table = TABLE(*[head, body], _class='table table-bordered', _id = 'tblPr')
    return dict(table = table) 

@auth.requires_login()
def purchase_request_grid_transaction_store_keeper():
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select()
    _tnx = db(db.Purchase_Request_Transaction_Received.purchase_request_no_id == request.args(0)).select().first()
    if not _tnx:
        for x in _query:
            db.Purchase_Request_Transaction_Received.insert(purchase_request_no_id = x.purchase_request_no_id,item_code_id = x.item_code_id,category_id = x.category_id,uom = x.uom)        
    row = []
    ctr = grand_total = 0   
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),_class='bg-success'))        
    for n in db(db.Purchase_Request_Transaction_Received.purchase_request_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Received.ALL, orderby = ~db.Purchase_Request_Transaction_Received.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Received.item_code_id)):
        ctr += 1      
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')  
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Received.item_code_id.item_code, INPUT(_type='text', _id = 'item_code_id', _name='item_code_id', _hidden = True, _value= n.Purchase_Request_Transaction_Received.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction_Received.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction_Received.uom,INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= n.Purchase_Request_Transaction_Received.uom)),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= n.Purchase_Request_Transaction_Received.quantity)),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = n.Purchase_Request_Transaction_Received.pieces))))
    row.append(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(INPUT(_type='submit'))))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table', _id = 'tblPr'))
    if form.accepts(request, session):
        response.flash = 'RECORD UPDATED'
        for x in xrange(ctr):
            _total_pieces = int(request.vars['quantity'][x]) * int(n.Purchase_Request_Transaction_Received.uom) + int(request.vars['pieces'][x])
            _item_code_id = int(request.vars['item_code_id'][x])
            _upd = db((db.Purchase_Request_Transaction_Received.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Received.item_code_id == _item_code_id)).select().first()
            _upd.update_record(quantity = request.vars['quantity'][x],pieces = request.vars['pieces'][x], total_pieces = _total_pieces)
            response.js = "$('#tblPr').get(0).reload()"
    elif form.errors:
        response.flash = 'FORM HAS ERROR'   
    return dict(form = form) 

@auth.requires_login()
def purchase_request_grid_view_accounts():
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
    session.dept_code_id = _id.dept_code_id
    session.supplier_code_id = _id.supplier_code_id
    session.location_code_id = _id.location_code_id
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def purchase_request_approved():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _id.update_record(status_id = 20, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)
        session.flash = 'PURCHASE REQUEST APPROVED'
    elif auth.has_membership(role = 'INVENTORY'):
        _id.update_record(status_id = 11, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)
        session.flash = 'PURCHASE REQUEST APPROVED'
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)   
        _id.update_record(status_id = 17, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now)
        session.flash = 'PURCHASE ORDER APPROVED'
    elif auth.has_membership(role = 'ACCOUNT USERS'):
        _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
        _id.update_record(status_id = 18, purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)
        session.flash = 'PURCHASE RECEIPT APPROVED'
    response.js = "$('#PRtbl').get(0).reload()"
    #ajax('{{=URL('generate_item_code_recent_cost')}}', ['item_code'], '_most_recent_cost'); 
@auth.requires_login()
def purchase_request_rejected():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)
        session.flash = 'PURCHASE REQUEST REJECTED'
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _id.update_record(status_id = 3, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now)
    elif auth.has_membership(role = 'ACCOUNT USERS'):
        _id.update_record(status_id = 3, purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)
    response.js = "$('#PRtbl').get(0).reload()"
    

def validate_empty(form):
    if request.vars.remarks == '':
        form.errors.remarks = 'empty'

@auth.requires_login()
def generate_purchase_request_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'POR')).select().first()    
    _serial = _trans_prfx.current_year_serial_key + 1
    _val_purchase_request_no = str(_trans_prfx.prefix) + str(_serial)
    return XML(INPUT(_type="text", _class="form-control", _id='purchase_request_no', _name='purchase_request_no', _value=_val_purchase_request_no, _disabled = True))

@auth.requires_login()
def generate_supplier_code_currency():    
    session.supplier_code_id = request.vars.supplier_code_id
    _s = db(db.Supplier_Master.id == request.vars.supplier_code_id).select().first()      
    if not _s:
        _currency = 0
    else:
        _currency = _s.currency_id
    _c = db(db.Currency.id == _currency).select().first() 
    if not _c:
        _value = 'None'        
        session.currency_id = None        
        return XML(INPUT(_type="text", _class="form-control", _id='currency_id', _name='currency_id', _value=_value, _disabled = True))
    else:        
        _value = str(_c.description) 
        session.currency_id = _c.id        
        return XML(INPUT(_type="text", _class="form-control", _id='currency_id', _name='currency_id', _value=_value, _disabled = True))

@auth.requires_login()
def generate_item_code_recent_cost():
    _i = db(db.Item_Master.item_code == request.vars.item_code).select().first()    
    _p = db(db.Item_Prices.item_code_id == _i.id).select().first()    
    _value = _p.most_recent_cost    
    return XML(INPUT(_type="text", _class="form-control", _id='most_recent_cost', _name='most_recent_cost', _value=locale.format('%.2F',_value or 0, grouping = True)))

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
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
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

def edit_test():
    form = SQLFORM(db.Purchase_Request_Transaction_Recieved_Temporary, request.args(0))
    if form.accepts(request, session):
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict()

def edit_test2():
    form = SQLFORM(db.Purchase_Request_Transaction_Recieved_Temporary, request.args(0))
    if form.accepts(request, session):
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict()

def edit_test3():
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select()
    _tm = db(db.Purchase_Request_Transaction_Recieved_Temporary.purchase_request_no_id == request.args(0)).select().first()
    if not _tm:
        for x in _query:
            db.Purchase_Request_Transaction_Recieved_Temporary.insert(purchase_request_no_id = x.purchase_request_no_id,item_code_id = x.item_code_id,category_id = x.category_id,uom = x.uom)        
    row = []
    ctr = grand_total = 0   
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),_class='bg-success'))    
    _temporary = db(db.Purchase_Request_Transaction_Recieved_Temporary).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Recieved_Temporary.ALL, orderby = ~db.Purchase_Request_Transaction_Recieved_Temporary.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Recieved_Temporary.item_code_id))            
    for n in _temporary:
        ctr += 1        
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Recieved_Temporary.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction_Recieved_Temporary.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction_Recieved_Temporary.uom),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value=0, _disabled = True)),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _disabled = True))))
    body = TBODY(*row)        
    table = TABLE(*[head, body], _class='table table-bordered', _id="editable")
    return dict(table = table) 

def edit_test4():
    return locals()