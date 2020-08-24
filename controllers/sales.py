# ------------------------------------------------------------------------------------------
# -------------------------------  S A L E S   S Y S T E M  --------------------------------
# ------------------------------------------------------------------------------------------

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
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action'),_class = 'bg-primary'))
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
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action'), _class = 'bg-primary'))
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
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action'),_class='bg-primary'))
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
def get_area_name_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Area Name'),TH('Zone'),TH('Municipality'),TD('Action')))
    for n in db().select(db.Area_Name.ALL, orderby = db.Area_Name.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('view_customer_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('put_area_name_id', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.area_name),TD(n.zone_no),TD(n.municipality),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(table = table)

@auth.requires_login()
def post_area_name():
    form = SQLFORM(db.Area_Name)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

@auth.requires_login()
def put_area_name_id():
    form = SQLFORM(db.Area_Name, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FOR HAS ERROR'
    return dict(form = form)

@auth.requires_login()
def customer_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Account No.'),TH('Group Code'),TH('Name'),TH('Category'),TH('Type'),TH('Action'),_class='bg-primary'))
    for n in db().select(db.Customer.ALL, orderby = db.Customer.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('view_customer_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_add_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        cont_lnk = A(I(_class='fas fa-user-plus'), _title='Add Contact Person', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_contact_person_add_form', args = n.id))
        cred_lnk = A(I(_class='fas fa-credit-card'), _title='Credit Limit', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_credit_limit_add_form', args = n.id))
        bank_lnk = A(I(_class='fas fa-money-check'), _title='Bank Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('customer_bank_details', args = n.id))
        docu_lnk = A(I(_class='fas fa-upload'), _title='Upload Documents', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_customer_documents_upload_id', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, cont_lnk, cred_lnk,bank_lnk,docu_lnk)
        row.append(TR(TD(n.id),TD(n.customer_account_no),TD(n.customer_group_code_id),TD(n.customer_name),TD(n.customer_category_id),TD(n.customer_account_type.description),TD(btn_lnk)))
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

def get_customer_documents_upload_id():
    db.Customer.customer_account_no.writable = False
    db.Customer.customer_name.writable = False
    db.Customer.parent_outlet.writable = False
    db.Customer.cr_no.writable = False
    db.Customer.po_box_no.writable = False
    db.Customer.unit_no.writable = False
    db.Customer.building_no.writable = False
    db.Customer.street_no.writable = False
    db.Customer.zone.writable = False
    db.Customer.area_name.writable = False
    db.Customer.state.writable = False
    db.Customer.country.writable = False
    db.Customer.telephone_no.writable = False
    db.Customer.mobile_no.writable = False
    db.Customer.fax_no.writable = False
    db.Customer.email_address.writable = False
    db.Customer.contact_person.writable = False
    db.Customer.longtitude.writable = False
    db.Customer.latitude.writable = False
    db.Customer.outlet_category.writable = False
    db.Customer.outlet_type.writable = False
    db.Customer.outlet_classification.writable = False
    db.Customer.sponsor_name.writable = False
    db.Customer.sponsor_contact_no.writable = False
    db.Customer.customer_group_code_id.writable = False
    db.Customer.customer_category_id.writable = False
    db.Customer.customer_account_type.writable = False
    db.Customer.department_id.writable = False
    db.Customer.area_name_id.writable = False
    db.Customer.status_id.writable = False   
    form = SQLFORM(db.Customer, request.args(0), upload=URL('download'))
    if form.process().accepted:
        response.flash = 'FORM UPLOADED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
        # print form.errors
    return dict(form = form)

def get_customer_documents_upload_id_():
    _id = db(db.Customer.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('cr_license','upload',requires=IS_UPLOAD_FILENAME(extension='pdf'),upload=URL('default','download')))
        # Field('guarantee','upload',requires=IS_UPLOAD_FILENAME(extension='pdf'),upload=URL('download')),    
        # Field('customer_form','upload',requires=IS_UPLOAD_FILENAME(extension='pdf'),upload=URL('download')),    
        # Field('sponsor_id','upload',requires=IS_UPLOAD_FILENAME(extension='pdf'),upload=URL('download')))
    if form.process().accepted:
        response.flash = 'DOCUMENTS UPLOADED'
        _id.update_record(
            cr_license = form.vars.cr_license,
            guarantee = form.vars.guarantee,
            customer_form = form.vars.customer_form,
            sponsor_id = form.vars.sponsor_id)            
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

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

@auth.requires_login()
def customer_documents():
    return dict()
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

@auth.requires_login()
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

@auth.requires_login()
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

@auth.requires_login()
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

def view_documents():
    _id = db(db.Customer.id == request.args(0)).select().first()
    row = []
    # form = SQLFORM(db.Customer, request.args(0), upload=URL('default','download'))
    if _id:
        cr_license = A(I(_class='fa fa-id-card'),_target='blank',_title='CR License', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('default','download', args = _id.cr_license)) if _id.cr_license else ""
        guarantee = A(I(_class='fa fa-id-card'),_target='blank',_title='Guarantee', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('default','download', args = _id.guarantee)) if _id.guarantee else ""
        customer_form = A(I(_class='fa fa-id-card'),_target='blank',_title='Customer Form', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('default','download', args = _id.customer_form)) if _id.customer_form else ""
        sponsor_id = A(I(_class='fa fa-id-card'),_target='blank',_title='Sponsor', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('default','download', args = _id.sponsor_id)) if _id.sponsor_id else ""
        body = TBODY(TR(TH('CR License'),TH('Guarantee'),TH('Customer Form'),TH('Sponsor'),_class='active'),        
        TR(TD(cr_license),TD(guarantee),TD(customer_form),TD(sponsor_id)))
        table = TABLE(*[body],_class='table table-bordered')
        return DIV(table)
    else:
        return CENTER(DIV(B('INFO! '),'Empty document uploaded',_class='alert alert-info',_role='alert'))
# ----------    SALES MAN FORM    ----------
@auth.requires_login()
def get_sales_man_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Name'),TH('Van Sales'),TH('Section'),TH('Status'),TH('Action')))
    for n in db(db.Sales_Man.status_id == 1).select():
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','put_sales_man_id', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('sales','put_sales_man_id', args = n.id)))         
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.employee_id.title,n.employee_id.first_name,' ',n.employee_id.middle_name,' ',n.employee_id.last_name,', ',n.mv_code),TD(n.van_sales),TD(n.section_id),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head,body],_class='table')
    return dict(table=table)

@auth.requires_login()
def post_sales_man():
    form = SQLFORM(db.Sales_Man)
    # form = SQLFORM.factory(db.Sales_Man)
    if form.process().accepted:
        response.flash = 'FORM SAVE'        
        # db.Sales_Man.insert(
        #     users_id = form.vars.users_id,
        #     employee_id = form.vars.employee_id,
        #     mv_code = form.vars.mv_code,
        #     van_sales = form.vars.van_sales,
        #     status_id = form.vars.status_id
        # )
        _id = db(db.Sales_Man.users_id == request.vars.users_id).select().first()
        if db(db.Sales_Man_Customer.users_id == form.vars.users_id).select().first():
            db(db.Sales_Man_Customer.users_id == form.vars.users_id).update(sales_man_id = _id.id)
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

@auth.requires_login()
def put_sales_man_id():
    form = SQLFORM(db.Sales_Man, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def get_user_id():
    session.users_id = request.vars.users_id    
    print 'get_user_id',session.users_id

def validate_sales_man_customer_id(form):
    _id = db(db.Sales_Man.id == request.args(0)).select().first()
    if _id:
        form.vars.users_id = _id.users_id
        form.vars.sales_man_id = _id.id        
    else:        
        form.vars.users_id = request.vars.users_id
        # form.vars.sales_man_id = _id.id
    # form.vars.users_id = session.users_id

def validate_sales_man(form):
    _id = db(db.Sales_Man.id == form.vars.sales_man_id).select().first()
    form.vars.users_id = _id.users_id

@auth.requires_login()
def get_sales_man_customer_grid():
    form = SQLFORM(db.Sales_Man_Customer)
    if form.process(onvalidation = validate_sales_man).accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Sales Man'),TH('Account Type'),TH('Status'),TH('Action')))
    for n in db(db.Sales_Man_Customer).select():
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        edit_lnk = A(I(_class='fa fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled') 
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback= URL('put_sales_man_customer_delete_id',args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.sales_man_id.employee_id.first_name,' ',n.sales_man_id.employee_id.last_name),TD(n.master_account_type_id),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')    
    return dict(form = form, table = table)

@auth.requires_login()
def get_sales_man_customer_id():    
    row = []
    ctr = 0
    _id = db(db.Sales_Man_Customer.sales_man_id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Man_Customer)
    if form.process(onvalidation = validate_sales_man_customer_id).accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:        
        response.flash = 'FORM HAS ERRRO'

    head = THEAD(TR(TH('#'),TH('Group Account'),TH('Status'),TH('Action')))
    for n in db(db.Sales_Man_Customer.sales_man_id == request.args(0)).select():
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        edit_lnk = A(I(_class='fa fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled') 
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback= URL('put_sales_man_customer_delete_id',args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.master_account_type_id),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')    
    return dict(form = form, table = table)

def put_sales_man_customer_delete_id():    
    db(db.Sales_Man_Customer.id == request.args(0)).delete()

# ----------    SALES ORDER FORM    ----------
@auth.requires_login()
def sales_order_form_testing():        
    # _query = db(db.Department.id == 1).select(db.Department.ALL, left = db.Department.on(db.Department.dept_name == db.Department_Group.department_group_name)).first()
    _query = db.Department.id != 1
    form = SQLFORM.factory(        
        Field('dept_code_id','reference Department', requires = IS_IN_DB(db(_query), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')))
    if form.process().accepted: 
        response.flash = 'ok'
    elif form.errors:
        response.flash = 'not ok'
    return dict(form = form)

@auth.requires_login()
def sales_order_form():    
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if auth.has_membership('SALES'):
        if _usr.van_sales == True: # Van sales => limited customer
            _query_dept = db.Department.id == 3
            _defa_dept = 3
            _query_cstmr = db.Master_Account.account_code == _usr.mv_code 
            _default = db(db.Master_Account.account_code == _usr.mv_code).select(db.Master_Account.id).first()        
        else: # Sales Man => Customer, Staff, Accounts Only
            _query_cstmr = (db.Sales_Man_Customer.sales_man_id == _usr.id) & (db.Sales_Man_Customer.master_account_type_id == db.Master_Account.master_account_type_id)
            _query_dept = db.Department.id == 3
            _defa_dept = 3
            _default = 0
    elif auth.has_membership('INVENTORY BACK OFFICE'):
        _query_dept = db.Department.id ==3
        _query_cstmr = db.Master_Account            
        _default = 0
    elif auth.has_membership('ROOT') | auth.has_membership('ACCOUNTS'): # All in Master Accounts                
        _query_dept = db.Department.id > 0
        _query_cstmr = db.Master_Account            
        _defa_dept = 0
        _default = 0

    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = session.discount = 0
    _total_selective_tax = _total_selective_tax_foc = 0
    form = SQLFORM.factory(
        Field('sales_order_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', requires = IS_IN_DB(db(_query_dept), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', default = 1, requires = IS_IN_DB(db(db.Location.location_group_code_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('customer_code_id','reference Master_Account', default = int(_default), requires = IS_IN_DB(db(_query_cstmr), db.Master_Account.id, '%(account_name)s, %(account_code)s', zero = 'Choose Customer')),    
        Field('customer_order_reference','string', length = 25),
        Field('delivery_due_date', 'date', default = request.now),
        Field('remarks', 'string'),         
        Field('status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:        
        if int(db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).count()) == 0:
            print 'empty'
            session.flash = 'Transactions empty not allowed.'
            redirect(URL('index'))
        else:
            print 'not empty'
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
            discount_added = request.vars.discount_var,
            total_amount_after_discount = request.vars.net_amount_var,
            section_id = _usr.section_id,
            sales_man_id = _usr.id,         
            status_id = form.vars.status_id)
        _id = db(db.Sales_Order.sales_order_no == ctr.current_year_serial_key).select().first()        
        _tmp = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select(orderby = db.Sales_Order_Transaction_Temporary.id)
        for n in _tmp:
            
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        

            db.Sales_Order_Transaction.insert(
                sales_order_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,                
                packet_price_cost = (n.price_cost / _item.uom_value), # converted to pieces
                average_cost = _pric.average_cost,
                sale_cost = (n.net_price / _item.uom_value), # converted to pieces
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                discount_percentage = n.discount_percentage,
                selective_tax = n.selective_tax,
                selective_tax_foc = n.selective_tax_foc,
                packet_selective_tax = (n.selective_tax / _item.uom_value), # converted to pieces
                packet_selective_tax_foc = (n.selective_tax_foc / _item.uom_value), # converted to pieces
                net_price = n.net_price,
                total_amount = n.total_amount)
            _grand_total += n.total_amount
            _total_selective_tax += n.selective_tax or 0
            _total_selective_tax_foc += n.selective_tax_foc 
            # print n.id, _total_selective_tax_foc, n.selective_tax_foc or 0
        _discount = session.discount or 0
        # _discount = float(_grand_total) * float(_discount) / 100
        _after_discount = float(_grand_total) - float(session.discount or 0)
        _trnx = db(db.Sales_Order_Transaction.sales_order_no_id == _id.id).select().first()    
        # if float(session.discount or 0) > 0:
        if _id.discount_added:
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom))- float(_id.discount_added)) / int(_trnx.uom)
            _trnx.update_record(sale_cost = _sale_cost, discounted = True, discount_added = _id.discount_added)
        _after_discount = float(_grand_total) - float(request.vars.discount_var or 0)
        _id.update_record(total_amount = _grand_total,  total_amount_after_discount = _after_discount, total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_selective_tax_foc) # discount_added = _discount,
        db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'SAVING SALES ORDER NO ' + str(_skey) + '.'    
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id)

@auth.requires_login()
def sales_order_form_abort():
    _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select()
    if not _query:
        session.flash = 'ABORT'
    else:        
        for n in _query:
            _id = db(db.Item_Master.id == n.item_code_id).select().first()
            _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select().first()
            _quantity = n.quantity * _id.uom_value + n.pieces            
            _s.stock_in_transit += int(_quantity)                        
            _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)
            _s.update_record()            
            db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).delete()            
        session.flash = 'ABORT'
 
@auth.requires_login()
def discount_session():    
    session.discount = request.vars.discount
    print 'discount_session: ', request.vars.discount
        
@auth.requires_login()
def item_code_description():
    response.js = "$('#btnadd, #no_table_pieces, #discount').removeAttr('disabled')"
    _icode = db(db.Item_Master.item_code == request.vars.item_code).select().first()        
    # _icode = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    
    if not _icode:
        # response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:        
        # response.js = "$('#btnadd').removeAttr('disabled')"
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()          
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()                
        if _sfile:               
            _provational_balanced = int(_sfile.closing_stock) + int(_sfile.stock_in_transit)
            if _icode.uom_value == 1:                
                response.js = "$('#no_table_pieces').attr('disabled','disabled'), $('#btnadd').removeAttr('disabled')"                
                _on_balanced = _provational_balanced
                _on_transit = _sfile.stock_in_transit
                _on_hand = _sfile.closing_stock                      
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_icode.id, _provational_balanced, _icode.uom_value)
                _on_transit = card(_icode.id, _sfile.stock_in_transit, _icode.uom_value)
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt.'),TH('Retail Price'),TH('Unit Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(_iprice.selective_tax_price),
                TD(_iprice.retail_price),
                TD(locale.format('%.2F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_balanced)),_class="bg-info"),_class='table'))            

        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

        
def test():
    for n in db(db.Item_Master.supplier_code_id == 5).select():
        n.update_record(selectivetax = 100)
from decimal import Decimal

@auth.requires_login()
def validate_sales_order_transaction(form):      
    _selective_tax_total = _selective_tax_total_foc = _selective_tax_per_uom = 0    
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    # print 'session', request.vars.item_code, session.stock_source_id
    if not _id:
        # form.errors._id = CENTER(DIV(B('DANGER! '),'Item code does not exist or empty.',_class='alert alert-danger',_role='alert'))            
        form.errors.item_code = 'Item code does not exist or empty.'
        
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():
        form.errors.item_code =  'Item code is zero in stock file'
        
        # form.errors.item_code =  CENTER(DIV(B('DANGER! '),'Item code does not exist in stock file',_class='alert alert-danger',_role='alert'))
    # elif request.vars.item_code and request.vars.category_id == 3:
    #     response.flash = 'RECORD ADDED'

    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Order_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Order_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Order_Transaction_Temporary.item_code).first()                                   

        if _id.uom_value == 1:
            form.vars.pieces = 0

        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces or 0)
        _item_discount = int(request.vars.discount_percentage or 0)
        
        if not _price:
            form.errors.item_code = "Item code does'nt have price."
        
        # if _price.selective_tax_price > 0: # >= request.vars.discount_percentage:
        if int(request.vars.discount_percentage) > 50:
            form.errors.discount_percentage = 'Discount not allowed'
            # form.errors.discount_percentage = 'Discount not allowed. ' 

        if ((_price.retail_price == 0.0 or _price.wholesale_price == 0.0)) and ((_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO')):
            form.errors.item_code = 'Cannot request this item because retail price/wholesale price is zero.'
                
        # if _exist == request.vars.item_code and (request.vars.category_id != 3):
        _excise_tax_amount = 0
        _unit_price = 0
        _total_excise_tax = _net_price = _total_excise_tax_foc = 0
        _selective_tax = _selective_tax_foc = _retail_price_per_uom = 0     
        _total_amount = _tax_per_uom = _wholesale_price_per_uom = 0 
        _retail_price_per_uom = _price.retail_price / _id.uom_value     
        _wholesale_price_per_uom = _price.wholesale_price / _id.uom_value
        # _selective_tax_per_uom = _price.selective_tax_price 
        _selective_tax_per_uom = _price.selective_tax_price / _id.uom_value


        if _price.selective_tax_price > 0:                        
            _tax_per_uom = _selective_tax_per_uom
        else:
            _tax_per_uom = 0

        if _exist:            
            form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'           
            # computation for excise tax foc
            # _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
            # _excise_tax_price_per_piece_foc = _excise_tax_amount / _id.uom_value
            # _selective_tax_foc += _excise_tax_price_per_piece_foc * _total_pcs
            # _unit_price = float(_price.wholesale_price) + _excise_tax_amount

            # form.errors.item_code = CENTER(DIV(B('DANGER! '),'Item code ' + str(_exist.item_code) + ' already exist.',_class='alert alert-danger',_role='alert'))                    
        else:
            if int(request.vars.category_id) == 3:                
                # computation for excise tax foc        
                _selective_tax = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax_foc = 0
                else:
                    _selective_tax_foc =  float(_tax_per_uom) * _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + _selective_tax_foc
                _selective_tax_total_foc += float(_tax_per_uom) * _total_pcs
                
                # _net_price_at_wholesale = 0.0
                # _net_price_at_wholesale = float(_wholesale_price_per_uom) * _id.uom_value + _selective_tax_foc   
                # print '_selective_tax_total_foc: ', _selective_tax_total_foc
                # _excise_tax_amount = float(_price.retail_price) * float(_price.selective_tax_price or 0) / 100
                # _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
                # _selective_tax_foc += _excise_tax_price_per_piece * _total_pcs
                # _unit_price = float(_price.wholesale_price) + _excise_tax_amount

                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()    
            else:
                # _selective_tax = 0
                # computation for excise tax
                _selective_tax_foc = _unit_price1 = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax = 0

                else:
                    _selective_tax =  float(_selective_tax_per_uom or 0) #* _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + (float(_selective_tax or 0) * _id.uom_value)
                
                _selective_tax_total += float(_selective_tax) * _total_pcs
                
                # _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
                # _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
                # _selective_tax += _excise_tax_price_per_piece * _total_pcs                
                # _unit_price = float(_price.wholesale_price) + _excise_tax_amount
                
                # computation for price per unit
                if float(_price.selective_tax_price) == 0: # without selective tax
                    _net_price = 0
                    _net_price = _unit_price - ((_unit_price * _item_discount) / 100) #+ (float(_selective_tax or 0) * _id.uom_value)
                    _total_amount = _net_price / _id.uom_value * _total_pcs                    
                else:   # with selective tax                    
                    # _net_price = 0
                    # _net_price_at_wholesale = 0.0
                    # _net_price_at_wholesale = float(_wholesale_price_per_uom) * _id.uom_value   
                    
                    _net_price = (float(_price.wholesale_price) * (100 - _item_discount) / 100) + float(_price.selective_tax_price)
                    # _net_price = _net_price_at_wholesale - ((_net_price_at_wholesale * _item_discount) / 100) + _selective_tax
                    # # print '_net_price_at_wholesale: ', _net_price_at_wholesale, _net_price                 
                    _total_amount = (_net_price / _id.uom_value) * _total_pcs

                # _net_price = (_unit_price * ( 100 - int(form.vars.discount_percentage or 0))) / 100
                # _price_per_piece = _net_price / _id.uom_value
                # _total_amount = _total_pcs * _price_per_piece
        
                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()                  
                                                
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(request.vars.pieces or 0) >= int(_id.uom_value):
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                       
        if form.vars.pieces == "":
            form.vars.pieces = 0            
        # _unit_price = float(_price.retail_price) / int(_id.uom_value)
        # _total = float(_unit_price) * int(_total_pcs)
        _provational_balanced = int(_stk_file.closing_stock) + int(_stk_file.stock_in_transit)
        if int(_stk_file.stock_in_transit) >=0:            
            if int(_total_pcs) > int(_stk_file.closing_stock): # pro = closing + transit
                _pro_bal = card(_stk_file.item_code_id, _stk_file.closing_stock, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than closing stock of ' + str(_pro_bal)
        else:            
            if int(_total_pcs) > int(_provational_balanced):             
                # _pro_bal = card(_stk_file.item_code_id, _stk_file.closing_stock, _id.uom_value)
                _pro_bal = card(_stk_file.item_code_id, _stk_file.probational_balance, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than provisional balance of ' + str(_pro_bal)
            # if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):
        
        form.vars.item_code_id = _id.id
        form.vars.selective_tax = _selective_tax_total
        form.vars.selective_tax_foc = _selective_tax_total_foc
        form.vars.total_pieces = _total_pcs
        form.vars.price_cost = float(_unit_price)
        form.vars.total_amount = _total_amount
        form.vars.net_price = _net_price
        form.vars.wholesale_price = _price.wholesale_price

@auth.requires_login()            
def sales_order_transaction_temporary():       
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_order_transaction).accepted:        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'                
        _id = db(db.Item_Master.id == form.vars.item_code_id).select().first()
        _stk_src = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
        db.Sales_Order_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            wholesale_price = form.vars.wholesale_price,
            total_amount = form.vars.total_amount,
            discount_percentage = form.vars.discount_percentage,
            category_id = form.vars.category_id,
            stock_source_id = session.stock_source_id,
            selective_tax = form.vars.selective_tax,
            selective_tax_foc = form.vars.selective_tax_foc,
            net_price = form.vars.net_price,
            ticket_no_id = session.ticket_no_id)        
        if db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:            
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:            
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        _stk_src.stock_in_transit -= int(form.vars.total_pieces)        
        _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)        
        _stk_src.update_record()                          
        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price/Sel.Tax'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Order_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Sales_Order_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction_Temporary.item_code_id)])    
    for n in _query:
        ctr += 1      
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Sales_Order_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Sales_Order_Transaction_Temporary.id),'_data-qt':(n.Sales_Order_Transaction_Temporary.quantity), '_data-pc':(n.Sales_Order_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Sales_Order_Transaction_Temporary.id), **{'_data-id':(n.Sales_Order_Transaction_Temporary.id)})
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
        btn_lnk = DIV( dele_lnk)
        _selective_tax += n.Sales_Order_Transaction_Temporary.selective_tax
        _selective_tax_foc += n.Sales_Order_Transaction_Temporary.selective_tax_foc
        if (_selective_tax > 0.0) or (_selective_tax_foc > 0.0):            
            _div_tax = DIV(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('REMARKS: TOTAL SELECTIVE TAX FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True)))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')

        
        row.append(TR(
            TD(ctr, INPUT(_name="ctr",_hidden='true',_value=n.Sales_Order_Transaction_Temporary.id)),
            TD(n.Sales_Order_Transaction_Temporary.item_code, INPUT(_name='item_code_id',_type='text',_hidden='true',_value=n.Sales_Order_Transaction_Temporary.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction_Temporary.category_id.mnemonic, INPUT(_name='wholesale_price',_type='number',_hidden='true',_value=n.Sales_Order_Transaction_Temporary.wholesale_price)),
            TD(n.Item_Master.uom_value, INPUT(_name='uom',_type='number',_hidden='true',_value=n.Item_Master.uom_value)),
            TD(INPUT(_class='form-control quantity',_name='quantity',_type='number',_value=n.Sales_Order_Transaction_Temporary.quantity), _align = 'right', _style="width:100px;"),
            TD(INPUT(_class='form-control pieces',_name='pieces',_type='number',_value=n.Sales_Order_Transaction_Temporary.pieces), _align = 'right', _style="width:100px;"),
            TD(INPUT(_class='form-control price_cost',_name='price_cost',_type='text',_value=locale.format('%.2F',n.Sales_Order_Transaction_Temporary.price_cost or 0, grouping = True)), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control discount_per',_name='discount_per',_type='number',_value=locale.format('%d',n.Sales_Order_Transaction_Temporary.discount_percentage or 0, grouping = True)), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control net_price',_name='net_price',_type='text',_value=locale.format('%.2F',n.Sales_Order_Transaction_Temporary.net_price or 0, grouping = True)), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control total_amount',_name='total_amount',_type='text',_value=locale.format('%.2F',n.Sales_Order_Transaction_Temporary.total_amount or 0, grouping = True)),_align = 'right', _style="width:100px;"),
            TD(btn_lnk)))
        grand_total += n.Sales_Order_Transaction_Temporary.total_amount
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount'), _align = 'right'),TD(H4(INPUT(_class='form-control net_amount', _name = 'net_amount', _id='net_amount', _disabled = True, _value = locale.format('%.2F',grand_total or 0, grouping = True))), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Total Amount'), _align = 'right'),TD(H4(INPUT(_class='form-control total_amount', _name = 'total_amount', _id='total_amount', _disabled = True, _value = locale.format('%.2F',grand_total or 0, grouping = True))), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Added Discount'), _align = 'right'),TD(H4(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right')),TD(P(_id='error'))))

    # foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F',_total_amount_after_discount or 0, grouping = True),_id='net_amount', _align = 'right'),TD()))
    # foot += TFOOT(TR(TD(),TD(_div_tax_foc),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F', _total_amount or 0, grouping = True),_id='total_amount', _align = 'right'),TD()))
    # foot += TFOOT(TR(TD(),TD(_div_tax),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control',_type='text',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True))),TD(_id="error")))

    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblsot'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            print 'updated'
            if isinstance(request.vars.ctr, list):
                print 'list'
                row = 0
                for x in request.vars.ctr:
                    _row = db(db.Sales_Order_Transaction_Temporary.id == x).select().first()
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    if _row.total_pieces != _qty or _row.discount_percentage != request.vars.discount_per[row]:
                        print 'not equal'
                        _stk_src_ctr = int(-_qty) - int(-_row.total_pieces)
                        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                        _stk_src.stock_in_transit += _stk_src_ctr
                        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                        _stk_src.update_record()
                        print request.vars.quantity[row], request.vars.discount_per[row]
                        _row.update_record(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], discount_percentage = request.vars.discount_per[row], total_pieces = _qty, total_amount = request.vars.total_amount[row])                    
                    else:
                        print 'equal'
                        print request.vars.quantity[row], request.vars.discount_per[row]
                    row += 1
                    session.grand_total = request.vars.grand_total
            else:
                print 'not list'
                _row = db(db.Sales_Order_Transaction_Temporary.id == request.vars.ctr).select().first()
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                if _row.total_pieces != _qty:
                    _stk_src_ctr = int(-_qty) - int(-_row.total_pieces)
                    _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                    _stk_src.stock_in_transit += _stk_src_ctr
                    _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                    _stk_src.update_record()
                    _row.update_record(quantity = request.vars.quantity, pieces = request.vars.pieces, discount_percentage = request.vars.discount_percentage, total_pieces = _qty, total_amount = request.vars.total_amount)
                    session.grand_total = request.vars.grand_total
        else:
            print 'not updated'
        response.js = "$('#tblsot').get(0).reload()"
    return dict(form = form, table = table, grand = grand_total)

