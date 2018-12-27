import time
from datetime import date

import locale
locale.setlocale(locale.LC_ALL,'')

# _user = '%s %s' % (auth.user.first_name.upper(), auth.user.last_name.upper()) 
_ckey = 0
# ---- Product Master  -----
@auth.requires_login()
def prod_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Division'),TH('Product Code'),TH('Product Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Division.ALL, db.Product.ALL, left=db.Division.on(db.Division.id == db.Product.div_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _href=URL('prod_edit_form', args = n.Product.id),_type='button', _class='btn btn-icon-toggle', **{'_data-toggle':'tooltip', '_data-placement':'top', '_data-original-title':'View Row'})
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row',_href=URL('prod_edit_form', args = n.Product.id),_type='button  ', _role='button', _class='btn btn-icon-toggle')
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _href=URL('prod_edit_form', args = n.Product.id),_type='button', _class='btn btn-icon-toggle', **{'_data-toggle':'tooltip', '_data-placement':'top', '_data-original-title':'Delete Row'})
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Product.id),TD(n.Division.div_name),TD(n.Product.prefix_id.prefix,n.Product.product_code),TD(n.Product.product_name),TD(n.Product.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover')
    return dict(table=table)

@auth.requires_login()  
def prod_add_form():
    _ckey = 0
    pre = db(db.Prefix_Data.prefix_key == 'PRO').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        _ckey = str(_skey).rjust(3,'0')
        ctr_val = pre.prefix+_ckey
        form = SQLFORM.factory(
            Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
            Field('product_name', 'string', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name', error_message = 'Record already exist or empty.')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'NEW RECORD SAVED'
            db.Product.insert(
                prefix_id = pre.id,
                div_code_id= form.vars.div_code_id, 
                product_code = _ckey, 
                product_name = form.vars.product_name, 
                status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form=form, ctr_val=ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('prod_mas'))

@auth.requires_login()
def prod_edit_form():
    ctr_val = db(db.Product.id == request.args(0)).select().first()
    form = SQLFORM(db.Product, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'        
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.product_code)

# ---- SubProduct Master  -----
@auth.requires_login()
def subprod_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Sub-Product Code'),TH('Sub-Product Name'),TH('Product Code'),TH('Product Name'),TH('Status'),TH('Action')))
    
    for n in db(db.SubProduct).select(db.Product.ALL, db.SubProduct.ALL, left=db.Product.on(db.Product.id == db.SubProduct.product_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.SubProduct.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('subprod_edit_form', args = n.SubProduct.id))
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.SubProduct.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.SubProduct.prefix_id.prefix,n.SubProduct.subproduct_code),TD(n.SubProduct.subproduct_name),TD(n.Product.prefix_id.prefix, n.Product.product_code),TD(n.Product.product_name),TD(n.SubProduct.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover') 
    return dict(table=table)

@auth.requires_login()
def subprod_add_form():        
    pre = db(db.Prefix_Data.prefix_key == 'SPC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1        
        _ckey = str(_skey)
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
            Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
            Field('subproduct_name','string', requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.SubProduct.insert(
                prefix_id = pre.id,
                div_code_id = form.vars.div_code_id,
                product_code_id = form.vars.product_code_id, 
                subproduct_code = _ckey, 
                subproduct_name = form.vars.subproduct_name, 
                status_id = form.vars.status_id
                )            
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('subprod_mas'))
def show_products():
    _pro = db(db.SubProduct.product_code_id == request.vars.product_code_id).select()
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Sub-Product Code'),TH('Sub-Product Name')))
    for p in _pro:
        ctr += 1
        row.append(TR(TD(ctr),TD(p.prefix_id.prefix,p.subproduct_code),TD(p.subproduct_name)))
    body = TBODY(*row)
    table = TABLE(*[thead, body], _class='table')
    return table
@auth.requires_login()
def subprod_edit_form():
    ctr_val = db(db.SubProduct.id == request.args(0)).select().first()
    form = SQLFORM(db.SubProduct, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.subproduct_code)


# ---- Supplier Master  -----
# @auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE'))
@auth.requires_login()
def suplr_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Supplier Sub Code'),TH('IB Account'),TH('Purchase Account'),TH('Sales Account'),TH('Department'),TH('Supplier Name'),TH('Contact Person'),TH('Supplier Type'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Master).select(orderby = db.Supplier_Master.id):
        view_lnk = A(I(_class='fas fa-search'), _target="#", _title='View Row', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _target="#", _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        addr_lnk = A(I(_class='fas fa-address-card'), _target="#", _title='Address', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_form', args = n.id))
        paym_lnk = A(I(_class='fas fa-list'), _target="#", _title='Payment Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_paymod_edit_form', args = n.id))
        bank_lnk = A(I(_class='fas fa-money-check-alt'),_target="#", _title='Bank Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank', args = n.id))
        forw_lnk = A(I(_class='fas fa-shipping-fast'),_target="#", _title='Shipping', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank', args = n.id))
        dept_lnk = A(I(_class='fas fa-building'), _target="#",_title='Department', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_dept_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, addr_lnk, paym_lnk, bank_lnk, dept_lnk, forw_lnk) 

        action = DIV(BUTTON("action",_type = "button", _class="btn btn-default dropdown-toggle", **{'_data-toggle':'dropdown', '_aria-haspopup':'true', '_aria-expanded':'false'}),
        UL(
            LI(A('View', _href = URL('suplr_view_form', args = n.id))),
            LI(A('Edit', _href = URL('suplr_edit_form', args = n.id))),           
            LI(A('Address', _href = URL('suplr_addr_form', args = n.id))),
            LI(A('Payment', _href = URL('suplr_paymod_edit_form', args = n.id))),
            LI(A('Bank', _href = URL('suplr_bank', args = n.id))),
            LI(A('Shipping', _href = URL('suplr_forw_form', args = n.id))),
            LI(A('Department', _href = URL('suplr_dept_form', args = n.id))),_class="dropdown-menu"),_class="btn-group btn-group-xs", role="group")
        ctr += 1
        row.append(TR(TD(ctr),TD(n.prefix_id.prefix,n.supp_code),TD(n.supp_sub_code),TD(n.supplier_ib_account),TD(n.supplier_purchase_account),
        TD(n.supplier_sales_account),TD(n.dept_code_id.dept_name),TD(n.supp_name),
        TD(n.contact_person),TD(n.supplier_type),TD(n.status_id.status),TD(action)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-striped')
    return dict(table = table)

# def gensup():
#     x = 10000
#     for s in db(db.Supplier_Master).select(orderby = db.Supplier_Master.id):
#         x += 1
#         s.update_record(supp_code = x)
#     return locals()

def validate_supplier_id(form):    
    _id = db(db.Supplier_Master.supp_code == request.vars.supplier_id).select().first()
    print request.vars.supplier_id
    if _id:
        print 'True'
        form.vars.supplier_id = _id.id
    else:
        print 'False'
        form.errors._id = DIV('error')        

@auth.requires_login()
def suplr_forw_form():
    row = []
    ctr = 0
    form = SQLFORM.factory(
        Field('forwarder_code_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Forwarder_Supplier.id, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder' )),
        Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Forwarders.insert(supplier_id = request.args(0), forwarders_code_id = form.vars.forwarders_code_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    head = THEAD(TR(TH('#'),TH('Forwarders'),TH('Status')))
    for n in db(db.Supplier_Forwarders.supplier_id == request.args(0)).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(n.forwarder_code_id.forwarder_code, ' - ' , n.forwarder_code_id.forwarder_name),TD(n.status_id.status)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)


@auth.requires_login()
def suplr_add_form():
    print request.vars._ckey
    # PREFIX 25- + serial supplier code	25-00001
    # Prefix 18 + serial supplier code	18-00001
    # Prefix 19 + serial supplier code	19-00001

    pre = db(db.Prefix_Data.prefix_key == 'SUP').select().first()

    if pre:
        _skey = pre.serial_key
        _skey += 1            
        _ckey = str(_skey)
        
        ctr_val = pre.prefix + _ckey
        supp_ib_acct_ctr = str(25)+'-'+_ckey
        supp_pu_acct_ctr = str(18)+'-'+_ckey
        supp_sa_acct_ctr = str(19)+'-'+_ckey
        # Supplier Master Table
        form = SQLFORM.factory(            
            Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
            Field('supp_name','string',length=50,requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Supplier_Master.supp_name')]),
            Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL'], zero = 'Choose Type')), # foriegn or local supplier
            Field('contact_person', 'string', length=30, requires = IS_UPPER()),
            Field('address_1','string', length = 50, requires = IS_UPPER()),
            Field('address_2','string', length = 50, requires = IS_UPPER()),    
            Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
            Field('contact_no','string', length=50, requires = IS_UPPER()),
            Field('fax_no','string', length=50, requires = IS_UPPER()),
            Field('email_address','string', length=50, requires = IS_UPPER()),
            Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
            Field('purchase_budget', 'decimal(10,2)'),        
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process(formname = 'step 1', keepvalues = True).accepted:
            db.Supplier_Master.insert(
                prefix_id = pre.id,
                dept_code_id = form.vars.dept_code_id,
                supp_code = _ckey, 
                supp_name = form.vars.supp_name, 
                supplier_type = form.vars.supplier_type,
                supplier_ib_account = supp_ib_acct_ctr,
                supplier_purchase_account = supp_pu_acct_ctr, 
                supplier_sales_account = supp_sa_acct_ctr,
                contact_person = form.vars.contact_person,
                address_1 = form.vars.address_1, 
                address_2 = form.vars.address_2,
                country_id = form.vars.country_id,
                contact_no = form.vars.contact_no,
                currency_id = form.vars.currency_id, 
                fax_no = form.vars.fax_no,
                email_adddress = form.vars.email_address,
                status_id = form.vars.status_id)
            
                      
            response.flash = 'RECORD SAVE'
        elif form.errors:
            response.flash = 'ENTRY HAS ERROR'
        
        # Supplier Contact Person Master Table
        form2 = SQLFORM.factory(
            Field('other_supplier_name', 'string', length = 50, requires = IS_UPPER()),
            Field('scp_contact_person', 'string', length=30, requires = IS_UPPER()),
            Field('scp_address_1','string', length = 50, requires = IS_UPPER()),
            Field('scp_address_2','string', length = 50, requires = IS_UPPER()),
            Field('scp_country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
            Field('scp_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))            
        if form2.process(formname = 'step 2', keepvalues = True, onvalidation = validate_supplier_id ).accepted:
            
            db.Supplier_Contact_Person.insert(
                supplier_id = _id.id, 
                other_supplier_name = form.vars.other_supplier_name,
                contact_person = form.vars.scp_contact_person,
                address_1 = form.vars.scp_address_1,
                address_2 = form.vars.scp_address_2,
                country_id = form.vars.scp_country_id,
                status_id = form.vars.scp_status_id)

            response.flash = 'RECORD SAVE'
        elif form2.errors:
            response.flash = 'ENTRY HAS ERROR'

        # Supplier Payment Mode Details Table
        form3 = SQLFORM.factory(
            Field('trade_terms_id', 'reference Supplier_Trade_Terms', label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')), 
            Field('payment_mode_id', 'reference Supplier_Payment_Mode', label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), 
            Field('payment_terms_id', 'reference Supplier_Payment_Terms', label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), 
            Field('spm_currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
            Field('forwarder_id', 'reference Forwarder_Supplier', label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
            Field('commodity_code','string',length=10),
            Field('discount_percentage','string',length=10),
            Field('custom_duty_percentage','string',length=10),
            Field('spm_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form3.process(fornmane = 'step 3', keepvalues = True, onvalidation = validate_supplier_id).accepted:
            db.Supplier_Payment_Mode_Details.insert(
                supplier_id = _id.id,
                trade_terms_id = form.vars.trade_terms_id,
                payment_mode_id = form.vars.payment_mode_id,
                payment_terms_id = form.vars.payment_terms_id,
                currency = form.vars.spm_currency,
                forwarder_id = form.vars.forwarder_id,
                commodity_code = form.vars.commodity_code,
                discount_percentage = form.vars.discount_percentage,
                custom_duty_percentage = form.vars.custom_duty_percentage,
                status_id = form.vars.spm_status_id)

            response.flash = 'RECORD SAVE'
        elif form3.errors:
            form3.errors._id.id = DIV('error')
            response.flash = 'ENTRY HAS ERROR'
            
        # Supplier Bank Table
        form4 = SQLFORM.factory(
            Field('account_no', 'string'),
            Field('bank_name', 'string'),
            Field('beneficiary_name', 'string'),
            Field('iban_code', 'string'),
            Field('swift_code', 'string'),
            Field('bank_address', 'string'),
            Field('city', 'string'),
            Field('sb_country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
            Field('sb_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form4.process(formname = 'step 4', keepvalues = True, onvalidation = validate_supplier_id).accepted:         
            db.Supplier_Bank.insert(
                supplier_id = _id.id,
                account_no = form.vars.account_no,
                beneficiary_name = form.vars.beneficiary_name, 
                iban_code = form.vars.iban_code,
                swift_code = form.vars.swift_code, 
                bank_address = form.vars.bank_address, 
                city= form.vars.city,
                country_id = form.vars.sb_country_id, 
                status_id = form.vars.sb_status_id)
            

            response.flash = 'NEW RECORD SAVE'
        elif form4.errors:
            response.flash = 'ENTRY HAS ERROR'
         
        form5 = SQLFORM(db.Supplier_Forwarders)
        
        if form5.process(formname = 'step 5', keepvalues = True, onvalidation = validate_supplier_id).accepted:
            response.flash = 'NEW RECORD SAVE'
        elif form5.errors:
            response.flash = 'ENTRY HAS ERROR'
            
        return dict(form = form, form2 = form2, form3 = form3, form4 = form4, form5 = form5, _ckey = _ckey, ctr_val = ctr_val, supp_ib_acct_ctr = supp_ib_acct_ctr,supp_pu_acct_ctr=supp_pu_acct_ctr,supp_sa_acct_ctr=supp_sa_acct_ctr)      
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('suplr_mas'))

@auth.requires_login()
def suplr_edit_form():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    ctr_val = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, supplier_id = supplier_id)

@auth.requires_login()
def suplr_bank():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('account_no', 'string'),
        Field('bank_name', 'string'),
        Field('beneficiary_name', 'string'),
        Field('iban_code', 'string'),
        Field('swift_code', 'string'),
        Field('bank_address', 'string'),
        Field('city', 'string'),
        Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Bank.insert(supplier_id = request.args(0),account_no = form.vars.account_no,
        bank_name = form.vars.bank_name, beneficiary_name = form.vars.beneficiary_name, iban_code = form.vars.iban_code,
        swift_code = form.vars.swift_code, bank_address = form.vars.bank_address, city= form.vars.city,
        country_id = form.vars.country_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS' 

    row = []
    thead = THEAD(TR(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Status'),TH('Action'))))
    for n in db(db.Supplier_Bank.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),TD(n.swift_code),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, table = table, supplier_id = supplier_id)

@auth.requires_login()
def suplr_bank_edit_form():
    db.Supplier_Bank.supplier_id.writable = False
    supplier_id = db(db.Supplier_Bank.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Bank, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def suplr_view_form():    
    _sm = db(db.Supplier_Master.id == request.args(0)).select().first()    
    return dict(_sm = _sm)

@auth.requires_login()
def suplr_paym_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Payment_Mode_Details.supplier_id == request.args(0)).select().first()
    if _query:        
        tbody1 = TBODY(
            TR(TD('Trade Terms'),TD('Payment Mode'),TD('Payment Terms'),TD('Currency'),TD('Forwarder'),_class='active'),
            TR(TD(_query.trade_terms_id.trade_terms),TD(_query.payment_mode_id.payment_mode),TD(_query.payment_terms_id.payment_terms),TD(_query.currency_id),TD(_query.forwarder_id.forwarder_name)))
        table1 = TABLE(*[tbody1], _class = 'table table-bordered')
        tbody2 = TBODY(
            TR(TD('Commodity'),TD('Discount %'),TD('Custom Duty%'),TD('Status'),_class='active'),
            TR(TD(_query.commodity_code),TD(_query.discount_percentage),TD(_query.custom_duty_percentage),TD(_query.status_id.status)))
        table2 = TABLE(*[tbody2], _class = 'table table-bordered')
        return DIV(table1,table2)
    else:
        return CENTER(DIV(B('INFO! '),'No payment mode details record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_bank_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Bank.supplier_id == request.args(0)).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Bank Address'),TH('City'),TH('Country'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),TD(n.swift_code),TD(n.bank_address),TD(n.city),TD(n.country_id),TD(n.status_id)))
        tbody = TBODY(*row)
        table = TABLE(*[thead, tbody], _class= 'table table-striped')
        return table
    else:        
        return CENTER(DIV(B('INFO! '),'No bank details record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_othr_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Contact_Person.supplier_id == request.args(0)).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Supplier Name'),TH('Contact Person'),TH('Address 1'),TH('Address 2'),TH('Country'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.other_supplier_name),TD(n.contact_person),TD(n.address_1),TD(n.address_2),TD(n.country_id.description),TD(n.status_id.status)))
            tbody = TBODY(*row)
            table = TABLE(*[thead, tbody], _class='table table-striped')
        return table
    else:
        return CENTER(DIV(B('INFO! '),'No other address record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_dept_view():    
    row = []
    ctr = 0
    _query = db(db.Supplier_Master_Department.supplier_id == request.args(0)).select()
    if _query:
        thead = THEAD(TR(TH('#'),TH('Department'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.dept_code_id.dept_name),TD(n.status_id.status)))
            tbody = TBODY(*row)
            table = TABLE(*[thead, tbody], _class='table table-striped')
        return table 
    else:
        return CENTER(DIV(B('INFO! '),'No departments record.',_class='alert alert-info',_role='alert'))
    
@auth.requires_login()
def suplr_ship_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Forwarders.supplier_id == request.args(0)).select()
    if _query:
        thead = THEAD(TR(TH('#'),TH('Forwarder'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.forwarder_code_id.forwarder_name),TD(n.status_id.status)))
            tbody = TBODY(*row)
            table = TABLE(*[thead, tbody], _class='table table-striped')
        return table 
    else:
        return CENTER(DIV(B('INFO! '),'No forwarders record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_addr_form():     
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('other_supplier_name', 'string', length = 50, requires = IS_UPPER()),
        Field('contact_person', 'string', length=30, requires = IS_UPPER()),
        Field('address_1','string', length = 50, requires = IS_UPPER()),
        Field('address_2','string', length = 50, requires = IS_UPPER()),
        Field('country_id','reference Made_In', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Contact_Person.insert(
            supplier_id = request.args(0),other_supplier_name = form.vars.other_supplier_name,contact_person = form.vars.contact_person, 
            address_1 = form.vars.address_1, address_2 = form.vars.address_2,
            country_id = form.vars.country_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    row = []
    thead = THEAD(TR(TH('#'),TH('Other Supplier Name'),TH('Contact Person'),TH('Address'),TH('Country'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Contact_Person.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.other_supplier_name),TD(n.contact_person),TD(n.address_1),TD(n.country_id),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, supplier_id = supplier_id, table = table)

@auth.requires_login()
def suplr_addr_edit_form():
    db.Supplier_Contact_Person.supplier_id.writable = False
    form = SQLFORM(db.Supplier_Contact_Person, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def suplr_dept_form():
    # chk_que = db((db.Supplier_Master_Department.supplier_id == request.args(0)) &  (db.Supplier_Master_Department.dept_code_id != db.Department.id))
    # print chk_que
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Master_Department.insert(supplier_id = request.args(0),dept_code_id = form.vars.dept_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    row = []
    thead = THEAD(TR(TH('#'),TH('Department'),TH('Status'),TH('Action')))  
    for n in db(db.Supplier_Master_Department.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_dept_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')                  
    return dict(form = form, supplier_id = supplier_id.supp_name, table = table)

@auth.requires_login()
def suplr_dept_edit_form():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    db.Supplier_Master_Department.supplier_id.writable = False
    form = SQLFORM(db.Supplier_Master_Department, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, supplier_id = supplier_id)

def validate_payment_supplier_id(form):
    db.Supplier_Payment_Mode_Details.supplier_id.writable = True
    _id = db(db.Supplier_Master.supp_code == request.vars._ckey).select().first()    
    form.vars.supplier_id = int(_id.id)
    
@auth.requires_login()
def suplr_paymod_form_():    
    form = SQLFORM(db.Supplier_Payment_Mode_Details)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'     
    return dict(form = form, _ckey = _ckey)

@auth.requires_login()
def suplr_paymod_form():    
    _ckey = db(db.Supplier_Master.id == request.args(0)).select().first()    
    form = SQLFORM(db.Supplier_Payment_Mode_Details)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'     
    return dict(form = form, _ckey = _ckey)

@auth.requires_login()
def suplr_paymod_edit_form():
    db.Supplier_Payment_Mode_Details.supplier_id.writable = False
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    _id = db(db.Supplier_Payment_Mode_Details.supplier_id == supplier_id.id).select().first()
    form = SQLFORM(db.Supplier_Payment_Mode_Details, _id or redirect(URL('suplr_paymod_form', args = request.args(0))))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, supplier_id = supplier_id)

@auth.requires_login()
def suplr_add_group_form():
    pre = db(db.Prefix_Data.prefix_key == 'SUP').select().first()
    _skey = pre.serial_key
    _skey += 1
    _ckey = str(_skey).rjust(5,'0')
    ctr_val = pre.prefix + _ckey
    form = SQLFORM(db.Supplier_Master)    
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Master.insert(supp_code = _ckey,supp_name = form.vars.supp_name)
        pre.update_record(serial_key = _skey)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'     
    spm_form = SQLFORM(db.Supplier_Payment_Mode)
    if spm_form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif spm_form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, spm_form = spm_form, ctr_val = ctr_val) 

@auth.requires_login()
def supp_trd_trms():
    form = SQLFORM(db.Supplier_Trade_Terms)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Trade Terms'),TH('Status'),TH('Action')))
    for n in db().select(db.Supplier_Trade_Terms.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('supp_trd_trms_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.trade_terms),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def supp_trd_trms_edit_form():
    form = SQLFORM(db.Supplier_Trade_Terms, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def supp_pay_mode():
    form = SQLFORM(db.Supplier_Payment_Mode)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Payment Mode'),TH('Status'),TH('Action')))
    for n in db().select(db.Supplier_Payment_Mode.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('supp_pay_mode_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.payment_mode),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def supp_pay_mode_edit_form():
    form = SQLFORM(db.Supplier_Payment_Mode, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def supp_pay_term():
    form = SQLFORM(db.Supplier_Payment_Terms)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Payment Terms'),TH('Status'),TH('Action')))
    for n in db().select(db.Supplier_Payment_Terms.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('supp_pay_term_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.payment_terms),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def supp_pay_term_edit_form():
    form = SQLFORM(db.Supplier_Payment_Terms, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def forw_supp():
    pre = db(db.Prefix_Data.prefix_key == 'FOR').select().first()
    if pre:
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        ctr = 0
        form = SQLFORM.factory(
            Field('forwarder_name','string',length = 50),
            Field('forwarder_type','string',length = 5, requires = IS_IN_SET(['AIR','SEA'], zero = 'Choose Type')),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Forwarder_Supplier.insert(forwarder_code = _ckey,forwarder_name = form.vars.forwarder_name,forwarder_type = form.vars.forwarder_type,status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        row = []
        thead = THEAD(TR(TH('#'),TH('Forwarder Code'),TH('Forwarder Name'),TH('Type'),TH('Status'),TH('Action')))
        for n in db().select(db.Forwarder_Supplier.ALL):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled   ', _href=URL('#', args = n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('forw_supp_edit_form', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
            ctr += 1
            row.append(TR(TD(ctr),TD(n.forwarder_code),TD(n.forwarder_name),TD(n.forwarder_type),TD(n.status_id.status),TD(btn_lnk)))
        tbody = TBODY(*row)
        table = TABLE(*[thead,tbody],_class='table table-striped')        
        return dict(form = form, ctr_val = ctr_val,table = table)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('default', 'index'))

@auth.requires_login()
def forw_supp_edit_form():
    _fld = db(db.Forwarder_Supplier.id == request.args(0)).select().first()
    form = SQLFORM(db.Forwarder_Supplier, request.args(0), deletable = True)    
    if form.process().accepted:        
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, _fld = _fld)

# ---- GroupLine Master  -----
@auth.requires_login()
def groupline_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Group Line Code'),TH('Group Line Name'),TH('Supplier Code'),TH('Supplier Name'),TH('Status'),TH('Actions')))
    query = db(db.GroupLine).select(db.GroupLine.ALL, db.Supplier_Master.ALL, left = db.Supplier_Master.on(db.Supplier_Master.id == db.GroupLine.supplier_id))
    for n in query:
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('groupline_edit_form', args = n.GroupLine.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        supp_lnk = A(I(_class='fas fa-paper-plane'), _title='Go To Supplier(s)', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='#', _href=URL('sbgplne_lnk', args = n.GroupLine.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, supp_lnk)
        row.append(TR(TD(ctr),TD(n.GroupLine.prefix_id.prefix,n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.Supplier_Master.supp_code),TD(n.Supplier_Master.supp_name),TD(n.GroupLine.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(table = table)

@auth.requires_login()
def groupline_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'GRL').select().first()
    if pre:
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(5,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(        
            Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'GroupLine.group_line_name')]),
            Field('supplier_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
            Field('status_id', 'reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.GroupLine.insert(supplier_id = form.vars.supplier_id,group_line_code = _ckey, group_line_name = form.vars.group_line_name,status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('groupline_mas'))

@auth.requires_login()
def groupline_edit_form():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()
    form = SQLFORM(db.GroupLine, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.prefix_id.prefix+ctr_val.group_line_code)

@auth.requires_login()
def sbgplne_lnk():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()    
    _id = db(db.GroupLine.id == request.args(0)).select().first()
    session.id = _id
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Sub_Group_Line.insert(group_line_code_id = ctr_val,supplier_code_id = form.vars.supplier_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'

    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Supplier Name'), TH('Status'),TH('Action')))
    query = db(db.Sub_Group_Line.group_line_code_id == request.args(0)).select(db.Sub_Group_Line.ALL, db.Supplier_Master.ALL, left = db.Supplier_Master.on(db.Supplier_Master.id == db.Sub_Group_Line.supplier_code_id))
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sub_Group_Line.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sbgplne_lnk_edit_form', args = n.Sub_Group_Line.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sub_Group_Line.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Sub_Group_Line.id),TD(n.Sub_Group_Line.supplier_code_id.supp_code),TD(n.Supplier_Master.supp_name),TD(n.Sub_Group_Line.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table=table, ctr_val = ctr_val)

@auth.requires_login()
def sbgplne_lnk_edit_form():
    form = SQLFORM(db.Sub_Group_Line, request.args(0), deletable= True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def sbgplne_lnk_add_form():
    ctr_val = db(db.GroupLine.id == session.id).select().first()
    sub_grp_lne_id = db(db.Sub_Group_Line.group_line_code_id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Sub_Group_Line.insert(group_line_code_id = ctr_val,supplier_code_id = form.vars.supplier_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.group_line_name, sub_grp_lne_id = sub_grp_lne_id)

# ---- Brand Line Master  -----
@auth.requires_login()
def brndlne_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Brand Line Code'),TH('Brand Line Name'),TH('Group Line Code'),TH('Group Line Name'),TH('Department'),TH('Status'),TH('Action')))
    query = db(db.Brand_Line).select(db.Brand_Line.ALL, db.GroupLine.ALL, orderby = db.Brand_Line.brand_line_code, left = db.GroupLine.on(db.Brand_Line.group_line_id == db.GroupLine.id))
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Line.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brndlne_edit_form', args = n.Brand_Line.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Line.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.Brand_Line.prefix_id.prefix,n.Brand_Line.brand_line_code),TD(n.Brand_Line.brand_line_name),TD(n.GroupLine.prefix_id.prefix,n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.Brand_Line.dept_code_id),TD(n.Brand_Line.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(table=table)

def showgroupline():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Brand Line Code'),TH('Brand Line Name')))
    for g in db(db.Brand_Line.group_line_id == request.vars.group_line_id).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(g.prefix_id.prefix,g.brand_line_code),TD(g.brand_line_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return table

@auth.requires_login()
def brndlne_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'BRL').select().first()
    if pre:        
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(5,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('group_line_id', 'reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')),
            Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
            Field('brand_line_code', 'string', default = _ckey),
            Field('brand_line_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Line.brand_line_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Brand_Line.insert(prefix_id = pre.id,
            group_line_id = form.vars.group_line_id,
            dept_code_id = form.vars.dept_code_id,
            brand_line_code = _ckey,
            brand_line_name = form.vars.brand_line_name,
            status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('brndlne_mas'))

@auth.requires_login()
def brndlne_edit_form():
    db.Brand_Line_Department.brand_line_code_id.writable = False
    db.Brand_Line.dept_code_id.writable = False
    ctr_val = db(db.Brand_Line.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Line, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    
    dform = SQLFORM(db.Brand_Line_Department)
    if dform.process(onvalidation = validate_brand_line_department).accepted:
        response.flash = 'RECORD  SAVE'
    elif dform.errors:
        response.flash = 'ENTRY HAS ERRORS'

    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Brand Line'),TH('Department'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Line_Department.brand_line_code_id == request.args(0)).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brand_line_department_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.brand_line_code_id.brand_line_name),TD(n.dept_code_id.dept_code + ' - ' + n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')        
    return dict(form = form, ctr_val = ctr_val, dform = dform, table = table)

def brand_line_department_edit_form():
    form = SQLFORM(db.Brand_Line_Department, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('brndlne_mas'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def validate_brand_line_department(form):
    form.vars.brand_line_code_id = request.args(0)

# ---- Brand Classification Master  -----
@auth.requires_login()
def brndclss_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Brand Classficaion Code'),TH('Brand Classification Name'),TH('Group Line Name'),TH('Department'),TH('Brand Line Name'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Classification).select(db.Brand_Classification.ALL, db.Brand_Line.ALL, db.GroupLine.ALL, orderby = db.Brand_Classification.brand_cls_code, left = [db.Brand_Line.on(db.Brand_Line.id == db.Brand_Classification.brand_line_code_id), db.GroupLine.on(db.Brand_Line.group_line_id == db.GroupLine.id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Classification.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brndclss_edit_form', args = n.Brand_Classification.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Classification.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.Brand_Classification.prefix_id.prefix,n.Brand_Classification.brand_cls_code),
        TD(n.Brand_Classification.brand_cls_name),
        TD(n.GroupLine.group_line_name),
        TD(n.Brand_Classification.dept_code_id),
        TD(n.Brand_Line.brand_line_name),TD(n.Brand_Classification.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(table=table)

def showbrandclass():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Brand Code'),TD('Brand Class Name')))
    for c in db(db.Brand_Classification.brand_line_code_id == request.vars.brand_line_code_id).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(c.brand_cls_code),TD(c.brand_cls_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return table
    

@auth.requires_login()
def brndclss_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'BRC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        
        _ckey = str(_skey).rjust(5, '0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
    	    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')), #ERROR - * Field should not be empty
            Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
            Field('brand_line_code_id','reference Brand_Line', label = 'Brand Line Code',requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
            Field('brand_cls_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Brand_Classification.insert(prefix_id = pre.id, 
            	group_line_id = form.vars.group_line_id,
                dept_code_id = form.vars.dept_code_id,
            	brand_line_code_id = form.vars.brand_line_code_id,
            	brand_cls_code = _ckey,
            	brand_cls_name = form.vars.brand_cls_name,
            	status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'

        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('brndclss_mas'))

@auth.requires_login()
def brndclss_edit_form():
    db.Brand_Classification.group_line_id.writable = False
    db.Brand_Classificatin_Department.brand_cls_code_id.writable = False
    # db.Brand_Classification.dept_code_id.writable = False
    ctr_val = db(db.Brand_Classification.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Classification, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    bform = SQLFORM(db.Brand_Classificatin_Department)
    if bform.process(onvalidation = validate_brand_classification_department).accepted:
        response.flash = 'RECORD SAVE'
    elif bform.errors:
        response.flash = 'ENTRY HAS ERRORS'

    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Brand Classification'),TH('Department'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Classificatin_Department.brand_cls_code_id == request.args(0)).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brand_classification_department_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        row.append(TR(TD(ctr),TD(n.brand_cls_code_id.brand_cls_name),TD(n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, ctr_val = ctr_val, bform = bform, table = table)

def validate_brand_classification_department(form):
    form.vars.brand_cls_code_id = request.args(0)

def brand_classification_department_edit_form():
    form = SQLFORM(db.Brand_Classificatin_Department, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('brndclss_mas'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)
# ---- Item Color Master  -----
@auth.requires_login()
def itmcol_mas():
    form = SQLFORM(db.Item_Color)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Color Name'),TH('Action')))    
    ctr = 0
    for n in db(db.Item_Color).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmcol_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.color_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')     
    return dict( form = form, table = table)

@auth.requires_login()
def itmcol_edit_form():
    form = SQLFORM(db.Item_Color, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Item Size Master  -----
@auth.requires_login()
def itmsze_mas():
    form = SQLFORM(db.Item_Size)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH()))    
    for n in db(db.Item_Size).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmsze_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form=form, table=table)

@auth.requires_login()
def itmsze_edit_form():
    
    form = SQLFORM(db.Item_Size, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Item Color Master  -----
@auth.requires_login()
def itmcoll_mas():
    form = SQLFORM(db.Item_Collection)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))    
    for n in db(db.Item_Collection).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmcoll_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    

    return dict(form=form, table=table)

@auth.requires_login()
def itmcoll_edit_form():
    form = SQLFORM(db.Item_Collection, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        # redirect(URL('default','itmcoll_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Made In Master  -----
@auth.requires_login()
def mdein_mas():
    form = SQLFORM(db.Made_In)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Made_In).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('mdein_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def mdein_edit_form():
    form = SQLFORM(db.Made_In, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Currency Master  -----
@auth.requires_login()
def curr_mas():
    form = SQLFORM(db.Currency)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Currency).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('curr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def curr_edit_form():
    form = SQLFORM(db.Currency, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Brand Master      -----
@auth.requires_login()
def brand_mas():
    form = SQLFORM(db.brandmas)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form)

# ---- Item Master      -----
@auth.requires_login()
def itm_typ_mas():  
    form = SQLFORM(db.Item_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db().select(orderby = db.Item_Type.mnemonic):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def itm_type_edit_form():
    form = SQLFORM(db.Item_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Supplier UOM Master      ----- 
# ---- to remove 
@auth.requires_login()
def suplr_uom_mas():  
    form = SQLFORM(db.Supplier_UOM)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_UOM).select():
        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_uom_edit_master', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)
@auth.requires_login()
def suplr_uom_edit_master():
    form = SQLFORM(db.Supplier_UOM, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

# ---- Weight Master   -----
@auth.requires_login()
def itm_weight():
    form = SQLFORM(db.Weight)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Weight).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

# ---- UOM Master      -----
# used both uom item and uom supplier
@auth.requires_login()
def uom_mas():  
    form = SQLFORM(db.UOM)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.UOM).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('uom_edit_master', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def uom_edit_master():
    form = SQLFORM(db.UOM, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

# ---- Color Master      -----
@auth.requires_login()
def col_mas():  
    form = SQLFORM(db.Color_Code)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Color'),TH('Action')))
    ctr = 0
    for n in db(db.Color_Code).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('col_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def col_edit_form():
    form =SQLFORM(db.Color_Code, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- ITEM Master Division  -----    
@auth.requires_login()
def itm_mas():    
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Int Barcode'),TH('Loc Barcode'),TH('Group Line'),TH('Brand Line'),TH('Status'),TH('Actions')))
    for n in db(db.Item_Master).select(orderby = db.Item_Master.item_code):        
        ctr += 1
        link_lnk = A(I(_class='fas fa-info-circle'), _title='Link Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_link_form', args = n.id))
        # view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(link_lnk, prin_lnk,edit_lnk, dele_lnk)        
        row.append(TR(TD(ctr),TD('ITM'+n.item_code),TD(n.item_description.upper()),TD(n.int_barcode),TD(n.loc_barcode),TD(n.group_line_id.group_line_name),TD(n.brand_line_code_id.brand_line_name),TD(n.item_status_code_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    return dict(table = table)

@auth.requires_login()
def itm_add_batch_form():
    db.Item_Master.item_code.writable = False
    db.Item_Master.item_description_ar.writable = False
    form = SQLFORM.factory(
        Field('item_description', 'string', label = 'Description', requires = IS_UPPER()),    
        Field('supplier_item_ref', 'string', length = 20, requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
        Field('int_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
        Field('loc_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
        Field('purchase_point', 'integer', default = 40),
        Field('uom_value', 'integer', default =1),    
        Field('uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM, '%(description)s', zero = 'Choose UOM Pack Size')),
        Field('supplier_uom_value', 'integer', default =1 ),
        Field('supplier_uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM, '%(description)s', zero = 'Choose UOM Pack Size')),
        Field('weight_value', 'integer'),
        Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(description)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(description)s', zero = 'Choose Type')), # saleable/non-saleable
        Field('selective_tax','string'),
        Field('vat_percentage','string'),    
        Field('division_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', default = 1, requires = IS_IN_DB(db, db.Item_Size.id, '%(description)s', zero = 'Choose Item Size')), #widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='')),    
        Field('gender_code_id','reference Gender',  requires = IS_IN_DB(db, db.Gender.id,'%(description)s', zero = 'Choose Gender')),
        Field('fragrance_code_id','reference Fragrance_Type',  requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(description)s', zero = 'Choose Fragrance Type')),
        Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = 'Choose Color')),
        Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(description)s', zero = 'Choose Collection')),
        Field('made_in_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(description)s', zero = 'Choose Country')),
        Field('item_status_code_id','reference Status', default = 1, requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        fnd = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()        
        _range = xrange(len(request.vars['counter']))

        # response.flash = _range
        if len(_range) <= 1:
            ctr = db(db.Item_Master).count()
            ctr = ctr + 1
            ctr = str(ctr).rjust(5,'0')
            itm_code = fnd.supp_code[-5:]+ctr
            db.Item_Master.insert(
                item_code = itm_code,
                item_description = form.vars.item_description,
                supplier_item_ref =form.vars.supplier_item_ref,
                int_barcode = form.vars.int_barcode,
                loc_barcode = form.vars.loc_barcode,
                size_code_id = form.vars.size_code_id,
                gender_code_id = form.vars.gender_code_id,
                fragrance_code_id = form.vars.fragrance_code_id,
                color_code_id = form.vars.color_code_id,
                purchase_point = form.vars.purchase_point,
                uom_value = form.vars.uom_value,
                uom_id = form.vars.uom_id,
                supplier_uom_value = form.vars.supplier_uom_value,
                supplier_uom_id = form.vars.supplier_uom_id,
                weight_value = form.vars.weight_value,
                weight_id = form.vars.weight_id,
                type_id = form.vars.type_id,
                selective_tax = form.vars.selective_tax,
                vat_percentage = form.vars.vat_percentage,
                division_id = form.vars.division_id,
                dept_code_id = form.vars.dept_code_id,
                supplier_code_id = form.vars.supplier_code_id,
                product_code_id = form.vars.product_code_id,
                subproduct_code_id = form.vars.subproduct_code_id,
                group_line_id = form.vars.group_line_id,
                brand_line_code_id = form.vars.brand_line_code_id,
                brand_cls_code_id = form.vars.brand_cls_code_id,
                section_code_id = form.vars.section_code_id,
                collection_code_id = form.vars.collection_code_id,
                made_in_id = form.vars.made_in_id,
                item_status_code_id = form.vars.item_status_code_id)
        else:
            for v in xrange(len(request.vars['counter'])):            
                ctr = db(db.Item_Master).count()
                ctr = ctr + 1
                ctr = str(ctr).rjust(5,'0')
                itm_code = fnd.supp_code[-5:]+ctr
                db.Item_Master.insert(
                    item_code = itm_code,
                    item_description = request.vars['item_description'][v],
                    supplier_item_ref =request.vars['supplier_item_ref'][v],
                    int_barcode = request.vars['int_barcode'][v],
                    loc_barcode = request.vars['loc_barcode'][v],

                    # size_code_id = form.vars.size_code_id[v],
                    # gender_code_id = form.vars.gender_code_id[v],
                    # fragrance_code_id = form.vars.fragrance_code_id[v],
                    # color_code_id = form.vars.color_code_id[v],

                    size_code_id = form.vars.size_code_id,
                    gender_code_id = form.vars.gender_code_id,
                    fragrance_code_id = form.vars.fragrance_code_id,
                    color_code_id = form.vars.color_code_id,

                    purchase_point = form.vars.purchase_point,
                    uom_value = form.vars.uom_value,
                    uom_id = form.vars.uom_id,
                    supplier_uom_value = form.vars.supplier_uom_value,
                    supplier_uom_id = form.vars.supplier_uom_id,
                    weight_value = form.vars.weight_value,
                    weight_id = form.vars.weight_id,
                    type_id = form.vars.type_id,
                    selective_tax = form.vars.selective_tax,
                    vat_percentage = form.vars.vat_percentage,
                    division_id = form.vars.division_id,
                    dept_code_id = form.vars.dept_code_id,
                    supplier_code_id = form.vars.supplier_code_id,
                    product_code_id = form.vars.product_code_id,
                    subproduct_code_id = form.vars.subproduct_code_id,
                    group_line_id = form.vars.group_line_id,
                    brand_line_code_id = form.vars.brand_line_code_id,
                    brand_cls_code_id = form.vars.brand_cls_code_id,
                    section_code_id = form.vars.section_code_id,
                    collection_code_id = form.vars.collection_code_id,
                    made_in_id = form.vars.made_in_id,
                    item_status_code_id = form.vars.item_status_code_id)
                
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
        # response.flash = _range
        # response.flash = form.vars.size_code_id
    return dict(form = form)

@auth.requires_login()
def itm_add_form():
    itm = db(db.Division.id == request.args(0)).select().first()
    ctr = db(db.Item_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')    
    form = SQLFORM.factory(
        Field('division_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('item_description', 'string', label = 'Description', requires = IS_UPPER()),    
        Field('item_description_ar', 'string', label = 'Arabic Name', requires = IS_UPPER()),
        Field('supplier_item_ref', 'string', length = 20, requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
        Field('int_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
        Field('loc_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
        Field('purchase_point', 'integer', default = 40),
        Field('uom_value', 'integer', default = 1),
        Field('uom_id', 'reference UOM', default = 1,requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose UOM Text')),
        Field('supplier_uom_value', 'integer', default = 1),
        Field('supplier_uom_id', 'reference UOM', requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose Supplier UOM') ),
        Field('weight_value', 'integer'),
        Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(description)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(description)s', zero = 'Choose Type')), # saleable/non-saleable
        Field('selectivetax','decimal(10,2)', default = 0, label = 'Selective Tax'),    
        Field('vatpercentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),    
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(description)s', zero = 'Choose Size')),    
        Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(description)s', zero = 'Choose Gender')),
        Field('fragrance_code_id','reference Fragrance_Type', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(description)s', zero = 'Choose Fragrance Code')),
        Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = None)),
        Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(description)s', zero = 'Choose Collection')),
        Field('made_in_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(description)s', zero = 'Choose Country')),
        Field('item_status_code_id','reference Status', default = 1, requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        
        fnd = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()
        itm_code = fnd.supp_code[-5:]+ctr
        db.Item_Master.insert(
            division_id = form.vars.division_id, 
            dept_code_id = form.vars.dept_code_id, 
            item_code = itm_code,
            item_description = form.vars.item_description,
            item_description_ar = form.vars.item_description_ar,
            supplier_item_ref = form.vars.supplier_item_ref,
            int_barcode = form.vars.int_barcode,
            loc_barcode = form.vars.loc_barcode,
            purchase_point = form.vars.purchase_point,
            uom_value = form.vars.uom_value,
            uom_id = form.vars.uom_id,
            supplier_uom_value = form.vars.supplier_uom_value,
            supplier_uom_id = form.vars.supplier_uom_id,
            weight_value = form.vars.weight_value,
            weight_id = form.vars.weight_id,
            type_id = form.vars.type_id,
            selective_tax = form.vars.selective_tax,
            vat_percentage = form.vars.vat_percentage,        
            supplier_code_id = form.vars.supplier_code_id,
            product_code_id = form.vars.product_code_id,
            subproduct_code_id = form.vars.subproduct_code_id,
            group_line_id = form.vars.group_line_id,
            brand_line_code_id = form.vars.brand_line_code_id,
            brand_cls_code_id = form.vars.brand_cls_code_id,
            section_code_id = form.vars.section_code_id,
            size_code_id = form.vars.size_code_id,
            gender_code_id = form.vars.gender_code_id,
            fragrance_code_id = form.vars.fragrance_code_id,
            color_code_id = form.vars.color_code_id,
            collection_code_id = form.vars.collection_code_id,
            made_in_id = form.vars.made_in_id,
            item_status_code_id = form.vars.item_status_code_id)
        response.flash = 'ITEM CODE '+str(itm_code)+'. RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'        
    return dict(form = form, itm = itm)


@auth.requires_login()
def itm_edit_form():
    db.Item_Master.uom_value.writable = False
    db.Item_Master.uom_id.writable = False
    db.Item_Master.division_id.writable = False
    db.Item_Master.dept_code_id.writable = False
    db.Item_Master.supplier_code_id.writable = False
    _fld = db(db.Item_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Item_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form, _fld = _fld)

@auth.requires_login()
def itm_link():
    db.Item_Master.division_id.writable = False
    db.Item_Master.dept_code_id.writable = False
    db.Item_Master.supplier_code_id.writable = False
    _fld = db(db.Item_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Item_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, _fld = _fld)    
def itm_view_pop(x = request.args(0)):
    for x in db(db.Item_Master.id == x).select(db.Item_Master.ALL):
        t = TABLE(*[
            TR(TD('Item Code:  '), TD(x.item_code, _style = 'text-align: right')),
            TR(TD('Item Desc.: '), TD(x.item_description, _style = 'text-align: right')),
            TR(TD('Item Desc.AR: '), TD(x.item_description_ar, _style = 'text-align: right')),
            TR(TD('Supplier Item Ref.: '), TD(x.supplier_item_ref, _style = 'text-align: right')),
            TR(TD('Int. Barcode:  '), TD(x.int_barcode, _style = 'text-align: right')),
            TR(TD('Loc. Barcode:  '), TD(x.loc_barcode, _style = 'text-align: right')),
            TR(TD('ReOrder Value:  '), TD(x.purchase_point, _style = 'text-align: right')),
            TR(TD('UOM:  '), TD(x.uom_value, _style = 'text-align: right')),
            TR(TD('Supplier UOM:  '), TD(x.supplier_uom_value,' ', x.supplier_uom_id.description or None, _style = 'text-align: right')),
            TR(TD('Weight:  '), TD(x.weight_value, _style = 'text-align: right')),
            TR(TD('Item Type:  '), TD(x.type_id, _style = 'text-align: right')),
            TR(TD('Selective Tax:  '), TD(x.selective_tax, _style = 'text-align: right')),
            TR(TD('Vat Percentage:  '), TD(x.vat_percentage, _style = 'text-align: right')),
            TR(TD('Division:'), TD(x.division_id.div_name, _style = 'text-align: right')),
            TR(TD('Department:'), TD(x.dept_code_id.dept_name, _style = 'text-align: right')),
            TR(TD('Supplier:'), TD(x.supplier_code_id.supp_name, _style = 'text-align: right')),
            TR(TD('Product:'), TD(x.product_code_id.product_code, _style = 'text-align: right')),
            TR(TD('SubProduct:'), TD(x.subproduct_code_id.subproduct_code, _style = 'text-align: right')),
            TR(TD('Group Line:'), TD(x.group_line_id.group_line_name, _style = 'text-align: right')),
            TR(TD('Brand Line:'), TD(x.brand_line_code_id.brand_line_name, _style = 'text-align: right')),
            TR(TD('Brand Cls Code:'), TD(x.brand_cls_code_id.brand_cls_name, _style = 'text-align: right')),
            TR(TD('Section Code:'), TD(x.section_code_id.section_name, _style = 'text-align: right')),
            TR(TD('Size Code:'), TD(x.size_code_id.description, _style = 'text-align: right')),
            TR(TD('Gender:'), TD(x.gender_code_id.gender_name, _style = 'text-align: right')),
            TR(TD('Fragrance Code:'), TD(x.fragrance_code_id.fragrance_name, _style = 'text-align: right')),
            TR(TD('Color:'), TD(x.color_code_id.description, _style = 'text-align: right')),
            TR(TD('Collection:'), TD(x.collection_code_id.collection_name, _style = 'text-align: right')),
            TR(TD('Made In:'), TD(x.made_in_id.description, _style = 'text-align: right')),
            TR(TD('Status:'), TD(x.item_status_code_id.status, _style = 'text-align: right'))])
    table = str(XML(t, sanitize = False))
    return table
@auth.requires_login()
def itm_link_form():

    return dict()

def item_master_profile():
    _query = db(db.Item_Master.id == request.args(0)).select().first()
    if _query:
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Description En'),TD('Description AR'),TD('Supplier Ref.'),TD('Barcode Int.'),TD('Barcode Loc.'),TD('Purchase Point'), _class='active'),
            TR(TD(_query.item_code),TD(_query.item_description),TD(_query.item_description_ar),TD(_query.supplier_item_ref),TD(_query.int_barcode),TD(_query.loc_barcode),TD(_query.purchase_point)))
        table1 = TABLE(*[tbody1],_class = 'table table-bordered')
        tbody2 = TBODY(
            TR(TD('IB'),TD('UOM'),TD('Supplier UOM'),TD('Weight'),TD('Type'),TD('Selective Tax'), _class='active'),
            TR(TD(_query.ib),TD(_query.uom_value, ' ', _query.uom_id.description),TD(_query.supplier_uom_value, ' ', _query.supplier_uom_id.description),TD(_query.weight_value, ' ', _query.weight_id),TD(_query.type_id.description),TD(_query.selectivetax)))
        table2 = TABLE(*[tbody2], _class = 'table table-bordered')
        tbody3 = TBODY(
            TR(TD('Division'),TD('Department'),TD('Supplier'),TD('Product'),TD('Subproduct'),_class='active'),
            TR(TD(_query.division_id.div_code, ' - ', _query.division_id.div_name),TD(_query.dept_code_id.dept_code, ' - ', _query.dept_code_id.dept_name),TD(_query.supplier_code_id.supp_name),TD(_query.product_code_id.product_name),TD(_query.subproduct_code_id.subproduct_name)))
        table3 = TABLE(*[tbody3], _class = 'table table-bordered')

        return DIV(table1, table2, table3)        
    else:
        return CENTER(DIV(B('INFO! '),'No item master record.',_class='alert alert-info',_role='alert'))

def item_master_prices():    
    _query = db(db.Item_Prices.item_code_id == request.args(0)).select().first()
    if _query:
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Recent Cost'),TD('Average Cost'),TD('Landed Cost'),TD('Op. Average Cost'),_class='active'),
            TR(TD(_query.item_code_id.item_code),TD(_query.most_recent_cost),TD(_query.average_cost),TD(_query.most_recent_landed_cost),TD(_query.opening_average_cost)))
        table1 = TABLE(*[tbody1],_class = 'table table-bordered')

        tbody2 = TBODY(
            TR(TD('Wholesale Price'),TD('Retail Price'),TD('Vansale Price'),TD('Reorder Qty'),TD('Last Issued Date'),TD('Currency'),_class='active'),
            TR(TD(_query.wholesale_price),TD(_query.retail_price),TD(_query.vansale_price),TD(_query.reorder_qty),TD(_query.last_issued_date),TD(_query.currency_id.description)))
        table2 = TABLE(*[tbody2],_class = 'table table-bordered')
        return DIV(table1, table2)        
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item price record.',_class='alert alert-info',_role='alert'))

def item_master_stocks():
    return CENTER(DIV(B('INFO! '),'Still in progress.',_class='alert alert-info',_role='alert'))
def item_master_batch_info():    
    return CENTER(DIV(B('INFO! '),'Still in progress.',_class='alert alert-info',_role='alert'))
def item_master_sales_quantity():
    return CENTER(DIV(B('INFO! '),'Still in progress.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def itm_link_profile():
    form = SQLFORM(db.Item_Master, request.args(0))
    _itim_master = db(db.Item_Master.id == request.args(0)).select().first()
    return dict(_itim = _item_master)

# ------------------------------------------------------------------------------------------
# ----------------------------  S   E   T   T   I   N   G   S  -----------------------------
# ------------------------------------------------------------------------------------------

# ---- Prefix Master       -----
@auth.requires_login()
def pre_mas():
    form = SQLFORM(db.Prefix_Data)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'        
    row = []
    thead = THEAD(TR(TH('ID'),TH('Prefix'),TH('Prefix Key'),TH('Serial Key'),TH('Prefix Name'),TH('Action')))
    query = db(db.Prefix_Data).select(db.Prefix_Data.ALL, orderby = db.Prefix_Data.id)
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('edit_pre_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled',  _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        edit_lnk = A('Edit', _href=URL('edit_pre_form', args=n.id ))
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_key),TD(n.serial_key),TD(n.prefix_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def pre_add_form():
    form = SQLFORM(db.Prefix_Data)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def edit_pre_form():
    form = SQLFORM(db.Prefix_Data, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('pre_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'    
    return dict(form = form)

# ---- Transaction Prefix Master       -----
@auth.requires_login()
def trns_pre_mas():
    row = []
    thead = THEAD(TR(TH('ID'),TH('Prefix'),TH('Prefix Name'),TH('Prefix Key'),TH('Department'),TH('Current Year Serial'),TH('Previous Year Serial'),TH('Action')))
    query = db(db.Transaction_Prefix).select()
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('trns_pre_edit_mas', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        edit_lnk = A('Edit', _href=URL('edit_pre_form', args=n.id ))
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.prefix_key),TD(n.dept_code_id.dept_name),TD(n.current_year_serial_key),TD(n.previous_year_serial_key),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(table = table)

@auth.requires_login()
def trns_pre_add_mas():
    form = SQLFORM(db.Transaction_Prefix)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def trns_pre_edit_mas():
    form = SQLFORM(db.Transaction_Prefix, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED',
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'    
    return dict(form = form)

# ---- Division Master       -----
def div_err(form):
    return "jQuery('[href='#tab1']').tab('show');"

@auth.requires_login()
def div_mas():    
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Code'),TH('Name'),TH('Status'),TH('Action')))
    for n in db(db.Division).select(db.Division.ALL, db.Prefix_Data.ALL, left = db.Prefix_Data.on(db.Prefix_Data.id == db.Division.prefix_id)):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('div_edit_form', args = n.Division.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('div_edit_form', args = n.Division.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('div_edit_form', args = n.Division.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr +=1
        row.append(TR(TD(ctr),TD(n.Prefix_Data.prefix,n.Division.div_code),TD(n.Division.div_name),TD(n.Division.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')
    return dict(table=table)

@auth.requires_login()
def _update_division(form):
    pre = db(db.Prefix_Data.prefix_key == 'DIV').select().first()
    _skey = pre.serial_key
    _skey += 1    
    pre.update_record(serial_key = _skey)   

@auth.requires_login()
def div_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'DIV').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1        
        _ckey = str(_skey).rjust(2, '0')
        ctr_val = pre.prefix+_ckey
        form = SQLFORM.factory(
            Field('div_name','string', length = 50, label = 'Division Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Division.div_name')]), 
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id, '%(status)s', zero='Choose Status')))
        if form.process(onvalidation = _update_division).accepted:
            db.Division.insert(prefix_id = pre.id, div_code = _ckey, div_name = form.vars.div_name, status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)    
            response.flash = 'RECORD SAVE'
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'   
        return dict(form=form,ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('div_mas'))

@auth.requires_login()
def div_edit_form():
    ctr_val = db(db.Division.id == request.args(0)).select().first()
    form = SQLFORM(db.Division, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'     
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, ctr_val = ctr_val.prefix_id.prefix+ctr_val.div_code)

# ---- Department Master  -----
@auth.requires_login()
def dept_mas(): # change to division name
    ctr = 0
    row = []
    thead = THEAD(TR(TH('ID'),TH('Department Code'),TH('Department Name'),TH('Status'),TH('Actions')))    
    for n in db().select(db.Department.ALL, db.Division.ALL, db.Prefix_Data.ALL, left = [db.Division.on(db.Division.id == db.Department.div_code_id), db.Prefix_Data.on(db.Prefix_Data.id == db.Department.prefix_id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('dept_edit_form', args = n.Department.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('dept_edit_form', args = n.Department.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('dept_edit_form', args = n.Department.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.Prefix_Data.prefix,n.Department.dept_code),TD(n.Department.dept_name),TD(n.Department.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table=table)
@auth.requires_login()
def dept_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'DEP').select().first()   
    if pre:
        _skey = pre.serial_key
        _skey += 1    
        _ckey = str(_skey).rjust(2, '0')
        ctr_val = pre.prefix+_ckey
        form = SQLFORM.factory(
            Field('div_code_id', 'reference Division', label='Division Code',requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division')),
            Field('dept_code', label = 'Department Code', default = ctr_val),
            Field('dept_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.dept_name')]),
            Field('order_qty', 'integer', default = 40),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'NEW RECORD SAVE'
            db.Department.insert(
                prefix_id = pre.id,
                div_code_id = form.vars.div_code_id,
                dept_code=_ckey,
                dept_name=form.vars.dept_name,
                status_id=form.vars.status_id)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('dept_mas'))
@auth.requires_login()
def dept_edit_form():
    ctr_val = db(db.Department.id == request.args(0)).select(db.Department.dept_code).first()
    form = SQLFORM(db.Department, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form, ctr_val = ctr_val.dept_code)

# ---- Item Status Master       -----
@auth.requires_login()
def stat_mas():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Status.ALL, orderby=db.Status.status):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('stat_edit_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stat_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('stat_edit_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')
    return dict(form = form, table = table)
@auth.requires_login()
def stat_add_form():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)
@auth.requires_login()
def stat_edit_form():
    form = SQLFORM(db.Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'    
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)
# ---- Stock/Sales Master  -----
@auth.requires_login()
def stock_n_sale_status():
    form = SQLFORM(db.Stock_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action')))
    for n in db(db.Stock_Status).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_n_sale_status_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.required_action),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table table-hover')
    return dict(form = form, table = table)

@auth.requires_login()
def stock_n_sale_status_edit_form():
    form = SQLFORM(db.Stock_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Record Status Master  -----
@auth.requires_login()
def recst_mas():
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(orderby = db.Record_Status.status):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('recst_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table table-hover')
    return dict(form = form, table = table)
@auth.requires_login()
def recst_add_form(): # to remove
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)
@auth.requires_login()
def recst_edit_form():
    db.Record_Status.id.readable = False
    form = SQLFORM(db.Record_Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)


# ---- Made In Master  -----
@auth.requires_login()
def sec_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Section Code'),TH('Section Name'),TH('Status'),TH()))    
    for n in db(db.Section).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sec_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.section_code),TD(n.section_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')    
    return dict(table = table)
@auth.requires_login()
def sec_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'SEC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('section_name','string',length=25, requires = [IS_UPPER(), IS_LENGTH(25), IS_NOT_IN_DB(db, 'Section.section_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Section.insert(prefix_id = pre.id, section_code = _ckey,section_name = form.vars.section_name,status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('sec_mas'))
@auth.requires_login()
def sec_edit_form():
    ctr_val = db(db.Section.id == request.args(0)).select().first()
    form = SQLFORM(db.Section, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.prefix_id.prefix+ctr_val.section_code)

# ---- Transaction Master -----
@auth.requires_login()
def trans_mas():
    form = SQLFORM(db.trnmas)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form)

# ---- Gender Master   -----
@auth.requires_login()
def gndr_mas():
    form = SQLFORM(db.Gender)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))
    ctr = 0
    for n in db(db.Gender).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('gndr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled  ', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        ctr += 1
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, table = table)

@auth.requires_login()
def gndr_edit_form():
    
    form = SQLFORM(db.Gender, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Location Sub Group Master   -----
@auth.requires_login()
def locsubgrp_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Location Sub-Group Code'),TH('Location Sub-Group Name'),TH('Status'),TH('Action')))
    for n in db(db.Location_Sub_Group).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('locgrp_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(n.id),TD(n.location_sub_group_code),TD(n.location_sub_group_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

@auth.requires_login()
def locsubgrp_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'LSG').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('location_sub_group_code','string',length=10, writable =False),
            Field('location_sub_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location_Sub_Group.location_sub_group_name')]),
            Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Location_Sub_Group.insert(
                prefix_id = pre.id, 
                location_sub_group_code = _ckey, 
                location_sub_group_name = form.vars.location_sub_group_name, 
                status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('locsubgrp_mas'))

# ---- Location Group Master   -----
@auth.requires_login()
def locgrp_mas():
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Group Code'),TH('Group Name'),TH('Status'),TH('Action')))
    for n in db(db.Location_Group).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('locgrp_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(ctr),TD(n.prefix_id.prefix,n.location_group_code),TD(n.location_group_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

@auth.requires_login()
def locgrp_add_form():
    # pre = db(db.Prefix_Data).select().first()    
    pre = db(db.Prefix_Data.prefix_key == 'LCG').select().first()
    if pre:
        _skey = pre.serial_key        
        _skey = _skey + 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('location_group_name','string',length=50, requires = [IS_UPPER(), IS_LENGTH(50),IS_NOT_IN_DB(db, 'Location_Group.location_group_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status'))) 
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Location_Group.insert(prefix_id = pre.id, location_group_code = _ckey, location_group_name = form.vars.location_group_name, status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('locgrp_mas'))

@auth.requires_login()
def locgrp_edit_form():
    ctr_val = db(db.Location_Group.id == request.args(0)).select(db.Location_Group.location_group_code).first()
    form = SQLFORM(db.Location_Group, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.location_group_code)

# ---- Location Master   -----
@auth.requires_login()
def loc_mas():
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Location Code'),TH('Location Name'),TH('Location Group Name'),TH('Location Sub Group Name'),TH('Status'),TH('Action')))
    for n in db(db.Location).select(db.Location.ALL, db.Location_Group.ALL, db.Location_Sub_Group.ALL, orderby = db.Location.location_code, 
    left= [db.Location_Group.on(db.Location_Group.id == db.Location.location_group_code_id),
    db.Location_Sub_Group.on(db.Location_Sub_Group.id == db.Location.location_sub_group_id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('loc_edit_form', args = n.Location.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.Location.prefix_id.prefix,n.Location.location_code),
            TD(n.Location.location_name),
            TD(n.Location_Group.location_group_name),
            TD(n.Location_Sub_Group.location_sub_group_name), 
            TD(n.Location.status_id.status),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)
@auth.requires_login()
def loc_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'LOC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(4,'0')
        ctr_val = pre.prefix + _ckey   
        form = SQLFORM.factory(
            Field('location_group_code_id','reference Location_Group', ondelete = 'NO ACTION',label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),    
            Field('location_sub_group_id','reference Location_Sub_Group', ondelete = 'NO ACTION',label = 'Location Sub-Group Code', requires = IS_IN_DB(db, db.Location_Sub_Group.id, '%(location_sub_group_code)s - %(location_sub_group_name)s', zero = 'Choose Location Sub-Group')),
            Field('location_code','string',length=10, writable =False),
            Field('location_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),    
            Field('status_id','reference Record_Status', label = 'Status', default = 1,  requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Location.insert(
                prefix_id = pre.id, 
                location_code = _ckey, 
                location_name = form.vars.location_name, 
                location_group_code_id = form.vars.location_group_code_id, 
                location_sub_group_id = form.vars.location_sub_group_id,
                status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'please fill up the form'

        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('loc_mas'))
@auth.requires_login()
def loc_edit_form():
    # db.Location.stock_adjustment_code.writable = False
    ctr_val = db(db.Location.id == request.args(0)).select().first()
    form = SQLFORM(db.Location, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('loc_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.location_code)

# ---- Fragrance Type Master  -----  
@auth.requires_login()
def frgtype_mas():
    form = SQLFORM(db.Fragrance_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))
    ctr = 0
    for n in db(db.Fragrance_Type).select():
        edit_lnk = A('Edit', _href=URL('frgtype_edit_form', args = n.id ))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('frgtype_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')        
    return dict(form = form ,table = table)

@auth.requires_login()
def frgtype_edit_form():    
    form = SQLFORM(db.Fragrance_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Voucher Master   -----
@auth.requires_login()
def vouc_mas():
    form = SQLFORM(db.trnvou)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form)



def testing():
    form = SQLFORM(db.Item_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'ok'
    

    return dict(form = form)
import datetime

def testing2():
    
    db(db.Stock_Transaction_Temp.created_by ==  auth.user_id).delete()
    form2 = SQLFORM.factory(        
        Field('stock_request_date', 'date', default = datetime.date.today()),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
        Field('stock_due_date','date', default = datetime.date.today()),
        Field('remarks','string'))
    # if form2.process(formname = 'head').accepted:
    if form2.accepts(request.vars):
        response.flash = 'save'
        response.js =  "jQuery('target').get(0).reload();"
    elif form2.errors:
        response.flash = 'invalid values in form!'
    # records = SQLTABLE(db.Stock_Transaction_Temp).select(),headers='fieldname:capitalize')
    # print request.vars.item_code_id, ' from testing 2'
    return dict(form2 = form2)

def tail():
    grand_total = 0
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'reference Transaction_Item_Category', default = 4, requires = IS_IN_DB(db((db.Transaction_Item_Category.mnemonic != 'E') & (db.Transaction_Item_Category.mnemonic != 'S')), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')),
        Field('srn_status_id','reference Stock_Status', default = 3, requires = IS_IN_DB(db(db.Stock_Status.id == 3), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process(formname = 'tail', onvalidation=dups).accepted:        
        
        uom = db(db.Item_Master.id == request.vars.item_code_id).select(db.Item_Master.uom_value).first()
        rpv = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select(db.Item_Prices.retail_price).first()
        total_pcs = int(request.vars.quantity) * int(uom.uom_value) + int(request.vars.pieces)  
        unit_price = int(rpv.retail_price) / int(uom.uom_value)      
        total_amount_value = int(unit_price) * int(total_pcs)

        _id = db(db.Stock_Transaction_Temp.item_code_id == request.vars.item_code_id).select().first()        
      
        
        # stk = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select(db.Stock_File.ALL).first()        
        print request.vars.stock_source_id
        # stk.stock_in_transit += total_pcs
        # stk.probational_balance = int(stk.closing_stock) - int(stk.stock_in_transit)        
        # stk.update_record()

        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        grand_total = db().select(total).first()[total]
        db.Stock_Transaction_Temp.insert(
            item_code_id = form.vars.item_code_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            category_id = form.vars.category_id,
            amount = total_amount_value,
            stock_source_id = request.vars.stock_source_id)
        # grand_total += float(total_amount_value)
        # form.vars.grand_total = grand_total
        # print form.vars.grand_total, 'from grand_total'
        # transact = (db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id) & (db.Stock_Request_Temp.requested_by == db.Stock_Transaction_Temp.created_by)
        # records = SQLTABLE(db().select(db.Stock_Transaction_Temp.ALL),headers='fieldname:capitalize')

        # if _id.category_id.mnemonic == 'P':
        #     # print _id.category_id
        #     # _id.amount = 0.00
        #     # _id.update_record()
        # else:

        # _id.amount = total_amount_value
        # _id.update_record()        

        response.flash = 'item inserted!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
    for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        ctr += 1            
        # edit_lnk = A(I(_class='fas fa-pencil-alt'), _target="blank", _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', _href=URL('testing2', args = k.Stock_Transaction_Temp.id)) #**{'_data-toggle':'modal', '_data-target':'#data-toggle="modal" data-target="#editModal'})
        # dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id), '_data-in':(n.invoice_number)})
        edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', 
        callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), 
        **{
            '_data-id':(k.Stock_Transaction_Temp.id),
            '_data-it':(k.Stock_Transaction_Temp.item_code_id),                
            '_data-qt':(k.Stock_Transaction_Temp.quantity), 
            '_data-pc':(k.Stock_Transaction_Temp.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))
        
        btn_lnk = DIV(edit_lnk, dele_lnk, _class="hidden-sm action-buttons")
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),
        TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),TD(),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')

    return dict(form = form, records = table)

import locale
def testing3():    
    row = []
    total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
    grand_total = db().select(total).first()[total]
            
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
    for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        ctr += 1            
        # view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
        
        edit_lnk = A('EDIT', _title='Edit Row', _onclick = "jQuery(show)", callback=URL(args = k.Stock_Transaction_Temp.id), _class='edit', **{'_data-id':k.Stock_Transaction_Temp.id})

        dele_lnk = A('Delete', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))

        # dele_lnk = A(SPAN(_class = 'fas fa-trash-alt'), _name='btndel',_title="Delete", _onclick = "jQuery(show)",callback=URL(args=k.Stock_Transaction_Temp.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id), '_data-in':(k.Stock_Transaction_Temp.id)})
        # dele_lnk = A('Delete', callback=URL('del_item', args = k.Stock_Transaction_Temp.id  ), delete = 'tr')
        # dele_lnk = A(SPAN(_class = 'fas fa-trash-alt'), _name='btndel',_title="Delete", callback=URL( args=k.Stock_Transaction_Temp.id),_class='delete')
        # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', _onclick = "jQuery().fadeOut()", callback=URL('del_item',args = k.Stock_Transaction_Temp.id))
        btn_lnk = DIV(edit_lnk, dele_lnk, _class="hidden-sm action-buttons")
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id),TD(k.Item_Master.uom_value),TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),TD(k.Item_Prices.retail_price, _align='right'),TD(k.Stock_Transaction_Temp.amount, _align='right'),TD(),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
        
    return dict(table = table)

def itm_prcs():
    form = SQLFORM(db.Item_Prices)       
    return dict(form = form)

# ---- Stock Request Master   -----
def itm_req():
    row = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Group Line'),TH('Brand Line'),TH('Description'),TH('Retail Price'),TH('UOM'),TH('Stock on Hand'),TH('Stock on Transit'),TH('Prov.Bal.')))
    for n in db(db.Item_Master).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), 
    db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)]):
        row.append(TR(TD(n.Item_Master.id),TD(n.Item_Master.item_code),TD(n.Item_Master.group_line_id.group_line_name),TD(n.Item_Master.brand_line_code_id.brand_line_name),TD(n.Item_Master.item_description),TD(n.Item_Prices.retail_price),TD(n.Item_Master.uom_value),TD(n.Stock_File.opening_stock),TD(n.Stock_File.stock_in_transit),TD(n.Stock_File.probational_balance)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return table

def trans_itm_cat_mas():
    form = SQLFORM(db.Transaction_Item_Category)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Transaction_Item_Category).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('trans_itm_cat_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form = form, table = table)
    
def trans_itm_cat_edit_form():
    form = SQLFORM(db.Transaction_Item_Category, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

def json_item():
    value = db().select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, 
    left = [
        db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), 
        db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)])
    return dict(value = value)

def v_complete():
    return dict()
def j_complete():
    
    return locals()

def stk_req_trns():
    form = SQLFORM(db.Stock_Transaction)
    if form.accepts(request, formname = None):
        return TABLE(*[TR(t.item_code_id) for i in db(db.Stock_Transaction).select(orderby=~db.Stock_Transaction.item_code_id)])
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
def stk_tran_grid(): #STORE USERS

    return dict()


def stk_req_val_form(form):
    ctr = db(db.Stock_Request.stock_request_no).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5, '0')
    ctr_val = 'SRN' + ctr            
    form.vars.stock_request_no = ctr_val

def stk_file():
    form = SQLFORM(db.Stock_File)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ERROR'
    return dict(form = form)
    
def validate_item_code(form):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()        

    _id_tmp = db((db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id) & (db.Stock_Transaction_Temp.item_code == request.vars.item_code)).select(db.Stock_Transaction_Temp.item_code).first()        
                
    _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()

    
    _price = db(db.Item_Prices.item_code_id == _id.id).select().first()

    
    
    if not _id:        
        form.errors._id = CENTER(DIV(B('WARNING! '),'Item code does not exist',_class='alert alert-warning',_role='alert'))                        

    if not _stk_file:
        form.errors._stk_file =  CENTER(DIV(B('WARNING! '),'Item code does not exist in stock file',_class='alert alert-warning',_role='alert'))                        

    if not _price:
        form.errors._stk_file =  CENTER(DIV(B('WARNING! '),'Item code does not have price.',_class='alert alert-warning',_role='alert'))        

    qty = form.vars.quantity

    pcs = form.vars.pieces
            
    if (_price.retail_price == float(0.0) or _price.wholesale_price == float(0.0)) and (_id.type_id.mnemonic == 'SALE' or _id.type_id.mnemonic == 'PRO'):
        form.errors._price = CENTER(DIV(B('WARNING! '),'Cannot request this item because retail price is zero',_class='alert alert-warning',_role='alert'))

    if _id_tmp:
        form.errors.item_code_id = CENTER(DIV(B('WARNING! '),'Item Code already exist.',_class='alert alert-warning',_role='alert'))

    if _id.uom_value == 1:
        if pcs > 0:
            form.errors.pieces =  CENTER(DIV(B('WARNING! '),' Pieces value is not applicable to this item.',_class='alert alert-warning',_role='alert')) 
            pcs = 0
        else:
            response.flash = 'ok'
    elif pcs >= int(_id.uom_value):            
        form.errors._id = CENTER(DIV(B('WARNING! '),' Pieces value should  be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-warning',_role='alert')) 
    
    # to be modified 
    # print request.vars.category_id
    if (form.vars.category_id == 3) and (_id.type_id.mnemonic == 'SALE' or _id.type_id.mnemonic == 'PRO'):            
        form.errors.mnemonic = CENTER(DIV(B('WARNING! '),' This saleable item cannot be transfered as FOC.',_class='alert alert-warning',_role='alert')) 
        # ' this saleable item cannot be transfered as FOC'

    # if int(_stk_file.probational_balance) == 0:
    
    _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces)    

    _unit_price = float(_price.retail_price) / int(_id.uom_value)

    _total = float(_unit_price) * int(_total_pcs)
    
    if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):            
        strr = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
        form.errors.quantity = CENTER(DIV(B('WARNING! '),' Quantity should not be more than probational balance ' + str(strr) ,_class='alert alert-warning',_role='alert')) 

    # stk = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select(db.Stock_File.ALL).first()        
    _stk_file.stock_in_transit += _total_pcs    
    _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
    _stk_file.update_record()
    
    if not _stk_file.last_transfer_date:
        _card = card(_stk_file.item_code_id, _stk_file.last_transfer_qty, _id.uom_value)
        _remarks = 'LTD: ' + str(date.today()) + ' - QTY: ' + str(_card)
    else:
        _card = card(_stk_file.item_code_id, _stk_file.last_transfer_qty, _id.uom_value)
        _remarks = 'LTD: ' + str(_stk_file.last_transfer_date.strftime("%y/%m/%d")) + ' - QTY: ' + str(_card)

    form.vars.item_code_id = _id.id
    form.vars.amount = float(_total)
    form.vars.price_cost = float(_unit_price)
    form.vars.remarks = _remarks
    form.vars.qty = _total_pcs


def del_item():
    # print request.vars.grand_total, 'total from del_item'
    itm = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    uom = db(db.Item_Master.id == itm.item_code_id).select().first()
    total_pcs = int(itm.quantity) * int(uom.uom_value) + int(itm.pieces)  

    stk = db((db.Stock_File.item_code_id == itm.item_code_id) & (db.Stock_File.location_code_id == db.Stock_Transaction_Temp.stock_source_id)).select(db.Stock_File.ALL).first()        
    stk.stock_in_transit -= total_pcs
    stk.probational_balance = int(stk.closing_stock) - int(stk.stock_in_transit)        
    stk.update_record()
    total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
    grand_total = db().select(total).first()[total]
    db(db.Stock_Transaction_Temp.id == request.args(0)).delete()

def test_up():
    # print 'from testing3 id', request.args(0), request.args(1), request.args(2)
    # parent = $(this).parent("div").parent("td").parent("tr");
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _tmp = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    # db(db.Stock_Transaction_Temp.id == request.args(0)).delete()
    # return "jQuery('#target').html(%s);" % repr(request.vars.name)
    _tmp.update_record(quantity = _qty, pieces = _pcs)

# itm_description #
def itm_description_():

    _item_char = db(db.Item_Master.item_code == request.vars.item_code_id).select().first()
    if _item_char:

        return _item_char.id
    else:
        return 'wa'

def itm_description():

    _itm_code = db(db.Item_Master.item_code == request.vars.item_code).select().first()       

    if _itm_code:
    
        _item_price = db(db.Item_Prices.item_code_id == _itm_code.id).select().first()
        
        _stk_file = db((db.Stock_File.item_code_id == _itm_code.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()

        if _stk_file:
            _outer = int(_stk_file.probational_balance) / int(_itm_code.uom_value)        
            _pcs = int(_stk_file.probational_balance) - int(_outer * _itm_code.uom_value)    
            _on_hand = str(_outer) + ' ' + str(_pcs) + '/' +str(_itm_code.uom_value)

            _outer_transit = int(_stk_file.stock_in_transit) / int(_itm_code.uom_value)   
            _pcs_transit = int(_stk_file.stock_in_transit) - int(_outer * _itm_code.uom_value)
            _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_itm_code.uom_value)

            _outer_on_hand = int(_stk_file.closing_stock) / int(_itm_code.uom_value)
            _pcs_on_hand = int(_stk_file.closing_stock) / int(_outer_on_hand * _itm_code.uom_value) 
            _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_itm_code.uom_value)
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance'))),
            TBODY(TR(TD(_itm_code.item_code),TD(_itm_code.item_description.upper()),TD(_itm_code.group_line_id.group_line_name),TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),TD(_on_hand),TD(_on_transit),TD(_on_hand)),_class="bg-info"),_class='table'))
    else:       
        return CENTER(DIV(B('WARNING! '),'No item on stock file.',_class='alert alert-warning',_role='alert'))

def itm_view_():
    form = SQLFORM(db.Stock_Transaction_Temp)
    if form.accepts(request, formname = None, onvalidation = validate_item_code):
        response.flash = 'ok'
        return 'table ok'
    elif form.errors:
        response.flash = 'not ok'
        return 'table not ok'

def val(form):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()    
    form.vars.item_code_id = _id.id
    form.vars.amount = float(393.03)

def itm_view():    
    row = []
    uom_value = 0
    retail_price_value = 0
    total_pcs = 0    
    grand_total = 0
    form = SQLFORM(db.Stock_Transaction_Temp)
    if form.accepts(request, formname=None, onvalidation = validate_item_code):    
        
        # uom = db(db.Item_Master.item_code == request.vars.item_code).select().first()
        
        # rpv = db(db.Item_Prices.item_code_id == uom.id).select(db.Item_Prices.retail_price).first()
        
        # total_pcs = int(request.vars.quantity) * int(uom.uom_value) + int(request.vars.pieces)  
        
        # unit_price = float(rpv.retail_price) / int(uom.uom_value)      
        
        # total_amount_value = float(unit_price) * int(total_pcs)

        # _id = db((db.Stock_Transaction_Temp.item_code_id == uom.id)&(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id))).select().first()        
      
        # if _id.category_id.mnemonic == 'P':
        #     # print _id.category_id
        #     # _id.amount = 0.00
        #     # _id.update_record()
        # else:

        # stk = db((db.Stock_File.item_code_id == uom.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select(db.Stock_File.ALL).first()        
        # stk.stock_in_transit += total_pcs
        # stk.probational_balance = int(stk.closing_stock) - int(stk.stock_in_transit)        
        # stk.update_record()
        
        # if stk.last_transfer_date:
        #     _card = card(_id.item_code_id, stk.last_transfer_qty, uom.uom_value)
        #     _remarks = 'LTD: ' + str(stk.last_transfer_date.strftime("%y/%m/%d")) + ' - QTY: ' + str(_card)
        # else:
        #     _card = card(_id.item_code_id, stk.last_transfer_qty, uom.uom_value)
        #     _remarks = 'LTD: ' + str(date.today()) + ' - QTY: ' + str(_card)

        # _id.update_record(qty = total_pcs, amount = total_amount_value, price_cost = unit_price, remarks = str(_remarks))
        
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        grand_total = db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(total).first()[total]

        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(
            db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, 
            left = [
                db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),
                db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        
            ctr += 1            
            
            # edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))            
            # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = k.Stock_Transaction_Temp.id))
            btn_lnk = DIV(dele_lnk)
            row.append(TR(TD(ctr),
            TD(k.Item_Master.item_code),
            TD(k.Item_Master.item_description.upper()),
            TD(k.Stock_Transaction_Temp.category_id.mnemonic),
            TD(k.Item_Master.uom_value),
            TD(k.Stock_Transaction_Temp.quantity),
            TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
        return table
    elif form.errors:

        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
            ctr += 1            
            
            # edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))            
            # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = k.Stock_Transaction_Temp.id))
            btn_lnk = DIV(dele_lnk)
            row.append(TR(TD(ctr),
            TD(k.Item_Master.item_code),
            TD(k.Item_Master.item_description.upper()),
            TD(k.Stock_Transaction_Temp.category_id.mnemonic),
            TD(k.Item_Master.uom_value),
            TD(k.Stock_Transaction_Temp.quantity),
            TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[TR(v) for k, v in form.errors.items()],_class='table')        
        table += TABLE(*[head, body, foot], _id='tblIC',_class='table')
        return table

import string
import random
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
from datetime import date


@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_request_dept_code_id():   
    return SELECT(_class='form-control', _id='stk_item_code_id', _name="stk_item_code_id", *[OPTION(r.item_code, _value = r.id) for r in db(db.Item_Master.dept_code_id == request.vars.dept_code_id).select(orderby=db.Item_Master.item_code)])

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_request_no_prefix():   
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'SRN')).select().first()    
    _serial = _trans_prfx.current_year_serial_key + 1
    _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
    return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True))
    
@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_add_form():          
    ctr = db(db.Transaction_Prefix.prefix_key == 'SRN').select().first()
    _skey = ctr.current_year_serial_key 
    _skey += 1        
    _ticket_no = id_generator()
    form = SQLFORM.factory(       
        Field('ticket_no_id', 'string', default = _ticket_no),
        Field('stock_request_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Location')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Destination')),    
        Field('stock_due_date','date', default = request.now),
        Field('remarks','string'),
        Field('srn_status_id','reference Stock_Status', default = 3, requires = IS_IN_DB(db(db.Stock_Status.id == 3), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:          
        ctr = db((db.Transaction_Prefix.prefix_key == 'SRN')&(db.Transaction_Prefix.dept_code_id == form.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key 
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)
        
        response.flash = 'SAVING STOCK REQUEST NO SRN' +str(_skey) + '.'       
        db.Stock_Request.insert(
            ticket_no = form.vars.ticket_no_id,
            stock_request_no_id = ctr.id,
            stock_request_no = ctr.current_year_serial_key ,
            stock_request_date = request.now,
            stock_requested_by = '%s %s' % (auth.user.first_name.upper(), auth.user.last_name.upper()),
            stock_due_date = form.vars.stock_due_date,
            dept_code_id = form.vars.dept_code_id,
            stock_source_id = form.vars.stock_source_id,
            stock_destination_id = form.vars.stock_destination_id,
            srn_status_id = form.vars.srn_status_id,
            requested_by = auth.user_id,
            remarks = form.vars.remarks)
        _id = db(db.Stock_Request.stock_request_no == ctr.current_year_serial_key ).select().first()
        _src = db((db.Stock_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Transaction_Temp.ticket_no_id == form.vars.ticket_no_id)).select()
        

        for s in _src:
            _itm = db(db.Item_Master.id == s.item_code_id).select().first()
            _prc = db(db.Item_Prices.item_code_id == s.item_code_id).select().first()
            db.Stock_Request_Transaction.insert(
                stock_request_id = _id.id,
                item_code_id = s.item_code_id,
                category_id = s.category_id,
                uom = _itm.uom_value,
                price_cost = s.price_cost,
                quantity = s.qty,               
                average_cost = _prc.average_cost,
                wholesale_price = _prc.wholesale_price,
                retail_price = _prc.retail_price,
                vansale_price = _prc.vansale_price,               
                remarks = s.remarks,
                # ticket_no_id = _id.ticket_no,
                created_by = s.created_by
                )

        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        grand_total = db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(total).first()[total]
        _id.update_record(total_amount = grand_total)

        db((db.Stock_Transaction_Temp.created_by == auth.user_id)&(db.Stock_Transaction_Temp.ticket_no_id == str(_id.ticket_no))).delete()

    elif form.errors:
        response.flash = 'ENTRY HAS ERROR' 

    form2 = SQLFORM.factory(
        Field('item_code', 'string', length = 10),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'reference Transaction_Item_Category', default = 4, requires = IS_IN_DB(db((db.Transaction_Item_Category.mnemonic != 'E') & (db.Transaction_Item_Category.mnemonic != 'S')), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')))
    if form2.process().accepted:
        response.flash = 'record save'
    elif form.errors:
        response.flash = 'error'

    return dict(form = form,  form2 = form2, ticket_no_id = _ticket_no)

# STOCK REQUEST FORM #

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_details_form():
    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.stock_due_date.writable = False        
    db.Stock_Request.dept_code_id.writable = False    
    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.srn_status_id.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')

    db.Stock_Request.stock_request_date_approved.writable = False
    
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORDS UPDATED'
    if form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    # total = db.Stock_Request_Transaction.amount.sum().coalesce_zero()
    # grand_total = db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select(total).first()[total]
    grand_total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks'),TH('Action')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        
        if (_id.srn_status_id == 1) | (_id.srn_status_id == 5) | (_id.srn_status_id == 6):        
            edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle', _disabled="disabled", _href=URL('stk_req__trans_edit_form', args = k.Stock_Request_Transaction.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', _disabled="disabled", delete = 'tr', callback=URL('stk_req_del', args = k.Stock_Request_Transaction.id))            
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle', _href=URL('stk_req__trans_edit_form', args = k.Stock_Request_Transaction.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('stk_req_del', args = k.Stock_Request_Transaction.id))            

        btn_lnk = DIV(edit_lnk,dele_lnk, _class="hidden-sm action-buttons")
        ctr += 1            
        grand_total += int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD( # validate if uom = 1, present whole number
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Item_Prices.retail_price, _align='right'),TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2F',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id)

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_details_add_form():   
    _stk_req_no = db(db.Stock_Request.id == request.args(0)).select().first()
    # _stk_trn_no = db(db.Stock_Request_Transaction.stock_request_id == _stk_req_no.id).select().first()

    return dict(_stk_req_no = _stk_req_no, _stk_trn_no = '_stk_trn_no')

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_form():   
    
    return dict()

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_del():
    itm = db(db.Stock_Request_Transaction.id == request.args(0)).select().first()
    itm.update_record(delete = True)
    # uom = db(db.Item_Master.id == itm.item_code_id).select().first()
    # total_pcs = int(itm.quantity) * int(uom.uom_value) + int(itm.pieces)  

    # stk = db((db.Stock_File.item_code_id == itm.item_code_id) & (db.Stock_File.location_code_id == db.Stock_Request_Transaction.stock_source_id)).select(db.Stock_File.ALL).first()        
    # stk.stock_in_transit -= total_pcs
    # stk.probational_balance = int(stk.closing_stock) - int(stk.stock_in_transit)        
    # stk.update_record()
    # total = db.Stock_Request_Transaction.amount.sum().coalesce_zero()
    # grand_total = db().select(total).first()[total]
    # db(db.Stock_Request_Transaction.id == request.args(0)).delete()

def stk_req__trans_edit_form():
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first()
    _tot_amt = _id.quantity * _id.price_cost
    form = SQLFORM(db.Stock_Request_Transaction, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id, _tot_amt = _tot_amt)

# STORE KEEPER

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid():    
    return dict()

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid_details():
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.stock_due_date.writable = False        
    db.Stock_Request.dept_code_id.writable = False    
    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.srn_status_id.writable = False

    db.Stock_Request.stock_request_date_approved.writable = False
    

    # db.Stock_Request.src_status.writable = False
    # db.Stock_Request.item_status_code_id.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 5)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1            
        grand_total += int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Item_Prices.retail_price, _align='right'),TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')    
    return dict(form = form, table = table, _id = _id)

def str_kpr_grid_gen_stk_trn_():  
    print 'redirect to '
    redirect(URL('inventory', 'str_kpr_grid'))  

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid_gen_stk_trn():    

    _stk_req = db(db.Stock_Request.id == request.vars._id).select().first()
    if _stk_req.srn_status_id != 5:

        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_req.dept_code_id) & (db.Transaction_Prefix.prefix == 'STV')).select().first()

        _skey = _trns_pfx.current_year_serial_key
        
        _skey += 1
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        _stk_req.update_record(srn_status_id = 5,stock_transfer_no_id = _trns_pfx.id, stock_transfer_no = _skey, stock_transfer_date_approved = request.now, stock_transfer_approved_by = auth.user_id)
        session.flash = 'SAVING STOCK TRANSFER NO STV' +str(_skey) + '.'       
        redirect(URL('str_kpr_grid'))
    else:
        session.flash = "STOCK TRANSACTION ALREADY PROCESSED"
    


# MANAGER 
@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_req_grid():

    return dict()

def mngr_btn_aprvd():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()

    _id.update_record(srn_status_id = 1, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id)
    session.flash = 'STOCK REQUEST APPROVED'
    redirect(URL('inventory', 'mngr_req_grid'))
    return dict()
    
def mngr_btn_reject():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(srn_status_id = 2, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id)
    session.flash = 'STOCK REQUEST REJECT'
    redirect(URL('inventory', 'mngr_req_grid'))
    return dict()

@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER'))
def mngr_aprvd(form):
    form.vars.stock_request_date_approved = request.now
    form.vars.stock_request_approved_by = auth.user_id


@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER'))
def mngr_req_details():
    # db.Stock_Request.stock_request_approved_by.represent = lambda row: row + ' ' + row if row else ''
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.stock_transfer_date_approved.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 2) | (db.Stock_Status.id == 3)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.auth_user.id.represent = lambda auth_id, row: row.first_name + ' ' + row.last_name
    # db.auth_user._format = '%(first_name)s %(last_name)s'
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process(onvalidation = mngr_aprvd).accepted:
        response.flash = 'APPROVED'
        redirect(URL('inventory', 'mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1            
        grand_total += int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Item_Prices.retail_price, _align='right'),TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id)


# ---- Stock Transaction Master   -----
def stk_trn_add_form():
    return dict()

def stk_tns_form():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Transaction No'),TH('Transaction Date'),TH('Prepared By'),TH('Status'),TH('Action')))
    for n in db().select(db.Stock_Request.ALL):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stk_tns_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.stock_request_no),TD(n.stock_source_id),TD(n.stock_destination_id),TD(n.srn_status_id),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')        
    return dict(table = table)

def stk_tns_edit_form():
    form = SQLFORM(db.Stock_Request, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

def stk_tns_val_form(form):
    ctr = db(db.Stock_Request.stv_no).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5, '0')
    ctr_val = 'STN' + ctr            
    form.vars.stv_no = ctr_val

def stk_tns_add_form():
    db.Stock_Request.stock_request_no.writable = False
    db.Stock_Request.stock_request_date.writable = False
    db.Stock_Request.stock_source.writable = False
    db.Stock_Request.stock_destination.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.requested_by.writable = False
    db.Stock_Request.srn_status.writable = False
    db.Stock_Request.approved_by.writable = False
 
    db.Stock_Request.src_no.writable = False
    db.Stock_Request.src_date.writable = False
    db.Stock_Request.src_prepared_by.writable = False
    db.Stock_Request.src_status.writable = False

    form = SQLFORM(db.Stock_Request)
    if form.process(onvalidation = stk_tns_val_form).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

# ---- Stock Receipt Master   -----
def stk_rcpt_form():
    
    return locals()

# ---- Stock Adjustment Begin   -----    

def adjustment_type():
    form = SQLFORM(db.Adjustment_Type)
    if form.process().accepted:
        response.flash = 'save'
    elif form.errors:
        response.flash = 'error'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Action')))
    for n in db(db.Adjustment_Type).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)        

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_add_new():    
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    db.Stock_Adjustment.srn_status_id.default = 3    
    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process(onvalidation = stock_adjustment_form_validation).accepted:     
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
        response.flash = 'RECORD SAVE. ' + str(_trns_pfx.current_year_serial_key)
        _id = db(db.Stock_Adjustment.stock_adjustment_no == int(_trns_pfx.current_year_serial_key)).select().first()     
        _total_cost = 0
        _tmp = db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.ALL).first()
        for i in db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.ALL):         
            _itm_code = db(db.Item_Master.id == i.item_code_id).select().first()
            _itm_price = db(db.Item_Prices.item_code_id == i.item_code_id).select().first()            
            _qty = i.quantity * _itm_code.uom_value + i.pieces                        
            _price_cost = i.average_cost /_itm_code.uom_value # price_cost per pcs.
            _total_cost += _price_cost * _qty # total cost per line
            db.Stock_Adjustment_Transaction.insert(stock_adjustment_no_id = _id.id, item_code_id = i.item_code_id, stock_adjustment_date = i.stock_adjustment_date, 
                category_id = i.category_id,quantity = _qty, uom = _itm_code.uom_value, price_cost = _price_cost, wholesale_price = _itm_price.wholesale_price, 
                retail_price = _itm_price.retail_price,vansale_price = _itm_price.vansale_price, average_cost = i.average_cost)          
        
        _id.update_record(total_amount = _total_cost)       
        db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).delete()     

    elif form.errors:
        response.flash = 'error'
    db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')   
    db.Stock_Adjustment_Transaction_Temp.category_id.default = 4

    # db.Stock_Adjustment_Transaction_Temp.item_code_id.requires = IS_IN_DB(db(db.Item_Master.dept_code_id == request.vars.dept_code_id), db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')    

    form2 = SQLFORM(db.Stock_Adjustment_Transaction_Temp)
    
    if form2.process().accepted:
    
        response.flash = 'OK'                    
    
    elif form2.errors:
    
        response.flash = 'error'
            
    return dict(form = form, form2 = form2, ticket_no_id = id_generator(), _loc_cod_id = request.vars._loc_code_id)

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_browse():

    return dict()

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_form_validation(form):
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
    _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1   
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
    db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == str(request.args(0))).select()
    form.vars.stock_adjustment_no_id = _trns_pfx.id
    form.vars.stock_adjustment_no = int(_skey)
    form.vars.stock_adjustment_code = _loc_code.stock_adjustment_code

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_form():

    ctr_val = "ADJ18100000"  # temporary autogenerated

    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    
    db.Stock_Adjustment.srn_status_id.default = 3
    
    form = SQLFORM(db.Stock_Adjustment)
    
    if form.process(onvalidation = stock_adjustment_form_validation).accepted:     
       
        response.flash = 'save'

        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()

        _id = db(db.Stock_Adjustment.stock_adjustment_no == int(_trns_pfx.current_year_serial_key)).select().first()                
        _total = 0
        _total_cost = 0

        for i in db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == str(request.args(0))).select(db.Stock_Adjustment_Transaction_Temp.ALL):
            
            _itm_code = db(db.Item_Master.id == i.item_code_id).select().first()
            
            _itm_price = db(db.Item_Prices.item_code_id == i.item_code_id).select().first()
            
            _qty = i.quantity * _itm_code.uom_value + i.pieces            
            
            _price_cost = i.average_cost /_itm_code.uom_value # price_cost per pcs.

            _total_cost += _price_cost * _qty # total cost per line

            db.Stock_Adjustment_Transaction.insert(stock_adjustment_no_id = _id.id, item_code_id = i.item_code_id, stock_adjustment_date = i.stock_adjustment_date, category_id = i.category_id,            
            quantity = _qty, uom = _itm_code.uom_value, price_cost = _price_cost, wholesale_price = _itm_price.wholesale_price, retail_price = _itm_price.retail_price,
            vansale_price = _itm_price.vansale_price, average_cost = i.average_cost)          

        # _total_cost = db.Stock_Adjustment_Transaction.total_cost.sum().coalesce_zero()

        # _total_cost = db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == _id.id).select(_total_cost).first()[_total_cost]
        _id.update_record(total_amount = _total_cost)        
        
        db(db.Stock_Adjustment_Transaction_Temp.created_by == auth.user_id).delete()     

    elif form.errors:

        response.flash = 'error'

    return dict(form = form, ctr_val = ctr_val)

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_table_validation(form):      
    
    _stk_fil = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()
    
    _uom = db(db.Item_Master.id == request.vars.item_code_id).select().first()        
    _id = db((db.Stock_Adjustment_Transaction_Temp.item_code_id == request.vars.item_code_id) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.item_code_id).first()
    _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
    _itm_pric = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    _qty = int(request.vars.quantity) * int(_itm_code.uom_value) + int(request.vars.pieces)
    _unt = float(_itm_pric.average_cost) / int(_itm_code.uom_value)
    _total_cost = float(_unt) * int(_qty)
    form.vars.total_amount = float(_total_cost)
    
    if _qty > _stk_fil.closing_stock:
        form.errors._qty = 'quantity should not exceed the closing stock'

    if _id:

        form.errors._id = 'already exists!'       
    
    if _uom.uom_value == 1:

        form.vars.pieces = 0
    
    form.vars.stock_adjustment_date = request.now

    form.vars.ticket_no_id = request.vars.ticket_no_id
    
    if form.vars.average_cost == float(0.0):
    
        itm_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    
        form.vars.average_cost = itm_price.average_cost

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_no():        
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
    _serial = _trans_prfx.current_year_serial_key + 1
    _stk_no = str(_trans_prfx.prefix) + str(_serial)
    return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_code():        
    _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    return XML(INPUT(_class="integer form-control", _name='location_code', _value=_loc_code.stock_adjustment_code, _disabled = True))

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_average_cost():          
    _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    _item_price_none = db(db.Item_Prices.item_code_id == None).select().first()
    
    if _item_price:
        return XML(INPUT(_class="integer form-control", _name='average_cost', _value=_item_price.average_cost))                
    elif _item_price_none:    
        _item_price.average_cost = _item_price_none
    
@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_description():
    
    _item_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()   
    _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()
    print _item_code, _item_price, _stk_file   
    _item_price_none = db(db.Item_Prices.item_code_id == None).select().first()
    _stk_file_none = db((db.Stock_File.item_code_id == None) & (db.Stock_File.location_code_id == None)).select().first()


    # if _item_code and _item_price and _stl_file:
    _outer = int(_stk_file.probational_balance) / int(_item_code.uom_value)        
    _pcs = int(_stk_file.probational_balance) - int(_outer * _item_code.uom_value)    
    _on_hand = str(_outer) + ' ' + str(_pcs) + '/' +str(_item_code.uom_value)

    _outer_transit = int(_stk_file.stock_in_transit) / int(_item_code.uom_value)   
    _pcs_transit = int(_stk_file.stock_in_transit) - int(_outer * _item_code.uom_value)
    _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_item_code.uom_value)

    _outer_on_hand = int(_stk_file.closing_stock) / int(_item_code.uom_value)
    _pcs_on_hand = int(_stk_file.closing_stock) / int(_outer_on_hand * _item_code.uom_value) 
    _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_item_code.uom_value)


    if request.vars.item_code_id:
        # return CENTER(XML("<b>ITEM CODE:</b> " + _item_code.item_code + ' - ' + str(_item_code.item_description.upper())+ ' - ' + str(_item_code.group_line_id.group_line_name) + ' ' + str(_item_code.brand_line_code_id.brand_line_name) + ' - <B>UOM:</B> ' + str(_item_code.uom_value) + ' - <B>Retail Price: QR </B>' + str(_item_price.retail_price) + ' -  <B>On-Hand: </B>'+ _on_hand + ' -  <B>On-Transit: </B>' + _on_transit +' -  <B>On-Balance: </B> ' + _on_hand ),_class = 'bg-info')
        return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance')),_class="bg-active"),TBODY(TR(TD(_item_code.item_code),TD(_item_code.item_description.upper()),TD(_item_code.group_line_id.group_line_name),TD(_item_code.brand_line_code_id.brand_line_name),TD(_item_code.uom_value),TD(_item_price.retail_price),TD(_on_hand),TD(_on_transit),TD(_on_hand)),_class="bg-info"),_class='table'))
    elif request.vars.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])    
    
    elif _item_price_none:
        _item_code_none.average_cost = None

    elif _stk_file_none:
        _stk_file_none.average_cost = None

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_table():    
    # db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')
    # db.Stock_Adjustment_Transaction_Temp.category_id.default = 4
    
    form = SQLFORM(db.Stock_Adjustment_Transaction_Temp)
    if form.accepts(request, formname = None, onvalidation = stock_adjustment_table_validation):
        response.flash = 'ITEM CODE INSERTED'            
        row = []
        ctr = 0
        _total_amount = 0
        _unt = 0.0        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Average Cost'),TH('Total Cost'),TH('Action')))  
        for i in db((db.Stock_Adjustment_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.ALL, db.Item_Master.ALL, db.Item_Prices.ALL,
        left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction_Temp.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Adjustment_Transaction_Temp.item_code_id)]):
            ctr += 1                
            _itm_code = db(db.Item_Master.id == i.Stock_Adjustment_Transaction_Temp.item_code_id).select().first()
            _itm_pric = db(db.Item_Prices.item_code_id == i.Stock_Adjustment_Transaction_Temp.item_code_id).select().first()
            _qty = (i.Stock_Adjustment_Transaction_Temp.quantity) * int(_itm_code.uom_value) + int(i.Stock_Adjustment_Transaction_Temp.pieces)
            _unt = float(_itm_pric.average_cost) / int(_itm_code.uom_value)
            
            _total_cost = float(_unt) * int(_qty)
            _total_amount += _total_cost
            save_lnk = A(I(_class='fas fa-save'), _title='Save Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
            edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
            btn_lnk = DIV(dele_lnk)

            
            # if edit_lnk:
            row.append(TR(TD(ctr),
            TD(i.Stock_Adjustment_Transaction_Temp.item_code_id.item_code),TD(i.Item_Master.item_description.upper()),TD(i.Stock_Adjustment_Transaction_Temp.category_id.mnemonic),
            TD(i.Item_Master.uom_value),
            TD(i.Stock_Adjustment_Transaction_Temp.quantity),
            TD(i.Stock_Adjustment_Transaction_Temp.pieces),
            TD(locale.format('%.2F', i.Stock_Adjustment_Transaction_Temp.average_cost or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.2F',_total_cost or 0, grouping = True), _align = 'right'), TD(btn_lnk)))
            # else:
            #     row.append(TR(TD(ctr),
            #     TD(i.Stock_Adjustment_Transaction_Temp.item_code_id.item_code),TD(i.Item_Master.item_description.upper()),TD(i.Stock_Adjustment_Transaction_Temp.category_id.mnemonic),
            #     TD(i.Item_Master.uom_value),
            #     TD(i.Stock_Adjustment_Transaction_Temp.quantity),
            #     TD(i.Stock_Adjustment_Transaction_Temp.pieces),
            #     TD(locale.format('%.2F', i.Stock_Adjustment_Transaction_Temp.average_cost or 0, grouping = True), _align = 'right'),
            #     TD(locale.format('%.2F',_total_cost or 0, grouping = True), _align = 'right'), TD(btn_lnk)))


        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2f', _total_amount or 0, grouping = True), _align = 'right'),TD())))
        table = TABLE(*[head, body, foot],  _class='table', _id = 'tmptbl')        
        return table   
    elif form.errors:
        # response.flash = 'error'
        # table = 'error'
        table = TABLE(*[TR(k, v) for k, v in form.errors.items()], _class="bg-warning")
    # return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_table_form():    
    db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')
    db.Stock_Adjustment_Transaction_Temp.category_id.default = 4
    form = SQLFORM(db.Stock_Adjustment_Transaction_Temp)
    if form.process().accepted:
        response.flash = 'OK'                    
    elif form.errors:
        response.flash = 'error'
    return dict(form = form)    

def stock_adjustment_delete():    
    # db(db.Stock_Adjustment_Transaction_Temp.id == request.args(0)).select().delete()
    print 'delete ', request.args(0)    
    # response.js =  "web2py_component('#tmptbl').get(0).reload();"
    # response.js = web2py_component('{{=URL("inventory","stock_adjustment_table.load")}}', 'tab');

def stock_adjustment_manager_details():
    
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'updated'
    elif form.errors:
        response.flash = 'errors'
    row = []
    ctr = 0
    _total_amount = 0
    _unt = 0.0
    _total_cost = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Average Cost'),TH('Total Cost')))  
    for i in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(db.Item_Master.ALL, db.Stock_Adjustment_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        ctr += 1                
        _total_amount += int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.average_cost) / int(i.Stock_Adjustment_Transaction.uom)
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_type_edit_form', args = i.Stock_Adjustment_Transaction.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)
                
        _total_cost = float(i.Stock_Adjustment_Transaction.price_cost) * int(i.Stock_Adjustment_Transaction.quantity)

        row.append(TR(TD(ctr),
        TD(i.Stock_Adjustment_Transaction.item_code_id.item_code),
        TD(i.Item_Master.item_description),
        TD(i.Stock_Adjustment_Transaction.category_id.mnemonic),
        TD(i.Stock_Adjustment_Transaction.uom),
        TD(card(i.Item_Master.id,i.Stock_Adjustment_Transaction.quantity,i.Stock_Adjustment_Transaction.uom )),
        TD(locale.format('%.2F',i.Stock_Adjustment_Transaction.average_cost or 0, grouping = True), _align = 'right'),
        TD(locale.format('%.2F',_total_cost or 0, grouping = True), _align = 'right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2F',_total_amount or 0, grouping = True)),_align = 'right')))
    table = TABLE(*[head, body, foot],  _class='table')        
    _btn_approved = A('approved', _type='submit', _class="btn btn-success", callback = URL('inventory','stock_adjustment_manager_details_approved', args = request.args(0)))
    _btn_reject = A('reject', _type='button', _class="btn btn-danger", callback = URL('inventory','stock_adjustment_manager_details_reject', args = request.args(0)))
    return dict(form = form, table = table, _stk_adj = _stk_adj, _btn_approved = _btn_approved, _btn_reject = _btn_reject)

def stock_adjustment_manager_details_approved():
    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
       
    _stk_adj.update_record(srn_status_id = 1)

    _clo_stk = 0   

    for s in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(db.Stock_Adjustment_Transaction.ALL):
              
        _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
        
        _stk_file = db((db.Stock_File.item_code_id == s.item_code_id) & (db.Stock_File.location_code_id == _stk_adj.location_code_id)).select().first()
        
        if (_stk_adj.adjustment_type == 1) and _stk_file:            
        
            _clo_stk = _stk_file.closing_stock + s.quantity 

            _trans_type = 7
        
        elif (_stk_adj.adjustment_type == 2) and _stk_file:            
       
            _clo_stk = _stk_file.closing_stock - s.quantity 

            _trans_type = 8
        
        _stk_file.update_record(closing_stock = _clo_stk)

        db.Merch_Stock_Transaction.insert(
            voucher_no = '%s%s' % (_stk_adj.stock_adjustment_no_id.prefix,_stk_adj.stock_adjustment_no),
            location_code = '%s' % (_stk_adj.location_code_id.location_name),
            transaction_type = _trans_type,
            transaction_date = request.now,
            account = '%s' % (_stk_adj.location_code_id.stock_adjustment_code),
            item_code = '%s' % (s.item_code_id.item_code), # price cost = sales cost
            uom = s.uom,
            quantity = s.quantity,
            price_cost = s.price_cost,            
            average_cost = s.average_cost,            
            whole_sale_price = s.wholesale_price,
            retail_price = s.retail_price,
            vansale_price = s.vansale_price,
            dept_code = '%s' % (_stk_adj.dept_code_id.dept_name)
        )
    
    _stk_adj.update_record(approved_by = auth.user_id, date_approved = request.now)

    response.flash = 'record approved'        

def stock_adjustment_manager_details_reject():
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    _stk_adj.update_record(srn_status_id = 2)
    response.flash = 'record rejected'    
    print 'reject'  

def stock_adjustment_browse_details():   
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()     
    if _stk_adj.srn_status_id == 1:
        db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 1), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'updated'
    elif form.errors:
        response.flash = 'errors'
        
    row = []
    ctr = 0
    _total_amount = 0

    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Average Cost'),TH('Total Cost'),TH('Action')))  

    for i in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(db.Item_Master.ALL, db.Stock_Adjustment_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        ctr += 1                
        
        _total_amount += int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.average_cost) / int(i.Stock_Adjustment_Transaction.uom)

        _apprvd = db(db.Stock_Adjustment.id == i.Stock_Adjustment_Transaction.stock_adjustment_no_id).select(db.Stock_Adjustment.ALL).first()

        if _apprvd.srn_status_id == 1:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = URL('stock_adjustment_browse_details_edit', args = i.Stock_Adjustment_Transaction.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('stock_adjustment_browse_details_delete', args = i.Stock_Adjustment_Transaction.id))
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('stock_adjustment_browse_details_edit', args = i.Stock_Adjustment_Transaction.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_browse_details_delete', args = i.Stock_Adjustment_Transaction.id))

        btn_lnk = DIV(edit_lnk, dele_lnk)
        _price_cost = int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.price_cost)
        row.append(TR(TD(ctr),
        TD(i.Stock_Adjustment_Transaction.item_code_id.item_code),
        TD(i.Item_Master.item_description),
        TD(i.Stock_Adjustment_Transaction.category_id.mnemonic),
        TD(i.Stock_Adjustment_Transaction.uom),
        TD(card(i.Item_Master.id,i.Stock_Adjustment_Transaction.quantity,i.Stock_Adjustment_Transaction.uom )),
        TD(locale.format('%.2F',i.Stock_Adjustment_Transaction.average_cost or 0, grouping = True), _align = 'right'),
        TD(locale.format('%.2F', _price_cost or 0, grouping = True), _align = 'right'),
        TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2F',_total_amount or 0, grouping = True)),_align = 'right'),TD()))
    table = TABLE(*[head, body, foot],  _class='table', _id = 'dettbl')    
    return dict(form = form, table = table, _stk_adj = _stk_adj)
    
# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
# ---- C A R D Function  -----
    

def stock_adjustment_browse_details_delete():
    
    _stk_adj_tran = db(db.Stock_Adjustment_Transaction.id == request.args(0)).select().first()

    _stk_adj = db(db.Stock_Adjustment.id == _stk_adj_tran.stock_adjustment_no_id).select().first()

    db(db.Stock_Adjustment_Transaction.id == request.args(0)).delete()

    _total_amount = 0
       
    for i in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == _stk_adj.id).select():

        _total_amount += int(i.quantity) * float(i.average_cost) / int(i.uom)
    
    _stk_adj.update_record(total_amount = _total_amount)

def stock_adjustment_browse_details_edit():

    _stk_adj_tran = db(db.Stock_Adjustment_Transaction.id == request.args(0)).select().first()
    
    _itm_cod = db(db.Item_Master.id == _stk_adj_tran.item_code_id).select().first()
    
    _qty = _stk_adj_tran.quantity / _stk_adj_tran.uom
    
    _pcs = _stk_adj_tran.quantity - _stk_adj_tran.quantity / _stk_adj_tran.uom * _stk_adj_tran.uom
    
    _total_amount = 0

    form = SQLFORM.factory(
    
        Field('quantity','integer', default = _qty),
    
        Field('pieces','integer', default = _pcs))
    
    if form.process().accepted:
    
        session.flash = 'record updated'

        _qty = int(int(request.vars.quantity) * int(_stk_adj_tran.uom)) + int(request.vars.pieces)        
        
        _stk_adj_tran.update_record(quantity = int(_qty))

        for i in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == _stk_adj_tran.stock_adjustment_no_id).select():

            _total_amount += int(i.quantity) * float(i.average_cost) / int(i.uom)
        
        _stk_adj = db(db.Stock_Adjustment.id == _stk_adj_tran.stock_adjustment_no_id).select().first()
        
        _stk_adj.update_record(total_amount = _total_amount)

        redirect(URL('stock_adjustment_browse_details', args = (_stk_adj.id)))

    elif form.errors:

        response.flash = 'form has errors'

    return dict(form = form, _stk_adj_tran = _stk_adj_tran, _itm_cod = _itm_cod)
@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def stock_adjustment_manager():
    row = []
    ctr = 0
    _total_amount = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Adjustment No'),TH('Department'),TH('Location'),TH('Type'),TH('Amount'),TH('Status'),TH('Approved By'),TH('Action')))  
    for i in db(db.Stock_Adjustment).select(orderby = ~db.Stock_Adjustment.stock_adjustment_no):
        ctr += 1        
        row.append(TR(TD(ctr),
        TD(i.stock_adjustment_date),
        TD(i.stock_adjustment_no),
        TD(i.dept_code_id.dept_name),
        TD(i.location_code_id.location_name),
        TD(i.adjustment_type.mnemonic),
        TD(i.total_amount),        
        TD(i.srn_status_id.description),
        TD(i.approved_by),
        TD()))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table')    
    return dict(table = table)

# ---- Stock Adjustment End   -----    

def stk_rpt():
    return locals()

def itm_price():
    form = SQLFORM(db.Item_Prices)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)


# ---- Transaction       -----
def transaction():
    return locals()
# ---- Stock Request     -----
def stock_request():
    return locals()
# ---- Stock Voucher     -----
def stock_voucher():
    return locals()
# ---- Stock Receipt     -----
# @auth.requires(lambda: auth.has_membership('INVENTORY POS'))
def stock_receipt():
    return locals()

def stock_receipt_details():
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False

    # db.Stock_Request.src_status.writable = False
    # db.Stock_Request.item_status_code_id.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 5) | (db.Stock_Status.id == 6)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'APPROVED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1            
        grand_total += int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Item_Prices.retail_price, _align='right'),TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id)
    
def stock_receipt_generator():
    
    _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()

    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix == 'SRC')).select().first()

    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    
    response.flash = 'SAVING STOCK RECEIVE NO SRC' +str(_skey) + '.'         

    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
    _stk_rcpt.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id)

    _stk_fil = db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select()

    for srt in _stk_fil:

        _stk_file_des = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_destination_id)).select(db.Stock_File.ALL).first()
        _stk_file_src = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_source_id)).select(db.Stock_File.ALL).first()            
        if _stk_file_des:
            
            _add = int(int(_stk_file_des.closing_stock) + int(srt.quantity))
            
            _stk_file_des.update_record(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = _add, last_transfer_qty = srt.quantity, last_transfer_date = request.now)  

        else:

            db.Stock_File.update_or_insert(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = srt.quantity, last_transfer_qty = srt.quantity, last_transfer_date = request.now)

        if _stk_file_src:
            _min = int(int(_stk_file_src.closing_stock) - int(srt.quantity))            

            _min_or_trn = int(_stk_file_src.stock_in_transit) - int(srt.quantity)
            
            _stk_file_src.update_record(closing_stock = _min, stock_in_transit = _min_or_trn, last_transfer_qty = srt.quantity)


    return dict()

# ----          Reports           -----
def reports():
    return locals() 


##########          R E P O R T S           ##########

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
from datetime import date
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
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.8*inch, leftMargin=20, rightMargin=20)#, showBoundary=1)
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

def _landscape_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage],['PRICE LIST REPORT']], colWidths='*')
    header.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .1 * cm)

    # Footer
    today = date.today()
    footer = Table([[merch],[today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),8),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ('LINEABOVE',(0,1),(0,1),0.25, colors.gray)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

def _transfer_header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Footer
    today = date.today()
    _trn = db(db.Stock_Request.id == request.args(0)).select().first()
    footer = Table([
        [str(_trn.stock_transfer_approved_by.first_name + ' ' + _trn.stock_transfer_approved_by.last_name),'',''],
        ['Issued by','Receive by', 'Delivered by'],
        ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))],
        ['','- - WAREHOUSE COPY - -',''],
        [merch,'',''],['','',today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('TOPPADDING',(0,0),(0,3),15),
        # ('TEXTCOLOR',(0,4),(1,4), colors.black),
        ('ALIGN',(0,0),(2,1),'CENTER'),
        ('FONTSIZE',(0,0),(2,1),8),
        ('FONTSIZE',(0,5),(2,5),8),
        ('FONTSIZE',(0,2),(2,2),7),
        ('ALIGN',(0,3),(1,3),'CENTER'),
        ('FONTSIZE',(0,3),(1,3),8),
        ('ALIGN',(0,2),(2,2),'RIGHT'),        
        ('ALIGN',(0,5),(2,5),'RIGHT'),
        ('LINEABOVE',(0,5),(2,5),1, colors.Color(0, 0, 0, 0.55))
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

def _header_footer_stock_receipt(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([[img]], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        # ('LINEBELOW',(0,0),(0, 0),0.10, colors.gray),
        # ('BOTTOMPADDING',(0,0),(0, 1),10)
        # ('TOPPADDING',(0,2),(1,2),6)
        ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .7 * inch)


    # Footer
    today = date.today()
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    footer = Table([
        [str(_stk_req.stock_receipt_approved_by.first_name + ' ' + _stk_req.stock_receipt_approved_by.last_name),''],
        ['Received by:','Delivered by:'],
        ['',''],
        [merch,''],['',today.strftime("%A %d. %B %Y")]], colWidths=[None])
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

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([[img]], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        # ('LINEBELOW',(0,0),(0, 0),0.10, colors.gray),
        # ('BOTTOMPADDING',(0,0),(0, 1),10)
        # ('TOPPADDING',(0,2),(1,2),6)
        ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .7 * inch)


    # Footer
    
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    footer = Table([
        [str(_stk_req.created_by.first_name + ' ' + _stk_req.created_by.last_name),str(_stk_req.stock_request_approved_by.first_name + ' ' + _stk_req.stock_request_approved_by.last_name)],
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

def reprint():
    query = db(db.Stock_Request_Transaction.stock_request_id == 11).select(
        db.Stock_Request_Transaction.ALL,
        db.Item_Master.ALL, 
        db.Stock_Request.ALL,
        
    
    left  = [
        db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id),        
        db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id)]
    )
    for q in query:
        # for s in db(db.Stock_File.location_code_id == q.Stock_Request.stock_destination_id).select(db.Stock_Request.ALL, db.Stock_File.ALL,
        # db.Stock_Request_Transaction.ALL):
        print 'item master stock: ',q.Stock_Request.id,q.Stock_Request_Transaction.item_code_id#, s.Stock_File.closing_stock
        for f in db(db.Stock_File.item_code_id == q.Stock_Request_Transaction.item_code_id).select():
            print 'stock location', f.location_code_id
    return locals()
import inflect 
from decimal import Decimal
w=inflect.engine()
def stock_transaction_report():
    _id = request.args(0)
    _grand_total = 0
    ctr = 0
    _total = 0
    for s in db(db.Stock_Request.id == _id).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK TRANSFER'],   
            [''],            
            ['STOCK TRANSFER NO',':  '+ str(s.Stock_Request.stock_transfer_no_id.prefix)+str(s.Stock_Request.stock_transfer_no), 'STOCK TRANSACTION DATE',':  ' +str(s.Stock_Request.stock_transfer_date_approved)],
            ['Stock Request No',':  '+ str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no), 'Stock Request Date',':  ' +str(s.Stock_Request.stock_request_date)],
            ['Stock Request From', ':  '+ s.Stock_Request.stock_source_id.location_name,'Stock Request To',':  '+ s.Stock_Request.stock_destination_id.location_name],
            ['Department',':  '+ s.Stock_Request.dept_code_id.dept_name,'',''],
            ['Remarks',':  '+ s.Stock_Request.remarks,'','']]
        
    
    stk_trn = [['#', 'ITEM CODE', 'ITEM DESCRIPTION','UNIT','CAT.', 'UOM','QTY.','UNIT PRICE','TOTAL']]
    for i in db(db.Stock_Request_Transaction.stock_request_id == _id).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total        
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper()),
        i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),
        # i.Stock_Request_Transaction.quantity,
        i.Item_Prices.retail_price,        
        locale.format('%.2F',_total or 0, grouping = True)])
    
    stk_trn.append(['','', '', '','','','','TOTAL AMOUNT:',locale.format('%.2F',_grand_total or 0, grouping = True)])

    stk_tbl = Table(stk_req_no, colWidths=[150, 130,150,130 ], rowHeights=20)
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (0,2), (-1,2), 1, colors.black),
        ('BACKGROUND',(0,2),(-1,2),colors.gray),
        ('SPAN',(0,0),(3,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('TOPPADDING',(0,0),(0,0),12),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('FONTSIZE',(0,0),(0,0),12),
        ('FONTSIZE',(0,2),(-1,2),9),        
        ('FONTSIZE',(0,3),(3,-1),8)
        ]))
    
    trn_tbl = Table(stk_trn, colWidths = [20,55,200,50,30,30,50,60,60])
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,-1), (-1,-1), 1, colors.Color(0, 0, 0, 0.35)),
        # ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.gray),
        # ('LINEBELOW', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.25)), #background
        ('ALIGN',(6,0),(6,-1),'RIGHT'),
        ('ALIGN',(6,1),(6,-1),'RIGHT'),
        ('ALIGN',(7,0),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8)]))    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)

    # wrds_trnls = [['QR ' + string.capwords(amt2words(123.25)) ]] # num2words str(number-int(number)).split('.')[1:]
    # _grand_total = 3408.72
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    
    x =locale.format('%.2f',_grand_total or 0, grouping = True)
    
    wrds_trnls = [['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS']] # inflect
    wrds_tbld = Table(wrds_trnls, colWidths='*')
    wrds_tbld.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('LINEABOVE', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.35)),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.35)),
        ('FONTSIZE',(0,0),(-1,-1),8)
    ]))
    row.append(Spacer(1,.7*cm))
    row.append(wrds_tbld)

    doc.build(row, onFirstPage=_transfer_header_footer, onLaterPages=_transfer_header_footer)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

def str_kpr_rpt():
    
    _grand_total = 0
    ctr = 0
    _total = 0
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK REQUEST'],   
            [''],            
            ['STOCK REQUEST NO',':  '+ str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no), 'STOCK REQUEST DATE',':  ' +str(s.Stock_Request.stock_request_date.strftime('%d-%m-%Y'))],
            ['Stock Request From', ':  '+ s.Stock_Request.stock_source_id.location_name,'Stock Request To',':  '+ s.Stock_Request.stock_destination_id.location_name],
            ['Department',':  '+ s.Stock_Request.dept_code_id.dept_name,'',''],
            ['Remarks',':  '+ s.Stock_Request.remarks,'','']]
        
    
    stk_trn = [['#', 'ITEM CODE', 'ITEM DESCRIPTION','UNIT','CAT.', 'UOM','QTY.','PRICE','SOH','TOTAL']]
    for i in db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_File.ALL, 
        # join = db.Stock_Request_Transaction.on(db.Stock_Request_Transaction.item_code_id == db.Stock_File.item_code_id),
        left = [

        db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id)  
        # db.Stock_File.on(db.Stock_File.item_code_id == db.Stock_Request_Transaction.item_code_id)
        # db.Stock_Request.on(db.Stock_Request.stock_destination_id == db.Stock_File.location_code_id),
        
        
        ]):
        ctr += 1
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total
        # _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, i.Stock_File.closing_stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str('Remarks: ')+str(i.Stock_Request_Transaction.remarks),        
        i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Stock_Request_Transaction.item_code_id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.retail_price,
        '_stock_on_hand',
        locale.format('%.2F',_total or 0, grouping = True)])

    stk_trn.append(['','', '','', '','','','','TOTAL AMOUNT:',locale.format('%.2F',_grand_total or 0, grouping = True)])

    stk_tbl = Table(stk_req_no, colWidths=[120, 150,120,150 ], rowHeights=20)
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (0,2), (-1,2), 1, colors.Color(0, 0, 0, 0.2)),
        
        ('BACKGROUND',(0,2),(-1,2),colors.gray),
        ('SPAN',(0,0),(3,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('TOPPADDING',(0,0),(0,0),12),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,2),(-1,2),10),        
        ('FONTSIZE',(0,3),(3,-1),9)
        ]))
    
    trn_tbl = Table(stk_trn, colWidths = [25,55,170,30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,-1), (-1,-1), .5, colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.gray),
        ('ALIGN',(6,1),(9,-1),'RIGHT'),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        # ('ALIGN',(8,0),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8)]))
    row.append(stk_tbl)
    row.append(Spacer(1,.10*cm))
    row.append(trn_tbl)
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    wrds_trnls = [['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS']] # inflect
    wrds_tbld = Table(wrds_trnls, colWidths='*')
    wrds_tbld.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('LINEABOVE', (0,0), (-1,0), .5, colors.black),
        ('LINEBELOW', (0,0), (-1,0), .5, colors.black),
        ('FONTSIZE',(0,0),(-1,-1),8)
    ]))
    row.append(Spacer(1,.7*cm))
    row.append(wrds_tbld)

    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   


def stock_receipt_report():
    _id = request.args(0)
    _grand_total = 0
    ctr = 0
    _total = 0
    for s in db(db.Stock_Request.id == _id).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK RECEIPT'],   
            [''],            
            ['STOCK RECEIPT NO',':  '+ str(s.Stock_Request.stock_receipt_no_id.prefix)+str(s.Stock_Request.stock_receipt_no), 'STOCK RECEIPT DATE',':  ' +str(s.Stock_Request.stock_receipt_date_approved)],
            ['STOCK TRANSFER NO',':  '+ str(s.Stock_Request.stock_transfer_no_id.prefix)+str(s.Stock_Request.stock_transfer_no), 'STOCK TRANSACTION DATE',':  ' +str(s.Stock_Request.stock_transfer_date_approved)],
            ['STOCK REQUEST NO',':  '+ str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no), 'STOCK REQUEST DATE',':  ' +str(s.Stock_Request.stock_request_date)],
            ['Stock Request From', ':  '+ s.Stock_Request.stock_source_id.location_name,'Stock Request To',':  '+ s.Stock_Request.stock_destination_id.location_name],
            ['Department',':  '+ s.Stock_Request.dept_code_id.dept_name,'',''],
            ['Remarks',':  '+ s.Stock_Request.remarks,'','']]
        
    
    stk_trn = [['#', 'ITEM CODE', 'ITEM DESCRIPTION','UNIT','CAT.', 'UOM','QTY.','PRICE','SOH','TOTAL']]
    for i in db(db.Stock_Request_Transaction.stock_request_id == _id).select(db.Stock_Request_Transaction.ALL, 
    db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, db.Stock_Request.ALL,
    left = [
        db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id), 
        db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id),
        db.Stock_File.on(db.Stock_File.item_code_id == db.Stock_Request_Transaction.item_code_id),
        db.Stock_Request.on(db.Stock_File.location_code_id == db.Stock_Request.stock_source_id)
        ]):
        ctr += 1
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total
        _stock_on_hand = card(i.Item_Master.id, i.Stock_File.closing_stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks),        
        i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Item_Prices.retail_price,
        _stock_on_hand,
        locale.format('%.2F',_total or 0, grouping = True)])

    stk_trn.append(['','', '','', '','','','','TOTAL AMOUNT:',locale.format('%.2F',_grand_total or 0, grouping = True)])

    stk_tbl = Table(stk_req_no, colWidths=[120, 150,150,120 ], rowHeights=20)
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (0,2), (-1,2), 1, colors.Color(0, 0, 0, 0.2)),
        
        ('BACKGROUND',(0,2),(-1,2),colors.gray),
        ('SPAN',(0,0),(3,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('TOPPADDING',(0,0),(0,0),12),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,2),(-1,2),10),        
        ('FONTSIZE',(0,3),(3,-1),9)
        ]))
    
    trn_tbl = Table(stk_trn, colWidths = [25,55,170,30,30,30,50,50,50])
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (0,0), (-1,0), 1, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,-1), (-1,-1), .5, colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.gray),
        ('ALIGN',(6,1),(9,-1),'RIGHT'),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        # ('ALIGN',(8,0),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8)]))
    row.append(stk_tbl)
    row.append(Spacer(1,.10*cm))
    row.append(trn_tbl)
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    wrds_trnls = [['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS']] # inflect
    wrds_tbld = Table(wrds_trnls, colWidths='*')
    wrds_tbld.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('LINEABOVE', (0,0), (-1,0), .5, colors.black),
        ('LINEBELOW', (0,0), (-1,0), .5, colors.black),
        ('FONTSIZE',(0,0),(-1,-1),8)
    ]))
    row.append(Spacer(1,.7*cm))
    row.append(wrds_tbld)

    doc.build(row, onFirstPage=_header_footer_stock_receipt, onLaterPages=_header_footer_stock_receipt)
    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

