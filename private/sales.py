import string, random, locale
from datetime import date

# ----------    S A L E S  O R D E R  S E T T I N G S    ----------
@auth.requires_login()
def customer_category_grid():
    form = SQLFORM(db.Customer_Category)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action')))
    for n in db(db.Customer_Category).select(orderby = db.Customer_Category.id):        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_category_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login()
def customer_category_edit_form():
    form = SQLFORM(db.Customer_Category, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def customer_account_type_grid():
    form = SQLFORM(db.Customer_Account_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action')))
    for n in db(db.Customer_Account_Type).select(orderby = db.Customer_Account_Type.id):        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_account_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login()
def customer_account_type_edit_form():
    form = SQLFORM(db.Customer_Account_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def customer_group_code_grid():
    form = SQLFORM(db.Customer_Group_Code)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action')))
    for n in db(db.Customer_Group_Code).select(orderby = db.Customer_Group_Code.id):        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_group_code_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login()
def customer_group_code_edit_form():
    form = SQLFORM(db.Customer_Group_Code, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ----------    C U S T O M E R  F O R M    ----------
@auth.requires_login()
def customer_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Account No.'),TH('Group Code'),TH('Name'),TH('Category'),TH('Type'),TH('Action')))
    for n in db().select(db.Customer.ALL, orderby = db.Customer.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('view_customer_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_add_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        cont_lnk = A(I(_class='fas fa-user-plus'), _title='Add Contact Person', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_contact_person_add_form', args = n.id))
        cred_lnk = A(I(_class='fas fa-credit-card'), _title='Credit Limit', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_credit_limit_add_form', args = n.id))
        bank_lnk = A(I(_class='fas fa-money-check'), _title='Bank Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_bank_details', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, cont_lnk, cred_lnk,bank_lnk)
        row.append(TR(TD(n.id),TD(n.customer_account_no),TD(n.customer_group_code_id),TD(n.customer_name),TD(n.customer_category_id),TD(n.customer_account_type),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

@auth.requires_login()
def customer_add_form():
    form = SQLFORM(db.Customer)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def customer_add_edit_form():
    form = SQLFORM(db.Customer, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('customer_grid'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def customer_contact_person_add_form():
    form = SQLFORM(db.Customer_Contact_Person)
    if form.process(onvalidation = validate_customer_contact_person).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    head = THEAD(TR(TH('#'),TH('Contact Person'),TH('Contact No'),TH('Position'),TH('Email'),TH('Action')))
    for n in db(db.Customer_Contact_Person.customer_id == request.args(0)).select(db.Customer_Contact_Person.ALL, orderby = db.Customer_Contact_Person.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_contact_person_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.contact_person),TD(n.contact_number),TD(n.position),TD(n.email_address),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(form = form, table = table)

def validate_customer_contact_person(form):
    form.vars.customer_id = request.args(0)    
    
@auth.requires_login()
def customer_contact_person_edit_form():    
    _id = db(db.Customer_Contact_Person.id == request.args(0)).select().first()    
    form = SQLFORM(db.Customer_Contact_Person, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'            
        redirect(URL('customer_contact_person_add_form', args = _id.customer_id))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def customer_credit_limit_add_form():
    form = SQLFORM(db.Customer_Credit_Limit)
    if form.process(onvalidation = validate_customer_credit_limit).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    head = THEAD(TR(TH('#'),TH('Department'),TH('Amount'),TH('Action')))
    for n in db().select(db.Customer_Credit_Limit.ALL, orderby = db.Customer_Credit_Limit.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_credit_limit_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.dept_code_id.dept_name),TD(n.credit_limit_amount),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return dict(form = form, table = table)

def validate_customer_credit_limit(form):
    form.vars.customer_id = request.args(0)

@auth.requires_login()
def customer_credit_limit_edit_form():
    _id = db(db.Customer_Credit_Limit.id == request.args(0)).select().first()
    form = SQLFORM(db.Customer_Credit_Limit, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('customer_credit_limit_add_form', args = _id.customer_id))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def customer_bank_details():
    form = SQLFORM(db.Customer_Bank_Detail)
    if form.process(onvalidation = validate_customer_bank_details).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    head = THEAD(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Action')))
    for n in db(db.Customer_Bank_Detail.customer_id == request.args(0)).select(db.Customer_Bank_Detail.ALL, orderby = db.Customer_Bank_Detail.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_bank_details_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),TD(n.swift_code),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

def validate_customer_bank_details(form):
    form.vars.customer_id = request.args(0)
    
@auth.requires_login()
def customer_bank_details_edit_form():
    _id = db(db.Customer_Bank_Detail.id == request.args(0)).select().first()
    form = SQLFORM(db.Customer_Bank_Detail, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('customer_bank_details', args = _id.customer_id))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'    
    return dict(form = form)

@auth.requires_login()
def view_customer_details():
    return dict()


def view_customer_info():
    _id = db(db.Customer.id == request.args(0)).select().first()
    if _id:
        _body_1 = TBODY(
            TR(TD('Account No'),TD('Group Code'),TD('Customer Name'),TD('Category'),TD('Type'),_class='active'),
            TR(TD(_id.customer_account_no),TD(_id.customer_group_code_id),TD(_id.customer_name),TD(_id.customer_category_id),TD(_id.customer_account_type)))
        _table_1 = TABLE(*[_body_1],_class='table table-bordered')

        _body_2 = TBODY(
            TR(TD('PO Box No.'),TD('Unit No.'),TD('Building No.'),TD('Street No.'),TD('Zone'),TD('Telephone No.'),TD('Fax No.'),TD('Email Address'),_class='active'),
            TR(TD(_id.po_box_no),TD(_id.unit_no),TD(_id.building_no),TD(_id.street_no),TD(_id.zone),TD(_id.telephone_no),TD(_id.fax_no),TD(_id.email_address)))
        _table_2 = TABLE(*[_body_2],_class='table table-bordered')

        _body_3 = TBODY(
            TR(TD('Area Name.'),TD('State'),TD('Country'),TD('Sponsor Name'),TD('Status'),_class='active'),
            TR(TD(_id.po_box_no),TD(_id.unit_no),TD(_id.building_no),TD(_id.street_no),TD(_id.zone)))
        _table_3 = TABLE(*[_body_3],_class='table table-bordered')

        return DIV(_table_1, _table_2, _table_3)    
    else:
        return CENTER(DIV(B('INFO! '),'No customer record.',_class='alert alert-info',_role='alert'))

def view_contact():
    _id = db(db.Customer_Contact_Person.customer_id == request.args(0)).select()
    if _id:
        row = []
        ctr = 0
        _head = THEAD(TR(TH('#'),TH('Contact Person'),TH('Contact No.'),TH('Position'),TH('Email Address')))
        for n in _id:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.contact_person),TD(n.contact_number),TD(n.position),TD(n.email_address)))
        _body = TBODY(*row)
        _table = TABLE(*[_head, _body], _class= 'table table-bordered-striped')       
        return DIV(_table)    
    else:
        return CENTER(DIV(B('INFO! '),'No contact person record.',_class='alert alert-info',_role='alert'))

def view_bank():
    _id = db(db.Customer_Bank_Detail.customer_id == request.args(0)).select()
    if _id:
        row = []
        ctr = 0
        head = THEAD(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Bank Address'),TH('City'),TH('Country'),TH('Status')))
        for n in _id:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),TD(n.swift_code),TD(n.bank_address),TD(n.city),TD(n.country_id),TD(n.status_id)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table table-bordered-striped')
        return DIV(table)    
    else:
        return CENTER(DIV(B('INFO! '),'No customer bank detail.',_class='alert alert-info',_role='alert'))

# ----------    SALES ORDER FORM    ----------

@auth.requires_login()
def sales_order_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = 0
    form = SQLFORM.factory(
        Field('sales_order_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('customer_code_id','reference Customer', requires = IS_IN_DB(db, db.Customer.id, '%(customer_account_no)s - %(customer_name)s', zero = 'Choose Customer')),    
        Field('customer_order_reference','string', length = 25),
        Field('delivery_due_date', 'date', default = request.now),
        Field('remarks', 'string'),        
        Field('status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:        
        ctr = db((db.Transaction_Prefix.prefix_key == 'SOR') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        db.Sales_Order.insert(
            transaction_prefix_id = ctr.id,
            sales_order_no = ctr.current_year_serial_key,
            sales_order_date = request.now,
            dept_code_id = form.vars.dept_code_id,
            stock_source_id = form.vars.stock_source_id,
            customer_code_id =  form.vars.customer_code_id,
            customer_order_reference = form.vars.customer_order_reference,
            delivery_due_date = form.vars.delivery_due_date,
            remarks = form.vars.remarks,            
            status_id = form.vars.status_id)
        _id = db(db.Sales_Order.sales_order_no == ctr.current_year_serial_key).select().first()        
        _tmp = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _tmp:
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
            _price_cost = _pric.wholesale_price / _item.uom_value
            _total_qty = (n.quantity * _item.uom_value) + n.pieces
            db.Sales_Order_Transaction.insert(
                sales_order_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = _total_qty,
                uom = _item.uom_value,
                price_cost = _price_cost,
                average_cost = _pric.average_cost,
                # sale_cost = _pric.sale_cost,
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                discount_percentage = n.discount_percentage,
                selective_tax = n.selective_tax)
                # vat_percentage = n.vat_percentage)
            _grand_total += float(_price_cost) * int(_total_qty)
        _discount = session.discount or 0
        _discount = float(_grand_total) * float(_discount) / 100
        _after_discount = float(_grand_total) - float(_discount)
        print _grand_total, _discount, _after_discount
        _id.update_record(total_amount = _grand_total, discount_percentage = _discount, total_amount_after_discount = _after_discount )
        session.discount = 0
        db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'SAVING SALES ORDER NO ' + str(_skey) + '.'    
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id)

def discount_session():
    session.discount = request.vars.discount    

def item_code_description():
    response.js = "$('#btnadd').removeAttr('disabled')"
    response.js = "$('#no_table_pieces').removeAttr('disabled')"    
    response.js = "$('#discount').removeAttr('disabled')"    
    _icode = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    
    if not _icode:
        response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))
    else:        
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
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
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Unit Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(locale.format('%.2F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_balanced)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        
    # if _icode.selectivetax > 0:
    #     response.js = "$('#discount').attr('disabled','disabled')"

def validate_sales_order_transaction(form):        
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    
    if not _id:
        # form.errors._id = CENTER(DIV(B('DANGER! '),'Item code does not exist or empty.',_class='alert alert-danger',_role='alert'))            
        form.errors.item_code = 'Item code does not exist or empty.'
        
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():
        form.errors.item_code =  'Item code does not exist in stock file'
        
        # form.errors.item_code =  CENTER(DIV(B('DANGER! '),'Item code does not exist in stock file',_class='alert alert-danger',_role='alert'))
    # elif request.vars.item_code and request.vars.category_id == 3:
    #     response.flash = 'RECORD ADDED'

    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Order_Transaction_Temporary.item_code == request.vars.item_code)).select(db.Sales_Order_Transaction_Temporary.item_code).first()                                   
        
        if not _price:
            form.errors.item_code = "Item code does'nt have price."
        
        if (_price.retail_price == 0.0 or _price.wholesale_price == 0.0) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.error.item_code = 'Cannot request this item because retail price/wholesale price is zero.'
        
        # if _exist == request.vars.item_code and (request.vars.category_id != 3):
        if _exist:
            if int(request.vars.category_id) != 3:                
                form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'
            
            # form.errors.item_code = CENTER(DIV(B('DANGER! '),'Item code ' + str(_exist.item_code) + ' already exist.',_class='alert alert-danger',_role='alert'))            
        
        # if _exist:
        #     form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'

        if _id.uom_value == 1:
            form.vars.pieces = 0
        
        # if _id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO':
        #     form.errors.category_id = 'This saleable item cannot be transfered as FOC'

        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)
        
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(form.vars.pieces) >= int(_id.uom_value):
            # print 'total ', int(form.vars.pieces), _id.uom_value
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                 
        _unit_price = float(_price.retail_price) / int(_id.uom_value)
        _total = float(_unit_price) * int(_total_pcs)

        if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):
            form.errors.quantity = 'Quantity should not be more than probational balance.'
        
        _stk_file.stock_in_transit += _total_pcs    
        _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
        _stk_file.update_record()

        form.vars.item_code_id = _id.id
        

def sales_order_transaction_temporary():        
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25, requires = IS_NOT_EMPTY(error_message='cannot be empty!')),
        Field('quantity','integer', default = 0, requires = IS_NOT_EMPTY(error_message='cannot be empty!')),
        Field('pieces','integer', default = 0, requires = IS_NOT_EMPTY(error_message='cannot be empty!')),
        Field('discount_percentage', 'decimal(10,2)', default = 0, requires = IS_NOT_EMPTY(error_message='cannot be empty!')),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_order_transaction).accepted:        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'
        _id = db(db.Item_Master.id == form.vars.item_code_id).select().first()
        db.Sales_Order_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            discount_percentage = form.vars.discount_percentage,
            category_id = form.vars.category_id,
            stock_source_id = session.stock_source_id,
            ticket_no_id = session.ticket_no_id)
        if db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled');"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled');"
        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price/Sel.Tax'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Order_Transaction_Temporary.ALL, db.Item_Prices.ALL, 
    orderby = ~db.Sales_Order_Transaction_Temporary.id, 
    left = [
        db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction_Temporary.item_code_id), 
        db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1

        _total_pcs = n.Sales_Order_Transaction_Temporary.quantity * n.Item_Master.uom_value + n.Sales_Order_Transaction_Temporary.pieces

        _excise_tax_amount = float(float(n.Item_Prices.retail_price) * float(n.Item_Master.selectivetax or 0) / 100)

        _excise_tax_price_per_piece = _excise_tax_amount / n.Item_Master.uom_value
        _total_excise_tax += _excise_tax_price_per_piece * _total_pcs
        
        if _total_excise_tax > 0:
            session.discount = 0
            response.js = "$('#discount').val(0)"
            response.js = "$('#discount').attr('disabled','disabled')"

        _unit_price = float(n.Item_Prices.wholesale_price) + _excise_tax_amount
        _price_per_piece = _unit_price / n.Item_Master.uom_value
        _total_amount = _total_pcs * _price_per_piece        
        grand_total += float(_total_amount)
        # _grand_total = grand_total
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Sales_Order_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Sales_Order_Transaction_Temporary.id),'_data-qt':(n.Sales_Order_Transaction_Temporary.quantity), '_data-pc':(n.Sales_Order_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Sales_Order_Transaction_Temporary.id), **{'_data-id':(n.Sales_Order_Transaction_Temporary.id)})
        btn_lnk = DIV(edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction_Temporary.category_id.mnemonic),
            TD(n.Item_Master.uom_value),
            TD(n.Sales_Order_Transaction_Temporary.quantity),
            TD(n.Sales_Order_Transaction_Temporary.pieces),
            TD(locale.format('%.2F',_unit_price or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            # TD(n.Sales_Order_Transaction_Temporary.taxable_value, _align = 'right'),
            # TD(n.Sales_Order_Transaction_Temporary.tax_percentage, _align = 'right'),
            # TD(n.Sales_Order_Transaction_Temporary.tax_amount, _align = 'right'),
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right', _style="width:120px;"),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_total_excise_tax or 0, grouping = True)) ,_colspan = '2'),TD(H4('TOTAL AMOUNT'), _align = 'right', _colspan = '5'),TD(H4(INPUT(_class='form-control', _name = 'grand_total', _id='grand_total', _disabled = True, _value = locale.format('%.2F',grand_total or 0, grouping = True))), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(H4('DISCOUNT %'), _align = 'right', _colspan = '8'),TD(H4(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right')),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')
    return dict(form = form, table = table, grand = grand_total)


def generate_total_amount(item, qty, pcs):
    _i = db(db.Item_Master.id == item).select().first()
    _p = db(db.Item_Prices.item_code_id == _i.id).select().first()
   
    _pcs = qty * _i.uom_value + pcs  
    
    _excise_tax_amount = float(float(_p.retail_price) * float(_i.selectivetax or 0) / 100)
    
    _excise_tax_price_per_piece = _excise_tax_amount / _i.uom_value
    _total_excise_tax = _excise_tax_price_per_piece * _pcs

    _unit_price = float(_p.wholesale_price) + _excise_tax_amount
    _price_per_piece = _unit_price /  _i.uom_value
    _total_amount = _pcs * _price_per_piece
    # _tamount = float(_uprice) * int(_pcs)    
    print 'excise tax ', _excise_tax_amount, _unit_price, _total_amount
    return _unit_price

def generate_total_amount_(qty, pcs, uom, price ):
    _pcs = qty * uom + pcs
    _uprice = float(price) / int(uom)
    _tamount = float(_uprice) * int(_pcs)
    return _tamount

def sales_order_transaction_temporary_edit():
    print 'request ', request.args(0), request.args(1), request.args(2)

@auth.requires_login()
def sales_order_transaction_temporary_edit_():
    _id = db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).select().first()
    _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _total_pcs = _qty * _im.uom_value + _pcs
    if _total_pcs >= _im.uom_values:
        response.flash = 'QUANTITY HAS ERROR'
    else:
        _amount = float(_id.price_cost) * int(_total_pcs)
        _id.update_record(quantity = _qty, pieces = _pcs)
        response.js = "$('#tblso').get(0).reload()"
    