@auth.requires_login()
def sales_order_transaction_temporary_edit():
    _tmp = db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).select().first()
    _uom = db(db.Item_Master.id == _tmp.item_code_id).select().first()
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _total_pcs = _qty * _uom.uom_value + _pcs
    if _total_pcs >= _uom.uom_value:
        response.flash = 'QUANTITY HAS ERROR'
        # print 'if', request.args(0), _uom.uom_value, _tmp.item_code_id, _total_pcs
    else:
        # print 'else', request.args(0), request.args(1), request.args(2)
        _amount = float(_tmp.price_cost) * int(_total_pcs)
        _tmp.update_record(quantity = _qty, pieces = _pcs, total_pieces = _total_pcs, total_amount = _amount)
        response.js = "$('#tblsot').get(0).reload()"
    
@auth.requires_login()
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
    # print 'excise tax ', _excise_tax_amount, _unit_price, _total_amount
    return _unit_price


@auth.requires_login()
def sales_order_transaction_temporary_delete():
    _id = db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).select().first()    
    _s = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
    _s.stock_in_transit += _id.total_pieces
    _s.probational_balance = int(_s.closing_stock) - int(_id.total_pieces)
    _s.update_record()        
    db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).delete()     
    if db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() == 0:            
        response.flash = 'RECORD DELETED'
        response.js = "$('#tblsot').get(0).reload(), jQuery('#btnsubmit').attr('disabled','disabled')"
    else:    
        response.flash = 'RECORD DELETED'
        response.js = "$('#tblsot').get(0).reload()"

def get_sales_order_workflow_grid():    
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    # for n in db((db.Sales_Order.created_by == auth.user.id) & (db.Sales_Order.archives == False)).select(orderby = ~db.Sales_Order.id):  

    for n in db((db.Sales_Order.created_by == auth.user_id) & (db.Sales_Order.archives == False) & (db.Sales_Order.status_id != 7)  & (db.Sales_Order.status_id != 10)).select(orderby = ~db.Sales_Order.id):          
        
        if n.status_id == 7:
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        btn_lnk = DIV(view_lnk, clea_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            # _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)            
            # _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            # _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        if n.cancelled == True:
            row.append(TR(
                TD(n.sales_order_date),
                TD(_sales),
                TD(_note),
                TD(_inv),
                TD(n.dept_code_id.dept_name),
                TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),
                TD(n.stock_source_id.location_name),
                TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
                TD('Cancelled'),
                TD(n.remarks),
                TD(),_class='text-danger'))
        else:
            row.append(TR(
                TD(n.sales_order_date),
                TD(_sales),
                TD(_note),
                TD(_inv),
                TD(n.dept_code_id.dept_name),
                TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),
                TD(n.stock_source_id.location_name),
                TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))

    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'tblSO')#, **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

def get_sales_invoice_workflow_reports():    
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    # for n in db((db.Sales_Order.created_by == auth.user.id) & (db.Sales_Order.archives == False)).select(orderby = ~db.Sales_Order.id):  
    for n in db((db.Sales_Order.created_by == auth.user_id) & (db.Sales_Order.archives == False) & (db.Sales_Order.status_id == 7)).select(orderby = ~db.Sales_Order.id):          
        # if n.status_id == 7:
        #     clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})            
        #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
        # else:
        #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
        #     clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        # btn_lnk = DIV(view_lnk, clea_lnk)
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_view', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')#, _href=URL('customer_category_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')#, _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(
            TD(n.sales_order_date),
            TD(_sales),
            TD(_note),
            TD(_inv),
            TD(n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),
            TD(n.stock_source_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'tblSO')#, **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def get_fmcg_sales_order_workflow_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Sales_Order.created_by == auth.user.id) & (db.Sales_Order.archives == False) & (db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)).select(orderby = db.Sales_Order.id):          
        if n.status_id == 7:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        btn_lnk = DIV(view_lnk, clea_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(
            TD(n.sales_order_date),
            TD(_sales),
            TD(_note),
            TD(_inv),
            TD(n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_name,', ',n.customer_code_id.account_code ),
            TD(n.stock_source_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'tblSOR')
    return dict(table = table)    
    

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def get_fmcg_sales_return_workflow_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Sales_Return.created_by == auth.user_id) & (db.Sales_Return.status_id != 13)).select(orderby = ~db.Sales_Return.id):  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','sales_return_browse_load_view', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(n.sales_return_date),
            TD(n.transaction_prefix_id.prefix,n.sales_return_no),
            TD(n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_name,', ',n.customer_code_id.account_code),
            TD(n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblSRT')
    return dict(table = table)    
    
@auth.requires_login()
def sales_order_browse():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),T('Approved By'),TH('Action Required'),TH('Action')),_class='bg-primary')
    if auth.has_membership(role = 'ACCOUNTS') | auth.has_membership(role = 'MANAGEMENT'):
        _query = db().select(orderby = ~db.Sales_Order.id)
    else:
        _query = db((db.Sales_Order.created_by == auth.user.id) & (db.Sales_Order.archives == False)).select(orderby = ~db.Sales_Order.id)
    for n in _query:  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_sales_report_id', args = [1, n.id]))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        if n.sales_order_approved_by == None:
            _approved_by = 'None'
        else:
            _approved_by = n.sales_order_approved_by.first_name,' ',n.sales_order_approved_by.last_name
        row.append(TR(TD(n.sales_order_date),TD(_sales),TD(_note),TD(_inv),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,'-',n.customer_code_id.account_name),
            TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),TD(_approved_by),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'tblso', **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

@auth.requires_login()
def delivery_note_browse():
    row = []
    head = THEAD(TR(TH('Date'),TH('Delivery Note No.'),TH('Sales Order No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Approved By'),TH('Action Required'),TH('Action')),_class='bg-primary')
    if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT') :
        _query = db().select(orderby = db.Delivery_Note.id)
    else:
        _query = db(db.Delivery_Note.created_by == auth.user_id).select(orderby = ~db.Delivery_Note.id)   
    for n in _query:  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_sales_report_id', args = [2, n.id]))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href=URL('delivery_note_reports','get_workflow_delivery_reports_id', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(TD(n.delivery_note_date_approved.date()),TD(_note),TD(_sales),TD(_inv),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),TD(n.delivery_note_approved_by.first_name,' ', n.delivery_note_approved_by.last_name),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def sales_invoice_browse():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Invoice No.'),TH('Delivery Note No.'),TH('Sales Order No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Approved by'),TH('Action Required'),TH('Action')),_class='bg-primary')
    if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'):
        _query = db().select(orderby = ~db.Sales_Invoice.id)
    else:
        _query = db(db.Sales_Invoice.created_by == auth.user_id).select(orderby = ~db.Sales_Invoice.id)   
    for n in _query:  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_sales_report_id', args = [3, n.id]))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href=URL('default','get_workflow_sales_invoice_reports_id', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(TD(n.sales_invoice_date_approved.date()),TD(_inv),TD(_note),TD(_sales),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),TD(n.sales_invoice_approved_by.first_name,' ', n.sales_invoice_approved_by.last_name),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()   
def sales_return_browse():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Status'),TH('Requested by'),TH('Action Required'),TH('Action'),_class='bg-warning'))
    for n in db(db.Sales_Return.status_id == 13).select(orderby = ~db.Sales_Return.id):  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_sales_return_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _target='_blank',_role='button', _class='btn btn-icon-toggle', _href=URL('default','sales_return_report_account_user', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(n.sales_return_date),TD(n.transaction_prefix_id.prefix,n.sales_return_no),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ',n.customer_code_id.account_code),
            TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount   or 0, grouping = True), _align = 'right'),TD(n.status_id.description),TD(n.sales_man_id.employee_id.first_name,' ', n.sales_man_id.employee_id.last_name),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def get_sales_return_id():
    return dict(_id = db(db.Sales_Return.id==request.args(0)).select().first())

def get_sales_report_id():
    if int(request.args(0)) == 1:
        _id = db(db.Sales_Order.id == request.args(1)).select().first()
        _title = 'Sales Order'
    elif int(request.args(0)) == 2:
        _id = db(db.Delivery_Note.id == request.args(1)).select().first()
        _title = 'Delivery Note'
    elif int(request.args(0)) == 3:
        _id = db(db.Sales_Invoice.id == request.args(1)).select().first()
        _title = 'Sales Invoice'
    return dict(_id = _id, _title = _title)

def get_sales_report_transaction_id():
    # print 'get_sales_report_transaction_id', request.args(0),request.args(1)
    ctr = _grand_total= _selective_tax = _selective_tax_foc = _total_amount = _total_amount_after_discount =_div_tax_foc=_div_tax=0
    row = []
    if int(request.args(0)) == 1:
        print 'sales order transaction: '
        _id = db(db.Sales_Order.id == request.args(1)).select().first()
        _query = db((db.Sales_Order_Transaction.sales_order_no_id ==request.args(1)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id)
    elif int(request.args(0)) == 2:
        print 'delivery note transaction: '
        _id = db(db.Delivery_Note.id == request.args(1)).select().first()
        _query = db((db.Delivery_Note_Transaction.delivery_note_id ==request.args(1)) & (db.Delivery_Note_Transaction.delete == False)).select(orderby = db.Delivery_Note_Transaction.id)
    elif int(request.args(0)) == 3:
        
        _id = db(db.Sales_Invoice.id == request.args(1)).select().first()
        print 'sales invoice transaction: ', _id.id, _id.total_amount_after_discount, _id.total_amount, _id.discount_added, _id.sales_invoice_no, _id.delivery_note_no, _id.sales_order_no
        _query = db((db.Sales_Invoice_Transaction.sales_invoice_no_id ==request.args(1)) & (db.Sales_Invoice_Transaction.delete == False)).select(orderby = db.Sales_Invoice_Transaction.id)        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    for n in _query:   
        ctr += 1
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        # discount & grand total computation
        _grand_total += float(n.total_amount or 0)
        # _discount = float(_grand_total) * int(_id.discount_added or 0) / 100
        _net_amount = float(_grand_total) - float(_id.discount_added or 0)
        
        # selective tax computation
        _selective_tax += n.selective_tax or 0
        _selective_tax_foc += n.selective_tax_foc or 0
        
        if _selective_tax > 0.0:
            _div_tax = DIV(H4('TOTAL SELECTIVE TAX: ',locale.format('%.2F', _selective_tax or 0, grouping = True)))            
        else:
            _div_tax = DIV('')

        if _selective_tax_foc > 0.0:
            _div_tax_foc = DIV(H4('TOTAL SELECTIVE TAX FOC: ',locale.format('%.2F', _selective_tax_foc or 0, grouping = True)))
        else:
            _div_tax_foc = DIV('')
        # ownership 
        if auth.user_id != n.created_by:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')
        else:
            if _id.status_id == 4:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_edit_view', args = n.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-icon-toggle delete', callback = URL( args = n.id, extension = False), **{'_data-id':(n.id)})
            else:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')

        btn_lnk = DIV( dele_lnk)
        _qty = n.quantity / n.uom        
        _pcs = n.quantity - n.quantity / n.uom * n.uom        
        
        _cst = (n.price_cost * n.uom) + (n.selective_tax / n.uom)
        # _pri = _qty * n.uom
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(_i.brand_line_code_id.brand_line_name),
            TD(_i.item_description),
            TD(n.category_id.mnemonic, _style = 'width:120px'),
            TD(n.uom, _style = 'width:120px'),
            TD(_qty, _style = 'width:80px'),
            TD(_pcs, _style = 'width:80px'),
            TD(locale.format('%.2F',n.price_cost or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%d',n.discount_percentage), _align = 'right', _style = 'width:80px'),
            TD(locale.format('%.2F',n.net_price or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%.2F',n.total_amount or 0,grouping = True), _align = 'right', _style = 'width:100px'),
            TD(btn_lnk)))
        _total_amount += n.total_amount
        _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True),_id='net_amount', _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F', _id.total_amount or 0, grouping = True),_id='total_amount', _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control',_type='text',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True),  _disabled = True)),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id='tbltrnx')
    return dict(table = table)      
    

def get_sales_report_transaction_id_():
    ctr = 0
    row = []                
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc =  DIV('')
    _id = db((db.Sales_Order.id == session.sales_order_no_id) & (db.Sales_Order.id == request.args(0))).select().first()
    if auth.has_membership(role = 'ROOT') | auth.has_membership(role = 'SALES'):
        _query = db((db.Sales_Order_Transaction.sales_order_no_id == session.sales_order_no_id) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id))
        _id = db(db.Sales_Order.id == session.sales_order_no_id).select().first()
    else:
        _query = db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id))
        _id = db(db.Sales_Order.id == request.args(0)).select().first()

    # _id = db(db.Sales_Order.id == session.sales_order_no_id).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    for n in _query:
    # for n in db((db.Sales_Order_Transaction.sales_order_no_id == session.sales_order_no_id) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,orderby = ~db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1

        # discount & grand total computation
        _grand_total += float(n.Sales_Order_Transaction.total_amount or 0)
        # _discount = float(_grand_total) * int(_id.discount_added or 0) / 100
        _net_amount = float(_grand_total) - float(_id.discount_added or 0)
        
        # selective tax computation
        _selective_tax += n.Sales_Order_Transaction.selective_tax or 0
        _selective_tax_foc += n.Sales_Order_Transaction.selective_tax_foc or 0
        
        if _selective_tax > 0.0:
            _div_tax = DIV(H4('TOTAL SELECTIVE TAX: ',locale.format('%.2F', _selective_tax or 0, grouping = True)))            
        else:
            _div_tax = DIV('')

        if _selective_tax_foc > 0.0:
            _div_tax_foc = DIV(H4('TOTAL SELECTIVE TAX FOC: ',locale.format('%.2F', _selective_tax_foc or 0, grouping = True)))
        else:
            _div_tax_foc = DIV('')
        # ownership 
        if auth.user_id != n.Sales_Order_Transaction.created_by:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')
        else:
            if _id.status_id == 4:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_edit_view', args = n.Sales_Order_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id, extension = False), **{'_data-id':(n.Sales_Order_Transaction.id)})
            else:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')

        btn_lnk = DIV( dele_lnk)
        _qty = n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom        
        _pcs = n.Sales_Order_Transaction.quantity - n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom * n.Sales_Order_Transaction.uom        
        
        _cst = (n.Sales_Order_Transaction.price_cost * n.Sales_Order_Transaction.uom) + (n.Sales_Order_Transaction.selective_tax / n.Sales_Order_Transaction.uom)
        # _pri = _qty * n.Sales_Order_Transaction.uom
        if db((db.Sales_Order.id == request.args(0)) & (db.Sales_Order.status_id == 7) | (db.Sales_Order.created_by != auth.user_id)).select().first():
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
        else:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Order_Transaction.category_id.mnemonic, _style = 'width:120px'),
            TD(n.Sales_Order_Transaction.uom, _style = 'width:120px'),
            TD(_qty, _style = 'width:80px'),
            TD(_pcs, _style = 'width:80px'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.price_cost or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%d',n.Sales_Order_Transaction.discount_percentage), _align = 'right', _style = 'width:80px'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.net_price or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.total_amount or 0,grouping = True), _align = 'right', _style = 'width:100px'),
            TD(btn_lnk)))
        _total_amount += n.Sales_Order_Transaction.total_amount
        _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F',_total_amount_after_discount or 0, grouping = True),_id='net_amount', _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F', _total_amount or 0, grouping = True),_id='total_amount', _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control',_type='text',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True),  _disabled = True)),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id='tbltrnx')
    return dict(table = table)  
        