def master_item_view():
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form.accepts(request):
        row = []
        i_row = []
        ctr = 0
        _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
        _stk_file = db(db.Stock_File.item_code_id == request.vars.item_code_id).select().first()
        _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()

        _outer = int(_stk_file.probational_balance) / int(_itm_code.uom_value)        
        _pcs = int(_stk_file.probational_balance) - int(_outer * _itm_code.uom_value)    
        _on_hand = str(_outer) + ' ' + str(_pcs) + '/' +str(_itm_code.uom_value)


        _outer_transit = int(_stk_file.stock_in_transit) / int(_itm_code.uom_value)   
        _pcs_transit = int(_stk_file.stock_in_transit) - int(_outer * _itm_code.uom_value)
        _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_itm_code.uom_value)

        _outer_on_hand = int(_stk_file.closing_stock) / int(_itm_code.uom_value)
        _pcs_on_hand = int(_stk_file.closing_stock) / int(_outer_on_hand * _itm_code.uom_value) 
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

        head = THEAD(TR(TD('#'),TD('Location Code'),TD('Opening Stock'),TD('Closing Stock'),TD('Stock In Transit'),TD('Available Balanced')))
        
        for i in db().select(db.Stock_File.ALL, db.Location.ALL, orderby = ~db.Location.location_name, left = db.Stock_File.on((db.Stock_File.location_code_id == db.Location.id) & (db.Stock_File.item_code_id == request.vars.item_code_id))):
            ctr += 1
            _avl_bal = int(i.Stock_File.closing_stock or 0) - int(i.Stock_File.stock_in_transit or 0)
            row.append(TR(TD(ctr),TD(i.Location.location_name),
            TD(i.Stock_File.opening_stock or 0, grouping = True),
            TD(i.Stock_File.closing_stock or 0, grouping = True),
            TD(i.Stock_File.stock_in_transit or 0, grouping = True),
            TD(_avl_bal or 0, grouping = True)))         
        body = TBODY(*row)
        table = TABLE(*[head, body], _class = 'table')
        return dict(form = form, i_table = i_table, table = table)
    else:
        return dict(form = form, table = 'table', i_table = 'i_table')

