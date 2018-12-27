import string
import random
import locale
from datetime import date
@auth.requires_login()
def sales_order_form():
    db.Sales_Order.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 3), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    db.Sales_Order.status_id.default = 3
    ctr = db(db.Transaction_Prefix.prefix_key == 'SO').select().first()
    _skey = ctr.current_year_serial_key
    _skey += 1
    form = SQLFORM(db.Sales_Order)
    if form.process().accepted:
        response.flash = 'SAVING SALES ORDER NO ' + str(_skey) + '.'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = id_generator())

def sales_order_transaction_temporary():
    form = SQLFORM(db.Sales_Order_Transaction_Temporary)
    if form.accepts(request, formname = None, onvalidation = validate_sales_order_transaction):        
        ctr = 0
        row = []                
        grand_total = 0
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Taxable Value'),TH('Tax %'),TH('Tax Amount'),TH('Total Amount'),TH('Action')))
        _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Order_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = ~db.Sales_Order_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction_Temporary.item_code_id)])
        for n in _query:

            ctr += 1
            _total_amount = generate_total_amount(n.Sales_Order_Transaction_Temporary.quantity, n.Sales_Order_Transaction_Temporary.pieces, n.Item_Master.uom_value, n.Item_Prices.retail_price)            
            grand_total += _total_amount 
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction_Temporary.id))            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction_Temporary.id))
            btn_lnk = DIV(dele_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Sales_Order_Transaction_Temporary.category_id.mnemonic),
                TD(n.Item_Master.uom_value),
                TD(n.Sales_Order_Transaction_Temporary.quantity),
                TD(n.Sales_Order_Transaction_Temporary.pieces),
                TD(n.Sales_Order_Transaction_Temporary.discount_percentage),
                TD(n.Item_Prices.retail_price, _align = 'right'),
                TD(n.Sales_Order_Transaction_Temporary.taxable_value, _align = 'right'),
                TD(n.Sales_Order_Transaction_Temporary.tax_percentage, _align = 'right'),
                TD(n.Sales_Order_Transaction_Temporary.tax_amount, _align = 'right'),
                TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right'),
                TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[head, body, foot], _class='table table-striped')
        return table        
    elif form.errors:
        ctr = 0
        row = []                
        grand_total = 0
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Taxable Value'),TH('Tax %'),TH('Tax Amount'),TH('Total Amount'),TH('Action')))
        _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Order_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = ~db.Sales_Order_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction_Temporary.item_code_id)])
        for n in _query:

            ctr += 1
            _total_amount = generate_total_amount(n.Sales_Order_Transaction_Temporary.quantity, n.Sales_Order_Transaction_Temporary.pieces, n.Item_Master.uom_value, n.Item_Prices.retail_price)            
            grand_total += _total_amount 
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction_Temporary.id))            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction_Temporary.id))
            btn_lnk = DIV(dele_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Sales_Order_Transaction_Temporary.category_id.mnemonic),
                TD(n.Item_Master.uom_value),
                TD(n.Sales_Order_Transaction_Temporary.quantity),
                TD(n.Sales_Order_Transaction_Temporary.pieces),
                TD(n.Item_Prices.retail_price, _align = 'right'),
                TD(n.Sales_Order_Transaction_Temporary.taxable_value, _align = 'right'),
                TD(n.Sales_Order_Transaction_Temporary.tax_percentage, _align = 'right'),
                TD(n.Sales_Order_Transaction_Temporary.tax_amount, _align = 'right'),
                TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right'),
                TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[TR(v) for k, v in form.errors.items()],_class='table')        
        table += TABLE(*[head, body, foot], _class='table table-striped')        
        return table


def validate_sales_order_transaction(form):    
    
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    _sfile = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()    
    _exist = db((db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id) & (db.Sales_Order_Transaction_Temporary.item_code == request.vars.item_code)).select(db.Sales_Order_Transaction_Temporary.item_code).first()        
    if _id:

        print 'here'    
    if _id.item_code == False:
        print 'not here'
        form.errors._id.item_code = CENTER(DIV(B('WARNING! '),'Item code does not exist',_class='alert alert-warning',_role='alert'))
    
    if not _sfile:
        form.errors._stk_file =  CENTER(DIV(B('WARNING! '),'Item code does not exist in stock file',_class='alert alert-warning',_role='alert'))
    
    if _exist:
        form.errors.item_code = CENTER(DIV(B('WARNING! '),'Item code ' + str(_exist.item_code) + ' already exist.',_class='alert alert-danger',_role='alert'))

    if _id.uom_value == 1:
        if form.vars.pieces > 0:
            form.errors.pieces = CENTER(DIV(B('WARNING! '),' Pieces value is not applicable to this item.',_class='alert alert-warning',_role='alert')) 
            form.vars.pieces = 0
    elif form.vars.pieces >= int(_id.uom_value):
        form.errors._id = CENTER(DIV(B('WARNING! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-warning',_role='alert')) 
            
    form.vars.item_code_id = _id.id
    form.vars.taxable_value = 0
    form.vars.tax_percentage = 0
    form.vars.tax_amount = 0
    

def generate_sales_order_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SO')).select().first()    
    _serial = _trans_prfx.current_year_serial_key + 1
    _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
    return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True))


def item_code_description():
    _icode = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == request.vars.dept_code_id)).select().first()    

    if _icode:
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()

        if _sfile:
           
            _on_hand = card(_icode.id, _sfile.probational_balance, _icode.uom_value)
            _on_transit = card(_icode.id, _sfile.stock_in_transit, _icode.uom_value)
            _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(locale.format('%.2F',_iprice.retail_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_hand)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV(B('WARNING! '),"Item code doesn't exist on location source.",_class='alert alert-warning',_role='alert'))        
    else:
        return CENTER(DIV(B('WARNING! '),"Item code doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))

@auth.requires_login()
def sales_order_browse():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Location Destination')))
    for n in db(db.Sales_Order).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(n.sales_order_no),TD(n.dept_code_id),TD(n.stock_source_id),TD(n.customer_code_id)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def generate_total_amount(qty, pcs, uom, price ):
    _pcs = qty * uom + pcs
    _uprice = float(price) / int(uom)
    _tamount = float(_uprice) * int(_pcs)
    return _tamount

# ------- form id generator ----------
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