@auth.requires_login()
def sales_order_cancell():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 10, update_on = request.now, updated_by = auth.user_id)
    session.flash = 'SALES ORDER CANCELLED'    

@auth.requires_login()
def get_sales_invoice_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order'),TH('Delivery Note'),TH('Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db(db.Sales_Order.status_id == 7).select(orderby = ~db.Sales_Order.id):  
        if n.status_id == 7:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False))            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _target='blank', _role='button', _class='btn btn-icon-toggle',  _href = URL('default','sales_order_report_account_user', args = n.id, extension = False))
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _target='blank', _role='button', _class='btn btn-icon-toggle disabled')

        btn_lnk = DIV(view_lnk, prin_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
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
        row.append(TR(TD(n.sales_order_date),TD(_sales),TD(_note),TD(_inv),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),
            TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def delivery_note_browse_():
    row = []
    head = THEAD(TR(TH('Date'),TH('Delivery Note No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Sales_Order.created_by == auth.user.id) & ((db.Sales_Order.archives != True) | (db.Sales_Order.status_id != 9) | (db.Sales_Order.status_id != 10))).select(orderby = ~db.Sales_Order.id):  
        if n.status_id == 7:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False))            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view', args = n.id, extension = False))        
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        btn_lnk = DIV(view_lnk)

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
        row.append(TR(TD(n.sales_order_date),TD(_note),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
            TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def sales_order_view():    
    session.sales_order_no_id = 0
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
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
    db.Sales_Order.section_id.writable = False     
    db.Sales_Order.total_amount_after_discount.writable = False 
    if _id.status_id == 3:
        db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 4)| (db.Stock_Status.id == 3)| (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 4)| (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 4    
    session.sales_order_no_id = request.args(0)        
    session.stock_source_id = _id.stock_source_id
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'            
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Action')))
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
        _qty = n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom        
        _pcs = n.Sales_Order_Transaction.quantity - n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom * n.Sales_Order_Transaction.uom
        if (n.Sales_Order.status_id == 7) | (n.Sales_Order.status_id == 8) | (n.Sales_Order.status_id == 9):        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)           
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_edit_view', args = n.Sales_Order_Transaction.id))            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id),  **{'_data-id':(n.Sales_Order_Transaction.id)})            
        btn_lnk = DIV(edit_lnk, dele_lnk)        
        row.append(TR(
            TD(ctr,INPUT(_name='ctr',_hidden='true',_value=n.Sales_Order_Transaction.id)),
            TD(n.Sales_Order_Transaction.item_code_id.item_code,INPUT(_name='item_code_id',_type='number',_hidden='true',_value=n.Sales_Order_Transaction.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom,INPUT(_name='uom',_hidden='true',_value=n.Sales_Order_Transaction.uom)),
            TD(INPUT(_class='form-control quantity',_name='quantity',_type='number',_value=_qty)),
            TD(INPUT(_class='form-control pieces',_name='pieces',_type='number',_value=_pcs)),
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),
            TD(n.Sales_Order_Transaction.total_amount or 0,_align = 'right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table table-striped', _id = 'tblsot')
    return dict(form = form, table = table, _id = _id) 

def cancel_tranx():
    print 'cancel_tranx', request.args(0)
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == int(_id.id)) & (db.Sales_Order_Transaction.delete == False)).select():
        _stk_src = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _stk_src.stock_in_transit += n.quantity
        _stk_src.probational_balance = _stk_src.closing_stock - _stk_src.stock_in_transit
        _stk_src.update_record()    
    _id.update_record(status_id = 10)
    

@auth.requires_login()
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
        _price_per_piece = _id.net_price / _id.uom
        _total_amount = form.vars.quantity * _price_per_piece
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id, total_amount = _total_amount)
        for n in db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False)).select():
            _total += n.total_amount
        _discount = float(_total) * int(_so.discount_percentage or 0) / 100
        _total_amount_after_discount = float(_total) - int(_discount)
        _so.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount)
        _nsit = _sf.stock_in_transit + _qty
        _sf.update_record(stock_in_transit = _nsit)
        session.flash = 'RECORD UPDATED'
        redirect(URL('sales_order_view', args = _so.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('sales_order_view', args = _so.id))
    return dict(form = form, btn_back = btn_back, _id = _id)

@auth.requires_login()
def validate_stock_in_transit(form):    
    _id = db(db.Sales_Order_Transaction.id == request.args(0)).select().first() # from sales order transaction table
    _im = db(db.Item_Master.id == _id.item_code_id).select().first() # Item master table
    _so = db(db.Sales_Order.id == _id.sales_order_no_id).select().first() # from sales order  table
    _sf = db(db.Stock_File.item_code_id == _id.item_code_id).select().first() # from stock file table
    _ip = db(db.Item_Prices.item_code_id == _id.item_code_id).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)            
    if _qty >= _sf.closing_stock:        
        form.errors.quantity = 'Total quantity should not be more than the stock file. '
    if int(request.vars.pieces) >= int(_id.uom):
        form.errors.quantity = 'Total quantity should not be more than UOM value.'
    form.vars.quantity = _qty    
    _old_stock_in_transit = _sf.stock_in_transit - _id.quantity
    _old_probational_balance = _sf.closing_stock - _old_stock_in_transit
    _sf.update_record(stock_in_transit = _old_stock_in_transit)

@auth.requires_login()
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

def sales_order_delete_view():
    _st = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()    
    _so = db(db.Sales_Order.id == _st.sales_order_no_id).select().first()
    
    _total = _selective_tax = _selective_tax_foc = 0

    _sf = db((db.Stock_File.item_code_id == _st.item_code_id) & (db.Stock_File.location_code_id == _so.stock_source_id)).select().first()    
    # # update the stock file table
    _sf.stock_in_transit += int(_st.quantity or 0)
    _sf.probational_balance += int(_st.quantity or 0)
    _sf.update_record()     

    _st.update_record(delete = True)

    _total_amount = _selective_tax = _selective_tax_foc = 0
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        _total_amount += float(n.total_amount or 0)
        _selective_tax += float(n.selective_tax or 0)
        _selective_tax_foc += float(n.selective_tax_foc or 0)
    _trnx = db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False) & (db.Sales_Order_Transaction.discounted==False) & (db.Sales_Order_Transaction.category_id==4)).select(orderby = db.Sales_Order_Transaction.id).first()
    if _trnx:
        if float(_so.discount_added or 0): # check if discount added                                                
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom)) - float(_so.discount_added or 0)) / int(_trnx.uom)            
            _trnx.update_record(discounted = True, sale_cost = _sale_cost, discount_added=_so.discount_added)   
    _total_amount_after_discount = _total_amount - float(_so.discount_added or 0)
    
    if db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False)).count() == 0:
        _so.update_record(status_id = 10, total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)         
        session.flash = 'RECORD DELETED'        
        response.js = 'jQuery(redirect())'       
    else:
        _so.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)         
        session.flash = 'RECORD DELETED'        
        response.js = '$("#tbltrnx").get(0).reload()'       

        

@auth.requires_login()
def sales_order_delete_view__():    
    response.js = "$('#tbltrnx').get(0).reload()"
    _st = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()    
    _so = db(db.Sales_Order.id == _st.sales_order_no_id).select().first()
    if _st.discounted == True:        
        # update tranx delete
        _st.update_record(delete = True)
        # resort the order
        _id = db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False)).select().first()
        # update the first item
        _sale_cost = _id.sale_cost or 0 - _so.discount_added or 0
        _id.update_record(sale_cost = _sale_cost, discounted = True)
        # update sales order header
        _total_amount = _so.total_amount - _st.total_amount
        _total_amount_after_discount = (_so.total_amount_after_discount - _total_amount) - _so.discount_added
        _so.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)
        print 'discounted: ', request.args(0), _st.id
    else:
        _id = db((db.Sales_Order_Transaction.sales_order_no_id == _so.id) & (db.Sales_Order_Transaction.delete == False)).select().first()
        _st.update_record(delete = True)
        _sale_cost = _id.sale_cost or 0 - _so.discount_added or 0
        if _id.discounted == True:
            _sale_cost = _id.wholesale_price / _id.uom
            _id.update_record(sale_cost = _sale_cost, discounted = False)
        else:
            _sale_cost = float(_id.sale_cost) - float(session.added_discount or 0)
            _id.update_record(sale_cost = _sale_cost)
        # update sales order header
        _total_amount = _so.total_amount - _st.total_amount
        _total_amount_after_discount = (_so.total_amount_after_discount - _total_amount) - _so.discount_added
        _so.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)

        print 'not discounted: ', request.args(0), _st.id

    _sf = db((db.Stock_File.item_code_id == _st.item_code_id) & (db.Stock_File.location_code_id == _so.stock_source_id)).select().first()    
    session.total_amount = _total_amount
    session.net_amount = _total_amount_after_discount
    session.added_discount = request.vars.added_discount
    print 'session: ', session.total_amount, session.net_amount, session.added_discount
    # update the stock file table
    _sf.stock_in_transit += int(_st.quantity or 0)
    _sf.probational_balance += int(_st.quantity or 0)
    _sf.update_record()
    session.flash = 'RECORD DELETED'    
    response.js = "$('#tbltrnx').get(0).reload()"


@auth.requires_login()
def sales_order_delete_view_():
    # initialization of variable
    _st = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()    
    _so = db(db.Sales_Order.id == _st.sales_order_no_id).select().first()
    
    # update the sales order transaction table
    _st.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)    
    _trnx_ctr = db((db.Sales_Order_Transaction.sales_order_no_id == int(_so.id)) & (db.Sales_Order_Transaction.delete == False)).count()
    
    if int(_trnx_ctr) < 1:
        # _so.update_record(cancelled=True,cancelled_by=auth.user_id,cancelled_on = request.now)        
        session.flash = 'This sales order transaction will be consider cancelled.'
        redirect(URL('inventory','get_back_off_workflow_grid'))
    
    elif int(_trnx_ctr) == 1:
        # generate re-computation in sales order transaction table        
        _trnx = db((db.Sales_Order_Transaction.sales_order_no_id == int(_so.id)) & (db.Sales_Order_Transaction.delete == False)).select().first()
        # _unit_price = ((float(_trnx.wholesale_price) / int(_trnx.uom)) * int(_trnx.quantity)) + (float(_trnx.selective_tax or 0) / int(_trnx.quantity)) * int(_trnx.quantity) #- float(_so.discount_added or 0))
        _trnx_total = float(_trnx.sale_cost) - float(_so.discount_added or 0)
        _trnx.update_record(total_amount = _trnx_total)
        _so.update_record(total_amount = _trnx.total_amount, total_amount_after_discount = _trnx_total)
    else:
        # generate re-computation in sales order transaction table
        _total = 0        
        for n in db((db.Sales_Order_Transaction.sales_order_no_id == int(_so.id)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):        
            _total += n.total_amount
        _trnx = db((db.Sales_Order_Transaction.sales_order_no_id == int(_so.id)) & (db.Sales_Order_Transaction.delete == False)).select().first()        
        _trnx_total = float(_trnx.total_amount) - float(_so.discount_added or 0)    

            
        _trnx.update_record(total_amount = _trnx_total)
            
        # update the sales order table
        _total_amount_after_discount = float(_total) - float(_so.discount_added or 0)
        _so.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount)
    session.flash = 'RECORD DELETED'    
    response.js = "$('#tblsot').get(0).reload()"
    
@auth.requires_login()
def sales_order_archived():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    _id.update_record(archives = True, updated_on = request.now, updated_by = auth.user_id)    
    response.flash = 'RECORD CLEARED'
    # response.js = "$('#tblso').get(0).reload()"