from datetime import datetime
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
        TD(_stk_file.opening_stock),
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
        
        _query = db.Stock_Request.srn_status_id == 6
        _query &= db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id     
        _query &= db.Stock_Request.stock_transfer_date_approved >= request.vars.start_date
        _query &= db.Stock_Request.stock_transfer_date_approved <= request.vars.end_date
        query = db(_query).select(db.Stock_Request_Transaction.ALL, db.Stock_Request.ALL, left = db.Stock_Request_Transaction.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)) 
        _bal = 0
        _bal = _stk_file.opening_stock
        
        for i in query: 

        # _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
        
        # _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()
        
        # _outer = int(_stk_file.probational_balance) / int(_itm_code.uom_value)        
        # _pcs = int(_stk_file.probational_balance) - int(_outer * _itm_code.uom_value)    
        # _on_hand = str(_outer) + ' ' + str(_pcs) + '/' +str(_itm_code.uom_value)
        
            # TD( # validate if uom = 1, present whole number
            # str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            # str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            # str(k.Item_Master.uom_value)), 
            # TD(k.Item_Prices.retail_price, _align='right'),TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks),TD(btn_lnk)))


            # print _stk_file.location_code_id , i.Stock_Request.stock_source_id
            if _stk_file.location_code_id == i.Stock_Request.stock_source_id:
                _outer  = i.Stock_Request_Transaction.quantity / i.Stock_Request_Transaction.uom
                _pcs    = i.Stock_Request_Transaction.quantity - i.Stock_Request_Transaction.quantity / i.Stock_Request_Transaction.uom * i.Stock_Request_Transaction.uom

                _bal = _bal - i.Stock_Request_Transaction.quantity
                _out = str(_outer) + ' - ' + str(_pcs) + '/' + str(_itm_code.uom_value)
                # _out = i.Stock_Request_Transaction.quantity
                _in = 0
                # print i.Stock_Request_Transaction.id, ' out'
            else:               
                _outer  = i.Stock_Request_Transaction.quantity / i.Stock_Request_Transaction.uom
                _pcs    = i.Stock_Request_Transaction.quantity - i.Stock_Request_Transaction.quantity / i.Stock_Request_Transaction.uom * i.Stock_Request_Transaction.uom

                _bal = _bal + i.Stock_Request_Transaction.quantity 
                _in = str(_outer) + ' - ' + str(_pcs) + '/' + str(_itm_code.uom_value)
                _out = 0
                # print 'in ', i.Stock_Request_Transaction.id
                
            ctr += 1
            row.append(TR(TD(ctr),
            TD(i.Stock_Request.stock_transfer_no_id.prefix),
            TD(i.Stock_Request.stock_transfer_no),
            TD(i.Stock_Request.stock_transfer_date_approved),
            TD(i.Stock_Request_Transaction.category_id.mnemonic),
            TD(_in),
            TD(_out),                                        
            TD(_bal)))

        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD('CLOSING STOCK AS PER MASTER STOCK',_colspan = '3'),TD(_stk_file.closing_stock)))
        table = TABLE(*[head, body, foot], _class = 'table')
        return dict(form = form, i_table = i_table, table = table)
    else:
        return dict(form = form, table = 'table', i_table = 'i_table')