@auth.requires_login()
def sales_order_transaction_temporary_delete():
    db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).delete()    
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblsot').get(0).reload()"

@auth.requires_login()
def sales_order_browse():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')))
    for n in db((db.Sales_Order.created_by == auth.user.id) & ((db.Sales_Order.archives != True) | (db.Sales_Order.status_id != 9) | (db.Sales_Order.status_id != 10))).select(orderby = ~db.Sales_Order.id):  
        if n.status_id == 7:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False))            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        btn_lnk = DIV(view_lnk, clea_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary', _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning', _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger', _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(TD(n.sales_order_date),TD(_sales),TD(_note),TD(_inv),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
            TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def sales_order_view():    
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.sales_man_id.writable = False    
    db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 4
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount'),TH('Action')))
    _query = db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, db.Sales_Order.ALL,
    orderby = ~db.Sales_Order_Transaction.id, 
    left = [
        db.Sales_Order.on(db.Sales_Order.id == db.Sales_Order_Transaction.sales_order_no_id),
        db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), 
        db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        if (n.Sales_Order.status_id == 7) | (n.Sales_Order.status_id == 8) | (n.Sales_Order.status_id == 9):        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)           
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_edit_view', args = n.Sales_Order_Transaction.id))            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id),  **{'_data-id':(n.Sales_Order_Transaction.id)})            
        btn_lnk = DIV(edit_lnk, dele_lnk)        
        row.append(TR(TD(ctr),TD(n.Sales_Order_Transaction.item_code_id.item_code),TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),TD(n.Sales_Order_Transaction.uom),TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),            
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right'),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table table-striped', _id = 'tblsot')
    return dict(form = form, table = table, _id = _id) 