@auth.requires_login()    
def sales_order_transaction_table():    
    ctr = 0
    row = []                
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    _selective_tax = _selective_tax_foc = _total_amount_after_discount = 0
    _div_tax = _div_tax_foc =  DIV('')
    _id = db((db.Sales_Order.id == session.sales_order_no_id) & (db.Sales_Order.id == request.args(0))).select().first()
    if auth.has_membership(role = 'ROOT') | auth.has_membership(role = 'SALES'):
        _query = db((db.Sales_Order_Transaction.sales_order_no_id == session.sales_order_no_id) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id))
        _id = db(db.Sales_Order.id == session.sales_order_no_id).select().first()
    else:
        _query = db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id))
        _id = db(db.Sales_Order.id == request.args(0)).select().first()

    # _id = db(db.Sales_Order.id == session.sales_order_no_id).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    for n in _query:
    # for n in db((db.Sales_Order_Transaction.sales_order_no_id == session.sales_order_no_id) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,orderby = ~db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1

        # discount & grand total computation
        _grand_total += float(n.Sales_Order_Transaction.total_amount or 0)
        # _discount = float(_grand_total) * int(_id.discount_added or 0) / 100
        _net_amount = float(_grand_total) - float(_id.discount_added or 0)
        
        # selective tax computation
        _selective_tax += n.Sales_Order_Transaction.selective_tax or 0
        _selective_tax_foc += n.Sales_Order_Transaction.selective_tax_foc or 0
        
        if _selective_tax > 0.0:
            _div_tax = DIV('TOTAL SELECTIVE TAX: ',locale.format('%.2F', _selective_tax or 0, grouping = True))
        else:
            _div_tax = DIV('')

        if _selective_tax_foc > 0.0:
            _div_tax_foc = DIV('TOTAL SELECTIVE TAX FOC: ',locale.format('%.2F', _selective_tax_foc or 0, grouping = True))
        else:
            _div_tax_foc = DIV('')
        # ownership 
        if auth.user_id != n.Sales_Order_Transaction.created_by:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')
        else:
            if _id.status_id == 4:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_edit_view', args = n.Sales_Order_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id, extension = False), **{'_data-id':(n.Sales_Order_Transaction.id)})
            else:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')

        btn_lnk = DIV( dele_lnk)
        _qty = n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom        
        _pcs = n.Sales_Order_Transaction.quantity - n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom * n.Sales_Order_Transaction.uom        
        
        _cst = (n.Sales_Order_Transaction.price_cost * n.Sales_Order_Transaction.uom) + (n.Sales_Order_Transaction.selective_tax / n.Sales_Order_Transaction.uom)
        # _pri = _qty * n.Sales_Order_Transaction.uom
        if db((db.Sales_Order.id == request.args(0)) & (db.Sales_Order.status_id == 7) | (db.Sales_Order.created_by != auth.user_id)).select().first():
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
        else:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Order_Transaction.category_id.mnemonic, _style = 'width:120px'),
            TD(n.Sales_Order_Transaction.uom, _style = 'width:120px'),
            TD(_qty, _style = 'width:80px'),
            TD(_pcs, _style = 'width:80px'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.price_cost or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%d',n.Sales_Order_Transaction.discount_percentage), _align = 'right', _style = 'width:80px'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.net_price or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.total_amount or 0,grouping = True), _align = 'right', _style = 'width:100px'),
            TD(btn_lnk)))
        _total_amount += n.Sales_Order_Transaction.total_amount
        _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control',_type='text',_style='text-align:right;font-size:14px',_id='net_amount',_name='net_amount',_disabled = True,_value=locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True)), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc,_colspan='3'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F', _id.total_amount or 0, grouping = True),_id='total_amount', _align = 'right'),TD()))
    if _id.status_id == 8:
        foot += TFOOT(TR(TD(),TD(_div_tax,_colspan='3'),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control',_type='text',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True),  _disabled = True)),TD(_id="error")))
    else:
        foot += TFOOT(TR(TD(),TD(_div_tax,_colspan='3'),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control',_type='text',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True))),TD(_id="error")))
    table = TABLE(*[head, body, foot], _class='table', _id='tbltrnx')
    return dict(table = table, _total_amount = _total_amount, _total_amount_after_discount = _total_amount_after_discount)        

def update_sales_transaction(): # audited
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    if float(request.vars.vdiscount) != float(_id.discount_added or 0):                
        _trnx = db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id).first()
        _sale_cost = (float(_trnx.wholesale_price) / int(_trnx.uom)) - float(request.vars.vdiscount or 0)
        _trnx.update_record(sale_cost = _sale_cost)        
        _id.update_record(status_id = request.vars.status_id, remarks = request.vars.remarks, discount_added = request.vars.vdiscount, total_amount =request.vars.vtotal_amount,total_amount_after_discount=request.vars.vnet_amount)
    else:        
        _id.update_record(status_id = request.vars.status_id,remarks = request.vars.remarks)
    response.flash = "RECORD UPDATED"

# @auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def sales_order_utility_tool():    
    head = THEAD(TR(TH('Date'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Focal Person'),TH('Action')), _class='bg-primary')
    for k in db(db.Sales_Order_Transaction_Temporary).select(db.Item_Master.ALL, db.Sales_Order_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = ~db.Sales_Order_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction_Temporary.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction_Temporary.item_code_id)]):
        redo_lnk = A(I(_class='fas fa-redo'), _title='Redo Row', _type='button ', _role='button',_id='redo', _class='btn btn-icon-toggle btnRedo', callback=URL('sales','sales_order_tool_redo', args = k.Sales_Order_Transaction_Temporary.id))
        btn_lnk = DIV(redo_lnk, _class="hidden-sm action-buttons")

        row.append(TR(            
            TD(k.Sales_Order_Transaction_Temporary.created_on),
            TD(k.Item_Master.item_code),
            TD(k.Item_Master.item_description.upper()),
            TD(k.Item_Master.uom_value),
            TD(card(k.Item_Master.id, k.Sales_Order_Transaction_Temporary.total_pieces, k.Item_Master.uom_value)),            
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Sales_Order_Transaction_Temporary.total_amount or 0, grouping = True), _align='right'),            
            TD(k.Sales_Order_Transaction_Temporary.remarks),
            TD(k.Sales_Order_Transaction_Temporary.created_by.first_name.upper(),' ',k.Sales_Order_Transaction_Temporary.created_by.last_name.upper()),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblsot',_class='table', **{'_data-toggle':'table','_data-search':'true', '_data-show-pagination-switch':'true','_data-pagination':'true'})
    return dict(table = table)

def sales_order_tool_redo():
    _id = db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).select().first()
    if not _id:
        redirect(URL('inventory','stock_utility_tool'))
    else:
        _stk_src = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _stk_src.stock_in_transit += _id.total_pieces
        _stk_src.probational_balance = _stk_src.closing_stock - _stk_src.stock_in_transit
        _stk_src.update_record()
        db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).delete()
        session.flash = 'ITEM REDO'        
        response.js = "$('#tblsot').get(0).reload()"

# ----------    S A L E S     R E T U R N   ----------
@auth.requires_login()
def sales_return_sales_manager():
    session.sales_return_no_id = 0
    db.Sales_Return.sales_return_date.writable = False
    db.Sales_Return.dept_code_id.writable = False
    db.Sales_Return.location_code_id.writable = False
    db.Sales_Return.customer_code_id.writable = False
    db.Sales_Return.customer_order_reference.writable = False
    db.Sales_Return.delivery_due_date.writable = False
    db.Sales_Return.total_amount.writable = False
    db.Sales_Return.discount_added.writable = False
    db.Sales_Return.total_amount_after_discount.writable = False
    db.Sales_Return.total_selective_tax.writable = False
    db.Sales_Return.total_selective_tax_foc.writable = False
    db.Sales_Return.total_vat_amount.writable = False    
    db.Sales_Return.sales_man_id.writable = False    
    db.Sales_Return.status_id.writable = False    
    # db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    # db.Sales_Return.status_id.default = 4
    session.sales_return_no_id = request.args(0)
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Return, request.args(0))
    if form.process().accepted:
        sales_return_sales_manager_approved()
        redirect(URL('inventory','mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _id = _id) 

@auth.requires_login()
def sales_return_sales_manager_approved():    
    if sales_return_price_validation():
        _id = db(db.Sales_Return.id == request.args(0)).select().first()
        _flash = 'Price Discrepancies.'
        _id.update_record(status_id = 10, remarks = 'Price Discrepancies.', sales_manager_date = request.now, sales_manager_id = auth.user_id)
    else:                
        _id = db(db.Sales_Return.id == request.args(0)).select().first()
        if _id.status_id == 4:        
            _flash = 'Sales return approved.'
            _id.update_record(status_id = 14, sales_manager_date = request.now, sales_manager_id = auth.user_id)
        else:
            _flash = 'Sales return no. ' + str(_id.sales_return_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' +str(_id.sales_manager_id.first_name)
    response.js = "$('#tblsrt').get(0).reload()"
    session.flash = _flash

def sales_return_price_validation():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    for n in db(db.Sales_Return_Transaction.sales_return_no_id == _id.id).select(orderby = db.Sales_Return_Transaction.id):
        _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
        if (n.wholesale_price != _i.wholesale_price) or (n.retail_price != _i.retail_price) or (n.average_cost != _i.average_cost):
            return True
        else:
            return False



@auth.requires_login()    
def sales_return_sales_manager_rejected():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, sales_manager_date = request.now, sales_manager_id = auth.user_id, remarks = request.vars.remarks)    
    session.flash = 'Sales return rejected'

@auth.requires_login()
def sales_return_warehouse_form():
    session.sales_return_no_id = 0
    db.Sales_Return.sales_return_date.writable = False
    db.Sales_Return.dept_code_id.writable = False
    db.Sales_Return.location_code_id.writable = False
    db.Sales_Return.customer_code_id.writable = False
    db.Sales_Return.customer_order_reference.writable = False
    db.Sales_Return.delivery_due_date.writable = False
    db.Sales_Return.total_amount.writable = False        
    db.Sales_Return.total_amount_after_discount.writable = False
    db.Sales_Return.discount_added.writable = False
    db.Sales_Return.total_selective_tax.writable = False
    db.Sales_Return.total_selective_tax_foc.writable = False
    db.Sales_Return.total_vat_amount.writable = False    
    db.Sales_Return.sales_man_id.writable = False    
    db.Sales_Return.status_id.writable = False    
    
    # db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    # db.Sales_Return.status_id.default = 4
    session.sales_return_no_id = request.args(0)
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Return, request.args(0))
    if form.process().accepted:
        sales_return_warehouse_form_approved()
        redirect(URL('inventory','str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _id = _id) 

@auth.requires_login()
def sales_return_warehouse_form_approved():
    if sales_return_price_validation():
        _id = db(db.Sales_Return.id == request.args(0)).select().first()
        _flash = 'Price Discrepancies.'
        _id.update_record(status_id = 10, remarks = 'Price Discrepancies.', warehouse_date = request.now, warehouse_id = auth.user_id)
    else:    
        _id = db(db.Sales_Return.id == request.args(0)).select().first()
        if _id.status_id == 14:
            _flash = 'Sales return approved.'
            _id.update_record(status_id = 12, warehouse_date = request.now, warehouse_id = auth.user_id)
        else:
            _flash = 'Sales return no. ' + str(_id.sales_return_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' +str(_id.warehouse_id.first_name)
    response.js = "$('#tblsrt').get(0).reload()"
    session.flash = _flash

@auth.requires_login()
def sales_return_warehouse_form_reject():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, warehouse_date = request.now, warehouse_id = auth.user_id, remarks = request.vars.remarks)
    session.flash = 'Sales return rejected'
        

@auth.requires_login()
def sales_return_accounts_form():
    session.sales_return_no_id = 0
    db.Sales_Return.sales_return_date.writable = False
    db.Sales_Return.dept_code_id.writable = False
    db.Sales_Return.location_code_id.writable = False
    db.Sales_Return.customer_code_id.writable = False
    db.Sales_Return.customer_order_reference.writable = False
    db.Sales_Return.delivery_due_date.writable = False
    db.Sales_Return.total_amount.writable = False
    db.Sales_Return.total_amount_after_discount.writable = False
    db.Sales_Return.discount_added.writable = False
    db.Sales_Return.total_selective_tax.writable = False
    db.Sales_Return.total_selective_tax_foc.writable = False
    db.Sales_Return.total_vat_amount.writable = False    
    db.Sales_Return.sales_man_id.writable = False        
    db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 12) | (db.Stock_Status.id == 13)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    # db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 12) | (db.Stock_Status.id == 13) | (db.Stock_Status.id == 14)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Return.status_id.default = 14
    session.sales_return_no_id = request.args(0)
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Return, request.args(0))
    if form.process().accepted:        
        session.flash = 'Sales return processed.'
        redirect(URL('inventory','account_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _id = _id)     

@auth.requires_login()
def sales_return_accounts_form_approved():
    if sales_return_price_validation():        
        _id = db(db.Sales_Return.id == request.args(0)).select().first()
        _flash = 'Price Discrepancies.'
        _id.update_record(status_id = 10, remarks = 'Price Discrepancies.', accounts_date = request.now, accounts_id = auth.user_id)
        response.js = "$('#tblsrt').get(0).reload()"
    else:
        _id = db(db.Sales_Return.id == request.args(0)).select().first()
        _damaged_qty = 0
        for n in db(db.Sales_Return_Transaction.sales_return_no_id == _id.id).select():
            _price = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            _stk_des = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first() 
            _stk_in_trn = int(_stk_des.stock_in_transit) - int(n.quantity)
            _stk_in_clo = int(_stk_des.closing_stock) + int(n.quantity)
            _stk_in_pro = int(_stk_des.closing_stock) + int(_stk_in_trn)
            _stk_in_dam = int(_stk_des.damaged_stock_qty) + int(n.quantity)        
            _stk_in_nor = int(_stk_in_clo) + int(_stk_in_trn)
            if int(n.category_id) == 1: # damaged return
                _stk_des.update_record(probational_balance = _stk_in_pro, damaged_stock_qty = _stk_in_dam, stock_in_transit = _stk_in_trn, last_transfer_qty = n.quantity, last_transfer_date = request.now)
            if (int(n.category_id) == 4) or (int(n.category_id) == 3): # normal and foc stocks
                _stk_des.update_record(closing_stock = _stk_in_clo, probational_balance = _stk_in_nor, stock_in_transit = _stk_in_trn, last_transfer_qty = n.quantity, last_transfer_date = request.now)                    
        _id.update_record(status_id = 13, accounts_date = request.now, accounts_id = auth.user_id)    
        _flash = 'Sales return approved.'        
        response.js = "jQuery(PrintSalesReturn(%s))" % (_id.id)    
    session.flash = _flash

@auth.requires_login()
def sales_return_accounts_form_rejected():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _id.updated_record(status_id = 3, sales_return_date_approved = request.now, sales_return_approved_by = auth.user_id)
    session.flash = 'SALES RETURNED REJECTED'

def validate_sales_return(form):
    form.vars.discount_added = request.vars.discount_var
    # form.vars.total_amount_after_discount = request.vars.net_amount_var

@auth.requires_login()
def sales_return_view():    
    session.sales_return_no_id = 0
    db.Sales_Return.sales_return_date.writable = False
    db.Sales_Return.dept_code_id.writable = False
    db.Sales_Return.location_code_id.writable = False
    db.Sales_Return.customer_code_id.writable = False
    db.Sales_Return.customer_order_reference.writable = False
    db.Sales_Return.delivery_due_date.writable = False
    db.Sales_Return.total_amount.writable = False
    db.Sales_Return.total_amount_after_discount.writable = False
    db.Sales_Return.discount_added.writable = False
    db.Sales_Return.total_selective_tax.writable = False
    db.Sales_Return.total_selective_tax_foc.writable = False
    db.Sales_Return.total_vat_amount.writable = False    
    db.Sales_Return.sales_man_id.writable = False    
    
    session.sales_return_no_id = request.args(0)
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    if _id.status_id == 10:
        db.Sales_Return.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 10), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Sales_Return.status_id.default = 10    
    else:
        db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Sales_Return.status_id.default = 4
    form = SQLFORM(db.Sales_Return, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _id = _id) 

   
def update_sales_return_transaction():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _id.update_record(remarks = request.vars.remarks, discount_added = request.vars.vdiscount, total_amount_after_discount = request.vars.vnet_amount)
    

@auth.requires_login()   
def sales_return_browse_load():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Salesman'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-warning'))
    for n in db(db.Sales_Return.archives == False).select(orderby = ~db.Sales_Return.id):  
        if n.status_id == 13:            
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_browse_load_view', args = n.id, extension = False))        
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_browse_load_view', args = n.id, extension = False))        
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                                
        btn_lnk = DIV(view_lnk, clea_lnk)

        row.append(TR(
            TD(n.sales_return_date),
            TD(n.transaction_prefix_id.prefix,n.sales_return_no),
            TD(n.dept_code_id.dept_name),
            TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
            TD(n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.sales_man_id),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def sales_return_browse_load_view():
    session.sales_return_no_id = 0
    db.Sales_Return.sales_return_date.writable = False
    db.Sales_Return.dept_code_id.writable = False
    db.Sales_Return.location_code_id.writable = False
    db.Sales_Return.customer_code_id.writable = False
    db.Sales_Return.customer_order_reference.writable = False
    db.Sales_Return.delivery_due_date.writable = False
    db.Sales_Return.total_amount.writable = False
    db.Sales_Return.discount_added.writable = False    
    db.Sales_Return.total_amount_after_discount.writable = False    
    db.Sales_Return.total_selective_tax.writable = False
    db.Sales_Return.total_selective_tax_foc.writable = False
    db.Sales_Return.total_vat_amount.writable = False    
    db.Sales_Return.sales_man_id.writable = False    
    db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Return.status_id.default = 4
    session.sales_return_no_id = request.args(0)
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Return, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _id = _id) 

def get_sales_return_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Sales_Return.status_id != 13) & (db.Sales_Return.created_by == auth.user_id)).select(orderby = db.Sales_Return.id):  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','sales_return_view', args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk) 
        if n.status_id == 10:
            _action = SPAN(n.remarks,_class='label label-danger')
        else:
            _action = n.status_id.required_action
        row.append(TR(TD(n.sales_return_date),TD(n.transaction_prefix_id.prefix,n.sales_return_no),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_name, ', ',n.customer_code_id.account_code),
            TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),
            TD(_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',_id='tblsrt')
    return dict(table = table)  

@auth.requires_login()
def sales_return_archived():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _id.update_record(archives = True, updated_on = request.now, updated_by = auth.user_id)
    response.flash = 'RECORD CLEARD'

@auth.requires_login()
def sales_return_form():
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if _usr.van_sales == True:        
        _q_dept = db.Department.id == 3
        _q_cstmr = db.Master_Account.account_code == _usr.mv_code
        _default = db(db.Master_Account.account_code == _usr.mv_code).select(db.Master_Account.id).first()
    else:
        _q_cstmr = (db.Sales_Man_Customer.sales_man_id == _usr.id) & (db.Sales_Man_Customer.master_account_type_id == db.Master_Account.master_account_type_id)
        _q_dept = db.Department.id == 3
        _default = 0
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = 0
    _total_selective_tax = 0
    _total_foc = 0
    form = SQLFORM.factory(
        Field('sales_order_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', requires = IS_IN_DB(db(_q_dept), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, requires = IS_IN_DB(db(db.Location.id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('customer_code_id','reference Master_Account', default=int(_default), ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db(_q_cstmr), db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Customer')),    
        Field('customer_order_reference','string', length = 25),
        Field('delivery_due_date', 'date', default = request.now),
        Field('remarks', 'string'),        
        Field('status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:        
        ctr = db((db.Transaction_Prefix.prefix_key == 'SRS') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        db.Sales_Return.insert(
            transaction_prefix_id = ctr.id,
            sales_return_no = ctr.current_year_serial_key,
            sales_return_date = request.now,
            dept_code_id = form.vars.dept_code_id,
            location_code_id = form.vars.location_code_id,
            customer_code_id =  form.vars.customer_code_id,
            discount_added = request.vars.discount_var,
            customer_order_reference = form.vars.customer_order_reference,
            delivery_due_date = form.vars.delivery_due_date,
            sales_man_id = _usr.id,
            remarks = form.vars.remarks,
            total_amount = request.vars.total_amount_var,             
            total_amount_after_discount = request.vars.net_amount_var,   
            status_id = form.vars.status_id)
        _id = db(db.Sales_Return.sales_return_no == ctr.current_year_serial_key).select().first()        
        _tmp = db(db.Sales_Return_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _tmp:
            
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
            if int(n.category_id) == 3:
                _price_cost = (_pric.average_cost / _item.uom_value)
                # _price_cost_discount = (_pric.average_cost / _item.uom_value)
                _sale_cost_no_tax = 0 
            else:
                _sale_cost_no_tax = ((n.net_price / _item.uom_value) - (_pric.selective_tax_price /  _item.uom_value))           
                _price_cost = (_pric.wholesale_price / _item.uom_value)
            
            _price_cost_discount = _price_cost - ((_price_cost * n.discount_percentage) / 100)
            db.Sales_Return_Transaction.insert(
                sales_return_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,
                average_cost = _pric.average_cost,
                sale_cost = (n.net_price / _item.uom_value), # converted to pieces
                sale_cost_notax_pcs = _sale_cost_no_tax, #((n.net_price / _item.uom_value) - (_pric.selective_tax_price /  _item.uom_value)),
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                discount_percentage = n.discount_percentage,
                selective_tax = n.selective_tax,
                selective_tax_foc = n.selective_tax_foc,
                selective_tax_price = _pric.selective_tax_price,
                price_cost_pcs = _price_cost,  #n.price_cost / _item.uom_value,
                average_cost_pcs = _pric.average_cost / _item.uom_value,
                wholesale_price_pcs = _pric.wholesale_price / _item.uom_value,
                retail_price_pcs = _pric.retail_price / _item.uom_value,
                price_cost_after_discount = _price_cost_discount, #(_pric.wholesale_price / _item.uom_value) - (_pric.wholesale_price / _item.uom_value) * n.discount_percentage / 100, #((n.price_cost * (100 - n.discount_percentage)) / 100) / _item.uom_value,
                total_amount = n.total_amount,
                net_price = n.net_price)
            _grand_total += n.total_amount or 0
            _total_selective_tax += n.selective_tax or 0
            _total_foc += n.selective_tax_foc or 0
        if float(request.vars.discount_var or 0): # check global discount exist
            _trnx = db(db.Sales_Return_Transaction.sales_return_no_id == _id.id).select().first()
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom)) - float(request.vars.discount_var or 0)) / int(_trnx.uom)
            _trnx.update_record(sale_cost = _sale_cost, discounted=True,discount_added=float(request.vars.discount_var))
        _id.update_record(total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_foc)        
        db(db.Sales_Return_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'Sales Return No ' + str(_skey) + 'process.'    
    elif form.errors:
        response.flash = 'Form has error.'
    return dict(form = form, ticket_no_id = ticket_no_id)

@auth.requires_login()
def sales_return_item_code_description():
    response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    _icode = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    _price = db((db.Item_Prices.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    if not _icode:        
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:   
        response.js = "$('#btnadd').removeAttr('disabled')"     
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()        
        if _sfile:           
            _provational_balanced = int(_sfile.closing_stock) + int(_sfile.stock_in_transit)
            if _icode.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_balanced = _provational_balanced
                _on_transit = _sfile.stock_in_transit
                _on_hand = _sfile.closing_stock      
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_icode.id, _provational_balanced, _icode.uom_value)
                _on_transit = card(_icode.id, _sfile.stock_in_transit, _icode.uom_value)
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)            
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt'),TH('Retail Price'),TH('Unit Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(_iprice.selective_tax_price),
                TD(_iprice.retail_price),
                TD(locale.format('%.2F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_balanced)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

@auth.requires_login()
def validate_sales_return_transaction(form):        
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    
    if not _id:
        # form.errors._id = CENTER(DIV(B('DANGER! '),'Item code does not exist or empty.',_class='alert alert-danger',_role='alert'))            
        form.errors.item_code = 'Item code does not exist or empty.'
        
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code =  'Item code does not exist in stock file'
        
        # form.errors.item_code =  CENTER(DIV(B('DANGER! '),'Item code does not exist in stock file',_class='alert alert-danger',_role='alert'))
    # elif request.vars.item_code and request.vars.category_id == 3:
    #     response.flash = 'RECORD ADDED'

    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Return_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Return_Transaction_Temporary.item_code).first()
        _categ = db((db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Return_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Return_Transaction_Temporary.category_id).first()
        _not_allowed = db(
            (db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & 
            (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & 
            ((int(request.vars.category_id) == 1) | (int(request.vars.category_id) == 4))).select().first()
        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)     
        _item_discount = float(request.vars.discount_percentage or 0) 
        _retail_price_per_uom = _price.retail_price / _id.uom_value     
        _wholesale_price_per_uom = _price.wholesale_price / _id.uom_value
        _selective_tax_per_uom = _price.selective_tax_price / _id.uom_value
        if _not_allowed:
            # form.errors.item_code = CENTER(DIV(B('Info! '),'Not Allowed to returned both Normal/Damaged.',_class='alert alert-danger',_role='alert'))            
            form.errors.item_code = "Not Allowed to returned both Normal/Damaged."

        if not _price:
            form.errors.item_code = "Item code does'nt have price."
        if (_price.retail_price == 0.0 or _price.wholesale_price == 0.0) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.error.item_code = 'Cannot request this item because retail price/wholesale price is zero.'

        _excise_tax_amount = _selective_tax_total =_selective_tax_total_foc = 0
        _unit_price = _tax_per_uom= 0
        _total_excise_tax = _net_price= _total_amount = 0
        _selective_tax = _selective_tax_foc = _total_excist_tax_foc = 0

        if _price.selective_tax_price > 0:                        
            _tax_per_uom = _selective_tax_per_uom
        else:
            _tax_per_uom = 0

        if _exist:
            form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'            
        else:

            if int(request.vars.category_id) == 3:
                # computation for excise tax foc        
                _selective_tax = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax_foc = 0
                else:
                    _selective_tax_foc =  float(_tax_per_uom) * _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + _selective_tax_foc
                _selective_tax_total_foc += float(_tax_per_uom) * _total_pcs
            else:
                # computation for excise tax
                _selective_tax_foc = _unit_price1 = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax = 0

                else:
                    _selective_tax =  float(_selective_tax_per_uom or 0) #* _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + (float(_selective_tax or 0) * _id.uom_value)
                
                _selective_tax_total += float(_selective_tax) * _total_pcs          
                if float(_price.selective_tax_price) == 0: # without selective tax
                    _net_price = 0
                    _net_price = _unit_price - ((_unit_price * _item_discount) / 100) #+ (float(_selective_tax or 0) * _id.uom_value)
                    _total_amount = _net_price / _id.uom_value * _total_pcs                    
                else:   # with selective tax                    
                    # _net_price = 0
                    # _net_price_at_wholesale = 0.0
                    # _net_price_at_wholesale = float(_wholesale_price_per_uom) * _id.uom_value   
                    
                    _net_price = (float(_price.wholesale_price) * (100 - _item_discount) / 100) + float(_price.selective_tax_price)
                    # _net_price = _net_price_at_wholesale - ((_net_price_at_wholesale * _item_discount) / 100) + _selective_tax
                    # # print '_net_price_at_wholesale: ', _net_price_at_wholesale, _net_price                 
                    _total_amount = (_net_price / _id.uom_value) * _total_pcs                

        if _id.uom_value == 1:
            form.vars.pieces = 0
                      
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(form.vars.pieces) >= int(_id.uom_value):
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                       
                    
        # _unit_price = float(_price.retail_price) / int(_id.uom_value)
        # _total = float(_unit_price) * int(_total_pcs)

        if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):
            form.errors.quantity = 'Quantity should not be more than probational balance.'
        
        
        form.vars.item_code_id = _id.id
        form.vars.selective_tax = _selective_tax_total
        form.vars.selective_tax_foc = _selective_tax_total_foc
        form.vars.total_pieces = _total_pcs
        form.vars.price_cost = _unit_price
        form.vars.total_amount = _total_amount or 0
        form.vars.net_price = _net_price

@auth.requires_login()      
def sales_return_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(10,2)', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_return_transaction).accepted:        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'                
        _id = db(db.Item_Master.id == form.vars.item_code_id).select().first()
        _stk_des = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        db.Sales_Return_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            total_amount = form.vars.total_amount,
            discount_percentage = form.vars.discount_percentage,
            net_price = form.vars.net_price,
            category_id = form.vars.category_id,
            stock_source_id = session.stock_source_id,
            selective_tax = form.vars.selective_tax,
            selective_tax_foc = form.vars.selective_tax_foc,
            ticket_no_id = session.ticket_no_id)        
        if db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:            
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:            
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        _stk_des.stock_in_transit += int(form.vars.total_pieces)
        _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
        _stk_des.update_record()     

    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    total_amount = 0
    _selective_tax = _selective_tax_foc = net_amount =0
    _div_tax = _div_tax_foc = DIV('')
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action')),_class='bg-primary')
    
    _query = db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Return_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Sales_Return_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Return_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1      
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Sales_Return_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Sales_Return_Transaction_Temporary.id),'_data-qt':(n.Sales_Return_Transaction_Temporary.quantity), '_data-pc':(n.Sales_Return_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Sales_Return_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Sales_Return_Transaction_Temporary.id)})
        btn_lnk = DIV(dele_lnk)
        _selective_tax += n.Sales_Return_Transaction_Temporary.selective_tax
        _selective_tax_foc += n.Sales_Return_Transaction_Temporary.selective_tax_foc
        if _selective_tax > 0.0 or _selective_tax_foc > 0.0:            
            _div_tax = DIV(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('REMARKS: TOTAL SELECTIVE TAX FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True)))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')
        total_amount += n.Sales_Return_Transaction_Temporary.total_amount       
        if n.Item_Master.uom_value == 1:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_readonly=True,_value=n.Sales_Return_Transaction_Temporary.pieces or 0)
        else:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=n.Sales_Return_Transaction_Temporary.pieces or 0)
        row.append(TR(
            TD(ctr,INPUT(_type='number',_name='ctr',_hidden=True,_value=n.Sales_Return_Transaction_Temporary.id)),
            TD(n.Sales_Return_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Return_Transaction_Temporary.category_id.mnemonic),
            TD(n.Item_Master.uom_value, INPUT(_type='number',_name='uom',_value=n.Item_Master.uom_value,_hidden=True)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=n.Sales_Return_Transaction_Temporary.quantity or 0), _align = 'right', _style="width:100px;"),
            TD(_pieces, _align = 'right', _style="width:100px;"),
            TD(INPUT(_class='form-control price_cost',_type='text',_name='price_cost',_value=locale.format('%.2F',n.Sales_Return_Transaction_Temporary.price_cost or 0)), _align = 'right', _style="width:120px;"), 
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_value=n.Sales_Return_Transaction_Temporary.discount_percentage or 0), _align = 'right', _style="width:90px;"),  
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price',_value=locale.format('%.2F',n.Sales_Return_Transaction_Temporary.net_price or 0)), _align = 'right', _style="width:120px;"),  
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.2F',n.Sales_Return_Transaction_Temporary.total_amount or 0)), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount',_colspan='2', _align = 'right'),TD(INPUT(_class='form-control net_amount', _name = 'net_amount', _id='net_amount', _disabled = True, _value = locale.format('%.2F',total_amount or 0)), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount',_colspan='2', _align = 'right'),TD(INPUT(_class='form-control grand_total_amount', _name = 'grand_total_amount', _id='grand_total_amount', _disabled = True, _value = locale.format('%.2F',total_amount or 0)), _align = 'right'),TD()))    
    foot += TFOOT(TR(TD(),TD(_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD('Discount Added', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control discount',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right'),TD(P(_id='error'))))
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblSR'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            response.flash = 'RECORD UPDATED'
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _row = db(db.Sales_Return_Transaction_Temporary.id == x).select().first()
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    if _row.total_pieces != _qty:
                        _row.update_record(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], total_pieces = _qty, total_amount = request.vars.total_amount[row])
                    row+=1
            else:
                _row = db(db.Sales_Return_Transaction_Temporary.id == int(request.vars.ctr)).select().first()
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                if _row.total_pieces != _qty:
                    _row.update_record(quantity = request.vars.quantity, pieces = request.vars.pieces, total_pieces = _qty, total_amount = request.vars.total_amount)
            response.js = "$('#tblSR').get(0).reload()"
    return dict(form = form, table = table, grand = total_amount)    

@auth.requires_login()
def sales_return_transaction_temporary_delete():
    _id = db(db.Sales_Return_Transaction_Temporary.id == request.args(0)).select().first()    
    _stk_file = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()    
    _stk_file.stock_in_transit -= _id.total_pieces    
    _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
    _stk_file.update_record()        
    db(db.Sales_Return_Transaction_Temporary.id == request.args(0)).delete()
    if db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() == 0:
        response.flash = 'RECORD DELETED' 
        response.js = "$('#tblSR').get(0).reload(), jQuery('#btnsubmit').attr('disabled','disabled')"
    else:
        response.flash = 'RECORD DELETED'
        response.js = "$('#tblSR').get(0).reload()"

@auth.requires_login()
def sales_return_grid():
    row = []
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    _query = db(db.Sales_Return).select(orderby = db.Sales_Return.id)
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):        
        if not _usr:
            _query = db((db.Sales_Return.status_id == 4) & (db.Sales_Return.archives == False)).select(orderby = db.Sales_Return.id)
        else:
            _query = db((db.Sales_Return.status_id == 4) & (db.Sales_Return.archives == False) & (db.Sales_Return.dept_code_id == _usr.department_id)).select(orderby = db.Sales_Return.id)        
            
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        # if not _usr:
        #     _query = db((db.Sales_Return.status_id == 14) & (db.Sales_Return.archives == False) & (db.Sales_Return.dept_code_id != 3)).select(orderby = ~db.Sales_Return.id)
        # else:
        _query = db((db.Sales_Return.status_id == 14) & (db.Sales_Return.archives == False) & (db.Sales_Return.dept_code_id == 3)).select(orderby = db.Sales_Return.id)                    
    elif auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT'):
        _query = db((db.Sales_Return.status_id == 12) & (db.Sales_Return.archives == False)).select(orderby = db.Sales_Return.id)
    head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in _query:
        if auth.has_membership(role = 'ROOT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_mngr_grid', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_invoice_no_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sale_order_manager_invoice_no_rejected', args = n.id, extension = False))            
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_sales_manager', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_return_sales_manager_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn disabled', callback = URL('sales','sales_return_sales_manager_rejected', args = n.id, extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            
        if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            if n.status_id == 14:
                view_lnk = A(I(_class='fas fa-search'), _title='View Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_warehouse_form', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_return_warehouse_form_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('sales','sales_return_warehouse_form_reject', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle',_target='_blank', _href=URL('sales_report','get_sales_return_reports_id',args = n.id, extension = False))
        if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'):
            if n.status_id == 12:
                view_lnk = A(I(_class='fas fa-search'), _title='View Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_accounts_form', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle btnAccounts', callback = URL('sales','sales_return_accounts_form_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('sales','sales_return_accounts_form_rejected', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            # elif n.status_id == 13:
            #     view_lnk = A(I(_class='fas fa-search'), _title='View Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_accounts_form', args = n.id, extension = False))        
            #     appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     reje_lnk = A(I(_class='fas fa-times'), _title='Reject Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                
            #     prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','sales_return_report_account_user', args = n.id, extension = False))        
        if auth.has_membership(role = 'ACCOUNTS MANAGER'):
                view_lnk = A(I(_class='fas fa-search'), _title='View Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_return_accounts_form', args = n.id, extension = False))  
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_return_accounts_form_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Sales Return Request', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_return_accounts_form_rejected', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _href = URL('sales','sales_return_report_account_user', args = n.id, extension = False))        
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        row.append(TR(TD(n.sales_return_date),TD(n.transaction_prefix_id.prefix,n.sales_return_no),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ',n.customer_code_id.account_code),
            TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.sales_man_id.employee_id.first_name,' ',n.sales_man_id.employee_id.first_name),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblsrt')
    return dict(table = table)    

@auth.requires_login()
def sales_return_transaction_table():      
    ctr = 0
    row = []                
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    _id = db((db.Sales_Return.id == request.args(0)) | (db.Sales_Return.id == session.sales_return_no_id)).select().first()
    if auth.has_membership(role = 'ROOT') | auth.has_membership(role = 'SALES'):
        _query = db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(db.Sales_Return_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id))
        _id = db((db.Sales_Return.id == request.args(0)) | (db.Sales_Return.id == session.sales_return_no_id)).select().first()
    else:
        _query = db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(db.Sales_Return_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id))
        _id = db((db.Sales_Return.id == request.args(0)) | (db.Sales_Return.id == session.sales_return_no_id)).select().first()

    # _id = db(db.Sales_Order.id == session.sales_order_no_id).select().first()
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action')),_class='bg-primary')
    for n in _query:
        ctr += 1
        if auth.has_membership(role = 'INVENTORY STORE KEEPER') | auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'ACCOUNTS MANAGER'):
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
        else:
            if _id.status_id > 4:
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
            else:
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        # discount & grand total computation
        # _grand_total += float(n.Sales_Return_Transaction.total_amount or 0)
        # _discount = float(_grand_total) * int(_id.discount_percentage or 0) / 100        
        # _grand_total = float(_grand_total) - int(_discount)                
        
        # selective tax computation
        _selective_tax += n.Sales_Return_Transaction.selective_tax or 0
        _selective_tax_foc += n.Sales_Return_Transaction.selective_tax_foc or 0
        if _selective_tax > 0.0 or _selective_tax_foc > 0.0:
            _div_tax = DIV(H4('TOTAL SELECTIVE TAX: ',locale.format('%.2F', _selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('TOTAL SELECTIVE TAX FOC: ',locale.format('%.2F', _selective_tax_foc or 0, grouping = True)))
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')
        
        _grand_total += n.Sales_Return_Transaction.total_amount
        # ownership        
        if auth.user_id != n.Sales_Return_Transaction.created_by:           
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')            
        else:
            if _id.status_id == 4:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_return_edit_view', args = n.Sales_Return_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Return_Transaction.id, extension = False), **{'_data-id':(n.Sales_Return_Transaction.id)})                
            else:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')                
        
        if auth.has_membership(role = 'INVENTORY STORE KEEPER') and _id.status_id == 2:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_return_edit_view', args = n.Sales_Return_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Return_Transaction.id, extension = False), **{'_data-id':(n.Sales_Return_Transaction.id)})                
        btn_lnk = DIV(dele_lnk)        
        _qty = n.Sales_Return_Transaction.quantity / n.Sales_Return_Transaction.uom
        _pcs = n.Sales_Return_Transaction.quantity - n.Sales_Return_Transaction.quantity / n.Sales_Return_Transaction.uom * n.Sales_Return_Transaction.uom
        if int(n.Sales_Return_Transaction.uom) == 1:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs or 0, _readonly='true')
        else:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs or 0)
        _quantity = INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty or 0)
        row.append(TR(
            TD(ctr,INPUT(_type='number',_name='ctr',_value=n.Sales_Return_Transaction.id,_hidden=True)),
            TD(n.Sales_Return_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Return_Transaction.category_id.mnemonic, _style = 'width:120px'),
            TD(n.Sales_Return_Transaction.uom,INPUT(_type='number',_name='uom',_hidden=True,_value=n.Sales_Return_Transaction.uom), _style = 'width:100px'),
            TD(_quantity, _style = 'width:100px'),
            TD(_pieces, _style = 'width:100px'),
            TD(INPUT(_class='form-control price_cost',_type='text',_name='price_cost',_value=locale.format('%.2F',n.Sales_Return_Transaction.price_cost or 0)), _align = 'right', _style = 'width:140px'),  
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_value=locale.format('%d',n.Sales_Return_Transaction.discount_percentage or 0)), _align = 'right', _style = 'width:100px'),  
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price',_value=locale.format('%.2F',n.Sales_Return_Transaction.net_price or 0)), _align = 'right', _style = 'width:100px'),  
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.2F',n.Sales_Return_Transaction.total_amount or 0)), _align = 'right', _style = 'width:100px'),  
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control net_total',name='net_total',_id='net_amount',_value=locale.format('%.2F',_id.total_amount_after_discount or 0)), _align = 'right', _style="width:120px;"),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control total_amount',name='total_amount',_id='total_amount',_value=locale.format('%.2F',_id.total_amount or 0)), _align = 'right', _style="width:120px;"),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount Added', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control discount',_type='number',_id='discount',_name='discount',_value=_id.discount_added or 0), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblSR')
    # table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblSR'))
    # if table.accepts(request, session):
    #     if request.vars.btnUpdate:
    #         response.flash = 'RECORD UPDATED'
    #         if isinstance(request.vars.ctr, list):
    #             row = 0
    #             for x in request.vars.ctr:
    #                 _row = db(db.Sales_Return_Transaction.id == x).select().first()
    #                 _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
    #                 if _row.quantity != _qty:
    #                     _row.update_record(quantity = _qty, total_amount = request.vars.total_amount[row])
    #                 row+=1
    #         else:
    #             _row = db(db.Sales_Return_Transaction.id == int(request.vars.ctr)).select().first()
    #             _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
    #             if _row.quantity != _qty:
    #                 _row.update_record(quantity = _qty, total_amount = request.vars.total_amount)
    #         response.js = "$('#tblSR').get(0).reload()"
    return dict(table = table)       

@auth.requires_login()
def validate_sales_return_edit_view(form):
    _id = db(db.Sales_Return_Transaction.id == request.args(0)).select().first()
    _so = db(db.Sales_Return.id == _id.sales_return_no_id).select().first()
    _sf = db((db.Stock_File.item_code_id == _id.id) &(db.Stock_File.location_code_id == _so.location_code_id)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    if _qty >= _sf.closing_stock:
        form.errors.quantity = 'Total quantity should not be more than the stock file.'
    if int(request.vars.pieces) >= int(_id.uom):
        form.errors.quantity = 'Total quantity should not be more than UOM value.'
    form.vars.quantity = _qty
    _old_stock_in_transit = _sf.stock_in_transit - _id.quantity
    _old_probational_balance = _sf.closing_stock - _old_stock_in_transit
    _sf.update_record(stock_in_transit = _old_stock_in_transit)

@auth.requires_login()
def sales_return_edit_view():
    _id = db(db.Sales_Return_Transaction.id == request.args(0)).select().first()
    _so = db(db.Sales_Return.id == _id.sales_return_no_id).select().first()
    _sf = db((db.Stock_File.item_code_id == _id.id) &(db.Stock_File.location_code_id == _so.location_code_id)).select().first()
    _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom
    _total = 0
    form = SQLFORM.factory(
        Field('quantity', 'integer', default = _qty),
        Field('pieces', 'integer', default = _pcs))
    if form.process(onvalidation = validate_sales_return_edit_view).accepted:
        _price_per_piece = _id.net_price / _id.uom
        _total_amount = form.vars.quantity * _price_per_piece
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id, total_amount = _total_amount)
        for n in db((db.Sales_Return_Transaction.sales_return_no_id == _so.id) & (db.Sales_Return_Transaction.delete == False)).select():
            _total += n.total_amount
        _discount = float(_total) * int(_so.discount_percentage or 0) / 100
        _total_amount_after_discount = float(_total) - int(_discount)
        _so.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount)
        _nsit = _sf.stock_in_transit + _qty
        _sf.update_record(stock_in_transit = _nsit)
        session.flash = 'RECORD UPDATED'
        if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            redirect(URL('sales','sales_return_warehouse_form', args = _so.id)) # sales/sales_return_warehouse_form/2
        else:
            redirect(URL('sales_return_browse_load_view', args = _so.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('sales_return_browse_load_view', args = _so.id))
    return dict(form = form, btn_back = btn_back)    

@auth.requires_login()
def sales_return_delete_view_():
    print 'delete: ', request.args(0)
    _id = db(db.Sales_Return_Transaction.id == request.args(0)).select().first()
    _id.update_record(delete = True)

@auth.requires_login()
def sales_return_delete_view_():
    _id = db(db.Sales_Return_Transaction.id == request.args(0)).select().first()
    _so = db(db.Sales_Return.id == _id.sales_return_no_id).select().first()    

    # check if only 1 remaining to remove
    if db((db.Sales_Return_Transaction.sales_return_no_id == _so.id) & (db.Sales_Return_Transaction.delete == False)).count() == 1:
        response.js = 'jQuery(autoCancel())'
    else:
        print 'more '

@auth.requires_login()
def sales_return_delete_view():
    # check if only 1 remaining to remove
    # if db((db.Sales_Return_Transaction.sales_return_no_id == _so.id) & (db.Sales_Return_Transaction.delete == False)).count() == 1:
    #     print 'are you sure?'
    # else:
    #     print 'more '
    # initialization of variable    
    _id = db(db.Sales_Return_Transaction.id == request.args(0)).select().first()
    _so = db(db.Sales_Return.id == _id.sales_return_no_id).select().first()    
    _stk_des = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _so.location_code_id)).select().first()    
    
    # update the stock file table
    
    _stk_des.stock_in_transit -= int(_id.quantity)
    _stk_des.probational_balance = int(_stk_des.closing_stock) - int(_stk_des.stock_in_transit)
    _stk_des.update_record()
    
    # update the sales order transaction table
    
    _id.update_record(delete = True)
    
    # generate re-computation in sales order transaction table
    
    _total = _selective_tax = _selective_tax_foc = 0
    for n in db((db.Sales_Return_Transaction.sales_return_no_id == _id.sales_return_no_id) & (db.Sales_Return_Transaction.delete == False)).select():
        _total += float(n.total_amount or 0)
        _selective_tax += float(n.selective_tax or 0)
        _selective_tax_foc += float(n.selective_tax_foc or 0)
    # _discount = float(_total) * int(_so.discount_percentage or 0) / 100
    _trnx = db((db.Sales_Return_Transaction.sales_return_no_id == _so.id) & (db.Sales_Return_Transaction.delete == False)&(db.Sales_Return_Transaction.discounted==False) & (db.Sales_Return_Transaction.category_id==4)).select(orderby = db.Sales_Return_Transaction.id).first()
    if _trnx:
        if float(_so.discount_added or 0):
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom)) - float(_so.discount_added or 0)) / int(_trnx.uom)        
            _trnx.update_record(discounted = True, sale_cost = _sale_cost, discount_added=_so.discount_added)
    
    # update the sales order table    
    _total_amount_after_discount = _total - float(_so.discount_added or 0)
    
    if db((db.Sales_Return_Transaction.sales_return_no_id == _so.id) & (db.Sales_Return_Transaction.delete == False)).count() == 0:                
        _so.update_record(status_id = 10, total_amount = _total, total_amount_after_discount = _total_amount_after_discount, selective_tax = _selective_tax, selective_tax_foc = _selective_tax_foc)
        session.flash = 'RECORD DELETED'    
        response.js = "jQuery(redirect())"
    else:        
        _so.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount, selective_tax = _selective_tax, selective_tax_foc = _selective_tax_foc)
        session.flash = 'RECORD DELETED'    
        # response.js = "$('#tblSR').get(0).reload()"