def price_list_report_print():
    ctr = 0
    _rep = [['#','Item Code','Supplier Ref.', 'Product','Subproduct','Group Line','Brand Line','Brand Classification','Description','UOM','Unit','Whole Price','Retail Price']]
    for n in db(db.Item_Master.supplier_code_id == request.args(0)).select(db.Item_Master.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.product_code_id | db.Item_Master.subproduct_code_id | db.Item_Master.group_line_id | db.Item_Master.brand_line_code_id | db.Item_Master.brand_cls_code_id ,  left = db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)):
        ctr += 1
        _rep.append([ctr,
        n.Item_Master.item_code,
        n.Item_Master.supplier_item_ref,
        n.Item_Master.product_code_id.product_name,    
        n.Item_Master.subproduct_code_id.subproduct_name,
        n.Item_Master.group_line_id.group_line_name,
        n.Item_Master.brand_line_code_id.brand_line_name,
        Paragraph(n.Item_Master.brand_cls_code_id.brand_cls_name, style = _style),            
        Paragraph(n.Item_Master.item_description, style = _style),            
        n.Item_Master.uom_value,
        n.Item_Master.uom_id.mnemonic,
        locale.format('%.2F',n.Item_Prices.wholesale_price or 0, grouping = True),
        locale.format('%.2F',n.Item_Prices.retail_price or 0, grouping = True)])
    _rep_tbl = Table(_rep, colWidths=[20,55,80,90,65,65,65,110,110,30,30,50,50], rowHeights=20)
    # _rep_tbl = Table(_rep, colWidths=(50*mm, 50*mm), rowHeights=(10*mm, 250*mm))
    _rep_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 1)),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(-1,-1),7),
        ('ALIGN', (9,1), (12,-1), 'RIGHT'),
    ]))
    row.append(_rep_tbl)
    doc.pagesize = landscape(A4)
    doc.build(row, onFirstPage=_landscape_header, onLaterPages= _landscape_header)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def price_list_report_option():
    row = []    
    _query = db(db.Item_Master.supplier_code_id == request.vars.supplier_code_id).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Product'),TH('Subproduct'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('UOM'),TH('Type'),TH('Whole Price'),TH('Retail Price')))
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
    


def test():
    
    elements = []
    # Make heading for each column and start data list
    column1Heading = "COLUMN ONE HEADING"
    column2Heading = "COLUMN TWO HEADING"
    # Assemble data for each column using simple loop to append it into data list
    data = [[column1Heading,column2Heading]]
    for i in range(1,100):
        data.append([str(i),str(i)])

    tableThatSplitsOverPages = Table(data, [6 * cm, 6 * cm], repeatRows=1)
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                           ('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                           ('BOX',(0,0),(-1,-1),1,colors.black),
                           ('BOX',(0,0),(0,-1),1,colors.black)])
    tblStyle.add('BACKGROUND',(0,0),(1,0),colors.lightblue)
    tblStyle.add('BACKGROUND',(0,2),(1,2),colors.gray)
    tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
    tableThatSplitsOverPages.setStyle(tblStyle)
    elements.append(tableThatSplitsOverPages)

    doc.build(elements)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data 