def sales_order_transaction_permanent():    
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),        
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(10,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_order_transaction).accepted:        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'
        db.Sales_Order_Transaction.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            discount_percentage = form.vars.discount_percentage,
            category_id = form.vars.category_id,
            stock_source_id = form.vars.stock_source_id)
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount'),TH('Action')))
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, 
    orderby = ~db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))            
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)
        
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),            
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),                     
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table table-striped', _id = 'tblsot')
    return dict(form = form, table = table)

@auth.requires_login()
def sales_order_edit_view():
    _id = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()
    _so = db(db.Sales_Order.id == _id.sales_order_no_id).select().first()
    _sf = db(db.Stock_File.item_code_id == _id.id).select().first()
    _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom
    _total = 0
    form = SQLFORM.factory(
        Field('quantity', 'integer', default = _qty),
        Field('pieces', 'integer', default = _pcs))
    if form.process(onvalidation = validate_stock_in_transit).accepted:
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id)
        for n in db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False)).select():
            _total += int(n.quantity) * float(n.price_cost)
        _so.update_record(total_amount = _total)
        _nsit = _sf.stock_in_transit + _qty
        _sf.update_record(stock_in_transit = _nsit)
        session.flash = 'RECORD UPDATED'
        redirect(URL('sales_order_view', args = _so.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('sales_order_view', args = _so.id))
    return dict(form = form, btn_back = btn_back)

def validate_stock_in_transit(form):
    
    _id = db(db.Sales_Order_Transaction.id == request.args(0)).select().first() # from sales order transaction table
    _im = db(db.Item_Master.id == _id.item_code_id).select().first() # Item master table
    _so = db(db.Sales_Order.id == _id.sales_order_no_id).select().first() # from sales order  table
    _sf = db(db.Stock_File.item_code_id == _id.item_code_id).select().first() # from stock file table

    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    
    if _qty >= _sf.closing_stock:        
        form.errors.quantity = 'Total quantity should not be more than the stock file. '

    form.vars.quantity = _qty
    _old_stock_in_transit = _sf.stock_in_transit - _id.quantity
    _old_probational_balance = _sf.closing_stock - _old_stock_in_transit
    _sf.update_record(stock_in_transit = _old_stock_in_transit)

def sales_order_cancelled_view():
    # initialization of variable
    _st = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()    
    _so = db(db.Sales_Order.id == _st.sales_order_no_id).select().first()
    _sf = db((db.Stock_File.item_code_id == _st.item_code_id) & (db.Stock_File.location_code_id == _so.stock_source_id)).select().first()        
    # update the stock file table
    _sf.stock_in_transit -= _st.quantity
    _sf.probational_balance = _sf.closing_stock - _sf.stock_in_transit
    _sf.update_record()    
    # update the sales order table
    _so.update_record(status_id = 10)
    redirect(URL('sales_order_browse'))

@auth.requires_login()
def sales_order_delete_view():
    # initialization of variable
    _st = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()    
    _so = db(db.Sales_Order.id == _st.sales_order_no_id).select().first()
    _sf = db((db.Stock_File.item_code_id == _st.item_code_id) & (db.Stock_File.location_code_id == _so.stock_source_id)).select().first()    
    # update the stock file table
    _sf.stock_in_transit -= _st.quantity
    _sf.probational_balance = _sf.closing_stock - _sf.stock_in_transit
    _sf.update_record()
    # generate computation in sales order transaction table
    _total = 0
    for n in db((db.Sales_Order_Transaction.id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select():
        _total += int(n.quantity) * float(n.price_cost)
    _total_amount = float(_so.total_amount) - float(_total)        
    # update the sales order table
    _so.update_record(total_amount = _total_amount)        
    # update the sales order transaction table
    _st.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)    
    # response.flash = 'RECORD DELETED'

@auth.requires_login()
def sales_order_archived():
    return locals()
# ----------  M A N A G E R ' S   G R I D   ----------
@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ACCOUNT USERS') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def sales_order_manager_grid():
    _query = db(db.Sales_Order).select(orderby = ~db.Sales_Order.id)
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _query = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.archives == False)).select(orderby = ~db.Sales_Order.id)    
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _query = db((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 8)).select(orderby = ~db.Sales_Order.id)
    elif auth.has_membership(role = 'ACCOUNT USERS'):
        _query = db((db.Sales_Order.status_id == 8) | (db.Sales_Order.status_id == 7)).select(orderby = ~db.Sales_Order.id)

    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')))
    for n in _query:        
        edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_manager_view', args = n.id, extension = False))        
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')  
        appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                   
        if n.status_id == 4:
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_manager_view', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_approved', args = n.id, extension = False))            
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                   
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')  
        elif n.status_id == 9:
            if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_store_keeper_view', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sale_order_manager_delivery_note_approved', args = n.id, extension = False))                            
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_rejected', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_report_store_keeper', args = n.id, extension = False))  
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')       
            else:
                appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
                reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                   
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle')                  
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')          
        
        elif n.status_id == 8:
            if auth.has_membership(role = 'ACCOUNT USERS'):
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view_account_user', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sale_order_manager_invoice_no_approved', args = n.id, extension = False))                            
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sale_order_manager_invoice_no_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')  
        elif n.status_id == 7:
            if auth.has_membership(role = 'ACCOUNT USERS'):
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view_account_user', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
                reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                   
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_report_account_user', args = n.id, extension = False))  
            # else:
            #     appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
            #     reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                   
            #     clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
            #     prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_store_keeper_view', args = n.id, extension = False))  

            # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', _id = 'del', callback = URL('#', args = n.id, extension = False))            
        else:            
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_manager_view', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
            reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                   
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')  
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            

        
        btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)  
        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary', _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note,  _class='text-warning', _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger', _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(TD(n.sales_order_date),TD(_sales),TD(_note),TD(_inv),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
            TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblso')
    return dict(table = table)

def sales_info(e = request.args(0)):
    for n in db(db.Sales_Order.id == e).select():
        if not n.sales_order_date_approved:
            _date = 'None'
            _appr = 'None'
        else:
            _date = n.sales_order_date_approved
            _appr = str(n.sales_order_approved_by.first_name.upper()) + ' ' + str(n.sales_order_approved_by.last_name.upper())
        i = TABLE(*[
            TR(TD('Date Approved: '),TD(_date, _align = 'right')),
            TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def delivery_info(e = request.args(0)):
    for n in db(db.Sales_Order.id == e).select():
        if not n.delivery_note_date_approved:
            _date = 'None'
            _appr = 'None'
        else:
            _date = n.delivery_note_date_approved
            _appr = str(n.delivery_note_approved_by.first_name.upper()) + ' ' + str(n.delivery_note_approved_by.last_name.upper())
        i = TABLE(*[
            TR(TD('Date Approved: '),TD(_date, _align = 'right')),
            TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def invoice_info(e = request.args(0)):
    for n in db(db.Sales_Order.id == e).select():
        if not n.sales_invoice_date_approved:
            _date = 'None'
            _appr = 'None'
        else:
            _date = n.sales_invoice_date_approved
            _appr = str(n.sales_invoice_approved_by.first_name.upper()) + ' ' + str(n.sales_invoice_approved_by.last_name.upper())
        i = TABLE(*[
            TR(TD('Date Approved: '),TD(_date, _align = 'right')),
            TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def sales_order_view_account_user():
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.sales_man_id.writable = False    
    db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 7) | (db.Stock_Status.id == 8)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 8
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory', 'str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount')))
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, 
    orderby = ~db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))            
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)
        
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),            
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),                     
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')
    return dict(form = form, table = table, _id = _id)

def validate_mngr_approved(form):
    form.vars.sales_order_date_approved = request.now
    form.vars.sales_order_approved_by = auth.user_id

def sales_order_store_keeper_view():
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.sales_man_id.writable = False    
    db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)| (db.Stock_Status.id == 9)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 9
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process(onvalidation = validate_mngr_approved).accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory', 'str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount')))
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, 
    orderby = ~db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))            
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)
        
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),            
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),                     
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')
    return dict(form = form, table = table, _id = _id)