@auth.requires_login()
def sales_return_form_abort():
    _query = db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select()
    if not _query:
        session.flash = 'ABORT'
    else:        
        for n in _query:
            _id = db(db.Item_Master.id == n.item_code_id).select().first()
            _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()            
            _s.stock_in_transit -= n.total_pieces
            _s.probational_balance = int(_s.closing_stock) - int(_s.stock_in_transit)
            _s.update_record()
            db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).delete()            
        session.flash = 'ABORT'

# ----------  M A N A G E R ' S   G R I D   ----------
# 1 sales invoiced all users approved
# 1-1 sales invoice by users approved
# 2 delivery note all users approved/pending
# 2-1 delivery note by users approved/pending
# 3 sales order all users requested
# 3-1 sales order by user requested
# 4 sales return all users approved
# 4-1 sales return 

def get_workflow_reports(): 
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    row = []
    if int(request.args(0)) == int(1): # sales invoiced
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            title = 'Sales Order Workflow Report'
            head = THEAD(TR(TH('Date'),TH('Sales Invoice No.'),TH('Delivery Note No.'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
            _query = db((db.Sales_Invoice.sales_order_approved_by == auth.user_id) & (db.Sales_Invoice.status_id == 7)).select(orderby = ~db.Sales_Invoice.id)
        elif auth.has_membership(role = 'SALES'):
            title = 'Sales Invoice Workflow Report'
            head = THEAD(TR(TH('Date'),TH('Sales Invoice No.'),TH('Delivery Note No.'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
            _query = db((db.Sales_Invoice.sales_man_id == _usr.id) & (db.Sales_Invoice.status_id == 7)).select(orderby = ~db.Sales_Invoice.id)
        elif auth.has_membership(role = 'ACCOUNTS'):
            title = 'Sales Invoice Workflow Report'
            head = THEAD(TR(TH('Date'),TH('Sales Invoice No.'),TH('Delivery Note No.'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
            _query = db((db.Sales_Invoice.status_id == 7) & (db.Sales_Invoice.sales_invoice_approved_by == auth.user_id)).select(orderby = ~db.Sales_Invoice.id)
        elif auth.has_membership(role = 'MANAGEMENT'):
            title = 'Sales Invoice Workflow Report'
            _query = db(db.Sales_Invoice.status_id == 7).select(orderby = ~db.Sales_Invoice.id)        
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            title = 'Sales Invoice Master Report'
            head = THEAD(TR(TH('Date'),TH('Sales Invoice No.'),TH('Delivery Note No.'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
            _query = db((db.Sales_Invoice.dept_code_id == 3) & (db.Sales_Invoice.status_id == 7)).select(orderby = ~db.Sales_Invoice.id)
        # else:
        #     title = 'DELIVERY NOTE GRID'
        #     _query = db((db.Delivery_Note.dept_code_id == 3) & ((db.Delivery_Note.status_id == 7) | (db.Delivery_Note.status_id == 8))).select(orderby = ~db.Delivery_Note.id)
        #     head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
        for n in _query:
            prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('sales','sales_order_delivery_note_report_store_keeper', args = n.id))
            if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_workflow_reports_id', args = [1, n.id]))
                prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('delivery_note_reports','get_workflow_delivery_reports_id', args = n.id))
            elif auth.has_membership(role = 'SALES') | auth.has_membership(role = 'INVENTORY SALES MANAGER'):                
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_workflow_reports_id', args = [1, n.id]))
            elif auth.has_membership(role = 'ACCOUNTS'):                
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_workflow_reports_id', args = [1, n.id]))
                prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('default','get_workflow_sales_invoice_reports_id', args = n.id))
            # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('sales','get_workflow_reports_id', args = n.id))                
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))

            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            if not n.transaction_prefix_id:
                _sales = 'None'
            else:
                _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
                _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
            if not n.delivery_note_no_prefix_id:
                _note = 'None'
            else:
                _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
                _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
            if not n.sales_invoice_no_prefix_id:
                _inv = 'None'            
            else:
                _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
                _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})        
            if auth.has_membership(role = 'ACCOUNTS') | auth.has_membership(role = 'INVENTORY STORE KEEPER') | auth.has_membership(role = 'MANAGEMENT'):
                row.append(TR(
                    TD(n.sales_invoice_date_approved.date()),                    
                    TD(_inv),
                    TD(_note),
                    TD(_sales),                                        
                    TD(n.dept_code_id.dept_name),                
                    TD(n.stock_source_id.location_name),
                    TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
                    TD(n.sales_man_id.employee_id.first_name.upper(), ' ',n.sales_man_id.employee_id.last_name.upper()),
                    TD(n.status_id.description),
                    TD(n.status_id.required_action),
                    TD(btn_lnk)))
            else:
                row.append(TR(
                    TD(n.sales_invoice_date_approved.date()),
                    TD(_inv),                    
                    TD(_note),
                    TD(_sales),
                    TD(n.dept_code_id.dept_name),                
                    TD(n.stock_source_id.location_name),
                    TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
                    TD(n.sales_man_id.employee_id.first_name.upper(), ' ',n.sales_man_id.employee_id.last_name.upper()),
                    TD(n.status_id.description),
                    TD(n.status_id.required_action),
                    TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='tblSO')                        
    elif int(request.args(0)) == int(2): # sales return
        title = 'SALES RETURN GRID'
        row = []
        _dept = db(db.User_Department.user_id == auth.user_id).select().first()
        if not _dept:
            _query = db((db.Sales_Return.archives == False) & (db.Sales_Return.dept_code_id != 3)).select(orderby = ~db.Sales_Return.id)
        else:
            _query = db((db.Sales_Return.archives == False) & (db.Sales_Return.dept_code_id == 3)).select(orderby = ~db.Sales_Return.id)   
        if auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT'):
            _query = db(db.Sales_Return.status_id == 13).select(orderby = ~db.Sales_Return.id)   
        elif auth.has_membership(role = 'ACCOUNTS'):             
            _query = db(db.Sales_Return.accounts_id == auth.user_id).select(orderby = ~db.Sales_Return.id)   
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            _query = db(db.Sales_Return.warehouse_id == auth.user_id).select(orderby = ~db.Sales_Return.id)
        elif auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            _query = db(db.Sales_Return.sales_manager_id == auth.user_id).select(orderby = ~db.Sales_Return.id)
        elif auth.has_membership(role = 'SALES'):
            _query = db(db.Sales_Return.sales_man_id == _usr.id).select(orderby = ~db.Sales_Return.id)
        head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-warning'))
        for n in _query:  
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_sales_return_workflow_report_view', args = n.id, extension = False))            
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _target='blank', _class='btn btn-icon-toggle', _href=URL('sales_report','get_sales_return_reports_id', args = n.id))                
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk) 
            row.append(TR(TD(n.sales_return_date),TD(n.transaction_prefix_id.prefix,n.sales_return_no),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='tblSR')
    elif int(request.args(0)) == int(3): # show delivery note all approved complete/incomplete by users
        title = 'Delivery Note Workflow Report'
        _query = db((db.Delivery_Note.dept_code_id == 3) & (db.Delivery_Note.delivery_note_approved_by == auth.user_id) & ((db.Delivery_Note.status_id == 7) | (db.Delivery_Note.status_id == 8))).select(orderby = ~db.Delivery_Note.id)
        head = THEAD(TR(TH('Date'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Approved By'),TH('Action'), _class='bg-primary'))
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_workflow_reports_id', args = [2, n.id]))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('delivery_note_reports','get_workflow_delivery_reports_id', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
            if not n.sales_invoice_no_prefix_id:
                _inv = 'None'            
            else:
                _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
                _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})        
            row.append(TR(
                TD(n.delivery_note_date_approved.date()),
                TD(_note),                                
                TD(_inv),
                TD(_sales),
                TD(n.dept_code_id.dept_name),
                # TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
                TD(n.stock_source_id.location_name),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
                TD(n.sales_man_id.employee_id.first_name.upper(), ' ',n.sales_man_id.employee_id.last_name.upper()),
                TD(n.status_id.description),
                TD(n.delivery_note_approved_by.first_name, ' ', n.delivery_note_approved_by.last_name),
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='tblDN')   
    elif int(request.args(0)) == int(4): # show delivery note all approved complete/incomplete 
        title = 'Delivery Note Master Report'
        _query = db(db.Delivery_Note.dept_code_id == 3).select(orderby = db.Delivery_Note.id)
        head = THEAD(TR(TH('Date'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Approved By'),TH('Action'), _class='bg-primary'))
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','get_workflow_reports_id', args = [2, n.id]))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('sales','sales_order_delivery_note_report_store_keeper', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
            if not n.sales_invoice_no_prefix_id:
                _inv = 'None'            
            else:
                _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
                _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})        
            row.append(TR(
                TD(n.delivery_note_date_approved.date()),
                TD(_note),                                
                TD(_inv),
                TD(_sales),
                TD(n.dept_code_id.dept_name),
                # TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
                TD(n.stock_source_id.location_name),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
                TD(n.sales_man_id.employee_id.first_name.upper(), ' ',n.sales_man_id.employee_id.last_name.upper()),
                TD(n.status_id.description),
                TD(n.delivery_note_approved_by.first_name, ' ', n.delivery_note_approved_by.last_name),
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='tblDN')           
    elif int(request.args(0)) == int(5): # sales order cancelled/rejected
        if auth.has_membership(role = 'SALES'):
            title = 'Sales Order Workflow Report'

            head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
            _query = db(db.Sales_Order.sales_man_id == _usr.id).select(orderby = ~db.Sales_Order.id)
            for n in _query:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('sales','get_workflow_reports_id', args = [1, n.id]))
                prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('default','get_workflow_sales_invoice_reports_id', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))

                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)

                if not n.transaction_prefix_id:
                    _sales = 'None'
                else:
                    _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
                    _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
                if not n.delivery_note_no_prefix_id:
                    _note = 'None'
                else:
                    _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
                    _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
                if not n.sales_invoice_no_prefix_id:
                    _inv = 'None'            
                else:
                    _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
                    _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})                        
                row.append(TR(
                    TD(n.sales_order_date),
                    TD(_sales),
                    TD(n.dept_code_id.dept_name),                
                    TD(n.stock_source_id.location_name),
                    TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
                    TD(n.sales_man_id.employee_id.first_name.upper(), ' ',n.sales_man_id.employee_id.last_name.upper()),
                    TD(n.status_id.description),
                    TD(n.status_id.required_action),
                    TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='tblSO')                                
    else:
        title = table = ''        
    return dict(title = title, table = table)

def get_sales_return_workflow_report_view():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    return dict(_id = _id)

def get_sales_order_grid():
    row = []
    # _query = db(db.Sales_Order.status_id == 7).select(orderby = ~db.Sales_Order.id)
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    if not _usr:
        _query = db(db.Sales_Order.dept_code_id != 3).select(db.Sales_Order.ALL, orderby = ~db.Sales_Order.id)
    else:
        _query = db(db.Sales_Order.dept_code_id == _usr.department_id).select(db.Sales_Order.ALL, orderby = ~db.Sales_Order.id)
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})        
        row.append(TR(
            TD(n.sales_order_date),
            TD(_sales),
            TD(_note),
            TD(_inv),
            TD(n.dept_code_id.dept_name),
            # TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
            TD(n.stock_source_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblso')
    return dict(table = table)
   
def get_workflow_reports_id():
    if int(request.args(0)) == 1:        
        title = 'Sales Invoice Workflow Report'
        # print '- sales invoice'
        _id = db(db.Sales_Invoice.id == request.args(1)).select().first()
    elif int(request.args(0)) == 2:        
        title = 'Delivery Note Workflow Report'
        # print '- delivery note'
        _id = db(db.Delivery_Note.id == request.args(1)).select().first()
    return dict(_id = _id, title=title)


def get_workflow_reports_transaction_id_():
    if int(request.args(0)) == 1:        
        _id = db(db.Sales_Invoice.id == request.args(1)).select().first()
        print 'sales invoice transaction', _id.id
        _query = db(db.Sales_Invoice_Transaction.sales_invoice_no_id == request.args(1)).select()
        for n in _query:
            _i = db(db.Item_Master.id == n.item_code_id).select().first()
            print n.id, _i.item_code

    elif int(request.args(0)) == 2:                
        _id = db(db.Delivery_Note.id == request.args(1)).select().first()
        print 'delivery note transaction', _id.id
        _query = db(db.Delivery_Note_Transaction.delivery_note_id == request.args(1)).select()
        for n in _query:
            _i = db(db.Item_Master.id == n.item_code_id).select().first()
            print n.id, _i.item_code

def get_workflow_reports_transaction_id():
    ctr = 0
    row = []                
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc =  DIV('')

    if int(request.args(0)) == 1: # sales invoice workflow report
        _id = db(db.Sales_Invoice.id == request.args(1)).select().first()
        _query = db(db.Sales_Invoice_Transaction.sales_invoice_no_id == request.args(1)).select()
    elif int(request.args(0)) == 2: # delivery note workflow report
        _id = db(db.Delivery_Note.id == request.args(1)).select().first()
        _query = db(db.Delivery_Note_Transaction.delivery_note_id == request.args(1)).select()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),_class='bg-primary'))
    for n in _query:
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        ctr += 1
        _grand_total += float(n.total_amount or 0)
        # _discount = float(_grand_total) * int(_id.discount_added or 0) / 100
        _net_amount = float(_grand_total) - float(_id.discount_added or 0)
        
        # selective tax computation
        _selective_tax += n.selective_tax or 0
        _selective_tax_foc += n.selective_tax_foc or 0
        
        if _selective_tax > 0.0:
            _div_tax = DIV(H4('Total Selective Tax: ',locale.format('%.2F', _selective_tax or 0, grouping = True)))            
        else:
            _div_tax = DIV('')

        if _selective_tax_foc > 0.0:
            _div_tax_foc = DIV(H4('Total Selective Tax FOC: ',locale.format('%.2F', _selective_tax_foc or 0, grouping = True)))
        else:
            _div_tax_foc = DIV('')

        _qty = n.quantity / n.uom        
        _pcs = n.quantity - n.quantity / n.uom * n.uom        
        
        _cst = (n.price_cost * n.uom) + (n.selective_tax / n.uom)

        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(_i.brand_line_code_id.brand_line_name),
            TD(_i.item_description),
            TD(n.category_id.mnemonic, _style = 'width:120px'),
            TD(n.uom, _style = 'width:120px'),
            TD(_qty, _style = 'width:80px'),
            TD(_pcs, _style = 'width:80px'),
            TD(locale.format('%.2F',n.price_cost or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%d',n.discount_percentage), _align = 'right', _style = 'width:80px'),
            TD(locale.format('%.2F',n.net_price or 0, grouping = True), _align = 'right', _style = 'width:100px'),
            TD(locale.format('%.2F',n.total_amount or 0,grouping = True), _align = 'right', _style = 'width:100px')))
        _total_amount += n.total_amount
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True), _align = 'right')))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc, _colspan='3'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F', _id.total_amount or 0, grouping = True), _align = 'right')))    
    foot += TFOOT(TR(TD(),TD(_div_tax, _colspan='3'),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:', _align = 'right',_colspan='2'),TD(locale.format('%.2F',_id.discount_added or 0, grouping = True), _align = 'right')))
    table = TABLE(*[head, body, foot], _class='table table-striped')
    return dict(table = table)        
# @auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ACCOUNT USERS') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
@auth.requires_login()
def sales_order_manager_grid():
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()    
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        if not _usr:
            _query = db(db.Sales_Order.status_id == 4).select(orderby = ~db.Sales_Order.id)                
        elif _usr.section_id == 'N':            
            _query = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.section_id == 'N') & (db.Sales_Order.cancelled == False) & (db.Sales_Order.dept_code_id == _usr.department_id)).select(orderby = ~db.Sales_Order.id)            
        else:        
            _query = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.section_id == 'F') & (db.Sales_Order.cancelled == False) & (db.Sales_Order.dept_code_id == _usr.department_id)).select(orderby = ~db.Sales_Order.id)    
        head = THEAD(TR(TH('#'),TH('Date'),TH('Sales Order No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        # if not _usr:            
        #     print 'not usr'
        #     _query = db(((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 8)) & (db.Sales_Order.dept_code_id != 3)).select(orderby = ~db.Sales_Order.id)
        # else:
        #     print 'in usr'
        _query = db(((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 1)) & (db.Sales_Order.dept_code_id == 3) & (db.Sales_Order.cancelled == False)).select(orderby = db.Sales_Order.delivery_note_no)
        head = THEAD(TR(TH('#'),TH('Date'),TH('Sales Order No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))        
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
        _query = db((db.Sales_Order.status_id == 8)).select(orderby = ~db.Sales_Order.id)
        head = THEAD(TR(TH('#'),TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    elif auth.has_membership(role = 'ACCOUNTS') | auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT'):
        _query = db((db.Sales_Order.status_id == 8) & (db.Sales_Order.cancelled == False)).select(orderby = db.Sales_Order.delivery_note_no)
        head = THEAD(TR(TH('#'),TH('Date'),TH('Delivery Note No.'),TH('Sales Order No.'), TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    else:
        _query = db(db.Sales_Order).select(orderby = ~db.Sales_Order.id)
        head = THEAD(TR(TH('#'),TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    row = []
    ctr = 0
    for n in _query:       
        ctr+=1
        edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
        clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled') 
        appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                    
        reje_lnk = A(I(_class='fas fa-user-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'ROOT'):
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_manager_view', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_approved', args = n.id, extension = False))            
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_rejected', args = n.id, extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _title="Print Sales Order", _type='button ', _target='blank', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_report_store_keeper', args = n.id, extension = False))  
            # clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            if n.status_id == 4:
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_manager_view', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_approved', args = n.id, extension = False))            
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btnSalesMngr disabled')#, callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            else:
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_manager_view', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('sales','sales_order_manager_approved', args = n.id, extension = False))            
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled') #, callback = URL('sales','sales_order_manager_rejected', args = n.id, extension = False))

        if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            if (n.status_id == 9) or (n.status_id == 1): 
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_store_keeper_view', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Generate Delivery Note', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sale_order_manager_delivery_note_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btnDelivery disabled')#, callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
                prin_lnk = A(I(_class='fas fa-print'), _title="Print Sales Order", _type='button ', _target='blank', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_report_store_keeper', args = n.id, extension = False))  
                # clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')       
            elif n.status_id == 8:
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_store_keeper_view', args = n.id, extension = False))        
                # appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
                # reje_lnk = A(I(_class='fas fa-user-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                                   
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Delivery Note',_type='button ', _target='blank', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_delivery_note_report_store_keeper', args = n.id, extension = False))  
                # clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')          
        if auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'ACCOUNTS') | auth.has_membership(role = 'MANAGEMENT'):
            if n.status_id == 8:
                edit_lnk = A(I(_class='fas fa-search'), _title='View Delivery Note', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view_account_user', args = n.id, extension = False))        
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Generate Sales Invoice', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('sales','sales_order_manager_invoice_no_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Delivery Note', _type='button ', _role='button', _class='btn btn-icon-toggle btnInvoice disabled')#, callback = URL('sales','sale_order_manager_invoice_no_rejected', args = n.id, extension = False), **{'_data-id':(n.id)})        
            elif n.status_id == 7:            
                edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','sales_order_view_account_user', args = n.id, extension = False))        
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _target='blank', _role='button', _class='btn btn-icon-toggle',  _href = URL('sales','sales_order_report_account_user', args = n.id, extension = False))   
        
        btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk)  
        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'):            
            row.append(TR(TD(ctr),TD(n.sales_order_date),TD(_sales),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            row.append(TR(TD(ctr),TD(n.sales_order_date),TD(_sales),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        elif auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'ACCOUNTS') | auth.has_membership(role = 'MANAGEMENT'):            
            row.append(TR(TD(ctr),TD(n.delivery_note_date_approved.date()),TD(_note),TD(_sales),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))        
        else:            
            row.append(TR(TD(ctr),TD(n.sales_order_date),TD(_sales),TD(_note),TD(_inv),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_code,' - ',n.customer_code_id.account_name),TD(n.stock_source_id.location_name),TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
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
    get_sales_order_header_writable_false()
    db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 7) | (db.Stock_Status.id == 8)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 8
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        # redirect(URL('inventory', 'str_kpr_grid'))
    elif form.errors:
        # print form.errors
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

def validate_store_keeper(form):
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    if form.vars.status_id == 1:
        print 'on hold'
        form.vars.delivery_note_date_approved = request.now
        form.vars.delivery_note_approved_by = auth.user_id          

    elif form.vars.status_id == 3:
        print 'rejected'
        form.vars.delivery_note_date_approved = request.now
        form.vars.delivery_note_approved_by = auth.user_id          
    else:
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'DLV')).select().first()    
        _skey = _trns_pfx.current_year_serial_key
        _skey += 1
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
        form.vars.delivery_note_no_prefix_id = _trns_pfx.id
        form.vars.delivery_note_no = _skey
        form.vars.delivery_note_date_approved = request.now
        form.vars.delivery_note_approved_by = auth.user_id          

def sales_order_store_keeper_view():
    get_sales_order_header_writable_false()
    db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 9)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 9
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if int(_id.status_id) == 9 or (int(_id.status_id) == 8) or (int(_id.status_id) == 1): 
        form = SQLFORM(db.Sales_Order, request.args(0))
        form.process(onvalidation = validate_store_keeper, detect_record_change=True)
        if form.record_changed:        
            session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.delivery_note_approved_by.first_name)
            redirect(URL('inventory', 'str_kpr_grid'))
        elif form.accepted:    
            session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' process.'
            response.js = 'jQuery(redirect())'            
        elif form.errors:
            response.flash = 'FORM HAS ERROR'            
        
    else:        
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.delivery_note_approved_by.first_name)
        redirect(URL('inventory','str_kpr_grid'))

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
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id == 9:
        response.flash = 'already process'
    else:
        for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
            _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
            # print n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost
            if n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost:
                _id.update_record(cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')
                get_sales_order_trnx_redo_id()
                session.flash ='Price Discrepancies.'                
                redirect(URL('inventory','mngr_req_grid'))
        form.vars.sales_order_date_approved = request.now
        form.vars.sales_order_approved_by = auth.user_id
        form.vars.status_id = 9

def get_validate_sales_order_trnx_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
        if n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost:                        
            return False

def get_sales_order_trnx_redo_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == _id.id).select(orderby = db.Sales_Order_Transaction.id)
    for n in _query:
        _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _s.stock_in_transit += int(n.quantity)
        _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)
        _s.update_record()    

def get_sales_order_header_writable_false():
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_amount_after_discount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_selective_tax_foc.writable = False
    db.Sales_Order.discount_added.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.section_id.writable = False    
    db.Sales_Order.sales_man_id.writable = False
def sales_order_manager_view():
    get_sales_order_header_writable_false()
    db.Sales_Order.status_id.writable = False           
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Sales_Order, request.args(0)) # check who approved and date/time, onvalidation = validate_mngr_approved
    form.process(onvalidation = validate_mngr_approved, detect_record_change=True)    
    if form.record_changed: # flash record detection
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.sales_order_approved_by.first_name)        
        redirect(URL('inventory', 'mngr_req_grid'))    
    elif form.accepted:# flash record approved        
        session.flash = 'Sales Order Processed'
        redirect(URL('inventory', 'mngr_req_grid'))
    elif form.errors: # flash error        
        response.flash = 'Form has error.'    
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

