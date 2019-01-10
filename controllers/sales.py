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
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_n_sale_status_edit_form', args = n.id))
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
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_n_sale_status_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login()
def customer_group_code_edit_form():
    form = SQLFORM(db.Customer_Group_Code)
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
    db.Sales_Order.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    db.Sales_Order.status_id.default = 4
    ctr = db(db.Transaction_Prefix.prefix_key == 'SOR').select().first()
    _skey = ctr.current_year_serial_key
    _skey += 1
    form = SQLFORM(db.Sales_Order)
    if form.process().accepted:
        response.flash = 'SAVING SALES ORDER NO ' + str(_skey) + '.'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = id_generator())

def validate_sales_order_form():

    return locals()

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
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Sel. Tax'),TH('Taxable Value'),TH('Tax %'),TH('Tax Amount'),TH('Total Amount'),TH('Action')))
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
                TD(n.Sales_Order_Transaction_Temporary.selective_tax, _align = 'right'),
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

    if not _id:
        form.errors._id = CENTER(DIV(B('DANGER! '),'Item code does not exist',_class='alert alert-danger',_role='alert'))            
    else:
        _sfile = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()    
        _exist = db((db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id) & (db.Sales_Order_Transaction_Temporary.item_code == request.vars.item_code)).select(db.Sales_Order_Transaction_Temporary.item_code).first()        
        
        if not _sfile:
            form.errors._stk_file =  CENTER(DIV(B('DANGER! '),'Item code does not exist in stock file',_class='alert alert-danger',_role='alert'))
        
        if _exist:
            form.errors.item_code = CENTER(DIV(B('DANGER! '),'Item code ' + str(_exist.item_code) + ' already exist.',_class='alert alert-danger',_role='alert'))

        if _id.uom_value == 1:
            if form.vars.pieces > 0:
                form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value is not applicable to this item.',_class='alert alert-danger',_role='alert')) 
                form.vars.pieces = 0
        elif form.vars.pieces >= int(_id.uom_value):
            form.errors._id = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert')) 
                
        form.vars.item_code_id = _id.id
        form.vars.taxable_value = 0
        form.vars.tax_percentage = 0
        form.vars.tax_amount = 0


# ----------    AUTOGENERATE FORM    ----------
def generate_sales_order_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SOR')).select().first()    
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
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))

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