def sales_order_transaction_table():
    ctr = 0
    row = []                
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price/Sel.Tax'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    for n in db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select(orderby = ~db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1
        _im = db(db.Item_Master.id == n.Sales_Order_Transaction.item_code_id).select().first()
        _ip = db(db.Item_Prices.item_code_id == n.Sales_Order_Transaction.item_code_id).select().first()
        _excise_tax_amount = float(_ip.retail_price) * float(_im.selectivetax or 0) / 100
        _excise_tax_price_per_piece = float(_excise_tax_amount) / int(n.Sales_Order_Transaction.uom)
        _total_excise_tax +=  float(_excise_tax_price_per_piece) * int(n.Sales_Order_Transaction.quantity)
        _total_amount = int(n.Sales_Order_Transaction.quantity) * float(n.Sales_Order_Transaction.price_cost)
        _grand_total += float(_total_amount)        
        _discount = float(_grand_total) * int(_id.discount_percentage or 0) / 100        
        _grand_total = float(_grand_total) - int(_discount)
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Order_Transaction.category_id.mnemonic, _style = 'width:120px'),
            TD(n.Sales_Order_Transaction.uom, _style = 'width:120px'),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom), _style = 'width:120px'),
            TD(locale.format('%.6F',n.Sales_Order_Transaction.price_cost or 0, grouping = True), _align = 'right', _style = 'width:140px'),            
            TD(locale.format('%.6F',_total_amount or 0, grouping = True), _align = 'right', _style = 'width:140px'),
            TD()))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(H4('TOTAL SELECTIVE TAX: ',locale.format('%.2F',_total_excise_tax or 0, grouping = True)) ,_colspan = '2'),TD(H4('TOTAL AMOUNT'), _align = 'right', _colspan = '4'),TD(H4(locale.format('%.2F',_grand_total or 0, grouping = True)), _align = 'right', _style="width:120px;"),TD()))
    foot += TFOOT(TR(TD(H4('DISCOUNT %'), _align = 'right', _colspan = '7'),TD(H4(locale.format('%d',_id.discount_percentage or 0, grouping = True), _align = 'right')),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')
    return dict(table = table)        

def sales_order_manager_view():
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.sales_man_id.writable = False    
    db.Sales_Order.status_id.writable = False    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process(onvalidation = validate_mngr_approved).accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory', 'mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount')))
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, 
    orderby = ~db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))            
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)
        
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),            
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),                     
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')
    return dict(form = form, table = table, _id = _id)