def sales_order_manager_approved():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id != 4:
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.sales_order_approved_by.first_name)
        response.js = "$('#tblso').get(0).reload()"
    else:
        if get_validate_sales_order_trnx_id() == False:
            _id.update_record(cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')
            get_sales_order_trnx_redo_id()
            session.flash ='Price Discrepancies.'                
            redirect(URL('inventory','mngr_req_grid'))
        else:
            _id.update_record(status_id = 9, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)
            session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' approved.'
            response.js = "$('#tblso').get(0).reload()"

def sales_order_manager_rejected():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id == 3:
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.sales_order_approved_by.first_name)        
        response.js = "$('#tblso').get(0).reload()"        
    elif _id.status_id != 3:        
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' rejected.'
        _id.update_record(status_id = 3, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)        
        response.js = "$('#tblso').get(0).reload()"

def sales_order_manager_view_rejected():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()           
    if _id.status_id == 4:        
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' rejected.'
        _id.update_record(status_id = 3, sales_order_date_approved = request.now, sales_order_approved_by = auth.user_id)        
    else:        
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.sales_order_approved_by.first_name)
    redirect(URL('inventory','mngr_req_grid'))
    
def sale_order_manager_delivery_note_approved_form():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id == 8:
        # print '==8', _id.id, _id.status_id
        session.flash = 'Delivery Note No. ' + str(_id.delivery_note_no) + ' already been prepared by ' + str(_id.delivery_note_approved_by.first_name)
        response.js = "jQuery(window.location.reload())"
    elif (_id.status_id == 1) and (_id.delivery_note_approved_by != auth.user_id):
        # print '<8'
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' is on hold by ' + str(_id.delivery_note_approved_by.first_name)
        response.js = "jQuery(redirect())"
    else:        
        _val = get_delivery_note_validation(1)
        if _val != 1:        
            _id.update_record(status_id = 10, cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')
            get_sales_order_trnx_redo(int(_id.id))                          
            response.js = "jQuery(redirect())"
        else:
            get_generate_delivery_note_id()            
            sync_to_delivery_note_db()            
            session.flash = 'Sales order processed.' 
            response.js = "jQuery(report(),redirect())"
        # else:            
    

def get_sales_order_trnx_redo(x):
    _id = db(db.Sales_Order.id == int(x)).select().first()
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == _id.id).select(orderby = db.Sales_Order_Transaction.id)
    session.flash ='Price Discrepancies.'                
    for n in _query:
        _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _s.stock_in_transit += int(n.quantity)
        _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)
        _s.update_record()    
    