def sales_order_manager_approved_form():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 9, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)
    session.flash = 'SALES ORDER APPROVED'
    response.js = "$('#tblso').get(0).reload()"

def sales_order_manager_rejected_form():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)
    session.flash = 'SALES ORDER REJECTED'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_delivery_note_approved_form():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'DLV')).select().first()    
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
    _id.update_record(status_id = 8, delivery_note_no_prefix_id = _trns_pfx.id, delivery_note_no = _skey, delivery_note_approved_by = auth.user_id, delivery_note_date_approved = request.now,)    
    session.flash = 'DELIVERY NOTE APPROVED'
    

def sales_order_manager_approved():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 9, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)
    session.flash = 'SALES ORDER APPROVED'
    response.js = "$('#tblso').get(0).reload()"

def sales_order_manager_rejected():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)
    session.flash = 'SALES ORDER REJECTED'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_delivery_note_approved():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'DLV')).select().first()    
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
    _id.update_record(status_id = 8, delivery_note_no_prefix_id = _trns_pfx.id, delivery_note_no = _skey, delivery_note_approved_by = auth.user_id, delivery_note_date_approved = request.now,)    
    session.flash = 'DELIVERY NOTE APPROVED'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_delivery_note_rejected():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, delivery_note_date_approved = request.now, delivery_note_approved_by = auth.user_id)
    session.flash = 'DELIVERY NOTE REJECTED'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_invoice_no_approved():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'INV')).select().first()        
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
    _id.update_record(status_id = 7, sales_invoice_no_prefix_id = _trns_pfx.id, sales_invoice_no = _skey, sales_invoice_approved_by = auth.user_id, sales_invoice_date_approved = request.now,)    
    session.flash = 'SALES INVOICE APPROVED'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_invoice_no_rejected():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, delivery_note_date_approved = request.now, delivery_note_approved_by = auth.user_id)
    session.flash = 'SALES INVOICE REJECTED'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_invoice_no_form_approved():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'INV')).select().first()        
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
    _id.update_record(status_id = 7, sales_invoice_no_prefix_id = _trns_pfx.id, sales_invoice_no = _skey, sales_invoice_approved_by = auth.user_id, sales_invoice_date_approved = request.now,)    