def sale_order_manager_delivery_note_approved():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id == 8:
        # response.flash = 'ALREADY ORDERED'
        response.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.delivery_note_approved_by.first_name)
        response.js = "$('#tblso').get(0).reload()"
    elif (_id.status_id == 1) and (_id.delivery_note_approved_by != auth.user_id):
        # print '<8'
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' is on hold by ' + str(_id.delivery_note_approved_by.first_name) 
        response.js = "$('#tblso').get(0).reload()" 
    else:                
        if get_validate_sales_order_trnx_id() == False:
            get_sales_order_trnx_redo(_id.id)
            _id.update_record(cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')            
            response.js = "$('#tblso').get(0).reload()"
        else:            
            get_generate_delivery_note_id()            
            sync_to_delivery_note_db()                 
            response.js = "$('#tblso').get(0).reload(), PrintDeliveryNote(%s)" % (request.args(0)) 


def get_delivery_note_validation(x):       
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        # print n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost
        # print n.wholesale_price, _i.wholesale_price , n.retail_price,_i.retail_price, n.average_cost,_i.average_cost
        if n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost:
            return 2
        else:
            return 1
    
def get_generate_delivery_note_id():
    # print 'get_generate_delivery_note_id'
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'DLV')).select().first()    
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
    _id.update_record(status_id = 8, delivery_note_no_prefix_id = _trns_pfx.id, delivery_note_no = _skey, delivery_note_approved_by = auth.user_id, delivery_note_date_approved = request.now,)    
    session.flash = 'Delivery Note No. ' + str(_id.delivery_note_no) + ' processed.'

def sync_to_delivery_note_db():    
    # print 'sync_to_delivery_note_db'
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    db.Delivery_Note.insert(
        transaction_prefix_id = _id.transaction_prefix_id,
        sales_order_no = _id.sales_order_no,
        sales_order_date = _id.sales_order_date,
        dept_code_id = _id.dept_code_id,
        stock_source_id = _id.stock_source_id,
        customer_code_id = _id.customer_code_id,
        customer_order_reference = _id.customer_order_reference,
        delivery_due_date = _id.delivery_due_date,
        total_amount = _id.total_amount,
        total_amount_after_discount = _id.total_amount_after_discount,
        total_selective_tax = _id.total_selective_tax,
        total_selective_tax_foc = _id.total_selective_tax_foc,
        discount_added = _id.discount_added,
        total_vat_amount = _id.total_vat_amount,
        sales_order_date_approved = _id.sales_order_date_approved,
        sales_order_approved_by = _id.sales_order_approved_by,
        remarks = _id.remarks,
        delivery_note_no_prefix_id = _id.delivery_note_no_prefix_id,
        delivery_note_no = _id.delivery_note_no,
        delivery_note_approved_by = _id.delivery_note_approved_by,
        delivery_note_date_approved = _id.delivery_note_date_approved,
        section_id = _id.section_id,
        sales_man_id = _id.sales_man_id,
        status_id = _id.status_id)
    _dn = db(db.Delivery_Note.delivery_note_no == _id.delivery_note_no).select().first()
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        # _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        # print 'sales order transaction', n.sales_order_no_id, 
        db.Delivery_Note_Transaction.insert(
            delivery_note_id = _dn.id,
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            uom = n.uom,
            price_cost  = n.price_cost,
            packet_price_cost = n.packet_price_cost,
            total_amount = n.total_amount,
            average_cost = n.average_cost,
            sale_cost = n.sale_cost,
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price,
            discount_percentage = n.discount_percentage,
            net_price = n.net_price,
            price_cost_pcs = (n.price_cost / n.uom),
            average_cost_pcs = (n.average_cost / n.uom),
            wholesale_price_pcs = (n.wholesale_price / n.uom),
            retail_price_pcs = (n.retail_price / n.uom),
            selective_tax = n.selective_tax,
            selective_tax_foc = n.selective_tax_foc,
            packet_selective_tax = n.packet_selective_tax,
            packet_selective_tax_foc = n.packet_selective_tax_foc,
            vat_percentage = n.vat_percentage)

def sale_order_manager_delivery_note_rejected():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, delivery_note_date_approved = request.now, delivery_note_approved_by = auth.user_id)
    session.flash = 'DELIVERY NOTE REJECTED'
    response.js = "$('#tblso').get(0).reload()"

def sales_order_manager_invoice_no_approved():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id == 7:        
        response.flash = 'Sales Invoice No. ' + str(_id.sales_invoice_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.sales_invoice_approved_by.first_name)
        response.js = '$("#tblso").get(0).reload()'
    else:
        _val = get_sales_invoice_validation(1)
        if _val == 2:
            _id.update_record(status_id = 10,cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')
            db(db.Delivery_Note.sales_order_no == _id.sales_order_no).update(status_id = 10, cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')
            get_sales_order_trnx_redo(_id.id)            
            response.js = '$("#tblso").get(0).reload()'
        else:            
            get_generate_sales_invoice_id()
            sync_to_sales_invoice_db()
            session.flash = 'Delivery note processed.'     
            response.js = '$("#tblso").get(0).reload(), PrintInvoice(%s)' % (request.args(0)) #window.open("{{=URL("default","sales_order_report_account_user",args = request.args(0))}}")'

        
def get_sales_invoice_validation(x):        
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    # for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):        
        _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        if n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost:            
            return 2

def get_generate_sales_invoice_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'INV')).select().first()        
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1    
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)            
    _id.update_record(status_id = 7, sales_invoice_no_prefix_id = _trns_pfx.id, sales_invoice_no = _skey, sales_invoice_approved_by = auth.user_id, sales_invoice_date_approved = request.now)        
    db(db.Delivery_Note.sales_order_no == _id.sales_order_no).update(status_id = 7, sales_invoice_no_prefix_id = _trns_pfx.id, sales_invoice_no = _skey, sales_invoice_approved_by = auth.user_id, sales_invoice_date_approved = request.now)    
    for n in db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select():
        _stk_file = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _transit = int(_stk_file.stock_in_transit) + int(n.quantity)
        _pro_bal = int(_stk_file.closing_stock) + int(_stk_file.stock_in_transit)
        _clo_stk = int(_stk_file.closing_stock) - int(n.quantity)
        _stk_file.update_record(closing_stock = _clo_stk, stock_in_transit = _transit, probational_balance = _pro_bal, last_transfer_quantity = n.quantity, last_transfer_date = request.now)
    # redirect(URL('default','sales_order_report_account_user', args = request.args(0)))

def sync_to_sales_invoice_db():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    db.Sales_Invoice.insert(
        transaction_prefix_id = _id.transaction_prefix_id,
        sales_order_no = _id.sales_order_no,
        sales_order_date = _id.sales_order_date,
        dept_code_id = _id.dept_code_id,
        stock_source_id = _id.stock_source_id,
        customer_code_id = _id.customer_code_id,
        customer_order_reference = _id.customer_order_reference,
        delivery_due_date = _id.delivery_due_date,
        total_amount = _id.total_amount,
        total_amount_after_discount = _id.total_amount_after_discount,
        total_selective_tax = _id.total_selective_tax,
        total_selective_tax_foc = _id.total_selective_tax_foc,
        discount_added = _id.discount_added,
        total_vat_amount = _id.total_vat_amount,
        sales_order_date_approved = _id.sales_order_date_approved,
        sales_order_approved_by = _id.sales_order_approved_by,
        remarks = _id.remarks,
        delivery_note_no_prefix_id = _id.delivery_note_no_prefix_id,
        delivery_note_no = _id.delivery_note_no,
        delivery_note_approved_by = _id.delivery_note_approved_by,
        delivery_note_date_approved = _id.delivery_note_date_approved,
        sales_invoice_no_prefix_id = _id.sales_invoice_no_prefix_id,
        sales_invoice_no = _id.sales_invoice_no,
        sales_invoice_approved_by = _id.sales_invoice_approved_by,
        sales_invoice_date_approved = _id.sales_invoice_date_approved,
        section_id = _id.section_id,
        sales_man_id = _id.sales_man_id,
        status_id = _id.status_id)
    _si = db(db.Sales_Invoice.sales_order_no == _id.sales_order_no).select().first()    
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        if int(n.category_id) == 3:
            _price_cost = (n.average_cost / n.uom)
            _price_cost_discount = (n.average_cost / n.uom)
            _sale_cost_no_tax = 0 
        else:            
            _sale_cost_no_tax = (n.sale_cost - (_i.selective_tax_price / n.uom))
            _price_cost = (n.wholesale_price / n.uom)
            _price_cost_discount = _price_cost - ((_price_cost * n.discount_percentage) / 100)
        

        # _price_cost_discount = ((n.price_cost * (100 - n.discount_percentage)) / 100) / n.uom
        db.Sales_Invoice_Transaction.insert(
            sales_invoice_no_id = _si.id,
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            uom = n.uom,
            price_cost  = n.price_cost,
            packet_price_cost = n.packet_price_cost,
            total_amount = n.total_amount,
            average_cost = n.average_cost,
            sale_cost = n.sale_cost,
            sale_cost_notax_pcs = _sale_cost_no_tax,
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,            
            price_cost_pcs = _price_cost, # if item normal/foc
            price_cost_after_discount = _price_cost_discount, 
            average_cost_pcs = (n.average_cost / n.uom),
            wholesale_price_pcs = (n.wholesale_price / n.uom),
            retail_price_pcs = (n.retail_price / n.uom),
            vansale_price = n.vansale_price,
            discount_percentage = n.discount_percentage,
            net_price = n.net_price,
            selective_tax = n.selective_tax,
            selective_tax_foc = n.selective_tax_foc,
            selective_tax_price = _i.selective_tax_price,
            packet_selective_tax = n.packet_selective_tax,
            packet_selective_tax_foc = n.packet_selective_tax_foc,
            vat_percentage = n.vat_percentage,
            delete = n.delete
        )
    
def sale_order_manager_invoice_no_rejected():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()        
    _id.update_record(status_id = 3, remarks = 'Item price transaction discrepancy.',delivery_note_date_approved = request.now, delivery_note_approved_by = auth.user_id)
    session.flash = 'Delivery Note Rejected'
    response.js = "$('#tblso').get(0).reload()"

def sale_order_manager_invoice_no_form_approved(): # from forms approval
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.status_id == 7:
        session.flash = 'Delivery Note No. ' + str(_id.delivery_note_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.sales_invoice_approved_by.first_name)
        response.js = 'jQuery(redirect())'
    else:
        _val = get_sales_invoice_validation(1)
        if _val == 2:                        
            # print 'not equal'
            _id.update_record(status_id = 10, cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now, remarks = 'Price Discrepancies.')            
            get_sales_order_trnx_redo(_id.id)
            response.js = 'jQuery(redirect())'
        else:
            # print 'equal'
            get_generate_sales_invoice_id()
            sync_to_sales_invoice_db()      
            session.flash = 'Sales Invoice No. ' + str(_id.sales_invoice_no) + ' process '      
            response.js = 'jQuery(report(), AccountRedirect())'        

        
def sales_order_cancel_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first() 
    _dn = db(db.Delivery_Note.sales_order_no == _id.sales_order_no).update(cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now)    
    _id.update_record(cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now)
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == _id.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _s.stock_in_transit += int(n.quantity)
        _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)
        _s.update_record()
    session.flash = 'Transaction cancelled.'
    
    

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
    if _c:
        return XML(DIV(DIV('Building No. ', _c.building_no),DIV('Street No. ', _c.street_no), _class="well well-sm"))
    else:
        return XML(DIV(''))

def generate_sales_order_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SOR')).select().first()    
    if _trans_prfx:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True))
    else:        
        return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _disabled = True))

def generate_sales_return_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRS')).select().first()    
    if _trans_prfx:
        _serial = _trans_prfx.current_year_serial_key + 1
        _val_sales_return = str(_trans_prfx.prefix) + str(_serial)
        return XML(INPUT(_type="text", _class="form-control", _id='sales_return_no', _name='sales_return_no', _value=_val_sales_return, _disabled = True))
    else:
        return XML(INPUT(_type="text", _class="form-control", _id='sales_return_no', _name='sales_return_no', _disabled = True))

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

def sales_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = request.vars.stock_source_id

def sales_return_session():
    session.dept_code_id = request.vars.dept_code_id
    session.location_code_id = request.vars.location_code_id

def sales_return_help():
    # print session.dept_code_id
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Description'),TH('Department'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance')))    
    for n in db(db.Item_Master.dept_code_id == session.dept_code_id).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
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
# -----------------     R  E  P  O  R  T  S     -----------------
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
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas    
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# pdfmetrics.registerFont(TTFont('Arabic', '/usr/share/fonts/truetype/fonts-arabeyes/ae_Arab.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/home/larry/Workspace/web2py/applications/mtc_inv/static/fonts/ae_Arab.ttf'))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.3 * inch,bottomMargin=1.5 * inch)#, showBoundary=1)
style = ParagraphStyle(name='Normal',fontName="Arabic", fontSize=25)

style.alignment=TA_CENTER
heading_style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=20)
heading_style.alignment=TA_CENTER

arabic_text = u'إذا أخذنا بعين'
arabic_text = arabic_reshaper.reshape(arabic_text) # join characters
arabic_text = get_display(arabic_text) # change orientation by using bidi   
arabic_text = Paragraph(get_display(arabic_text), style)

def arabic_shapers():
    print 'arabic_text: ', arabic_text
    doc.build([arabic_text])    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

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
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)

styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0

# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)

logo_path = request.folder + '/static/images/Merch.jpg'
text_path = request.folder + '/static/fonts/reports/'
img = Image(logo_path)
img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'

merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])


_ar_sales_return = u'فاتورة' 
_ar_sales_return = arabic_reshaper.reshape(_ar_sales_return) # join characters
_ar_sales_return = Paragraph(get_display(_ar_sales_return),heading_style)

def sales_invoice_footer(canvas, doc):     
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
        
    # Header 'Stock Request Report'
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name # + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            [Paragraph(arabic_text,_arabic)],
            ['Invoice No. ', ':',str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no),'','Invoice Date ',':',n.sales_invoice_date_approved.strftime('%d-%m-%Y')],
            ['Customer Code',':',n.customer_code_id.customer_account_no,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','','']]
    header = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def sales_order_store_keeper_header_footer_report(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    # Header 'Stock Request Report'
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = str(n.customer_code_id.account_name) #+ str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['SALES ORDER'],
            ['Sales Order No. ', ':',str(n.transaction_prefix_id.prefix)+str(n.sales_order_no),'','Sales Order Date ',':',n.sales_order_date.strftime('%d-%m-%Y')],
            ['Customer Code',':',n.customer_code_id.account_code,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','','']]

    header = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)


    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def sales_order_delivery_note_footer_report(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Order.id == request.args(0)).select().first()

    # Header 'Stock Request Report'
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name # + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['DELIVERY NOTE'],
            ['Delivery Note No. ', ':',str(n.delivery_note_no_prefix_id.prefix)+str(n.delivery_note_no),'','Delivery Note Date ',':',n.delivery_note_date_approved.strftime('%d-%m-%Y')],
            ['Customer Code',':',n.customer_code_id.account_code,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.sales_man_id.employee_id.first_name.upper()) + ' ' + str(n.sales_man_id.employee_id.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','','']]

    header = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)


    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def sales_return_accounts_header_footer_report(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Return.id == request.args(0)).select().first()

    # Header 'Stock Request Report'
    for n in db(db.Sales_Return.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name # + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['SALES RETURN'],
            [_ar_sales_return],
            ['Sales Return No. ', ':',str(n.transaction_prefix_id.prefix)+str(n.sales_return_no),'','Sales Return Date ',':',n.sales_return_date.strftime('%d-%m-%Y')],
            ['Customer Code',':',n.customer_code_id.account_code,'','Transaction Type',':','Sales Return'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.location_code_id.location_name],       
            ['','','','','Sales Man',':',str(n.sales_man_id.employee_id.first_name) + ' ' + str(n.sales_man_id.employee_id.last_name)],            
            ['','','','','','',''],
            ['','','','','','','']]

    header = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)


    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def sales_order_report_store_keeper():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _so = [['SALES ORDER'],['Sales Order No. ', ':',str(n.transaction_prefix_id.prefix)+str(n.sales_order_no),'','Sales Order Date ',':',n.sales_order_date.strftime('%d-%m-%Y')]]
    _so_tbl = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])
    _so_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),      
        ('FONTSIZE',(0,0),(0,0),9),
        ('FONTSIZE',(0,1),(6,1),8),   
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP')]))
    _others = [['Remarks',':',_id.remarks],['Customer Sales Order Ref. ',':',n.customer_order_reference]]
    _others_table = Table(_others, colWidths=[120,25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)]))

    _ap = [[_id.created_by.first_name.upper() + ' ' + _id.created_by.last_name.upper(),'',_id.sales_order_approved_by.first_name.upper() + ' ' + _id.sales_order_approved_by.last_name.upper()],['Prepared by:','','Approved by:']]
    _ap_tbl = Table(_ap, colWidths='*')
    _ap_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
    ]))    

    # row.append(_so_tbl)
    # sales_order_table_reports()
    row.append(Spacer(1,.5*cm))
    sales_order_transaction_table_reports()
    row.append(Spacer(1,.7*cm))
    row.append(_others_table)
    row.append(Spacer(1,2*cm))
    row.append(_ap_tbl)
  
    doc.build(row, onFirstPage=sales_order_store_keeper_header_footer_report, onLaterPages = sales_order_store_keeper_header_footer_report)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data