# ----------    S E T T I N G S  F O R M    ----------
@auth.requires_login()
def sales_man_grid():
    form = SQLFORM(db.Sales_Man)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'    
    return dict(form = form)

# ----------    AUTOGENERATE FORM    ----------
def customer_address():    
    _c = db(db.Customer.id == request.vars.customer_code_id).select().first()    
    return XML(DIV(DIV('Building No. ', _c.building_no),DIV('Street No. ', _c.street_no), _class="well well-sm"))

def generate_sales_order_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SOR')).select().first()    
    _serial = _trans_prfx.current_year_serial_key + 1
    _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
    return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True))



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


def sales_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = request.vars.stock_source_id


# -----------------     R  E  P  O  R  T  S     -----------------

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


MaxWidth_Content = 530
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
# styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle(
    name='BodyText',
    fontSize=7,
)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20)#, showBoundary=1)
logo_path = request.folder + 'static/images/Merch.jpg'
img = Image(logo_path)
img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'


merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])

def sales_order_store_keeper_header_footer_report(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([[img]], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .1 * inch)


    # Footer
    # today = date.today()
    
    footer = Table([
        # ['Received by:','Delivered by:'],
        # ['',''],
        [merch,''],['',today.strftime("%A %d. %B %Y, %I:%M%p ")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('FONTSIZE',(0,0),(-1,1),8),
        ('FONTSIZE',(1,1),(1,1),8),
        # ('ALIGN',(0,0),(-1,1),'CENTER'),
        ('ALIGN',(1,1),(1,1),'RIGHT'),
        ('LINEABOVE',(0,1),(1,1),0.25, colors.black)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def sales_order_report_store_keeper():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _so = [
            ['SALES ORDER'],
            ['SALES ORDER NO:', str(n.transaction_prefix_id.prefix)+str(n.sales_order_no), 'DATE:',n.sales_order_date.strftime('%d-%m-%Y'), 'DUE DATE:', n.delivery_due_date],
            ['Department:', n.dept_code_id.dept_name,'Location Source:',n.stock_source_id.location_name,'Sales Man:', str(n.created_by.first_name.upper()+' '+str(n.created_by.last_name.upper()))],
            ['Customer: ', str(n.customer_code_id.customer_name.upper()), 'Order Reference:',n.customer_order_reference.upper(),'Status: ',n.status_id.description ],
            ['Remarks:']]
    _so_tbl = Table(_so, colWidths=['*'])
    _so_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(5,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTSIZE',(0,0),(0,0),12),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('BACKGROUND',(0,1),(-1,1),colors.gray),
        ('FONTSIZE',(0,1),(-1,1),9),
        ('FONTSIZE',(0,2),(5,-1),8),
        ]))
    ctr = 0
    _st = [['#','ITEM CODE','ITEM DESCRIPTION','CAT','UOM','QTY','UNIT PRICE']]
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1
        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)
        _st.append([ctr,t.Item_Master.item_code, t.Item_Master.item_description, t.Sales_Order_Transaction.category_id.mnemonic, t.Sales_Order_Transaction.uom, _qty, locale.format('%.2F',t.Sales_Order_Transaction.price_cost or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[25,80,'*',50,50,50,70])
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('BACKGROUND',(0,0),(-1,0), colors.gray),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(6,-1),'RIGHT'),
    ]))
    row.append(_so_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_st_tbl)

    doc.build(row, onFirstPage=sales_order_store_keeper_header_footer_report, onLaterPages = sales_order_store_keeper_header_footer_report)

    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data
    

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def sales_order_report_account_user():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _so = [
            ['SALES INVOICE'],
            ['SALES INVOICE:', str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no), 'DATE:',n.sales_invoice_date_approved.strftime('%d-%m-%Y'), '', ''],
            ['DELIVERY NOTE NO:', str(n.delivery_note_no_prefix_id.prefix)+str(n.delivery_note_no), 'DATE:',n.delivery_note_date_approved.strftime('%d-%m-%Y'), '', ''],
            ['SALES ORDER NO:', str(n.transaction_prefix_id.prefix)+str(n.sales_order_no), 'DATE:',n.sales_order_date.strftime('%d-%m-%Y'), 'DUE DATE:', n.delivery_due_date.strftime('%d-%m-%Y')],
            ['Department:', n.dept_code_id.dept_name,'Location Source:',n.stock_source_id.location_name,'Sales Man:', str(n.created_by.first_name.upper()+' '+str(n.created_by.last_name.upper()))],
            ['Customer: ', str(n.customer_code_id.customer_name.upper()), 'Order Reference:',n.customer_order_reference.upper(),'Status: ',n.status_id.description ],
            ['Remarks:']]
    _so_tbl = Table(_so, colWidths=['*'])
    _so_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(5,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTSIZE',(0,0),(0,0),12),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('BACKGROUND',(0,1),(-1,1),colors.gray),
        ('FONTSIZE',(0,1),(-1,1),9),
        ('FONTSIZE',(0,2),(5,-1),8),
        ]))
    ctr = 0
    _st = [['#','ITEM CODE','ITEM DESCRIPTION','CAT','UOM','QTY','UNIT PRICE','AMOUNT']]
    
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0    
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1
        
        _im = db(db.Item_Master.id == t.Sales_Order_Transaction.item_code_id).select().first()
        _ip = db(db.Item_Prices.item_code_id == t.Sales_Order_Transaction.item_code_id).select().first()
        _excise_tax_amount = float(_ip.retail_price) * float(_im.selectivetax or 0) / 100
        _excise_tax_price_per_piece = float(_excise_tax_amount) / int(t.Sales_Order_Transaction.uom)
        _total_excise_tax +=  float(_excise_tax_price_per_piece) * int(t.Sales_Order_Transaction.quantity)
        _total_amount = int(t.Sales_Order_Transaction.quantity) * float(t.Sales_Order_Transaction.price_cost)
        _grand_total += float(_total_amount)        
        _discount = float(_grand_total) * int(_id.discount_percentage or 0) / 100        
        _grand_total = float(_grand_total) - int(_discount)

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)
        _st.append([ctr,t.Item_Master.item_code, t.Item_Master.item_description, t.Sales_Order_Transaction.category_id.mnemonic, t.Sales_Order_Transaction.uom, _qty, locale.format('%.4F',t.Sales_Order_Transaction.price_cost or 0, grouping = True), locale.format('%.2F', _total_amount or 0, grouping = True)])
    _st.append(['','','','','','','DISCOUNT %:',locale.format('%d',_id.discount_percentage or 0, grouping = True)])
    _st.append(['','TOTAL SELECTIVE TAX: '+ str(locale.format('%.2F',_total_excise_tax or 0, grouping = True)),'','','','','TOTAL AMOUNT:',locale.format('%.2F',_grand_total or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[20,70,'*',30,30,60,70,70])
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('BACKGROUND',(0,0),(-1,0), colors.gray),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('LINEABOVE', (0,-2), (-1,-2), .5, colors.black),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
    ]))
    row.append(_so_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_st_tbl)

    doc.build(row, onFirstPage=sales_order_store_keeper_header_footer_report, onLaterPages = sales_order_store_keeper_header_footer_report)

    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data
    