@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def sales_order_delivery_note_report_store_keeper():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _so = [['DELIVERY NOTE'],['Delivery Note No. ', ':',str(n.delivery_note_no_prefix_id.prefix)+str(n.delivery_note_no),'','Delivery Note Date ',':',n.delivery_note_date_approved.strftime('%d-%m-%Y')]]

    _others = [        
        ['Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no),'','Sales Order Date.',':',_id.sales_order_date.strftime('%d-%m-%Y')],        
        ['Remarks',':',Paragraph(_id.remarks, style = _style), '','Customer Sales Order Ref.',':',n.customer_order_reference]]
    _others_table = Table(_others, colWidths=['*',25,'*',25,'*',25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))

    _acknowledge = [['Customer Acknowledgement: Received the above items in good order and sound condition.']]
    _acknowledge_table = Table(_acknowledge, colWidths='*')
    _acknowledge_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8)]))

    _signatory = [
        ['','For ' + str(_id.customer_code_id.account_name),'','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Sales_Order_Transaction_Report_Counter.sales_order_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Sales_Order_Transaction_Report_Counter.insert(sales_order_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Sales_Order_Transaction_Report_Counter.update_or_insert(db.Sales_Order_Transaction_Report_Counter.sales_order_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)
    _customer = [["","-------------     CUSTOMER'S COPY     -------------","print count: " + str(ctr)]]
    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","print count: " + str(ctr)]]
    _pos = [["","-------------     WAREHOUSE'S COPY     -------------","print count: " + str(ctr)]]

    _c_tbl = Table(_customer, colWidths=[100,'*',100])
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    
    delivery_note_transaction_table_reports()        
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_acknowledge_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    row.append(_c_tbl)
    row.append(PageBreak())
    
    delivery_note_transaction_table_reports()        
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_acknowledge_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    row.append(_a_tbl)
    row.append(PageBreak())

    delivery_note_transaction_table_reports()        
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_acknowledge_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    row.append(_p_tbl)
    row.append(PageBreak())

    doc.build(row, onFirstPage=sales_order_delivery_note_footer_report, onLaterPages = sales_order_delivery_note_footer_report, canvasmaker=PageNumCanvas)

    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data    

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('ROOT'))
def sales_return_report_account_user():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
   
    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount','Net Price','Amount']]        
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0      
    for t in db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(orderby = ~db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id)):
        ctr += 1        
        _grand_total += float(t.Sales_Return_Transaction.total_amount or 0)        
        _discount = float(_grand_total) * int(_id.discount_added or 0) / 100        
        _grand_total = float(_grand_total) - int(_discount)

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Return_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Return_Transaction.quantity, t.Sales_Return_Transaction.uom)

        if t.Sales_Return_Transaction.category_id == 3:
            _net_price = 'FOC'
        else:
            _net_price = locale.format('%.2F',t.Sales_Return_Transaction.net_price or 0, grouping = True)
        if t.Sales_Return_Transaction.category_id != 4:
            _category = t.Sales_Return_Transaction.category_id.mnemonic
        else:
            _category = ''            
        _st.append([ctr,t.Item_Master.item_code, str(t.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(t.Item_Master.item_description), 
            t.Sales_Return_Transaction.uom, 
            _category,             
            _qty, 
            locale.format('%.2F',t.Sales_Return_Transaction.price_cost or 0, grouping = True), 
            locale.format('%.2F',t.Sales_Return_Transaction.discount_percentage or 0, grouping = True), 
            _net_price, 
            locale.format('%.2F',t.Sales_Return_Transaction.total_amount or 0, grouping = True)])
    if not _id.total_selective_tax:
        _selective_tax = _selective_tax_foc = ''
    else:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))            
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    _amount_in_words = 'QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'

    _st.append([_selective_tax,'','','','','','Total Amount','',':',locale.format('%.2F',_id.total_amount or 0, grouping = True)])
    _st.append([_selective_tax_foc,'','','','','','Discount %','',':',locale.format('%.2F',_id.discount_added or 0, grouping = True)])
    _st.append([_amount_in_words,'','','','','','Net Amount','',':',locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[20,60,'*',30,30,50,50,50,50,50])
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-3), (-1,-3), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,1), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('TOPPADDING',(0,-3),(-1,-1),5),
        ('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('TOPPADDING',(0,-2),(-1,-2),0),
        ('BOTTOMPADDING',(0,-3),(-2,-2),0), 
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,0),(9,-1),'TOP'),        
        ('ALIGN',(5,0),(9,-1),'RIGHT'),
    ]))      

    _others = [
        ['Remarks',':',_id.remarks],
        ['Sales Return Ref. ',':',_id.customer_order_reference],            
        ]
    _others_table = Table(_others, colWidths=[120,25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ]))
    # row.append(Spacer(1,.7*cm))
    

    _signatory = [
        ['','We hereby confirm receipt of this sales return.','','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Sales_Return_Transaction_Report_Counter.sales_return_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Sales_Return_Transaction_Report_Counter.insert(sales_return_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Sales_Return_Transaction_Report_Counter.update_or_insert(db.Sales_Return_Transaction_Report_Counter.sales_return_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)


    _customer = [["","-------------     CUSTOMER'S COPY     -------------","print count: " + str(ctr)]]
    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","print count: " + str(ctr)]]
    _pos = [["","-------------     WAREHOUSE'S COPY     -------------","print count: " + str(ctr)]]

    _c_tbl = Table(_customer, colWidths=[100,'*',100])
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))

    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)
    row.append(_c_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)
    row.append(_a_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)
    row.append(_p_tbl)
    row.append(PageBreak())
    
    doc.build(row, onFirstPage=sales_return_accounts_header_footer_report, onLaterPages = sales_return_accounts_header_footer_report, canvasmaker=PageNumCanvas)
    # doc.build(row, onFirstPage = sales_invoice_footer, onLaterPages = sales_invoice_footer)
    # doc.build([Paragraph(arabic_text, style)])   
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def sales_order_report_account_user(): # print direct to printer
    row = []
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name # + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['SALES INVOICE'],
            ['Invoice No. ', ':',str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no),'','Invoice Date ',':',n.sales_invoice_date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Customer Code',':',n.customer_code_id.customer_account_no,'','Transaction Type',':','Credit'],
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],
            ['','','','','','',''],
            ['','','','','','',''],            
            ]
    _so_tbl = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    _so_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(0,0),9),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        
        ]))
    
    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount','Net Price','Amount']]        
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0    
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = ~db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _grand_total += float(t.Sales_Order_Transaction.total_amount or 0)        
        _discount = float(_grand_total) * int(_id.discount_added or 0) / 100        
        _grand_total = float(_grand_total) - int(_discount)

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)

        if t.Sales_Order_Transaction.category_id == 3:
            _net_price = 'FOC'
        else:
            _net_price = locale.format('%.2F',t.Sales_Order_Transaction.net_price or 0, grouping = True)
        if t.Sales_Order_Transaction.category_id != 4:
            _category = t.Sales_Order_Transaction.category_id.mnemonic
        else:
            _category = ''

        _st.append([ctr,Paragraph(t.Item_Master.item_code,style = _style), t.Item_Master.brand_line_code_id.brand_line_name+ '\n' + t.Item_Master.item_description, 
            t.Sales_Order_Transaction.uom, 
            _category,             
            _qty,
            locale.format('%.2F',t.Sales_Order_Transaction.price_cost or 0, grouping = True), 
            locale.format('%.2F',t.Sales_Order_Transaction.discount_percentage or 0, grouping = True), 
            _net_price,
            locale.format('%.2F',t.Sales_Order_Transaction.total_amount or 0, grouping = True)])
        # _st.append(['','','','','','','','','',''])
    if not _id.total_selective_tax:
        _selective_tax = _selective_tax_foc = ''
    else:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    _amount_in_words = 'QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    # _st.append(['-------------     NOTHING TO FOLLOWS     -------------','','','','','','','','',''])
    _st.append([_selective_tax,'','','','','','Net Amount','',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    _st.append([_selective_tax_foc,'','','','','','Discount %','',':',locale.format('%.2F',_id.discount_added or 0, grouping = True)])
    _st.append([_amount_in_words,'','','','','','Total Amount','',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[20,60,'*',25,25,50,50,45,50,50], repeatRows=0)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),

        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-3), (-1,-3), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,1), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('TOPPADDING',(0,-3),(-1,-1),5),
        ('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('TOPPADDING',(0,-2),(-1,-2),0),
        ('BOTTOMPADDING',(0,-3),(-2,-2),0),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,0),(9,-1),'TOP'),        
        ('ALIGN',(5,0),(9,-1),'RIGHT'),
    ]))    

    _others = [        
        ['Delivery Note No.',':',str(_id.delivery_note_no_prefix_id.prefix)+str(_id.delivery_note_no), '','Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no)],
        ['Delivery Note Date.',':',_id.delivery_note_date_approved.strftime('%d-%m-%Y, %H:%M %p'), '','Sales Order Date.',':',_id.sales_order_date.strftime('%d-%m-%Y')],
        ['Remarks',':',Paragraph(_id.remarks, style = _style), '','Customer Sales Order Ref.',':',n.customer_order_reference]]
    _others_table = Table(_others, colWidths=['*',25,'*',25,'*',25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    # row.append(Spacer(1,.7*cm))    

    _signatory = [
        ['','We hereby confirm receipt of this invoice.','','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Sales_Invoice_Transaction_Report_Counter.sales_invoice_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Sales_Invoice_Transaction_Report_Counter.insert(sales_invoice_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Sales_Invoice_Transaction_Report_Counter.update_or_insert(db.Sales_Invoice_Transaction_Report_Counter.sales_invoice_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)


    _customer = [["","-------------     CUSTOMER'S COPY     -------------","print count: " + str(ctr)]]
    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","print count: " + str(ctr)]]
    _pos = [["","-------------     WAREHOUSE'S COPY     -------------","print count: " + str(ctr)]]

    _c_tbl = Table(_customer, colWidths=[100,'*',100])
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))


    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    # row.append(Spacer(.1,.2*cm))    
    row.append(_c_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    # row.append(Spacer(.1,.2*cm))    
    row.append(_a_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    # row.append(Spacer(.1,.2*cm))    
    row.append(_p_tbl)
    row.append(PageBreak())

    # doc.build(row)
    doc.build(row, onFirstPage = sales_invoice_footer, onLaterPages = sales_invoice_footer, canvasmaker=PageNumCanvas)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def sales_order_table_reports():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name # + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['Customer Code',':',n.customer_code_id.customer_account_no,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','',''],                         
            ]
    _so_tbl = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    _so_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,1),(2,-1)),
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    return row.append(_so_tbl)

def sales_order_transaction_table_reports():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()

    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount %','Net Price','Amount']]        
    _grand_total = 0
    _total_amount = _selective_tax_sum = _selective_tax_foc_sum = 0        
    _total_excise_tax = 0      
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _grand_total += float(t.Sales_Order_Transaction.total_amount or 0)        
        _discount = float(_grand_total) * int(_id.discount_added or 0) / 100        
        _grand_total = float(_grand_total) - int(_discount)
        _selective_tax_sum += t.Sales_Order_Transaction.selective_tax or 0
        _selective_tax_foc_sum += t.Sales_Order_Transaction.selective_tax_foc or 0
        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)

        if t.Sales_Order_Transaction.category_id == 3:
            _net_price = 'FOC-Price'
        else:
            _net_price = locale.format('%.2F',t.Sales_Order_Transaction.net_price or 0, grouping = True)
        if t.Sales_Order_Transaction.category_id != 4:
            _category = t.Sales_Order_Transaction.category_id.mnemonic
        else:
            _category = ''            
        _st.append([ctr,t.Item_Master.item_code, str(t.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(t.Item_Master.item_description), 
            t.Sales_Order_Transaction.uom, 
            _category,             
            _qty, 
            locale.format('%.2F',t.Sales_Order_Transaction.price_cost or 0, grouping = True), 
            locale.format('%d',t.Sales_Order_Transaction.discount_percentage or 0, grouping = True), 
            _net_price, 
            locale.format('%.2F',t.Sales_Order_Transaction.total_amount or 0, grouping = True)])
    if _selective_tax_sum > 0:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_selective_tax_sum or 0, grouping = True))        
    else:
        _selective_tax = ''
    
        
    
    if _selective_tax_foc_sum > 0:
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_selective_tax_foc_sum or 0, grouping = True))      
    else:    
        _selective_tax_foc = ''
    
        

    (_whole, _frac) = (int(_id.total_amount_after_discount), locale.format('%.2f',_id.total_amount_after_discount or 0, grouping = True))
    _amount_in_words = 'QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'

    _st.append([_selective_tax,'','','','','','Net Amount','',':',locale.format('%.2F',_id.total_amount or 0, grouping = True)])
    _st.append([_selective_tax_foc,'','','','','','Discount %','',':',locale.format('%.2F',_id.discount_added or 0, grouping = True)])
    _st.append([_amount_in_words,'','','','','','Total Amount','',':',locale.format('%.2F',_id.total_amount_after_discount or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[20,60,'*',30,30,50,50,50,50,50], repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-3), (-1,-3), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,1), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('TOPPADDING',(0,-3),(-1,-1),5),
        ('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('TOPPADDING',(0,-2),(-1,-2),0),
        ('BOTTOMPADDING',(0,-3),(-2,-2),0),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,0),(9,-1),'TOP'),        
        ('ALIGN',(5,0),(9,-1),'RIGHT'),
    ]))    
    return row.append(_st_tbl)

def delivery_note_transaction_table_reports():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    ctr = _total_qty = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty']]        

    _total_amount = 0        
    _total_excise_tax = 0    
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _total_qty += t.Sales_Order_Transaction.quantity

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)
        if t.Sales_Order_Transaction.category_id != 4:
            # _category = t.Sales_Order_Transaction.category_id.mnemonic
            _category = 'FOC-Price'
        else:
            _category = ''        
        _st.append([ctr,t.Item_Master.item_code, str(t.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(t.Item_Master.item_description), t.Sales_Order_Transaction.uom,_category, _qty])
        if not _id.total_selective_tax:
            _selective_tax = _selective_tax_foc = ''
        else:
            _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
            _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    _st.append(['','','-------------     NOTHING TO FOLLOWS     -------------','','',''])
    _st_tbl = Table(_st, colWidths=[20,70,'*',30,30,70], repeatRows = 1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),                
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)), 
        ('LINEBELOW', (0,1), (-1,-2), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('TOPPADDING',(0,-1),(-1,-1),5),
        ('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),                
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(5,-1),'TOP'),        
        ('ALIGN',(5,1),(5,-1),'RIGHT'),
        ('ALIGN',(5,0),(5,0),'CENTER'),
        ('ALIGN',(2,-1),(2,-1),'RIGHT'),
    ]))
    return row.append(_st_tbl)

def stock_corrections_header_footer_reports(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    
    # Header 'Stock Corrections Report'
    for n in db(db.Stock_Corrections.id == request.args(0)).select():
        _sh = [
            [],
            ['STOCK CORRECTIONS'],
            ['Stock Corrections No.',':',str(n.stock_corrections_id.prefix)+str(n.stock_corrections_no),'','Stock Corrections Date',':',n.date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Transaction No.',':',n.transaction_no,'','Transaction Date',':',n.transaction_date.strftime('%d-%m-%Y')],
            ['Department',':',n.dept_code_id.dept_name,'','Stock Quantity From',':',n.stock_quantity_from_id.description],
            ['Location',':',n.location_code_id.location_name,'','Stock Quantity To',':',n.stock_quantity_to_id.description]
        ]
    header = Table(_sh, colWidths=['*',20,'*',10,'*',20,'*'])
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),        
        ('FONTNAME',(0,0),(6,-1),'Courier'),
        ('FONTSIZE',(0,1),(6,-1),8),
        ('TOPPADDING',(0,1),(6,1),5),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        ('FONTSIZE',(0,1),(6,1),15),
        ('FONTNAME',(0,1),(6,1),'Courier-Bold',12),
        ('BOTTOMPADDING',(0,1),(6,1),12)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)

    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def stock_corrections_transaction_table_reports():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    ctr = 0
    _sc = [['#','Item Code','Description','UOM','Quantity']]
    for n in db(db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)).select(orderby = db.Stock_Corrections_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Corrections_Transaction.item_code_id)):
        ctr += 1
        if n.Stock_Corrections_Transaction.uom == 1:
            _qty = n.Stock_Corrections_Transaction.quantity
        else:
            _qty = card(n.Stock_Corrections_Transaction.item_code_id, n.Stock_Corrections_Transaction.quantity, n.Stock_Corrections_Transaction.uom)
        _sc.append([ctr,n.Stock_Corrections_Transaction.item_code_id.item_code, str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),n.Stock_Corrections_Transaction.uom, _qty])
    _sc.append(['','','----------  nothing to follows   ----------','',''])
    _sc_tbl = Table(_sc, colWidths=[20,60,'*',50,50], repeatRows = 1)
    _sc_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,-1),(-1,-1),15),        
        ('FONTNAME',(0,0),(-1,-1),'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,-1), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(4,-1),'TOP'),
        # ('SPAN',(0,-1),(-1,-1)),
        ]))    

    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths=[120,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),        
    ]))
    if _id.status_id == 16:
        _approved_by = str(_id.approved_by.first_name.upper()) + ' ' + str(_id.approved_by.last_name.upper())
    else:
        _approved_by = ''
    _signatory = [        
        ['',str(_id.created_by.first_name.upper()) + str(' ') + str(_id.created_by.last_name.upper()),'',_approved_by,''],
        ['','Requested by:','','Approved by:','']]

    _signatory_table = Table(_signatory, colWidths=[50,'*',50,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LINEABOVE', (1,1), (1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (3,1), (3,1), 0.25, colors.black,None, (2,2)),
        # ('BOTTOMPADDING',(0,0),(-1,0),30),
        # ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    row.append(_sc_tbl)    
    row.append(Spacer(1,.7*cm))
    row.append(_remarks_table) 
    row.append(Spacer(1,.7*cm))
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)    
    
    doc.build(row, onFirstPage=stock_corrections_header_footer_reports, onLaterPages = stock_corrections_header_footer_reports)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    # os.startfile(tmpfilename,'print')
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def obslo_stock_header_footer_reports(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    
    # Header 'Stock Corrections Report'
    for n in db(db.Obsolescence_Stocks.id == request.args(0)).select():
        _sh = [
            [],
            ['Obsolescence Stock Invoice'],
            ['Stock Issue No.',':',str(n.transaction_prefix_id.prefix)+str(n.obsolescence_stocks_no),'','Stock Issue Date',':',n.obsolescence_stocks_date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Transaction No.',':',n.transaction_no,'','Transaction Date',':',n.transaction_date.strftime('%d-%m-%Y')],
            ['Department',':',n.dept_code_id.dept_name,'','Account Code',':',n.account_code_id.account_code],
            ['Location',':',n.location_code_id.location_name,'','Account Name',':',n.account_code_id.account_name],
            ['Stock Quantity From',':',n.stock_type_id.description,'','','','']
        ]
    header = Table(_sh, colWidths=['*',20,'*',10,'*',20,'*'])
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),        
        ('FONTNAME',(0,0),(6,-1),'Courier'),
        ('FONTSIZE',(0,1),(6,-1),8),
        ('TOPPADDING',(0,1),(6,1),5),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        ('FONTSIZE',(0,1),(6,1),15),
        ('FONTNAME',(0,1),(6,1),'Courier-Bold',12),
        ('BOTTOMPADDING',(0,1),(6,1),12)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)

    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def obslo_stock_transaction_table_reports():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    ctr = 0
    _sc = [['#','Item Code','Description','UOM','Quantity']]
    for n in db(db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)).select(orderby = db.Obsolescence_Stocks_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction.item_code_id)):
        ctr += 1
        if n.Obsolescence_Stocks_Transaction.uom == 1:
            _qty = n.Obsolescence_Stocks_Transaction.quantity
        else:
            _qty = card(n.Obsolescence_Stocks_Transaction.item_code_id, n.Obsolescence_Stocks_Transaction.quantity, n.Obsolescence_Stocks_Transaction.uom)
        _sc.append([ctr,n.Obsolescence_Stocks_Transaction.item_code_id.item_code, str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),n.Obsolescence_Stocks_Transaction.uom, _qty])
    _sc.append(['','','----------  NOTHING TO FOLLOWS   ----------','',''])
    _sc_tbl = Table(_sc, colWidths=[20,60,'*',50,50], repeatRows = 1)
    _sc_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,-1),(-1,-1),15),
        
        ('FONTNAME',(0,0),(-1,-1),'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,-1), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(4,-1),'TOP'),
        # ('SPAN',(0,-1),(-1,-1)),
        ]))    

    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths=[120,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),        
    ]))

    _signatory = [
        ['','Requested by:','','Approved by:',''],
        ['',str(_id.created_by.first_name.upper()) + str(' ') + str(_id.created_by.last_name.upper()),'',str(_id.obsolescence_stocks_approved_by.first_name.upper() + str(' ') + str(_id.obsolescence_stocks_approved_by.last_name.upper())),''],
        ['','Name and Signature','','Name and Signature','']]

    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING',(0,0),(-1,0),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    # _prt_ctr = db(db.Stock_Issue_Transaction_Report_Counter.stock_issue_transaction_no_id == request.args(0)).select().first()
    # if not _prt_ctr:
    #     ctr = 1
    #     db.Stock_Issue_Transaction_Report_Counter.insert(stock_issue_transaction_no_id = request.args(0), printer_counter = ctr)
    # else:
    #     _prt_ctr.printer_counter += 1
    #     ctr = _prt_ctr.printer_counter
    #     db.Stock_Issue_Transaction_Report_Counter.update_or_insert(db.Stock_Issue_Transaction_Report_Counter.stock_issue_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)


    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","print count: " + str()]]
    _pos = [["","-------------     WAREHOUSE'S COPY     -------------","print count: " + str()]]

    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))

    row.append(_sc_tbl)    
    row.append(Spacer(1,.7*cm))
    row.append(_remarks_table) 
    row.append(Spacer(1,.7*cm))
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)    
    row.append(_a_tbl)
    row.append(PageBreak())    

    
    row.append(_sc_tbl)    
    row.append(Spacer(1,.7*cm))
    row.append(_remarks_table) 
    row.append(Spacer(1,.7*cm))
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)    
    row.append(_p_tbl)
    row.append(PageBreak())    

    doc.build(row, onFirstPage=obslo_stock_header_footer_reports, onLaterPages = obslo_stock_header_footer_reports, canvasmaker=PageNumCanvas2)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

########################################################################
class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """        Add the page number        """
        page = []
        _location = ''
        _page_count = page_count / 3
        _page_number = self._pageNumber
        if _page_count > 1:            
            if _page_number == 1:
                _location = "-------------     CUSTOMER'S COPY     -------------"
                _page_number = 1
            elif _page_number == 3:
                _location = "-------------     ACCOUNT'S COPY     -------------"
                _page_number = 1
            elif _page_number == 5:
                _location = "-------------     WAREHOUSE'S COPY     -------------"
                _page_number = 1
            else:
                _page_number = 2
                _location = ''
        else:
            _page_number = 1
        # page = [["Page"],[" of "]]
        # paget = Table(page, colWidths='*')
        # paget.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))]))
        # row.append(page)
        page = "Page %s of %s" % (_page_number, _page_count)        
        self.setFont("Courier-Bold", 8)
        self.drawRightString(148*mm, 45*mm, _location)
        self.drawRightString(115*mm, 35*mm, page)
 
class PageNumCanvas2(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """        Add the page number        """
        page = []
        _location = ''
        _page_count = page_count / 2
        _page_number = self._pageNumber
        if _page_count > 1:            
            if _page_number == 1:
                _location = "-------------     ACCOUNT'S COPY     -------------"
                _page_number = 1
            elif _page_number == 2:
                _location = "-------------     WAREHOUSE'S COPY     -------------"
                _page_number = 1
            else:
                _page_number = 1
                _location = ''
        else:
            _page_number = 1
        # page = [["Page"],[" of "]]
        # paget = Table(page, colWidths='*')
        # paget.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))]))
        # row.append(page)
        page = "Page %s of %s" % (_page_number, _page_count)        
        self.setFont("Courier-Bold", 8)
        self.drawRightString(148*mm, 45*mm, _location)
        self.drawRightString(115*mm, 35*mm, page)
 