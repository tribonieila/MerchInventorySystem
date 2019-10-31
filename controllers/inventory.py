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
    for n in db().select(db.Division.ALL, db.Product.ALL, orderby = db.Product.id, left=db.Division.on(db.Division.id == db.Product.div_code_id)):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Product.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('prod_edit_form', args = n.Product.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Product.id))
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
                subproduct_code = _skey, 
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

# ---- Exchange Rate Value  -----
@auth.requires_login()
def currency_exchange():
    form = SQLFORM(db.Currency_Exchange)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    head = THEAD(TR(TH('#'),TH('Currency'),TH('Exchange Rate'),TH('Status'),TH('Action')))    
    for n in db().select(db.Currency_Exchange.ALL):    
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','currency_exchange_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.currency_id.mnemonic),TD(n.exchange_rate_value),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

@auth.requires_login()
def currency_exchange_edit():
    form = SQLFORM(db.Currency_Exchange, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
        redirect(URL('inventory','currency_exchange'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

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
        row.append(TR(TD(n.id),TD(n.prefix_id.prefix,n.supp_code),TD(n.supp_sub_code),TD(n.supplier_ib_account),TD(n.supplier_purchase_account),
        TD(n.supplier_sales_account),TD(n.dept_code_id.dept_name),TD(n.supp_name),
        TD(n.contact_person),TD(n.supplier_type),TD(n.status_id.status),TD(action)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-striped')
    return dict(table = table)

@auth.requires_login()
def suplr_forw_form():
    _id = db(db.Supplier_Master.id == request.args(0)).select().first()
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
    return dict(form = form, table = table, _id=_id)


@auth.requires_login()
def suplr_add_form():
    # print request.vars._ckey
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
            Field('supp_sub_code', 'string',length = 10),
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
                supp_sub_code = form.vars.supp_sub_code,
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
        if form2.process(formname = 'step 2', keepvalues = True ).accepted:
            
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
        if form3.process(fornmane = 'step 3', keepvalues = True).accepted:
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
        if form4.process(formname = 'step 4', keepvalues = True).accepted:         
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
        
        if form5.process(formname = 'step 5', keepvalues = True).accepted:
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
        row.append(TR(TD(n.GroupLine.id),TD(n.GroupLine.prefix_id.prefix,n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.Supplier_Master.supp_code),TD(n.Supplier_Master.supp_name),TD(n.GroupLine.status_id.status),TD(btn_lnk)))
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
        row.append(TR(TD(ctr),TD(n.Brand_Line.prefix_id.prefix,n.Brand_Line.brand_line_code),TD(n.Brand_Line.brand_line_name),TD(n.GroupLine.prefix_id.prefix,n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.Brand_Line.dept_code_id.dept_name),TD(n.Brand_Line.status_id.status),TD(btn_lnk)))
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
        TD(n.Brand_Classification.dept_code_id.dept_name),
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
            Field('brand_line_code_id','reference Brand_Line', label = 'Brand Line Code',requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', orderby = db.Brand_Line.brand_line_name,  zero= 'Choose Brand Line')),
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
    db.Brand_Classification.brand_line_code_id.requires = IS_IN_DB(db(db.Brand_Line.group_line_id == ctr_val.group_line_id), db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')
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
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_weight_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def itm_weight_edit_form():
    form = SQLFORM(db.Weight, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

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
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Int Barcode'),TH('Loc Barcode'),TH('Group Line'),TH('Brand Line'),TH('Status'),TH('Actions')), _class='bg-primary')
    for n in db(db.Item_Master).select(orderby = db.Item_Master.item_code):        
        ctr += 1
        link_lnk = A(I(_class='fas fa-info-circle'), _title='Link Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_link_form', args = n.id))
        view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk,link_lnk, prin_lnk,edit_lnk, dele_lnk)        
        row.append(TR(TD(ctr),TD('ITM'+n.item_code),TD(n.item_description.upper()),TD(n.int_barcode),TD(n.loc_barcode),TD(n.group_line_id.group_line_name),TD(n.brand_line_code_id.brand_line_name),TD(n.item_status_code_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table',**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
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
            _id = db(db.Item_Master.item_code == itm_code).select().first()

            db.Item_Prices.insert(
                item_code_id = _id.id,                
            )            
            db.Stock_File.insert(item_code_id = _id.id, location_code_id = 1)
            
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

                _id = db(db.Item_Master.item_code == itm_code).select().first()
                db.Item_Prices.insert(item_code_id = _id.id)
                db.Stock_File.insert(item_code_id = _id.id, location_code_id = 1)
                
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
        # response.flash = _range
        # response.flash = form.vars.size_code_id
    return dict(form = form)

@auth.requires_login()
def gen_item_code():
    print 'generate item code'

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
        _id = db(db.Item_Master.item_code == itm_code).select().first()
        db.Item_Prices.insert(item_code_id = _id.id)
        # db.Stock_File.insert(item_code_id = _id.id, location_code_id = 1)            
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
            # TR(TD('Item Desc.AR: '), TD(x.item_description_ar, _style = 'text-align: right')),
            # TR(TD('Supplier Item Ref.: '), TD(x.supplier_item_ref, _style = 'text-align: right')),
            # TR(TD('Int. Barcode:  '), TD(x.int_barcode, _style = 'text-align: right')),
            # TR(TD('Loc. Barcode:  '), TD(x.loc_barcode, _style = 'text-align: right')),
            # TR(TD('ReOrder Value:  '), TD(x.purchase_point, _style = 'text-align: right')),
            # TR(TD('UOM:  '), TD(x.uom_value, _style = 'text-align: right')),
            # TR(TD('Supplier UOM:  '), TD(x.supplier_uom_value,' ', x.supplier_uom_id.description or None, _style = 'text-align: right')),
            # TR(TD('Weight:  '), TD(x.weight_value, _style = 'text-align: right')),
            # TR(TD('Item Type:  '), TD(x.type_id, _style = 'text-align: right')),
            # TR(TD('Selective Tax:  '), TD(x.selective_tax, _style = 'text-align: right')),
            # TR(TD('Vat Percentage:  '), TD(x.vat_percentage, _style = 'text-align: right')),
            # TR(TD('Division:'), TD(x.division_id.div_name, _style = 'text-align: right')),
            # TR(TD('Department:'), TD(x.dept_code_id.dept_name, _style = 'text-align: right')),
            # TR(TD('Supplier:'), TD(x.supplier_code_id.supp_name, _style = 'text-align: right')),
            # TR(TD('Product:'), TD(x.product_code_id.product_code, _style = 'text-align: right')),
            # TR(TD('SubProduct:'), TD(x.subproduct_code_id.subproduct_code, _style = 'text-align: right')),
            # TR(TD('Group Line:'), TD(x.group_line_id.group_line_name, _style = 'text-align: right')),
            # TR(TD('Brand Line:'), TD(x.brand_line_code_id.brand_line_name, _style = 'text-align: right')),
            # TR(TD('Brand Cls Code:'), TD(x.brand_cls_code_id.brand_cls_name, _style = 'text-align: right')),
            # TR(TD('Section Code:'), TD(x.section_code_id.section_name, _style = 'text-align: right')),
            # TR(TD('Size Code:'), TD(x.size_code_id.description, _style = 'text-align: right')),
            # TR(TD('Gender:'), TD(x.gender_code_id.gender_name, _style = 'text-align: right')),
            # TR(TD('Fragrance Code:'), TD(x.fragrance_code_id.fragrance_name, _style = 'text-align: right')),
            # TR(TD('Color:'), TD(x.color_code_id.description, _style = 'text-align: right')),
            # TR(TD('Collection:'), TD(x.collection_code_id.collection_name, _style = 'text-align: right')),
            # TR(TD('Made In:'), TD(x.made_in_id.description, _style = 'text-align: right')),
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
            TR(TD('IB'),TD('UOM'),TD('Pack Size'),TD('Supplier UOM'),TD('Pack Size'),TD('Weight'),TD('Type'),TD('Selective Tax'), _class='active'),
            TR(TD(_query.ib),TD(_query.uom_value),TD(_query.uom_id.description),TD(_query.supplier_uom_value),TD(_query.supplier_uom_id.description),TD(_query.weight_value, ' ', _query.weight_id),TD(_query.type_id.description),TD(_query.selectivetax)))
        table2 = TABLE(*[tbody2], _class = 'table table-bordered')
        tbody3 = TBODY(
            TR(TD('Division'),TD('Department'),TD('Supplier'),TD('Product'),TD('Subproduct'),_class='active'),
            TR(TD(_query.division_id.div_code, ' - ', _query.division_id.div_name),TD(_query.dept_code_id.dept_code, ' - ', _query.dept_code_id.dept_name),TD(_query.supplier_code_id.supp_name),TD(_query.product_code_id),TD(_query.subproduct_code_id.subproduct_name)))
        table3 = TABLE(*[tbody3], _class = 'table table-bordered')

        return DIV(table1, table2, table3)        
    else:
        return CENTER(DIV(B('INFO! '),'No item master record.',_class='alert alert-info',_role='alert'))

def item_master_prices():    
    _query = db(db.Item_Prices.item_code_id == request.args(0)).select().first()
    if _query:
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Recent Cost'),TD('Average Cost'),TD('Recent Landed Cost'),TD('Op. Average Cost'),_class='active'),
            TR(TD(_query.item_code_id.item_code),TD(_query.currency_id.mnemonic, ' ',locale.format('%.4F',_query.most_recent_cost or 0, grouping = True)),TD('QR ', locale.format('%.4F',_query.average_cost or 0, grouping = True)),TD('QR ', _query.most_recent_landed_cost),TD('QR ', _query.opening_average_cost)))
        table1 = TABLE(*[tbody1],_class = 'table table-bordered')
        session.average_cost =  _query.average_cost
        tbody2 = TBODY(
            TR(TD('Wholesale Price'),TD('Retail Price'),TD('Vansale Price'),TD('Reorder Qty'),TD('Last Issued Date'),TD('Currency'),_class='active'),
            TR(TD('QR ', _query.wholesale_price),TD('QR ', _query.retail_price),TD('QR ', _query.vansale_price),TD(_query.reorder_qty),TD(_query.last_issued_date),TD(_query.currency_id.description)))
        table2 = TABLE(*[tbody2],_class = 'table table-bordered')
        return DIV(table1, table2)        
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item price record.',_class='alert alert-info',_role='alert'))

def item_master_stocks():
    _query = db(db.Stock_File.item_code_id == request.args(0)).select().first()
    if _query:
        row = []
        head = THEAD(TR(TD(B('Item Code: ')),TD(_query.item_code_id.item_code),TD(B('Description: ')),TD(_query.item_code_id.item_description),TD(),TD(),TD(),_class='active'))
        head += THEAD(TR(TD(''),TD(),TD(),TD()))

        head += THEAD(TR(TH('Location'),TH('Opening Stock'),TH('Closing Stock'),TH('Prv.Yr. Closing Stock'),TH('Stock In Transit'),TH('Free/Promo Stock'),TH('Damaged/Expired Stock')),_class='active')
        _os = db.Stock_File.opening_stock.sum()
        _cs = db.Stock_File.closing_stock.sum()
        _ps = db.Stock_File.previous_year_closing_stock.sum()
        _si = db.Stock_File.stock_in_transit.sum()
        _fs = db.Stock_File.free_stock_qty.sum()
        _ds = db.Stock_File.damaged_stock_qty.sum()
        _opening_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_os).first()[_os]
        _closing_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_cs).first()[_cs]
        _previou_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_ps).first()[_ps]
        _transit_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_si).first()[_si]
        _freepro_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_fs).first()[_fs]
        _damaged_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_ds).first()[_ds]

        _total_stock = _closing_stock + _damaged_stock
        for n in db(db.Stock_File.item_code_id == request.args(0)).select():    
            row.append(TR(                
                TD(n.location_code_id.location_name),
                TD(card_view(n.item_code_id, n.opening_stock)),
                TD(card_view(n.item_code_id, n.closing_stock)),
                TD(card_view(n.item_code_id, n.previous_year_closing_stock)),
                TD(card_view(n.item_code_id, n.stock_in_transit)),
                TD(card_view(n.item_code_id, n.free_stock_qty)),
                TD(card_view(n.item_code_id, n.damaged_stock_qty))))
        body = TBODY(*[row])
        body += TR(
            TD(B('TOTAL :')),
            TD(B(card_view(n.item_code_id, _opening_stock))),
            TD(B(card_view(n.item_code_id, _total_stock))),
            TD(B(card_view(n.item_code_id, _previou_stock))),            
            TD(B(card_view(n.item_code_id, _transit_stock))),
            TD(B(card_view(n.item_code_id, _freepro_stock))),
            TD(B(card_view(n.item_code_id, _damaged_stock))))
        table = TABLE(*[head, body], _class='table')
        return DIV(table)
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item stock.',_class='alert alert-info',_role='alert'))
def item_master_batch_info():    
    _query = db(db.Purchase_Batch_Cost.item_code_id == request.args(0)).select().first()
    if _query:
        row = []
        ctr = _average = 0
        _id = db(db.Item_Master.id == request.args(0)).select().first()        
        _count = db(db.Purchase_Batch_Cost.item_code_id == request.args(0)).count()        
        head = THEAD(TR(TD(B('Item Code: ')),TD(_id.item_code),TD(B('Description: ')),TD(_id.item_description),_class='active'))
        head += THEAD(TR(TD(''),TD(),TD(),TD()))
        head += THEAD(TR(TH('#'), TH('Batch Date'),TH('Batch Cost'),TH('Batch Landed Cost'),TH('Batch Quantity')))        
        for n in db(db.Purchase_Batch_Cost.item_code_id == request.args(0)).select(orderby = ~db.Purchase_Batch_Cost.id):            
            ctr += 1
            _landed_cost = n.batch_cost * n.supplier_price
            _batch_cost = n.supplier_price
            row.append(TR(
                TD(ctr),TD(n.purchase_receipt_date.date()),
                TD(n.supplier_price),
                TD(locale.format('%.3F',_landed_cost or 0, grouping = True)),
                TD(card_view(n.item_code_id, n.batch_quantity))))
            _average += _landed_cost
        _ave = float(_average) / int(_count)
        body = TBODY(*[row])
        body += TR(TD(),TD(),TD(B('Average Cost:')),TD(B(locale.format('%.3F',session.average_cost or 0, grouping = True))),TD())
        table = TABLE(*[head, body], _class='table ')
        return DIV(table)
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item purchase batch record.',_class='alert alert-info',_role='alert'))
    # return CENTER(DIV(B('INFO! '),'Still in progress.',_class='alert alert-info',_role='alert'))

def item_master_sales_quantity():    
    _query = db(db.Sales_Order_Transaction.item_code_id == request.args(0)).select().first()
    if _query:
        _sales_sum = db.Sales_Order_Transaction.quantity.sum()
        _total_sales = db((db.Sales_Order_Transaction.item_code_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(_sales_sum).first()[_sales_sum]
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Description'),TD('Total Sales'), _class='active'),
            TR(TD(_query.item_code_id.item_code),TD(_query.item_code_id.item_description),TD(card_view(_query.item_code_id,_total_sales))))
        table1 = TABLE(*[tbody1], _class='table table-bordered')
        row = []
        ctr = 0        
        head = THEAD(TR(TD('#'),TD('Location'),TD('Total Sales'), _class='active'))
        _quantity = db.Sales_Order_Transaction.quantity.sum()
        _total_amount = db.Sales_Order_Transaction.total_amount.sum()
        _qty = db(db.Sales_Order_Transaction.item_code_id == request.args(0)).select(_quantity).first()[_quantity]
        _tot_amt = db(db.Sales_Order_Transaction.item_code_id == request.args(0)).select(_total_amount).first()[_total_amount]
        for n in db((db.Sales_Order_Transaction.item_code_id == request.args(0)) & (db.Sales_Order_Transaction.delete==True)).select(orderby = ~db.Sales_Order_Transaction.created_on):
            for y in db(db.Sales_Order.id == n.sales_order_no_id).select():
                ctr += 1
                row.append(TR(TD(ctr),TD(y.stock_source_id.location_name),TD(card_view(_query.item_code_id,_total_sales))))
        body = TBODY(*[row])
        # body += TR(TD(),TD(),TD(B('TOTAL:')),TD(B(card_view(n.item_code_id, _qty))),TD(B(locale.format('%.3F',_tot_amt or 0, grouping = True))))
        table = TABLE(*[head, body], _class='table table-bordered')
        return DIV(table1, table)        
    else:    
        return CENTER(DIV(B('INFO! '),'Grrrrr! No sales items', _class='alert alert-info',_role='alert'))

@auth.requires_login()
def itm_link_profile():
    form = SQLFORM(db.Item_Master, request.args(0))
    _itim_master = db(db.Item_Master.id == request.args(0)).select().first()
    return dict(_itim = _item_master)

def item_prices_grid():
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Most Recent Cost'),TH('Average Cost'),TH('Most Recent Landed Cost'),TH('Status'),TH('Actions')))
    for n in db(db.Item_Master).select(db.Item_Prices.ALL, db.Item_Master.ALL, left = db.Item_Prices.on(db.Item_Master.id == db.Item_Prices.item_code_id)):        
        ctr += 1        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Item_Prices.id))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','item_prices_edit', args = n.Item_Prices.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Item_Prices.id))
        # prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk,edit_lnk, dele_lnk)        
        row.append(TR(
            TD(ctr),
            TD('ITM'+n.Item_Master.item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Item_Prices.most_recent_cost),
            TD(n.Item_Prices.average_cost),
            TD(n.Item_Prices.most_recent_landed_cost),            
            TD(n.Item_Master.item_status_code_id.status),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    return dict(table = table)    

def item_prices_edit():
    db.Item_Prices.item_code_id.represent = lambda id, r: db.Item_Master(id).item_code
    form = SQLFORM(db.Item_Prices, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def master_account():
    form = SQLFORM(db.Master_Account)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    row = []
    thead = THEAD(TR(TH('#'),TH('Account Code'),TH('Account Name'),TH('Action')))
    for n in db(db.Master_Account).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('master_account_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_code),TD(n.account_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)          

def master_account_edit_form():
    form = SQLFORM(db.Master_Account, request.args(0))
    if form.process().accepted:
        respose.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form)
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
    for n in db().select(db.Status.ALL, orderby=db.Status.id):
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
    for n in db(db.Stock_Status).select(orderby = db.Stock_Status.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_n_sale_status_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.required_action),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
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
    row = db(db.Item_Master.dept_code_id == 3).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id))
    return dict(row = row)

def pop():
    return locals()
def testinghead():    
    # db(db.Stock_Transaction_Temp.created_by ==  auth.user_id).delete()
    form2 = SQLFORM.factory(        
        Field('stock_request_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
        Field('stock_due_date','date', default = request.now))
    # if form2.process(formname = 'head').accepted:
    if form2.accepts(request.vars):
        response.flash = 'save'
        
    elif form2.errors:
        response.flash = 'invalid values in form!'
    # records = SQLTABLE(db.Stock_Transaction_Temp).select(),headers='fieldname:capitalize')
    # print request.vars.item_code_id, ' from testing 2'
    return dict(form2 = form2, ticket_no_id = 'ayos')

def tail():
    
    grand_total = 0
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'reference Transaction_Item_Category', default = 4, requires = IS_IN_DB(db((db.Transaction_Item_Category.mnemonic != 'E') & (db.Transaction_Item_Category.mnemonic != 'S')), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')),
        Field('srn_status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 3), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process(formname = 'tail').accepted:                
        print 'tick: ', request.args(0), request.vars.ticket_no_id, form.vars.ticket_no_id
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        grand_total = db().select(total).first()[total]
        db.Stock_Transaction_Temp.insert(
            item_code_id = form.vars.item_code_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            category_id = form.vars.category_id,
            # amount = total_amount_value,
            stock_source_id = request.vars.stock_source_id,
            ticket_no_id = form.vars.ticket_no_id)
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
    
        
    return dict()

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

def stock_file_grid():
    row = []
    db.Stock_File.item_code_id.represent = lambda id, r: db.Item_Master(id).item_code
    db.Stock_File.location_code_id.represent = lambda id, r: db.Location(id).location_name
    table = SQLFORM.grid(db.Stock_File)
    return dict(table = table)

def update_stock_file():
    for n in db(db.Stock_File).select():
        if not n.damaged_stock_qty:
            n.update_record(damaged_stock_qty = 0)
    return dict()

def abort_entry():    
    for n in db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select():        
        _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select().first()
        _d = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_destination_id)).select().first()
        _s.stock_in_transit += n.qty
        _d.stock_in_transit -= n.qty
        _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)                      
        _d.probational_balance = int(_d.closing_stock) + int(_d.stock_in_transit)
        _s.update_record()
        _d.update_record()

        db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).delete()         
    session.flash = 'ABORT'
    

def test_up():
    # print 'from testing3 id', request.args(0), request.args(1), request.args(2)
    # parent = $(this).parent("div").parent("td").parent("tr");
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _tmp = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    # db(db.Stock_Transaction_Temp.id == request.args(0)).delete()
    # return "jQuery('#target').html(%s);" % repr(request.vars.name)
    _tmp.update_record(quantity = _qty, pieces = _pcs)

def itm_description_():
    print '-----', request.now, '-------'
    _itm_code = db(db.Item_Master.item_code == str(request.vars.item_code)).select().first()       
    if not _itm_code:
        print 'not available'
    else:
        _stk_file = db((db.Stock_File.item_code_id == _itm_code.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()
        _item_price = db(db.Item_Prices.item_code_id == _itm_code.id).select().first()
    
        if all([_itm_code, _stk_file, _item_price]):
            print 'all'
        elif not _stk_file:
            print 'no stock file'
        elif not _item_price:
            print 'no item price'
        else:
            print 'error'        

def itm_description():   
    # print '-----', request.now, '-------' 
    response.js = "$('#add').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled')"    
    _itm_code = db(db.Item_Master.item_code == request.vars.item_code).select().first()       
    if not _itm_code:        
        # response.js = "$('#add').attr('disabled','disabled')"
        return CENTER(DIV("Item code no doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))        
    else:        
        _stk_file = db((db.Stock_File.item_code_id == _itm_code.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()
        _item_price = db(db.Item_Prices.item_code_id == _itm_code.id).select().first()        
        if all([_itm_code, _stk_file, _item_price]):                        
            # response.js = "$('#add').removeAttr('disabled')"
            if _itm_code.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"                
                _on_balanced = _stk_file.probational_balance
                _on_transit = _stk_file.stock_in_transit
                _on_hand = _stk_file.closing_stock      
            else:    
                response.js = "$('#no_table_pieces').removeAttr('disabled')"
                _on_balanced = card_view(_stk_file.item_code_id, _stk_file.probational_balance)
                _on_transit = card_view(_stk_file.item_code_id, _stk_file.stock_in_transit)
                _on_hand = card_view(_stk_file.item_code_id, _stk_file.closing_stock)
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance'))),
            TBODY(TR(TD(_itm_code.item_code),TD(_itm_code.item_description.upper()),TD(_itm_code.group_line_id.group_line_name),TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),TD(_on_hand),TD(_on_transit),TD(_on_balanced)),_class="bg-info"),_class='table'))
            
        elif not _stk_file:             
            return CENTER(DIV("Empty stock file on selected stock source.", _class='alert alert-warning',_role='alert'))            
            # response.js = "$('#add').attr('disabled','disabled')"               
        elif not _item_price:            
            return CENTER(DIV("Empty retail price.", _class='alert alert-warning',_role='alert'))         
            # response.js = "$('#add').attr('disabled','disabled')"    

def itm_view():    
    row = []
    uom_value = 0
    retail_price_value = 0
    total_pcs = 0        
    grand_total = 0
    form = SQLFORM(db.Stock_Transaction_Temp)
    if form.accepts(request, formname=None, onvalidation = validate_item_code):                           
        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, 
            left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
            ctr += 1            

            edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})            
            # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = k.Stock_Transaction_Temp.id))

            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type=' button', _role=' button', _class='btn btn-icon-toggle', delete = 'tr', _id = 'del',callback=URL('del_item', args = k.Stock_Transaction_Temp.id, extension = False))            
            btn_lnk = DIV(edit_lnk, dele_lnk)
            # g = sum(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).amount for a in session.grand_total.items()
            grand_total += float(k.Stock_Transaction_Temp.amount)
            row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),
            TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f', grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
        return dict(table = table)
    elif form.errors:
        grand_total = 0
        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
            ctr += 1            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))            
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
        table += TABLE(*[head, body, foot], _class='table')
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
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _disabled = True)
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True)

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def category_option():
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()

    if not _id:
        return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db((db.Transaction_Item_Category.id == 1) |(db.Transaction_Item_Category.id == 3)|(db.Transaction_Item_Category.id == 4)).select(orderby=db.Transaction_Item_Category.id)])
    else:
        # print request.vars.stock_destination_id
        if int(request.vars.stock_destination_id) != 1:     
            # print 'if'
            # _des = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_destination_id)).select().first()
            _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
            if _id.type_id == 3 or _id.type_id == 2:
                return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db(db.Transaction_Item_Category.id == 4).select(orderby=db.Transaction_Item_Category.id)])        
            if _id.type_id == 1:
                return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db(db.Transaction_Item_Category.id == 3).select(orderby=db.Transaction_Item_Category.id)])            
            # if _id.type_id == 3 and _des.location_code_id == 1:
        else:
            # print 'else'
            return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db((db.Transaction_Item_Category.id == 1) |(db.Transaction_Item_Category.id == 3)|(db.Transaction_Item_Category.id == 4)).select(orderby=db.Transaction_Item_Category.id)])

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_add_form():          
    ctr = db(db.Transaction_Prefix.prefix_key == 'SRN').select().first()
    _skey = ctr.current_year_serial_key 
    _skey += 1        
    _ticket_no = id_generator()
    session.ticket_no_id = _ticket_no
    # session.grand_total = 0
    form = SQLFORM.factory(       
        Field('ticket_no_id', 'string', default = _ticket_no),
        Field('stock_request_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Location')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Destination')),    
        Field('stock_due_date','date', default = request.now),
        Field('remarks','string'),
        Field('srn_status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:          
        ctr = db((db.Transaction_Prefix.prefix_key == 'SRN')&(db.Transaction_Prefix.dept_code_id == form.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key 
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        response.flash = 'SAVING STOCK REQUEST NO SRN' +str(_skey) + '.'       
        db.Stock_Request.insert(
            # ticket_no = form.vars.ticket_no_id,
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
        if not _src:
            form.errors._src = DIV('errossr')
        for s in _src:
            _itm = db(db.Item_Master.id == s.item_code_id).select().first()
            _prc = db(db.Item_Prices.item_code_id == s.item_code_id).select().first()
            _qty = s.quantity * _itm.uom_value + s.pieces
            db.Stock_Request_Transaction.insert(
                stock_request_id = _id.id,
                item_code_id = s.item_code_id,
                category_id = s.category_id,
                uom = _itm.uom_value,
                price_cost = s.price_cost,
                quantity = _qty,
                average_cost = _prc.average_cost,
                wholesale_price = _prc.wholesale_price,
                retail_price = _prc.retail_price,
                vansale_price = _prc.vansale_price,
                remarks = s.remarks,
                created_by = s.created_by)
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        _grand_total = db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(total).first()[total]
        _id.update_record(total_amount = session.grand_total)
        print 'grand_total submit: ', session.grand_total, _grand_total
        db(db.Stock_Transaction_Temp.ticket_no_id == form.vars.ticket_no_id).delete()
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR' 
    btnHelp = A(_class='btn btn-info', _type = 'button', _href = URL('inventory', 'item_help', args = [form.vars.dept_code_id, form.vars.stock_source_id]))
    return dict(form = form, ticket_no_id = _ticket_no, btnHelp = btnHelp)
 
def validate_item_code(form):    
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty.'
        # form.errors._id = CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' does not exist or empty.',_class='alert alert-danger',_role='alert'))
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():        
        form.errors.item_code =  'Item code is zero in stock file'
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first():        
        form.errors.item_code =  'Item code is not allowed in stock file destination'
    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        
            # form.errors._stk_file =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' is zero in stock file',_class='alert alert-danger',_role='alert'))                        
        
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id) & (db.Stock_Transaction_Temp.item_code == request.vars.item_code)).select(db.Stock_Transaction_Temp.item_code).first()                   

        _total_pcs = (int(request.vars.quantity) * int(_id.uom_value)) + int(request.vars.pieces)    
        
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
            # print 'zero not allowed'
            response.js = "$('#no_table_item_code').val('')"

        if int(_stk_file.stock_in_transit) >= 0:
            # print 'positive'
            if int(_total_pcs) > int(_stk_file.closing_stock):
                _pb = card(_stk_file.item_code_id, _stk_file.closing_stock, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than closing stock of ' + str(_pb)            
        else:
            # print 'negative'
            if int(_total_pcs) > int(_stk_file.probational_balance):
                _pb = card(_stk_file.item_code_id, _stk_file.probational_balance, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than provisional balance of ' + str(_pb)                            

        if not _price:
            # print 'price validation ', _id.item_code
            form.errors.item_code =  "Item code does'nt have price."
            _total = _unit_price = 0
            # form.errors._stk_file =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), " does'nt have price.",_class='alert alert-danger',_role='alert'))        
        elif (_price.retail_price == float(0.0) or _price.wholesale_price == float(0.0)) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.errors._price = 'Cannot request this item because retail price is zero'
        else:
            _unit_price = float(_price.retail_price) / int(_id.uom_value)
            _total = float(_unit_price) * int(_total_pcs)            
            # form.errors._price = CENTER(DIV('Cannot request this item because retail price is zero',_class='alert alert-danger',_role='alert'))

        if _exist:
            form.errors.item_code = 'Item code ' + str(form.vars.item_code) + ' already exist.'
            # print 'exist'
            # return CENTER(DIV('The same item already added on the grid.',_class='alert alert-danger',_role='alert'))            
            # form.errors.item_code_id = CENTER(DIV('Item Code ' , B(str(request.vars.item_code)),' already exist.',_class='alert alert-danger',_role='alert'))

        # if _id.uom_value == 1:
        #     form.vars.pieces = 0        
        if int(form.vars.pieces) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value of ' + str(_id.uom_value)            
            # print pcs
            # Pieces Value is not applicable to this item because UOM is equal to 1
            # form.errors.pcs = CENTER(DIV('Pieces value should not be more than or equal to UOM value ',_class='alert alert-danger',_role='alert')) 
        
        # to be modified 
        # print request.vars.category_id
        if (form.vars.category_id == 3) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):            
            form.errors.mnemonic = 'This saleable item cannot be transfered as FOC.'
            # form.errors.mnemonic = CENTER(DIV(B('WARNING! '),' This saleable item cannot be transfered as FOC.',_class='alert alert-danger',_role='alert')) 
            # ' this saleable item cannot be transfered as FOC'

        # if int(_stk_file.probational_balance) == 0:
        

            # form.errors.clear()
            # form.errors.quantity = CENTER(DIV(B('WARNING! '),' Quantity should not be more than probational balance ' + str(strr) ,_class='alert alert-danger',_role='alert')) 

        # stk = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select(db.Stock_File.ALL).first()        
 
        if not _stk_file.last_transfer_date:        
            # _remarks = 'LTD: ' + str(date.today().strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)
            _remarks = 'None' 
        else:
            _card = card(_stk_file.item_code_id, _stk_file.last_transfer_qty, _id.uom_value)
            _remarks = 'LTD: ' + str(_stk_file.last_transfer_date.strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)
        if request.vars.category_id == None:
            response.js = "$('#category_id').show()"

        form.vars.item_code_id = _id.id        
        form.vars.stock_source_id = int(session.stock_source_id)
        form.vars.stock_destination_id = int(session.stock_destination_id)        
        form.vars.amount = float(_total)        
        form.vars.price_cost = float(_unit_price)
        form.vars.remarks = _remarks
        form.vars.qty = int(_total_pcs)
        # response.js = "('#no_table_item_code').setfocus()"

def stock_request_transaction_temporary_table():
    ctr = 0
    row = []        
    grand_total = 0
    form = SQLFORM.factory(
        # Field('item_code', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.item_code, limitby = (0,10), min_length = 2)),
        Field('item_code', 'string', length = 15),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'integer', default = 4))
    if form.process(onvalidation = validate_item_code).accepted:
        _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _stk_dest = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first()
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'
        db.Stock_Transaction_Temp.insert(
            item_code_id = form.vars.item_code_id,
            item_code = request.vars.item_code,
            stock_source_id = form.vars.stock_source_id, 
            stock_destination_id = form.vars.stock_destination_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces or 0, 
            qty = form.vars.qty,
            price_cost = form.vars.price_cost,
            category_id = form.vars.category_id,
            amount = form.vars.amount, 
            remarks = form.vars.remarks, 
            ticket_no_id = session.ticket_no_id)                
        if db(db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled');"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled');"
        _tmp = db(db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id).select().first()        
        _stk_file.stock_in_transit -= int(form.vars.qty)                
        _stk_dest.stock_in_transit += int(form.vars.qty)
        _stk_file.probational_balance = int(_stk_file.closing_stock) + int(_stk_file.stock_in_transit)
        _stk_dest.probational_balance = int(_stk_dest.closing_stock) + int(_stk_dest.stock_in_transit)
        # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
        _stk_file.update_record()   
        _stk_dest.update_record()
        # print _stk_file.stock_in_transit, _stk_file.probational_balance, int(form.vars.qty)

    elif form.errors:        
        table = TABLE(*[TR(v) for k, v in form.errors.items()])
        response.flash = XML(v)
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price',_style="width:10px;"),TH('Total Amount',_style="width:100px;"),TH('Remarks'),TH('Action'), _class='bg-success'))
    for k in db(db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = db.Stock_Transaction_Temp.id, 
        left = [
            db.Item_Master.on(db.Item_Master.item_code == db.Stock_Transaction_Temp.item_code),
            db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        ctr += 1            
        # save_lnk = A(I(_class='fas fa-save'), _title='Update Row', _type=' button', _role=' button', _class='btn btn-icon-toggle update', callback=URL('inventory','stock_request_temp_update',args=[k.Stock_Transaction_Temp.id,request.vars.quantity], extension = False))
        # save_lnk = A(I(_class='fas fa-save'), _title='Update Row', _type=' button', _role=' button', _class='btn btn-icon-toggle update', callback=URL('inventory','stock_request_temp_update', args = k.Stock_Transaction_Temp.id,request.vars.quantity)) 
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type=' button', _role=' button', _class='btn btn-icon-toggle delete', callback=URL( args = k.Stock_Transaction_Temp.id, extension = False), **{'_data-id':(k.Stock_Transaction_Temp.id)})            
        btn_lnk = DIV(dele_lnk)
        grand_total += float(k.Stock_Transaction_Temp.amount)
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        row.append(TR(
            TD(ctr, INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true',_value=k.Stock_Transaction_Temp.id)),
            TD(k.Stock_Transaction_Temp.item_code.upper(),INPUT(_class='form-control item_code_id',_type='text',_name='item_code_id',_hidden='true',_value=k.Stock_Transaction_Temp.item_code_id)),
            TD(k.Item_Master.item_description),
            # TD(k.Stock_Transaction_Temp.category_id.description),
            TD(k.Stock_Transaction_Temp.category_id),
            TD(k.Item_Master.uom_value, INPUT(_type='number',_name='uom',_hidden='true',_value=k.Item_Master.uom_value)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=k.Stock_Transaction_Temp.quantity), _style='text-align:right;width:100px;'),
            TD(INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=k.Stock_Transaction_Temp.pieces or 0), _style='text-align:right;width:100px;'), 
            TD(INPUT(_class='form-control unit_price',_type='text',_name='unit_price', _value=locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True)),_align='right'),
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True)),_align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))
        print k.Stock_Transaction_Temp.id
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(INPUT(_class='form-control grand_total',_name='grand_total', _type='text',_value=locale.format('%.2f', grand_total or 0, grouping = True))), _align = 'right'),TD(_btnUpdate),TD()))
    table = FORM(TABLE(*[head, body, foot], _id='tblIC',_class='table'))
    if table.accepts(request,session):
        if request.vars.btnUpdate:
            print 'updated'
            if isinstance(request.vars.ctr, list):
                print 'list'
                row = 0
                for x in request.vars.ctr:                    
                    _row = db(db.Stock_Transaction_Temp.id == x).select().first()
                    _qty = (int(request.vars.quantity[row]) * int(request.vars.uom[row])) + int(request.vars.pieces[row])

                    print request.vars.quantity[row], x,_qty, _row.qty
                    if _row.qty != _qty:
                        print 'not equal'
                        _stk_src_ctr = int(-_qty) - int(-_row.qty)
                        _stk_des_ctr = int(_qty) - (_row.qty)
                        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                        _stk_des = db((db.Stock_File.item_code_id == int(request.vars.item_code_id[row])) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                        _stk_src.stock_in_transit += _stk_src_ctr
                        _stk_des.stock_in_transit += _stk_des_ctr
                        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                        _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                        _stk_src.update_record()
                        _stk_des.update_record()                        
                        _amount = int(_qty) * float(_row.price_cost)
                        db(db.Stock_Transaction_Temp.id == x).update(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], qty = _qty, amount = _amount)                        
                    else:
                        print 'equal'

                    row+=1
                    session.grand_total = request.vars.grand_total
                    print 'grand total updated: ', request.vars.grand_total

            else:
                print 'not list'
                _row = db(db.Stock_Transaction_Temp.id == int(request.vars.ctr)).select().first()
                _qty = (int(request.vars.quantity) * int(request.vars.uom)) + int(request.vars.pieces)
                if _row.qty != _qty:
                    _stk_src_ctr = int(-_qty) - int(-_row.qty)
                    _stk_des_ctr = int(_qty) - (_row.qty)
                    _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                    _stk_des = db((db.Stock_File.item_code_id == int(request.vars.item_code_id)) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                    _stk_src.stock_in_transit += _stk_src_ctr
                    _stk_des.stock_in_transit += _stk_des_ctr
                    _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                    _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                    _stk_src.update_record()
                    _stk_des.update_record()            
                    _amount = int(_qty) * float(_row.price_cost)
                    db(db.Stock_Transaction_Temp.id == int(request.vars.ctr)).update(quantity = request.vars.quantity, pieces = request.vars.pieces, qty = _qty, amount = _amount)                        
                    session.grand_total = request.vars.grand_total
                    print 'grand total updated: ', request.vars.grand_total
        else:
            print 'not updated'
        response.js = "$('#tblIC').get(0).reload();"        
    return dict(form = form, table = table)

def stock_request_temp_update():
    print 'updated', request.args(0), request.args(1)
    # _id = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    # _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    # _qty = int(_id.quantity) * int(_im.uom_value) + int(_id.pieces)
    # _id.update_record(quantity = _qty, )

def stock_request_temp_update_():
    row = 0
    if isinstance(request.vars.ctr, list):
        for x in request.vars.ctr:
            _qty = request.vars.quantity[row] * request.vars.uom[row] + request.vars.pieces[row] 
            db(db.Stock_Transaction_Temp.id == x).update(quantity = request.vars['quantity'][row], pieces = request.vars['pieces'][row], qty = _qty)
            row+=1        
    else:
        _qty = request.vars.quantity * request.vars.uom + request.vars.pieces
        db(db.Stock_Transaction_Temp.id == request.vars.ctr).update(quantity = request.vars.quantity, pieces = request.vars.pieces, qty = _qty)

def push_to_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = request.vars.stock_source_id
    session.stock_destination_id = request.vars.stock_destination_id

def del_item():
    itm = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()    
    uom = db(db.Item_Master.id == itm.item_code_id).select().first()
    total_pcs = int(itm.quantity) * int(uom.uom_value) + int(itm.pieces)  
    _stk_src = db((db.Stock_File.item_code_id == itm.item_code_id) & (db.Stock_File.location_code_id == itm.stock_source_id)).select().first()
    _stk_des = db((db.Stock_File.item_code_id == itm.item_code_id) & (db.Stock_File.location_code_id == itm.stock_destination_id)).select().first()
    _stk_src.stock_in_transit += itm.qty
    _stk_des.stock_in_transit -= itm.qty
    _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
    _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
    _stk_src.update_record()
    _stk_des.update_record()

    db(db.Stock_Transaction_Temp.id == request.args(0)).delete()        
    response.js = "$('#tblIC').get(0).reload()"


def stock_request_transaction_temporary_table_edit():    
    _tmp = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    _uom = db(db.Item_Master.id == _tmp.item_code_id).select().first()
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _total_pcs = _qty * _uom.uom_value + _pcs
    if _total_pcs >= _uom.uom_value:
        response.flash = 'QUANTITY HAS ERROR'
    else:
        _amount = float(_tmp.price_cost) * int(_total_pcs)
        _tmp.update_record(quantity = _qty, pieces = _pcs, qty = _total_pcs, amount = _amount)
        # response.js = "$('#tblIC').get(0).reload()"

# STOCK REQUEST FORM #

def validateremarks(form):
    form.vars.remarks = ''

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_details_form():    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.stock_due_date.writable = False        
    db.Stock_Request.dept_code_id.writable = False        
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False    
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Stock_Request.stock_request_date_approved.writable = False
    ticket_no_id = id_generator()
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process(onvalidation = validateremarks).accepted:
        response.flash = 'RECORDS UPDATED'
        redirect(URL('inventory','stk_req_form'))
    if form.errors:
        response.flash = 'FORM HAS ERRORS'

    row = []
    _grand_total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    session.stock_source_id = _id.stock_source_id
    session.stock_destination_id = _id.stock_destination_id
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks'),TH('Action')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Stock_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1
        _total_amount = int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        _grand_total += _total_amount
        _qtty = k.Stock_Request_Transaction.quantity / k.Stock_Request_Transaction.uom
        _pcs = k.Stock_Request_Transaction.quantity - k.Stock_Request_Transaction.quantity / k.Stock_Request_Transaction.uom * k.Stock_Request_Transaction.uom
        if (_id.srn_status_id == 2) | (_id.srn_status_id == 5) | (_id.srn_status_id == 6):        
            edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle disabled')   
            _quantity = INPUT(_class='form-control quantity',_type='number',_name='qty',_value=_qtty, _readonly='true')
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pcs',_value=_pcs,_readonly='true')                        
        else:
            _quantity = INPUT(_class='form-control quantity',_type='number',_name='qty',_value=_qtty)
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pcs',_value=_pcs)
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('stk_req__trans_edit_form', args = k.Stock_Request_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = k.Stock_Request_Transaction.id), **{'_data-id':(k.Stock_Request_Transaction.id)})          
        btn_lnk = DIV( dele_lnk)        
        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true',_value=k.Stock_Request_Transaction.id)),
            TD(k.Item_Master.item_code,INPUT(_class='form-control ico',_type='text',_name='ico',_hidden='true',_value=k.Stock_Request_Transaction.item_code_id)),
            TD(k.Item_Master.item_description.upper(),INPUT(_class='form-control uom',_type='number',_name='uom',_hidden='true',_value=k.Stock_Request_Transaction.uom)),
            TD(k.Stock_Request_Transaction.category_id.mnemonic),        
            TD(_quantity, _style='width:100px;'),
            TD(_pieces, _style='width:100px;'),
            TD(INPUT(_class='form-control unit_price',_type='text',_name='unit_price',_value=k.Item_Prices.retail_price), _style='width:100px;'),
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.2F', _total_amount or 0, grouping = True)), _style='width:100px;'),
            TD(k.Stock_Request_Transaction.remarks),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(INPUT(_class='form-control grand_total',_name='grand_total', _type='text',_value=locale.format('%.2F',_grand_total or 0, grouping = True))), _align = 'right'),TD(INPUT(_id='btnSave', _name='btnSave', _type= 'submit', _value='update', _class='btn btn-success')),TD()))
    table = FORM(TABLE(*[head, body, foot],_id='tblIC', _class='table'))
    if table.accepts(request,session):
        if request.vars.btnSave:
            # print 'save'    
            _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
            if isinstance(request.vars.ctr, list):                
                # print 'list'
                row = 0                
                for x in request.vars.ctr:                    
                    _row = db(db.Stock_Request_Transaction.id == x).select().first()
                    _qty = (int(request.vars.qty[row]) * int(request.vars.uom[row])) + int(request.vars.pcs[row])
                    # print x, _row.quantity, _qty
                    if _row.quantity != _qty:                                                   
                        _stk_src_inc = int(-_qty) - int(-_row.quantity)
                        _stk_src_dec = int(_qty) - (_row.quantity)
                        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                        _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                        # print _stk_src.stock_in_transit, _stk_des.stock_in_transit
                        _stk_src.stock_in_transit += _stk_src_inc
                        _stk_des.stock_in_transit += _stk_src_dec
                        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                        _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                        _stk_src.update_record()
                        _stk_des.update_record()            
                        db(db.Stock_Request_Transaction.id == x).update(quantity = _qty, updated_by = auth.user_id, updated_on = request.now)        
                    row+=1                
                    # else:
                    #     print 'equal', _row.quantity

            else:                
                _row = db(db.Stock_Request_Transaction.id == int(request.vars.ctr)).select().first()
                _qty = (int(request.vars.qty) * int(request.vars.uom)) + int(request.vars.pcs)        
                if _row.quantity != _qty:                    
                    _stk_src_inc = int(-_qty) - int(-_row.quantity)
                    _stk_src_dec = int(_qty) - (_row.quantity)
                    _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                    _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                    _stk_src.stock_in_transit += _stk_src_inc
                    _stk_des.stock_in_transit += _stk_src_dec
                    _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                    _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                    _stk_src.update_record()
                    _stk_des.update_record()

                    db(db.Stock_Request_Transaction.id == int(request.vars.ctr)).update(quantity = _qty, updated_by = auth.user_id, updated_on = request.now)
                #     print 'not equal', _stk_src_inc, _qty, _row.quantity
                # else:
                #     print 'equal'
            
            # print 'grand total: repalce', request.vars.grand_total.replace(",","")
            _grandTotal = request.vars.grand_total.replace(",","")
            db(db.Stock_Request.id == request.args(0)).update(total_amount=_grandTotal)
            
        else:
            print 'not save'
        response.js = "$('#btnUpdate').get(0).reload();"
    btnAdd = A('Add New',_class='btn btn-success', _role = 'button', _id = 'btnrewReq', callback = URL('addNewItem',  args = [request.args(0), ticket_no_id]))       
    
    # btnHelp = A('Help?',_class='btn btn-success', _role = 'button', _id = 'btnHelp', _target = 'blank', _href=URL('item_help',args = _id.dept_code_id))
    form2 = SQLFORM.factory(        
        Field('item_code', 'string', length = 15),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'integer', default = 4))
    if form2.process(onvalidation = validate_updated_item_code).accepted:        
        response.flash = 'ITEM CODE ' + str(form2.vars.item_code) + ' ADDED'        
        _ic = db(db.Item_Master.item_code == form2.vars.item_code).select().first()   
        _ip = db(db.Item_Prices.item_code_id == _ic.id).select().first()     
        _qty = int(form2.vars.quantity) * int(_ic.uom_value) + int(form2.vars.pieces)
        _ppp = float(_ip.retail_price) / int(_ic.uom_value) 
        _tot = int(_qty) * float(_ppp)        
        # print request.args(0), form2.vars.category_id, _ip.retail_price, _tot, _ppp, _ip.average_cost, _ip.wholesale_price, _ip.vansale_price
        db.Stock_Request_Transaction.insert(
            stock_request_id = request.args(0),
            item_code_id = _ic.id,
            category_id = form2.vars.category_id,
            quantity = _qty,
            uom = _ic.uom_value,
            price_cost = _ppp,
            retail_price = _ip.retail_price,
            average_cost = _ip.average_cost,
            wholesale_price = _ip.wholesale_price,
            vansale_price = _ip.vansale_price,
            remarks = form2.vars.remarks)
        _stk_src = db((db.Stock_File.item_code_id == _ic.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _stk_des = db((db.Stock_File.item_code_id == _ic.id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first()
        _stk_src.stock_in_transit -= int(_qty)
        _stk_des.stock_in_transit += int(_qty)
        _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
        _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
        _stk_src.update_record()   
        _stk_des.update_record()

    # else:
    #     response.flash = 'FORM HAS ERROR'

    return dict(form = form, form2 = form2, table = table, _id = _id, ticket_no_id = ticket_no_id)

def validate_updated_item_code(form2):    
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    if not _id:
        form2.errors.item_code = 'Item code does not exist or empty.'
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():
        form2.errors._stk_file =  'Item code is zero in stock file'
    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Stock_Request_Transaction.item_code_id == _id.id) & (db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.item_code_id).first()                   
        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)            
        if _total_pcs == 0:
            form2.errors.quantity = 'Zero quantity not accepted.'
            # print 'zero not allowed'
            response.js = "$('#no_table_item_code').val('')"
        
        if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):            
            strr = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
            _pb = card(_stk_file.item_code_id, strr, _id.uom_value)            
            form2.errors.quantity = 'Quantity should not be more than provisional balance of ' + str(_pb)

        if not _price:            
            form2.errors.item_code =  "Item code does'nt have price."
            _total = _unit_price = 0            
        elif (_price.retail_price == float(0.0) or _price.wholesale_price == float(0.0)) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form2.errors._price = 'Cannot request this item because retail price is zero'
        else:
            _unit_price = float(_price.retail_price) / int(_id.uom_value)
            _total = float(_unit_price) * int(_total_pcs)            
        if _exist:
            form2.errors.item_code = 'Item code ' + str(form2.vars.item_code) + ' already exist.'
        if int(form2.vars.pieces) >= _id.uom_value:
            form2.errors.pieces = 'Pieces value should not be more than or equal to UOM value of ' + str(_id.uom_value)
            # print pcs
            # Pieces Value is not applicable to this item because UOM is equal to 1
        
        # to be modified 
        # print request.vars.category_id
        if (form2.vars.category_id == 3) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):            
            form2.errors.mnemonic = 'This saleable item cannot be transfered as FOC.'
            # form2.errors.mnemonic = CENTER(DIV(B('WARNING! '),' This saleable item cannot be transfered as FOC.',_class='alert alert-danger',_role='alert')) 
            # ' this saleable item cannot be transfered as FOC'
        if not _stk_file.last_transfer_date:        
            # _remarks = 'LTD: ' + str(date.today().strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)
            _remarks = 'None' 
        else:
            _card = card(_stk_file.item_code_id, _stk_file.last_transfer_qty, _id.uom_value)
            _remarks = 'LTD: ' + str(_stk_file.last_transfer_date.strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)       
        # form2.vars.item_code_id = _id.id        
        # form2.vars.amount = float(_total)        
        # form2.vars.price_cost = float(_unit_price)
        form2.vars.remarks = _remarks
        # form2.vars.qty = int(_total_pcs)    
   
def stock_request_update_():    
    if isinstance(request.vars.ctr, list):                
        row = 0
        for x in request.vars.ctr:           
            _qty = (int(request.vars.qty[row]) * int(request.vars.uom[row])) + int(request.vars.pcs[row])        
            _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
            _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
            # print _stk_src.stock_in_transit, _stk_des.stock_in_transit
            _stk_src.stock_in_transit -= _qty
            _stk_des.stock_in_transit += _qty
            _stk_src.update_record()
            _stk_des.update_record()            
            db(db.Stock_Request_Transaction.id == x).update(quantity = _qty, updated_by = auth.user_id, updated_on = request.now)        
            row+=1                
    else:        
        _qty = (int(request.vars.qty) * int(request.vars.uom)) + int(request.vars.pcs)        
        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
        _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
        # print _stk_src.stock_in_transit, _stk_des.stock_in_transit
        _stk_src.stock_in_transit -= _qty
        _stk_des.stock_in_transit += _qty
        _stk_src.update_record()
        _stk_des.update_record()

        db(db.Stock_Request_Transaction.id == int(request.vars.ctr)).update(quantity = _qty, updated_by = auth.user_id, updated_on = request.now)
        
def addNewItem():    
    for n in db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select():     
        _id = db(db.Item_Master.id == n.item_code_id).select().first()
        _sr = db(db.Stock_Request.id == request.args(0)).select().first()
        _qty = n.quantity / n.uom
        _pcs = n.quantity - n.quantity / n.uom * n.uom
        _amt = int(n.quantity) * float(n.price_cost)
        db.Stock_Transaction_Temp.insert(item_code_id = n.item_code_id,item_code = _id.item_code,stock_source_id = _sr.stock_source_id,stock_destination_id = _sr.stock_destination_id,
            quantity = _qty,pieces = _pcs,qty = n.quantity,price_cost = n.price_cost,category_id = n.category_id,amount = _amt,remarks = n.remarks,ticket_no_id = request.args(1))        

def help_request():    
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Description'),TH('Department'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance')))    
    for n in db(db.Item_Master.dept_code_id == session.dept_code_id).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
        for s in db((db.Stock_File.item_code_id == n.Item_Master.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select():
            if not n.Item_Master.supplier_code_id:
                _supplier = 'None'
            else:
                _supplier = n.Item_Master.supplier_code_id.supp_name
            row.append(TR(            
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.item_description),            
                TD(n.Item_Master.dept_code_id.dept_name),
                TD(_supplier),
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

def item_help():        
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Description'),TH('Department'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance')))    
    for n in db(db.Item_Master.dept_code_id == int(session.dept_code_id)).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
        for s in db((db.Stock_File.item_code_id == n.Item_Master.id) & ((db.Stock_File.location_code_id == session.location_code_id) | (db.Stock_File.location_code_id == session.stock_source_id))).select():
            if n.Item_Master.uom_value == 1:                                
                _on_hand = s.closing_stock
                _on_transit = s.stock_in_transit
                _on_balance = s.probational_balance
            else:
                _on_hand = on_hand(n.Item_Master.id)
                _on_transit = on_transit(n.Item_Master.id)
                _on_balance = on_balance(n.Item_Master.id)
            row.append(TR(TD(n.Item_Master.item_code),TD(n.Item_Master.item_description),TD(n.Item_Master.dept_code_id.dept_name),TD(n.Item_Master.supplier_code_id),TD(n.Item_Master.group_line_id.group_line_name),TD(n.Item_Master.brand_line_code_id.brand_line_name),TD(n.Item_Master.uom_value),TD(n.Item_Prices.retail_price),TD(_on_hand),TD(_on_transit),TD(_on_balance)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'display', _id = 'example', _style = "width:100%")
    return dict(table = table)

def on_hand(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _closing = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _on_hand = _closing.closing_stock
        return _on_hand
    else:
        _s = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _outer_on_hand = int(_s.closing_stock) / int(_i.uom_value)
        _pcs_on_hand = int(_s.closing_stock) - int(_outer_on_hand * _i.uom_value) 
        _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_i.uom_value)
        return _on_hand

def on_balance(e):    
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _balance = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _on_balance = _balance.probational_balance
        return _on_balance
    else:
        _s = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _outer = int(_s.probational_balance) / int(_i.uom_value)        
        _pcs = int(_s.probational_balance) - int(_outer * _i.uom_value)    
        _on_balance = str(_outer) + ' ' + str(_pcs) + '/' + str(_i.uom_value)
        return _on_balance

def on_transit(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _transit = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _on_transit = _transit.stock_in_transit
        return _on_transit
    else:
        _s = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
        _outer_transit = int(_s.stock_in_transit or 0) / int(_i.uom_value)
        _pcs_transit = int(_s.stock_in_transit) - int(_outer_transit * _i.uom_value)
        _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_i.uom_value)
        return _on_transit

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_details_add_form():   
    _stk_req_no = db(db.Stock_Request.id == request.args(0)).select().first()
    # _stk_trn_no = db(db.Stock_Request_Transaction.stock_request_id == _stk_req_no.id).select().first()
    return dict(_stk_req_no = _stk_req_no, _stk_trn_no = '_stk_trn_no')

def stock_request_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_request_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        if not _id.stock_request_date_approved:
            _date = 'None'
        else:
            _date = _id.stock_request_date_approved
        if not _id.stock_request_approved_by:
            _appr = 'None'
        else:        
            _appr = str(_id.stock_request_approved_by.first_name.upper()) + ' ' + str(_id.stock_request_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_transfer_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_transfer_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        _date = _id.stock_transfer_date_approved
        _appr = str(_id.stock_transfer_approved_by.first_name.upper()) + ' ' + str(_id.stock_transfer_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_receipt_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_receipt_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        _date = _id.stock_receipt_date_approved
        _appr = str(_id.stock_receipt_approved_by.first_name.upper()) + ' ' + str(_id.stock_receipt_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align='right')),
        TR(TD('Approved by: '),TD(_appr))])
    table=str(XML(i,sanitize=False))
    return table

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_form():   
    row = []
    _total_amount = _amount = 0
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary' )
    # print '--- now ---', request.now
    for n in db(db.Stock_Request.created_by == auth.user_id).select(orderby = ~db.Stock_Request.id):
        # for tnx in db((db.Stock_Request_Transaction.stock_request_id == int(n.id)) & (db.Stock_Request_Transaction.delete == False)).select():
        #     _total_amount = int(tnx.quantity) * float(tnx.price_cost)
        #     print 'id: ', tnx.id, tnx.stock_request_id, tnx.quantity, tnx.price_cost
        # _amount += _total_amount
        # print 'total_amount: ', _total_amount, _amount
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(_stock_request),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    # table = TABLE(*[head, body], _class='table_class', _id='table_id',**{'_data-toggle':'table', '_data-classes':'table table-striped',  '_data-search':'true', '_data-show-pagination-switch':'true','_data-pagination':'true'})
    table = TABLE(*[head, body], _class='table_class', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def get_stock_request_grid():
    row = []
    thead = THEAD(TR(TH('Date'),TH('Stock Requet No.'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-primary'))
    for n in db().select(orderby = ~db.Stock_Request.id):
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id), _target="blank")
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align ='right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[thead, body], _class='table')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_del():
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first()
    _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first()

    _stk_src = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
    _stk_des = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first()
    _stk_src.stock_in_transit += _id.quantity
    _stk_des.stock_in_transit -= _id.quantity
    _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
    _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
    _stk_src.update_record()
    _stk_des.update_record()
    # update the stock file table        
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)    
    # _sr.update_record(total_amount)
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblIC').get(0).reload()"
    
    
def validate_stock_in_transit(form):
    
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first() # from stock request transaction table
    _im = db(db.Item_Master.id == _id.item_code_id).select().first() # Item master table
    _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first() # from stock request  table
    _sf = db(db.Stock_File.item_code_id == _id.item_code_id).select().first() # from stock file table

    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    
    if _qty >= _sf.closing_stock:        
        form.errors.quantity = 'Total quantity should not be more than the stock file. '

    form.vars.quantity = _qty
    _old_stock_in_transit = _sf.stock_in_transit - _id.quantity
    _old_probational_balance = _sf.closing_stock - _old_stock_in_transit
    _sf.update_record(stock_in_transit = _old_stock_in_transit)

def stk_req__trans_edit_form():
    _total = 0
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first()
    
    _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first()
    
    _sf = db(db.Stock_File.item_code_id == _id.item_code_id).select().first()
    _it = db(db.Item_Master.id == _id.item_code_id).select().first()

    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom    
    _tot_amt = _id.quantity * _id.price_cost

    form = SQLFORM.factory(    
        Field('quantity','integer', default = _qty),
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = validate_stock_in_transit).accepted:
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id)
        for n in db((db.Stock_Request_Transaction.stock_request_id == _id.stock_request_id) & (db.Stock_Request_Transaction.delete == False)).select():
            _total += int(n.quantity) * float(n.price_cost)
        _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first()
        _new_stock_in_transit = _sf.stock_in_transit + _qty
        _sr.update_record(total_amount = _total)
        _sf.update_record(stock_in_transit = _new_stock_in_transit)
        session.flash = 'RECORD UPDATED'
        redirect(URL('stk_req_details_form', args = _sr.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('stk_req_details_form', args = _sr.id))
    return dict(form = form, _id = _id, _it = _it, _tot_amt = _tot_amt, btn_back = btn_back)

# --------- ACCOUNT USERS  ---------
@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def account_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-danger' ))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        
        
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        if not n.stock_receipt_no_id:
            _receipt = 'None'
        else:
            _receipt = str(n.stock_receipt_no_id.prefix) +''+ str(n.stock_receipt_no)

        if not n.stock_transfer_no_id:
            _transfer = 'None'
        else:
            _transfer = str(n.stock_transfer_no_id.prefix) +''+ str(n.stock_transfer_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_transfer),
            TD(_receipt),    
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

def corrections_grid():
    head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-danger'))
    for n in db((db.Stock_Corrections.created_by == auth.user.id) & (db.Stock_Corrections.archive != True)).select(orderby = ~db.Stock_Corrections.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_view', args = n.id, extension = False))        
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False))                            
        btn_lnk = DIV(view_lnk, clea_lnk)
        row.append(TR(         
            TD(n.stock_corrections_date),
            TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.adjustment_type.description),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tmptbl')                
    return dict(table = table) 
# STORE KEEPER
@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def str_kpr_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-danger' ))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        
        # view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
        
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        if not n.stock_receipt_no_id:
            _receipt = 'None'
        else:
            _receipt = str(n.stock_receipt_no_id.prefix) +''+ str(n.stock_receipt_no)

        if not n.stock_transfer_no_id:
            _transfer = 'None'
        else:
            _transfer = str(n.stock_transfer_no_id.prefix) +''+ str(n.stock_transfer_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),

            TD(A(_transfer, _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': approved_by(n.id)})),
            TD(_receipt),    
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() ,' ', n.created_by.last_name.upper()),            
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

def approved_by(x = request.args(0)):
    for x in db(db.Stock_Request.id == x).select():
        t = TABLE(*[
            TR(TD('Approved By: '),TD(x.stock_transfer_approved_by))
        ])
    table = str(XML(t, sanitize = False))
    return table

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_request_grid():    
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _query = db((db.Stock_Request.srn_status_id == 4) | (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id)
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _query = db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id)
    elif auth.has_membership(role = 'POS'):
        _query = db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id)
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-danger' ))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:
            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        
        
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        if not n.stock_receipt_no_id:
            _receipt = 'None'
        else:
            _receipt = str(n.stock_receipt_no_id.prefix) +''+ str(n.stock_receipt_no)

        if not n.stock_transfer_no_id:
            _transfer = 'None'
        else:
            _transfer = str(n.stock_transfer_no_id.prefix) +''+ str(n.stock_transfer_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_transfer),
            TD(_receipt),    
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)
    
def store_keeper_stock_request():
    row = []
    head = THEAD(TR(TH('Date'),('Stock Request No'),('Stock Source'),('Stock Destination'),('Requested By'),('Amount'),('Status'),('Required Action'),('Actions')))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:
            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(n.total_amount),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid_details():
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.stock_due_date.writable = False        
    db.Stock_Request.dept_code_id.writable = False    
    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    # db.Stock_Request.srn_status_id.writable = False

    db.Stock_Request.stock_request_date_approved.writable = False
    
    # db.Stock_Request.src_status_id.writable = False
    # db.Stock_Request.item_status_code_id.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) |(db.Stock_Status.id == 2) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
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


def validate_stock_transfer(form):
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if _id.srn_status_id == 2:
        str_kpr_grid_gen_stk_trn()
    else:
        redirect(URL('inventory','str_kpr_grid_details', args = _id.id))

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid_gen_stk_trn():    
    # print request.vars._id
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


# ----------------------------------------------------------------------------
# ------------    S T O C K  R E Q U E S T  A P P R O V A L    ---------------
# ----------------------------------------------------------------------------
@auth.requires_login()
def stock_request_approved():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _id.update_record(srn_status_id = 2, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id)
        session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' APPROVED'
        response.js = "$('#tblsr').get(0).reload()"

# ----------------------------------------------------------------------------
# ------------    S T O C K  R E Q U E S T  R E J E C T E D    ---------------
# ----------------------------------------------------------------------------
@auth.requires_login()
def stock_request_rejected():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _id.update_record(srn_status_id = 3, updated_by = auth.user_id, updated_on = request.now)
        session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' REJECTED'
        response.js = "$('#tblsr').get(0).reload()"

@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_req_grid():

    return dict()

@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_btn_aprvd():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(srn_status_id = 2, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id, remarks ='')
    session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' APPROVED'
    response.js = "$('#tblsr').get(0).reload()"
    
@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))    
def mngr_btn_reject():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(srn_status_id = 3, updated_by = auth.user_id, updated_on = request.now)
    session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' REJECTED'
    response.js = "$('#tblsr').get(0).reload()"

@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_btn_archive():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(archive = True, updated_by = auth.user_id, updated_on = request.now )
    session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' ARCHIVED'
    response.js = "$('#tblsr').get(0).reload()"


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
    db.Stock_Request.srn_status_id.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 2) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.auth_user.id.represent = lambda auth_id, row: row.first_name + ' ' + row.last_name
    # db.auth_user._format = '%(first_name)s %(last_name)s'
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process(onvalidation = mngr_aprvd).accepted:
        # session.flash = 'APPROVED'        
        redirect(URL('inventory', 'mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1            
        grand_total += int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Item_Prices.retail_price, _align='right'),
            TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
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
    thead = THEAD(TR(TH('Date'),TH('Stock Transfer No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')))
    for n in db(db.Stock_Request.srn_status_id == 5).select(orderby = ~db.Stock_Request.id):
        ctr += 1
        _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
        _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.stock_transfer_date_approved),TD(_stock_transfer),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.total_amount),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table',**{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})        
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
    db.Stock_Request.stock_source_id.writable = False
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    # db.Stock_Request.requested_by.writable = False
    db.Stock_Request.srn_status_id.writable = False
    db.Stock_Request.stock_request_approved_by.writable = False
 
    db.Stock_Request.stock_request_no.writable = False
    db.Stock_Request.stock_request_date.writable = False
    db.Stock_Request.stock_request_approved_by.writable = False
    # db.Stock_Request.src_status.writable = False

    form = SQLFORM(db.Stock_Request)
    if form.process(onvalidation = stk_tns_val_form).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

# ---- Stock Receipt Master   -----
def stk_rcpt_form():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')))
    for n in db(db.Stock_Request.srn_status_id == 6).select(orderby = ~db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        row.append(TR(TD(n.stock_receipt_date_approved),TD(_stock_receipt),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.total_amount),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toggle':'table','_data-classes':'table table-striped','_data-pagination':'true','_data-search':'true'})
    return dict(table = table)

# ---- Stock Adjustment Begin   -----    

def adjustment_type():
    form = SQLFORM(db.Adjustment_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Action')))
    for n in db(db.Adjustment_Type).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('adjustment_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)        

def adjustment_type_edit_form():
    form = SQLFORM(db.Adjustment_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

# ---- Stocks Type   -----    
def stock_type():
    form = SQLFORM(db.Stock_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Action')))
    for n in db(db.Stock_Type).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)        

def stock_type_edit_form():
    form = SQLFORM(db.Stock_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form)

def stock_adjustment_session():
    # print request.vars.dept_code_id, request.vars.location_code_id
    session.dept_code_id = request.vars.dept_code_id
    session.adjustment_type = request.vars.adjustment_type
    session.location_code_id = request.vars.location_code_id


@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_form_validation(form):    
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'ADJ')).select().first()
    _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1   
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)    
    form.vars.stock_adjustment_no_id = _trns_pfx.id
    form.vars.stock_adjustment_no = int(_skey)
    form.vars.stock_adjustment_code = _loc_code.stock_adjustment_code

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_add_new():        
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    db.Stock_Adjustment.srn_status_id.default = 4  
    form = SQLFORM(db.Stock_Adjustment)
    if form.process(onvalidation = stock_adjustment_form_validation).accepted:          
        
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'ADJ')).select().first()
        response.flash = 'RECORD SAVE. ' + str(_trns_pfx.current_year_serial_key)
        _id = db(db.Stock_Adjustment.stock_adjustment_no == int(_trns_pfx.current_year_serial_key)).select().first()     
        _total_cost = 0        
        _tmp = db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(db.Stock_Adjustment_Transaction_Temp.ALL).first()
        
        for i in db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(db.Stock_Adjustment_Transaction_Temp.ALL):         
            _itm_code = db(db.Item_Master.id == i.item_code_id).select().first()
            _itm_price = db(db.Item_Prices.item_code_id == i.item_code_id).select().first()            
            _qty = i.quantity * _itm_code.uom_value + i.pieces # converted to pcs.                     
            _price_cost = i.average_cost /_itm_code.uom_value # price_cost per pcs.
            _total_cost += _price_cost * _qty # total cost per line
            db.Stock_Adjustment_Transaction.insert(stock_adjustment_no_id = _id.id, item_code_id = i.item_code_id, stock_adjustment_date = request.now, category_id = i.category_id,
                quantity = i.total_quantity, uom = i.uom, price_cost = _price_cost, wholesale_price = _itm_price.wholesale_price, retail_price = _itm_price.retail_price,
                vansale_price = _itm_price.vansale_price, average_cost = i.average_cost)                  
        _id.update_record(total_amount = _total_cost)       
        db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).delete()     
        redirect(URL('stock_adjustment_browse'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')   
    db.Stock_Adjustment_Transaction_Temp.category_id.default = 4
    return dict(form = form, ticket_no_id = ticket_no_id)


@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def validate_adjustment_item_code(form):
    
    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()
    
    if not _id:        
        form.errors.item_code = CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' does not exist or empty.',_class='alert alert-danger',_role='alert'))
            
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' is zero in stock file.',_class='alert alert-danger',_role='alert'))
        # form.errors.item_code = 'Item code is zero in stock file.'

    else:        
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()                
        _exist = db((db.Stock_Adjustment_Transaction_Temp.item_code == request.vars.item_code) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == session.ticket_no_id) & (db.Stock_Adjustment_Transaction_Temp.category_id == request.vars.category_id)).select().first()    
        _adj = session.adjustment_type
        # print 'adjustment type ', _adj
        if _exist:
            form.errors.item_code = CENTER(DIV('The same item code ',B(str(request.vars.item_code)), ' already added on the grid.',_class='alert alert-danger',_role='alert'))
        
        if _id.uom_value == 1:        
            form.vars.pieces = 0
        
        _ip = db(db.Item_Prices.item_code_id == _id.id).select().first()    
        _tq = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces)
        # float("737,280,000".replace(',',''))

        if (request.vars.average_cost).strip():            
            _average_cost = float(request.vars.average_cost.replace(',',''))            
        else:            
            form.errors.average_cost = CENTER(DIV('Zero price not accepted.',_class='alert alert-danger',_role='alert'))            
            _average_cost = 0
        _pu = _average_cost / int(_id.uom_value)
        
        _tc = float(_pu) * int(_tq)

        if int(_adj) == int(2):                
            if _tq > _sf.closing_stock:
                form.errors.quantity = CENTER(DIV('Quantity should not exceed the closing stock ' + str(_sf.closing_stock),_class='alert alert-danger',_role='alert'))
        if _tq == 0:
            form.errors.quantity = CENTER(DIV('Zero quantity not accepted.',_class='alert alert-danger',_role='alert'))
            response.js = "$('#no_table_item_code').val('');"    

        form.vars.total_quantity = _tq
        form.vars.total_cost = _tc
        form.vars.item_code_id = _id.id    
        form.vars.uom = _id.uom_value
        form.vars.average_cost = _average_cost #float(request.vars.average_cost.replace(',',''))

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjutment_transaction_temporary_table():        
    ctr = 0
    row = []
    _total_amount = 0
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 15),    
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('average_cost','decimal(10,4)', default = 0),
        Field('category_id','reference Transaction_Item_Category', default  = 4,requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_adjustment_item_code).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'        
        db.Stock_Adjustment_Transaction_Temp.insert(item_code_id = form.vars.item_code_id,item_code = form.vars.item_code,quantity = form.vars.quantity,pieces = form.vars.pieces,
        category_id = form.vars.category_id,ticket_no_id = session.ticket_no_id,average_cost = form.vars.average_cost,uom = form.vars.uom,total_quantity = form.vars.total_quantity,
        total_cost = form.vars.total_cost)
        if db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled')"
    elif form.errors:
        # table = TABLE(*[TR(v) for k, v in form.errors.items()])
        response.flash = 'FORM HAS ERROR'
                 
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Average Cost'),TH('Total Cost'),TH('Action')))
    for i in db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == session.ticket_no_id).select(db.Stock_Adjustment_Transaction_Temp.ALL, db.Item_Master.ALL, left = db.Item_Master.on(db.Item_Master.item_code == db.Stock_Adjustment_Transaction_Temp.item_code)):         
        ctr += 1       
        _total_amount += i.Stock_Adjustment_Transaction_Temp.total_cost 
        save_lnk = A(I(_class='fas fa-save'), _title='Save Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', _id='del', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(i.Stock_Adjustment_Transaction_Temp.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Stock_Adjustment_Transaction_Temp.category_id.mnemonic),
            TD(i.Stock_Adjustment_Transaction_Temp.uom),
            TD(i.Stock_Adjustment_Transaction_Temp.quantity),
            TD(i.Stock_Adjustment_Transaction_Temp.pieces),
            TD(locale.format('%.2F', i.Stock_Adjustment_Transaction_Temp.average_cost or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.2F',i.Stock_Adjustment_Transaction_Temp.total_cost or 0, grouping = True), _align = 'right'), 
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2f', _total_amount or 0, grouping = True), _align = 'right'),TD())))
    table = TABLE(*[head, body, foot],  _class='table', _id = 'tmptbl')                
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_delete():    
    db(db.Stock_Adjustment_Transaction_Temp.id == request.args(0)).delete()    
    response.js =  "$('#tmptbl').get(0).reload()"

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ACCOUNT MANAGER')| auth.has_membership('ROOT'))
def stock_adjustment_browse():
    row = []
    ctr = 0
    if auth.has_membership(role = 'ACCOUNT USERS'): # MANOJ        
        _query = db(db.Stock_Adjustment.created_by == auth.user_id).select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    elif auth.has_membership(role = 'ACCOUNT MANAGER'): # JYOTHI
        _query = db(db.Stock_Adjustment.srn_status_id == 2).select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    elif auth.has_membership(role = 'ROOT'): # ADMIN
        _query = db().select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    head = THEAD(TR(TH('Date'),TH('Adjustment No'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Action')),_class='bg-primary')
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.stock_adjustment_date),TD(n.stock_adjustment_no_id.prefix,n.stock_adjustment_no),TD(n.dept_code_id.dept_name),TD(n.location_code_id.location_name),TD(n.adjustment_type.description),TD(n.total_amount),TD(n.srn_status_id.description),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_form():
    ctr_val = "ADJ18100000"  # temporary autogenerated
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')       
    db.Stock_Adjustment.srn_status_id.default = 4    
    form = SQLFORM(db.Stock_Adjustment)    
    if form.process(onvalidation = stock_adjustment_form_validation).accepted:            
        response.flash = 'save'
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'ADJ')).select().first()
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
    _unt = float(request.vars.average_cost) / int(_itm_code.uom_value)
    _total_cost = float(_unt) * int(_qty)
    form.vars.total_cost = float(_total_cost)    
    if _qty > _stk_fil.closing_stock:
        form.errors._qty = 'quantity should not exceed the closing stock'
    if _id:
        form.errors._id = 'already exists!'       
    if _uom.uom_value == 1:
        form.vars.pieces = 0
    form.vars.stock_adjustment_date = request.now
    form.vars.ticket_no_id = request.vars.ticket_no_id
    
    # if form.vars.average_cost == float(0.0):
    
    #     itm_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    
    #     form.vars.average_cost = itm_price.average_cost

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_no():        
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _disabled = True)        
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_code():        
    _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    if not _loc_code:
        return XML(INPUT(_class="integer form-control", _name='location_code', _disabled = True))    
    else:
        return XML(INPUT(_class="integer form-control", _name='location_code', _value=_loc_code.stock_adjustment_code, _disabled = True))

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_average_cost():          
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:
        return XML(INPUT(_class="form-control", _name='average_cost', _id='average_cost', _value='0.0'))                
    else:
        _item_price = db(db.Item_Prices.item_code_id == _id.id).select().first()        
        if _item_price:
            return XML(INPUT(_class="form-control", _name='average_cost', _id='average_cost', _value=locale.format('%.4F',_item_price.average_cost or 0, grouping = True)))                
    
@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ROOT'))
def stock_adjustment_description():        
    response.js = "$('#add').removeAttr('disabled')"
    response.js = "$('#no_table_pieces').removeAttr('disabled')"
    _item_code = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == request.vars.dept_code_id)).select().first()
    if not _item_code:
        response.js = "$('#add').attr('disabled','disabled')"
        return CENTER(DIV("Item code no " , B(str(request.vars.item_code)), " doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))
    else:
        response.js = "$('#add').removeAttr('disabled')"
        
        # if int(request.vars.adjustment_type) == 2:                
        _item_price = db(db.Item_Prices.item_code_id == _item_code.id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == _item_code.id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()        
        
        if _stk_file:
            if _item_code.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_balance = _stk_file.probational_balance
                _on_transit = _stk_file.stock_in_transit
                _on_hand = _stk_file.closing_stock
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"
                # if _item_code and _item_price and _stl_file:
                _outer = int(_stk_file.probational_balance) / int(_item_code.uom_value)        
                _pcs = int(_stk_file.probational_balance) - int(_outer * _item_code.uom_value)    
                _on_balance = str(_outer) + ' ' + str(_pcs) + '/' +str(_item_code.uom_value)

                _outer_transit = int(_stk_file.stock_in_transit) / int(_item_code.uom_value)   
                _pcs_transit = int(_stk_file.stock_in_transit) - int(_outer * _item_code.uom_value)
                _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_item_code.uom_value)

                _outer_on_hand = int(_stk_file.closing_stock) / int(_item_code.uom_value)
                _pcs_on_hand = int(_stk_file.closing_stock) - int(_outer_on_hand * _item_code.uom_value) 
                _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_item_code.uom_value)
            

            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock')),_class="bg-active"),
            TBODY(TR(TD(_item_code.item_code),TD(_item_code.item_description.upper()),TD(_item_code.group_line_id.group_line_name),TD(_item_code.brand_line_code_id.brand_line_name),TD(_item_code.uom_value),
                TD(_item_price.retail_price),TD(_on_hand)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))                    
          
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
        _total_cost = 0
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Average Cost'),TH('Total Cost'),TH('Action')))  
        for i in db((db.Stock_Adjustment_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.ALL, db.Item_Master.ALL, db.Item_Prices.ALL,
        left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction_Temp.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Adjustment_Transaction_Temp.item_code_id)]):
            ctr += 1       
                     
            # _itm_code = db(db.Item_Master.id == i.Stock_Adjustment_Transaction_Temp.item_code_id).select().first()
            # # _itm_pric = db(db.Item_Prices.item_code_id == i.Stock_Adjustment_Transaction_Temp.item_code_id).select().first()
            # _qty = (i.Stock_Adjustment_Transaction_Temp.quantity) * int(_itm_code.uom_value) + int(i.Stock_Adjustment_Transaction_Temp.pieces)
            # _unt = float(request.vars.average_cost) / int(_itm_code.uom_value)
            
            # _total_cost = float(_unt) * int(_qty)
            _total_amount += i.Stock_Adjustment_Transaction_Temp.total_cost 
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
            TD(locale.format('%.2F',i.Stock_Adjustment_Transaction_Temp.total_cost or 0, grouping = True), _align = 'right'), TD(btn_lnk)))
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


    # response.js = web2py_component('{{=URL("inventory","stock_adjustment_table.load")}}', 'tab');

def stock_adjustment_manager_details():
    
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
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
    
    if _stk_adj.srn_status_id == int(4):
        _btn_approved = A('approved', _type='submit', _class="btn btn-success", _role= 'button ', _id = 'btn', callback = URL('inventory','stock_adjustment_manager_details_approved', args = request.args(0)))
        _btn_reject = A('reject', _type='button', _class="btn btn-danger", _role = 'button ', _id = 'btn', callback = URL('inventory','stock_adjustment_manager_details_reject', args = request.args(0)))
    else:
        _btn_approved = A('approved', _type='submit', _class="btn btn-success disabled", _role= 'button ')
        _btn_reject = A('reject', _type='button', _class="btn btn-danger disabled", _role = 'button ')

    return dict(form = form, table = table, _stk_adj = _stk_adj, _btn_approved = _btn_approved, _btn_reject = _btn_reject)

@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def stock_adjustment_manager_details_approved():    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()            
    _stk_adj.update_record(srn_status_id = 2, approved_by = auth.user_id, date_approved = request.now)    
    _clo_stk = 0   
    for s in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(db.Stock_Adjustment_Transaction.ALL):                  
        _stk_file = db((db.Stock_File.item_code_id == s.item_code_id) & (db.Stock_File.location_code_id == _stk_adj.location_code_id)).select().first()
        if not _stk_file:        
            if _stk_adj.adjustment_type == 1:            
                db.Stock_File.insert(item_code_id = s.item_code_id,location_code_id = _stk_adj.location_code_id,closing_stock = s.quantity, last_transfer_date = request.now)            
                # _trans_type = 7            
            else:
                response.flash = 'error'
        elif _stk_adj.adjustment_type == 1:
            _clo_stk = _stk_file.closing_stock + s.quantity
            _stk_file.update_record(closing_stock = _clo_stk,last_transfer_date = request.now)
        else:
            _clo_stk = _stk_file.closing_stock - s.quantity
            _stk_file.update_record(closing_stock = _clo_stk,last_transfer_date = request.now)
    response.flash = 'STOCK ADJUSTMENT APPROVED'        
    response.js = "$('#tbladj').get(0).reload()"
            # elif (_stk_adj.adjustment_type == 2) and _stk_file:                    
            #     _clo_stk = _stk_file.closing_stock - s.quantity 
            #     # _trans_type = 8            
            # _stk_file.update_record(closing_stock = _clo_stk)

        # db.Merch_Stock_Transaction.insert(
        #     voucher_no = '%s%s' % (_stk_adj.stock_adjustment_no_id.prefix,_stk_adj.stock_adjustment_no),
        #     location_code = '%s' % (_stk_adj.location_code_id.location_name),
        #     transaction_type = _trans_type,
        #     transaction_date = request.now,
        #     account = '%s' % (_stk_adj.location_code_id.stock_adjustment_code),
        #     item_code = '%s' % (s.item_code_id.item_code), # price cost = sales cost
        #     uom = s.uom,
        #     quantity = s.quantity,
        #     price_cost = s.price_cost,            
        #     average_cost = s.average_cost,            
        #     whole_sale_price = s.wholesale_price,
        #     retail_price = s.retail_price,
        #     vansale_price = s.vansale_price,
        #     dept_code = '%s' % (_stk_adj.dept_code_id.dept_name)
        # )
    
@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def stock_adjustment_manager_details_reject():
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    _stk_adj.update_record(srn_status_id = 3)
    response.flash = 'STOCK ADJUSTMENT REJECTED'     
    response.js = "$('#tbladj').get(0).reload()"
    
def stock_adjustment_browse_details():   
    db.Stock_Adjustment.stock_adjustment_no_id.writable = False
    db.Stock_Adjustment.stock_adjustment_no.writable = False
    db.Stock_Adjustment.stock_adjustment_date.writable = False
    db.Stock_Adjustment.stock_adjustment_code.writable = False
    db.Stock_Adjustment.dept_code_id.writable = False
    db.Stock_Adjustment.location_code_id.writable = False
    db.Stock_Adjustment.adjustment_type.writable = False
    db.Stock_Adjustment.total_amount.writable = False
    db.Stock_Adjustment.approved_by.writable = False
    db.Stock_Adjustment.date_approved.writable = False
    db.Stock_Adjustment.archive.writable = False
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()     
    if _stk_adj.srn_status_id == 2:
        db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 2), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    elif _stk_adj.srn_status_id == 3:
        db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORDS UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'         
    return dict(form = form, _stk_adj = _stk_adj)


def stock_adjustment_browse_details_transaction():
    row = []
    ctr = 0
    _total_amount = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Average Cost'),TH('Total Cost'),TH('Action')))  
    for i in db((db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)) & (db.Stock_Adjustment_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Adjustment_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        ctr += 1                        
        _total_amount += int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.average_cost) / int(i.Stock_Adjustment_Transaction.uom)
        _apprvd = db(db.Stock_Adjustment.id == i.Stock_Adjustment_Transaction.stock_adjustment_no_id).select(db.Stock_Adjustment.ALL).first()
        if _apprvd.srn_status_id == 2:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('stock_adjustment_browse_details_edit', args = i.Stock_Adjustment_Transaction.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _id = 'del',callback = URL('stock_adjustment_browse_details_delete', args = i.Stock_Adjustment_Transaction.id))
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
    return dict(table = table)

def stock_adjustment_browse_details_delete():    
    _stk_adj_tran = db(db.Stock_Adjustment_Transaction.id == request.args(0)).select().first()
    _stk_adj = db(db.Stock_Adjustment.id == _stk_adj_tran.stock_adjustment_no_id).select().first()
    db(db.Stock_Adjustment_Transaction.id == request.args(0)).update(delete = True)
    _total_amount = 0       
    for i in db((db.Stock_Adjustment_Transaction.stock_adjustment_no_id == _stk_adj.id) & (db.Stock_Adjustment_Transaction.delete == False)).select():
        _total_amount += int(i.quantity) * float(i.average_cost) / int(i.uom)    
    _stk_adj.update_record(total_amount = _total_amount)
    response.js = '$("#dettbl").get(0).reload()'

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
    
        session.flash = 'RECORD UPDATED'

        _qty = int(int(request.vars.quantity) * int(_stk_adj_tran.uom)) + int(request.vars.pieces)        
        
        _stk_adj_tran.update_record(quantity = int(_qty))

        for i in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == _stk_adj_tran.stock_adjustment_no_id).select():

            _total_amount += int(i.quantity) * float(i.average_cost) / int(i.uom)
        
        _stk_adj = db(db.Stock_Adjustment.id == _stk_adj_tran.stock_adjustment_no_id).select().first()
        
        _stk_adj.update_record(total_amount = _total_amount)

        redirect(URL('stock_adjustment_browse_details', args = (_stk_adj.id)))

    elif form.errors:

        response.flash = 'FORM HAS ERRORS'

    return dict(form = form, _stk_adj_tran = _stk_adj_tran, _itm_cod = _itm_cod)

@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def account_manager_workflow():
    return dict()

@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT') | auth.has_membership('INVENTORY'))
def stock_adjustment_manager_grid():
    row = []        
    head = THEAD(TR(TH('Date'),TH('Stock Adjustment No'),TH('Department'),TH('Location'),TH('Amount'),TH('Adjustment Type'),TH('Requested By'),TH('Status'),TH('Action'), _class='bg-primary'))  
    for i in db((db.Stock_Adjustment.archive == False) & (db.Stock_Adjustment.srn_status_id == 4)).select(orderby = ~db.Stock_Adjustment.id):
        edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('stock_adjustment_manager_details', args = i.id, extension = False))
        appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        if i.srn_status_id == 2:
            appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
            reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', _id = 'del', callback = URL('stk_req_del', args = i.id, extension = False))            
        elif i.srn_status_id == 3:
            reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        else:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('stock_adjustment_manager_details_approved', args = i.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('stock_adjustment_manager_details_reject', args = i.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        
        btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, clea_lnk)        
        row.append(TR(
            TD(i.stock_adjustment_date),
            TD(i.stock_adjustment_no_id.prefix,i.stock_adjustment_no),
            TD(i.dept_code_id.dept_name),
            TD(i.location_code_id.location_name),
            TD(locale.format('%.2F', i.total_amount or 0, grouping = True), _align = 'right'),
            TD(i.adjustment_type.description),
            TD(i.created_by.first_name.upper(),' ',i.created_by.last_name.upper()),
            TD(i.srn_status_id.description),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id='tbladj')    
    return dict(table = table)
   
# -----------   ADJUSTMENT STOCKS     -----------------

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
# ---- C A R D Function  -----

def card_view(item_code_id, stock):
    _stock = _pieces = 0
    _item = db(db.Item_Master.id == item_code_id).select().first()
    if not stock:
        stock = 0
        return stock
    else:
        x = int(stock)
        u = int(_item.uom_value)
        if int(stock) < 0:            
            # print 'abs', abs(x) / u
            _stock = 0 - abs(x) / u
        else:
            # print 'no abs', x / u
            _stock = x / u
        _pieces = abs(x) - (abs(_stock) * u)
        # return str(int(_stock)) + ' - ' + str(int(stock) - int(stock) / int(_item.uom_value) * int(_item.uom_value))  + '/' + str(int(_item.uom_value))        
        return str(int(_stock)) + ' - ' + str(_pieces)  + '/' + str(int(_item.uom_value))        

def inventory_manager():
    return dict()

@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('INVENTORY') | auth.has_membership('ROOT'))
def stock_request_manager_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary')
    for n in db((db.Stock_Request.srn_status_id == 4) & (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id):
        edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('mngr_req_details', args = n.id, extension = False))        
        if n.srn_status_id == 2:
            appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
            reje_lnk = A(I(_class='fas fa-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('mngr_btn_archive', args = n.id, extension = False))            
        else:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_request_rejected', args = n.id, extension = False))
            # clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                    
        btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk)        
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id = 'tblsr', **{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    return dict(table = table)


@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def stock_request_tool():    
    head = THEAD(TR(TH('Date'),TH('Stock Src.'),TH('Stock Des.'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Focal Person'),TH('Action')), _class='thead-light')
    for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        redo_lnk = A(I(_class='fas fa-redo'), _title='Redo Row', _type='button ', _role='button',_id='redo', _class='btn btn-icon-toggle', callback=URL('inventory','stock_request_tool_redo', args = k.Stock_Transaction_Temp.id))
        btn_lnk = DIV(redo_lnk, _class="hidden-sm action-buttons")
        if k.Stock_Transaction_Temp.category_id == None:
            _category = 'None'
        else:
            _category = k.Stock_Transaction_Temp.category_id.description
        row.append(TR(            
            TD(k.Stock_Transaction_Temp.created_on),
            TD(k.Stock_Transaction_Temp.stock_source_id.location_name),
            TD(k.Stock_Transaction_Temp.stock_destination_id.location_name),
            TD(k.Item_Master.item_code),
            TD(k.Item_Master.item_description.upper()),
            TD(_category),
            TD(k.Item_Master.uom_value),
            TD(card(k.Item_Master.id, k.Stock_Transaction_Temp.qty, k.Item_Master.uom_value)),
            TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),            
            TD(k.Stock_Transaction_Temp.remarks),
            TD(k.Stock_Transaction_Temp.created_by.first_name.upper(),' ',k.Stock_Transaction_Temp.created_by.last_name.upper()),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblsrt',_class='table', **{'_data-toggle':'table','_data-search':'true', '_data-show-pagination-switch':'true','_data-pagination':'true'})
    return dict(table = table)
    
@auth.requires(lambda: auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def stock_request_tool_redo():     
    _id = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    if not _id:
        redirect(URL('inventory','stock_request_tool'))        
    else:
        _stk_src = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _stk_des = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _id.stock_destination_id)).select().first()
        _stk_src.stock_in_transit += _id.qty
        _stk_des.stock_in_transit -= _id.qty
        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
        _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
        _stk_src.update_record()
        _stk_des.update_record()
        db(db.Stock_Transaction_Temp.id == request.args(0)).delete()
        session.flash = 'ITEM REDO'


# ---- Stock Adjustment End   -----    
# -----------   OBSOLESCENCE STOCKS     -----------------
@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ACCOUNT MANAGER')| auth.has_membership('ROOT'))
def obsolescence_of_stocks():
    row = []
    head = THEAD(TR(TH('Date'),TH('Obsol. Stocks No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db(db.Obsolescence_Stocks.archives != True).select(orderby = ~db.Obsolescence_Stocks.id):
        if auth.has_membership(role = 'ACCOUNT USERS'):
            if n.status_id == 15:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        elif auth.has_membership(role = 'ACCOUNT MANAGER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))                
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
        # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        # edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
        # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(n.obsolescence_stocks_date),TD(n.transaction_prefix_id.prefix, n.obsolescence_stocks_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(n.total_amount),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table',**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    return dict(table = table)

def obsol_archived():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    _id.update_record(archives = True, update_on = request.now, updated_by = auth.user_id)
    response.flash = 'RECORD ARCHIVED'    

def obsol_of_stocks_view():
    db.Obsolescence_Stocks.obsolescence_stocks_date.writable = False
    db.Obsolescence_Stocks.dept_code_id.writable = False
    db.Obsolescence_Stocks.stock_type_id.writable = False
    db.Obsolescence_Stocks.location_code_id.writable = False
    db.Obsolescence_Stocks.account_code_id.writable = False
    db.Obsolescence_Stocks.total_amount.writable = False
    db.Obsolescence_Stocks.total_amount_after_discount.writable = False
    db.Obsolescence_Stocks.total_selective_tax.writable = False
    db.Obsolescence_Stocks.total_selective_tax_foc.writable = False
    db.Obsolescence_Stocks.total_vat_amount.writable = False
    db.Obsolescence_Stocks.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    form = SQLFORM(db.Obsolescence_Stocks, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price/Sel.Tax'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-danger'))
    _query = db((db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)) & (db.Obsolescence_Stocks_Transaction.delete == False)).select(db.Item_Master.ALL, db.Obsolescence_Stocks_Transaction.ALL, db.Item_Prices.ALL, orderby = ~db.Obsolescence_Stocks_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Obsolescence_Stocks_Transaction.item_code_id)])
    for n in _query:
        ctr += 1      
        if _id.status_id == 15:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', _href=URL('inventory','obsol_of_stocks_edit_view', args = n.Obsolescence_Stocks_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Obsolescence_Stocks_Transaction.id, extension = False), **{'_data-id':(n.Obsolescence_Stocks_Transaction.id)})
        btn_lnk = DIV( edit_lnk, dele_lnk)
        _selective_tax += n.Obsolescence_Stocks_Transaction.selective_tax
        _selective_tax_foc += n.Obsolescence_Stocks_Transaction.selective_tax_foc
        if _selective_tax > 0.0 or _selective_tax_foc > 0.0:            
            _div_tax = DIV(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('REMARKS: TOTAL SELECTIVE TAX FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True)))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')
        grand_total += n.Obsolescence_Stocks_Transaction.total_amount                
        row.append(TR(
            TD(ctr),
            TD(n.Obsolescence_Stocks_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Obsolescence_Stocks_Transaction.category_id.mnemonic),
            TD(n.Item_Master.uom_value),
            TD(card(n.Obsolescence_Stocks_Transaction.item_code_id, n.Obsolescence_Stocks_Transaction.quantity, n.Obsolescence_Stocks_Transaction.uom)),
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),             
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction.net_price or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(_div_tax_foc, _colspan= '2'),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2F',grand_total or 0, grouping = True)), _align = 'right'),TD()))    
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblSOT')    
    return dict(form = form, table = table, _id = _id)
    
def validate_obsol_of_stocks_edit_view(form):
    _id = db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).select().first()
    _os = db(db.Obsolescence_Stocks.id == _id.obsolescence_stocks_no_id).select().first()
    _sf = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _os.location_code_id)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)    
    if _sf.damaged_stock_qty == None:
        form.errors.quantity = 'Damaged stock is empty.'
    if _qty > _sf.damaged_stock_qty:        
        form.errors.quantity = 'Quantity exceeded the value in damaged stock.'
    form.vars.quantity = _qty

def obsol_of_stocks_edit_view():
    _id = db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).select().first()
    _os = db(db.Obsolescence_Stocks.id == _id.obsolescence_stocks_no_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom
    _total = 0
    form = SQLFORM.factory(
        Field('quantity', 'integer', default = _qty),
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = validate_obsol_of_stocks_edit_view).accepted:
        _price_per_piece = _id.net_price / _id.uom
        _total_amount = form.vars.quantity * _price_per_piece
        _id.update_record(quantity = form.vars.quantity, update_on = request.now, updated_by = auth.user_id, total_amount = _total_amount)
        for n in db((db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == _os.id) & (db.Obsolescence_Stocks_Transaction.delete == False)).select():
            _total += n.total_amount
            _os.update_record(total_amount = _total)
        session.flash = 'RECORD UDPATED'
        redirect(URL('inventory','obsol_of_stocks_view', args = _os.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('inventory','obsol_of_stocks_view', args = _os.id))
    return dict(form = form, btn_back = btn_back)

def obsol_of_stocks_delete_view():
    _id = db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).select().first()
    _os = db(db.Obsolescence_Stocks.id == _id.obsolescence_stocks_no_id).select().first()
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    _total = 0
    for n in db((db.Obsolescence_Stocks_Transaction.id == request.args(0)) & (db.Obsolescence_Stocks_Transaction.delete == False)).select():
        _total += n.total_amount
    _os.update_record(total_amount = _total, updated_on = request.now, updated_by = auth.user_id)
    session.flash = 'RECORD DELETED'

def obsolescence_of_stocks_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    _grand_total = _total_selective_tax = _total_selective_tax_foc = 0
    form = SQLFORM.factory(
        Field('obsolescence_stocks_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('stock_type_id','reference Stock_Type', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Type.id,'%(description)s', zero = 'Choose Stock Type')),
        Field('account_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Account')),    
        Field('remarks', 'string'),
        Field('status_id','reference Stock_Status', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:
        ctr = db((db.Transaction_Prefix.prefix_key == 'SIV') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        db.Obsolescence_Stocks.insert(
            transaction_prefix_id = ctr.id,
            obsolescence_stocks_no = ctr.current_year_serial_key,
            obsolescence_stocks_date = request.now,
            account_code_id = form.vars.account_code_id,
            dept_code_id = form.vars.dept_code_id,
            location_code_id = form.vars.location_code_id,
            stock_type_id =  form.vars.stock_type_id,                        
            remarks = form.vars.remarks,                        
            status_id = form.vars.status_id)
        _id = db(db.Obsolescence_Stocks.obsolescence_stocks_no == ctr.current_year_serial_key).select().first()
        _tmp = db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _tmp:
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()

            db.Obsolescence_Stocks_Transaction.insert(
                obsolescence_stocks_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,
                average_cost = _pric.average_cost,                
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                selective_tax = n.selective_tax,
                selective_tax_foc = n.selective_tax_foc,
                net_price = n.net_price,
                total_amount = n.total_amount)
            _grand_total += n.total_amount
            _total_selective_tax += n.selective_tax or 0
            _total_selective_tax_foc += n.selective_tax_foc or 0
        _id.update_record(
            total_amount = _grand_total,                         
            total_selective_tax = _total_selective_tax, 
            total_selective_tax_foc = _total_selective_tax_foc)        
        db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()                
            
        response.flash = 'SAVING OBSOLESCENCE STOCKS NO ' + str(_skey) + '.'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_obsolescence_stocks_transaction(form):
    _excise_tax_amount = _unit_price = _total_excise_tax = _total_excise_tax_foc = _net_price = _selective_tax = _selective_tax_foc = _total_amount = _total_pcs = 0           
    
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty.'
    
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code = 'Item code is empty in damage location.'
    
    else:
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        _exist = db((db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Obsolescence_Stocks_Transaction_Temporary.item_code == request.vars.item_code)).select(db.Obsolescence_Stocks_Transaction_Temporary.item_code).first()                                   

        if _id.uom_value == 1:
            form.vars.pieces = 0

        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces or 0)
        
        if not _price:
            form.errors.item_code = "Item code does'nt have price."
        
        if (_price.retail_price == 0.0 or _price.wholesale_price == 0.0) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.errors.item_code = 'Cannot request this item because retail price/wholesale price is zero.'
                
        # if _exist == request.vars.item_code and (request.vars.category_id != 3):

        if _exist:
            if int(request.vars.category_id) != 3:                
                form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'                
            else:
                # _unit_price = _excise_tax_amount or 0                                
                # computation for excise tax foc
                _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
                _excise_tax_price_per_piece_foc = _excise_tax_amount / _id.uom_value
                _selective_tax_foc += _excise_tax_price_per_piece_foc * _total_pcs
                _unit_price = float(_price.wholesale_price) + _excise_tax_amount

                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()                    

            # form.errors.item_code = CENTER(DIV(B('DANGER! '),'Item code ' + str(_exist.item_code) + ' already exist.',_class='alert alert-danger',_role='alert'))                    
        else:
            if int(request.vars.category_id) == 3:
                
                # computation for excise tax foc
                _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
                _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
                _selective_tax_foc += _excise_tax_price_per_piece * _total_pcs
                _unit_price = float(_price.wholesale_price) + _excise_tax_amount

                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()    
                
            else:
                _selective_tax_foc = 0
                # computation for excise tax
                _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
                _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
                _selective_tax += _excise_tax_price_per_piece * _total_pcs                
                _unit_price = float(_price.wholesale_price) + _excise_tax_amount
                
                # computation for price per unit
                _net_price = (_unit_price * ( 100 - int(form.vars.discount_percentage or 0))) / 100
                _price_per_piece = _net_price / _id.uom_value
                _total_amount = _total_pcs * _price_per_piece
        
                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()                  
                                                
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(session.stock_type_id) == 1:
            if int(_total_pcs) > int(_stk_file.closing_stock):
                form.errors.quantity = 'Items should not be more than '+ str(_stk_file.closing_stock) + str(' pieces.')

        if int(session.stock_type_id) == 2:
            if int(_total_pcs) > int(_stk_file.damaged_stock_qty):
                form.errors.quantity = 'Items should not be more than ' + str(_stk_file.damaged_stock_qty) + str(' pieces.')

        if int(session.stock_type_id) == 3:
            if int(_total_pcs) > int(_stk_file.free_stock_qty):
                form.errors.quantity = 'Items should not be more than ' + str(_stk_file.free_stock_qty) + str(' pieces.')


        if int(form.vars.pieces) >= int(_id.uom_value):
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                       
                    
        # _unit_price = float(_price.retail_price) / int(_id.uom_value)
        # _total = float(_unit_price) * int(_total_pcs)

        # if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):
        #     form.errors.quantity = 'Quantity should not be more than probational balance.'
        
    form.vars.item_code_id = _id.id
    form.vars.selective_tax = _selective_tax
    form.vars.selective_tax_foc = _selective_tax_foc
    form.vars.total_pieces = _total_pcs
    form.vars.price_cost = _unit_price
    form.vars.total_amount = _total_amount
    form.vars.net_price = _net_price

def obsolescence_stocks_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code','string', length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 1, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) |(db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))        
    if form.process(onvalidation = validate_obsolescence_stocks_transaction).accepted:
        _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        db.Obsolescence_Stocks_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            total_amount = form.vars.total_amount,            
            category_id = form.vars.category_id,
            stock_source_id = session.stock_source_id,
            selective_tax = form.vars.selective_tax,
            selective_tax_foc = form.vars.selective_tax_foc,
            net_price = form.vars.net_price,
            ticket_no_id = session.ticket_no_id)
        
        if db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:            
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:            
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        
        # upon approval by the accounts        
        # _sf.damaged_stock_qty -= form.vars.total_pieces            
        # _sf.update_record()  
        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'

    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price/Sel.Tax'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-danger'))
    _query = db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Obsolescence_Stocks_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = ~db.Obsolescence_Stocks_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Obsolescence_Stocks_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1      
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Obsolescence_Stocks_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Obsolescence_Stocks_Transaction_Temporary.id),'_data-qt':(n.Obsolescence_Stocks_Transaction_Temporary.quantity), '_data-pc':(n.Obsolescence_Stocks_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Obsolescence_Stocks_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Obsolescence_Stocks_Transaction_Temporary.id)})
        btn_lnk = DIV( dele_lnk)
        _selective_tax += n.Obsolescence_Stocks_Transaction_Temporary.selective_tax
        _selective_tax_foc += n.Obsolescence_Stocks_Transaction_Temporary.selective_tax_foc
        if _selective_tax > 0.0 or _selective_tax_foc > 0.0:            
            _div_tax = DIV(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('REMARKS: TOTAL SELECTIVE TAX FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True)))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')

        grand_total += n.Obsolescence_Stocks_Transaction_Temporary.total_amount
                
        row.append(TR(
            TD(ctr),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.category_id.mnemonic),
            TD(n.Item_Master.uom_value),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.quantity),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.pieces),
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction_Temporary.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),             
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction_Temporary.net_price or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction_Temporary.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(_div_tax_foc+str('\n')+_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(INPUT(_class='form-control', _name = 'grand_total', _id='grand_total', _disabled = True, _value = locale.format('%.2F',grand_total or 0, grouping = True))), _align = 'right'),TD()))
    # foot += TFOOT(TR(TD(),TD(_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT %'), _align = 'right'),TD(H4(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right')),TD(P(_id='error'))))
    table = TABLE(*[head, body, foot], _id = 'tblSOT', _class='table')
    return dict(form = form, table = table, grand = grand_total)    

def del_obsol_stocks():    
    db(db.Obsolescence_Stocks_Transaction_Temporary.id == request.args(0)).delete()
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblSOT').get(0).reload()"
    # response.js = "$('#tblot').get(0).reload()"
    
def generate_obsol_stocks_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SIV')).select().first()   
    if not _trans_prfx:
        return INPUT(_type = 'text', _class = 'form-control', _id = '_obsol_stk_no', _name = '_obsol_stk_no', _disabled = True) 
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _obsol_stk_no = str(_trans_prfx.prefix) + str(_serial)
        return XML(INPUT(_type="text", _class="form-control", _id='_obsol_stk_no', _name='_obsol_stk_no', _value=_obsol_stk_no, _disabled = True))

def obsol_item_description():
    response.js = "$('#btnadd').removeAttr('disabled')"
    response.js = "$('#no_table_pieces').removeAttr('disabled')"   
    response.js = "$('#discount').removeAttr('disabled')"    
    _icode = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()    
    # _icode = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    
    if not _icode:
        response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:        
        response.js = "$('#btnadd').removeAttr('disabled')"
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        
        if _sfile:    
            if int(session.stock_type_id) == 1:                                
                if not int(_sfile.closing_stock):                                        
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in closing stock file. ", _class='alert alert-warning',_role='alert'))           
            elif int(session.stock_type_id) == 2:                
                if not int(_sfile.damaged_stock_qty):# or (int(_sfile.free_stock_qty) == 0):                    
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in damaged stock file. ", _class='alert alert-warning',_role='alert'))           
            elif int(session.stock_type_id) == 3:                
                if not int(_sfile.free_stock_qty):# or (int(_sfile.free_stock_qty) == 0):
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in free stock file. ", _class='alert alert-warning',_role='alert'))           

            if _icode.uom_value == 1:                
                response.js = "$('#no_table_pieces').attr('disabled','disabled'), $('#btnadd').removeAttr('disabled')"                
                _on_hand = _sfile.closing_stock or 0
                _on_free_stk = _sfile.free_stock_qty or 0
                _on_damaged_qty = _sfile.damaged_stock_qty or 0                
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_hand = card(_icode.id, _sfile.closing_stock or 0, _icode.uom_value)
                _on_free_stk = card(_icode.id, _sfile.free_stock_qty or 0, _icode.uom_value)                
                _on_damaged_qty = card(_icode.id, _sfile.damaged_stock_qty or 0, _icode.uom_value)
            
            response.js = "$('#btnadd').removeAttr('disabled')"
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax'),TH('Retail Price'),TH('Unit Price'),TH('On-Normal Qty.'),TH('On-Free Stock Qty.'),TH('On-Damaged Stock Qty.'))),
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
                TD(_on_free_stk),
                TD(_on_damaged_qty)),_class="bg-info"),_class='table'))            
            
        else:            
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

def obsol_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_type_id =  request.vars.stock_type_id
    session.location_code_id = request.vars.location_code_id
    session.stock_source_id = request.vars.location_code_id

def obsol_abort():
    db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).delete()    
    session.flash = 'ABORT'

def obsol_grid():
    row = []
    head = THEAD(TR(TH('Date'),TD('Obsol. Stocks No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-danger'))
    for n in db(db.Obsolescence_Stocks.archives != True).select(orderby = ~db.Obsolescence_Stocks.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_grid_view', args = n.id, extension = False))        
        if n.status_id == 15:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
        else:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        row.append(TR(TD(n.obsolescence_stocks_date),TD(n.transaction_prefix_id.prefix, n.obsolescence_stocks_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(n.total_amount),TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

def obsol_grid_view():
    db.Obsolescence_Stocks.obsolescence_stocks_date.writable = False
    db.Obsolescence_Stocks.dept_code_id.writable = False
    db.Obsolescence_Stocks.stock_type_id.writable = False
    db.Obsolescence_Stocks.location_code_id.writable = False
    db.Obsolescence_Stocks.account_code_id.writable = False
    db.Obsolescence_Stocks.total_amount.writable = False
    db.Obsolescence_Stocks.total_amount_after_discount.writable = False
    db.Obsolescence_Stocks.total_selective_tax.writable = False
    db.Obsolescence_Stocks.total_selective_tax_foc.writable = False
    db.Obsolescence_Stocks.total_vat_amount.writable = False
    db.Obsolescence_Stocks.status_id.writable = False
    # db.Obsolescence_Stocks.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    session.location_code_id = _id.location_code_id
    form = SQLFORM(db.Obsolescence_Stocks, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price/Sel.Tax'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-danger'))
    _query = db((db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)) & (db.Obsolescence_Stocks_Transaction.delete == False)).select(db.Item_Master.ALL, db.Obsolescence_Stocks_Transaction.ALL, db.Item_Prices.ALL, orderby = ~db.Obsolescence_Stocks_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Obsolescence_Stocks_Transaction.item_code_id)])
    for n in _query:
        ctr += 1      
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','obsol_of_stocks_edit_view', args = n.Obsolescence_Stocks_Transaction.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL(args = n.Obsolescence_Stocks_Transaction.id, extension = False), **{'_data-id':(n.Obsolescence_Stocks_Transaction.id)})
        btn_lnk = DIV( edit_lnk, dele_lnk)
        _selective_tax += n.Obsolescence_Stocks_Transaction.selective_tax
        _selective_tax_foc += n.Obsolescence_Stocks_Transaction.selective_tax_foc
        if _selective_tax > 0.0 or _selective_tax_foc > 0.0:            
            _div_tax = DIV(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('REMARKS: TOTAL SELECTIVE TAX FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True)))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')
        grand_total += n.Obsolescence_Stocks_Transaction.total_amount                
        row.append(TR(
            TD(ctr),
            TD(n.Obsolescence_Stocks_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Obsolescence_Stocks_Transaction.category_id.mnemonic),
            TD(n.Item_Master.uom_value),
            TD(card(n.Obsolescence_Stocks_Transaction.item_code_id, n.Obsolescence_Stocks_Transaction.quantity, n.Obsolescence_Stocks_Transaction.uom)),
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),             
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction.net_price or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(_div_tax_foc, _colspan= '2'),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2F',grand_total or 0, grouping = True)), _align = 'right'),TD()))    
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')    
    return dict(form = form, table = table, _id = _id)

def obsol_grid_view_approved():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    _query = db(db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)).select()            
    for n in _query:
        _sf = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
        if int(_id.stock_type_id) == 1:
            # if _sf.closing_stock >= n.quantity:
            _sf.closing_stock -= n.quantity
            _sf.update_record()
            # else:
            #     session.flash = 'ERROR IN QUANTITY'

        if int(_id.stock_type_id) == 2:
            # if _sf.damaged_stock_qty >= n.quantity:
            _sf.damaged_stock_qty -= n.quantity
            _sf.update_record()
            # else:
            #     session.flash = 'ERROR IN QUANTITY'

        if int(_id.stock_type_id) == 3:
            # if _sf.free_stock_qty <= n.quantity:
            _sf.free_stock_qty -= n.quantity
            _sf.update_record()
            # else:
            #     session.flash = 'ERROR IN QUANTITY'

    _id.update_record(status_id = 15, obsolescence_stocks_approved_by = auth.user_id, obsolescence_stocks_date_approved = request.now)
    session.flash = 'OBSOLESCENCE OF STOCKS APPROVED'                

def obsol_grid_view_rejected():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, obsolescence_stocks_approved_by = auth.user_id, obsolescence_stocks_date_approved = request.now)
    session.flash = 'OBSOLESCENCE OF STOCKS REJECTED'    

# -----------   STOCKS CORRECTIONS     -----------------
def stock_corrections_session():
    session.dept_code_id = session.stock_source_id = 0
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = session.location_code_id = request.vars.location_code_id
    session.stock_quantity_from_id = request.vars.stock_quantity_from_id     
    
def stock_corrections_item_description():
    print '-- ', request.now
    response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    _icode = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == int(session.dept_code_id))).select().first()       
    if not _icode:    
        response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:   
        response.js = "$('#btnadd').removeAttr('disabled')"     
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first() 
              
        if not _sfile:
            response.js = "$('#btnadd').attr('disabled','disabled')"
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        
        if _sfile:      
            if int(session.stock_quantity_from_id) == 1:
                if int(_sfile.closing_stock) == 0:
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in closing stock file. ", _class='alert alert-warning',_role='alert'))           
            elif int(session.stock_quantity_from_id) == 2:
                if int(_sfile.damaged_stock_qty) == 0:
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in damaged stock file. ", _class='alert alert-warning',_role='alert'))

            elif int(session.stock_quantity_from_id) == 3:
                if int(_sfile.free_stock_qty) == 0:
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in free stock file. ", _class='alert alert-warning',_role='alert'))           
                    
            if _icode.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_hand = _sfile.closing_stock      
                _on_free_stk = _sfile.free_stock_qty                
                _on_damaged_qty = _sfile.damaged_stock_qty
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)          
                _on_free_stk = card(_icode.id, _sfile.free_stock_qty, _icode.uom_value)                  
                _on_damaged_qty = card(_icode.id, _sfile.damaged_stock_qty, _icode.uom_value)
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax'),TH('Retail Price'),TH('Unit Price'),TH('On-Normal Qty.'),TH('On-Free Stock Qty.'),TH('On-Damaged Stock Qty.'))),
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
                TD(_on_free_stk),
                TD(_on_damaged_qty)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ACCOUNT MANAGER')| auth.has_membership('ROOT'))
def stock_corrections():
    if auth.has_membership(role = 'ACCOUNT USERS'): # MANOJ        
        _query = db(((db.Stock_Corrections.status_id == 4) | (db.Stock_Corrections.status_id == 16))& (db.Stock_Corrections.archive != True)).select(orderby = ~db.Stock_Corrections.id)
    elif auth.has_membership(role = 'ACCOUNT MANAGER'): # JYOTHI
        # _query = db((db.Stock_Corrections.archive != True) & (db.Stock_Corrections.status_id == 4)).select(orderby = ~db.Stock_Corrections.id)
        _query = db((db.Stock_Corrections.archive != True) & (db.Stock_Corrections.status_id == 4) | (db.Stock_Corrections.status_id == 16)).select(orderby = ~db.Stock_Corrections.id)
    elif auth.has_membership(role = 'ROOT'): # ADMIN
        _query = db().select(orderby = ~db.Stock_Corrections.id)        
    head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Department'),TH('Location'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        if auth.has_membership(role = 'ACCOUNT USERS'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','get_stock_corrections_id', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                # appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_approved', args = n.id, extension = False))
                # reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                attc_lnk = A(I(_class='fas fa-paperclip'), _title='Upload File', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, clea_lnk,  attc_lnk)
            elif n.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                # appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                # reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                attc_lnk = A(I(_class='fas fa-paperclip'), _title='Upload File', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, clea_lnk,  attc_lnk)
        elif auth.has_membership(role = 'ACCOUNT MANAGER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
            elif n.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        # elif auth.has_membership(role = 'ROOT'):
        #     if n.status_id == 4:
        #         view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        #         edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        #     elif n.status_id == 16:
        #         view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle ', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        #         edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        row.append(TR(
            TD(n.stock_corrections_date),
            TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tblcor', **{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})                
    return dict(table = table)    

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ACCOUNT MANAGER')| auth.has_membership('ROOT'))
def get_stock_corrections_id():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()        
    db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Corrections, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def stock_corrections_archived():
    # print 'archived ', request.args(0)
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    _id.update_record(archive = True, updated_on = request.now, updated_by = auth.user_id)
    response.flash = 'RECORD CLEARD'

def stock_corrections_accounts_view():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()    
    db.Stock_Corrections.dept_code_id.writable = False
    db.Stock_Corrections.location_code_id.writable = False
    db.Stock_Corrections.stock_quantity_from_id.writable = False 
    db.Stock_Corrections.stock_quantity_to_id.writable = False 
    db.Stock_Corrections.status_id.writable = False   
    # db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Corrections, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def stock_corrections_accounts_view_approved():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    _query = db(db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)).select()    
    for n in _query:
        _sf = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()     
        if _id.stock_quantity_from_id == 1:
            _sf.closing_stock -= int(n.quantity) 
            if _id.stock_quantity_to_id == 2:
                _sf.damaged_stock_qty += int(n.quantity)
            else:
                _sf.free_stock_qty += int(n.quantity)
            _sf.update_record()

        elif _id.stock_quantity_from_id == 2:
            _sf.damaged_stock_qty -= int(n.quantity)            
            if _id.stock_quantity_to_id == 1:
                _sf.closing_stock += int(n.quantity)
            else:
                _sf.free_stock_qty += int(n.quantity)
            _sf.update_record()
        elif _id.stock_quantity_from_id == 3:
            _sf.free_stock_qty -= int(n.quantity)            
            if _id.stock_quantity_to_id == 1:
                _sf.closing_stock += int(n.quantity)
            else:
                _sf.damaged_stock_qty += int(n.quantity)
            _sf.update_record()
    _id.update_record(status_id = 16, approved_by = auth.user_id, date_approved = request.now)            
    session.flash = 'STOCK CORRECTIONS APPROVED'     
    response.js = "$('#tblcor').get(0).reload()"   

def stock_corrections_accounts_view_rejected():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    _id.update_record(status_id = 3, approved_by = auth.user_id, date_approved = request.now)
    session.flash = 'STOCK CORRECTIONS REJECTED'   
    response.js = "$('#tblcor').get(0).reload()"    

def stock_corrections_view():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()    
    db.Stock_Corrections.dept_code_id.writable = False
    db.Stock_Corrections.location_code_id.writable = False
    # db.Stock_Corrections.adjustment_type.writable = False    
    db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Corrections, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def gen_stock_corrections():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'COR')).select().first()
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _disabled = True)        
    else:
        session.dept_code_id = request.vars.dept_code_id        
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

def validate_stock_corrections(form):    
    _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'COR')).select().first()
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1   
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)    
    form.vars.stock_corrections_id = _trns_pfx.id
    form.vars.stock_corrections_no = int(_skey)    
    # print 'dept code', request.vars.dept_code_id, request.vars.location_code_id

def stock_corrections_add_new():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    db.Stock_Corrections.stock_quantity_from_id.requires = IS_IN_DB(db, db.Stock_Type.id, '%(description)s', zero = 'Choose Stock Type')
    db.Stock_Corrections.stock_quantity_to_id.requires = IS_IN_DB(db, db.Stock_Type.id, '%(description)s', zero = 'Choose Stock Type')
    db.Stock_Corrections.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Stock_Corrections.status_id.default = 4
    form = SQLFORM(db.Stock_Corrections)
    if form.process(onvalidation = validate_stock_corrections).accepted:        
        _id = db(db.Stock_Corrections.stock_corrections_no == form.vars.stock_corrections_no).select().first()        
        _query = db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()        
        for n in _query:
            _p = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            db.Stock_Corrections_Transaction.insert(
                stock_corrections_no_id = _id.id,
                item_code_id = n.item_code_id,
                quantity = n.total_quantity,
                uom = n.uom,                
                average_cost = _p.average_cost,
                wholesale_price = _p.wholesale_price,
                retail_price = _p.retail_price,
                vansale_price = _p.vansale_price)
            db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'COR')).select().first()        
        response.flash = 'RECORD SAVE. ' + str(_trns_pfx.current_year_serial_key)        
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_stock_corrections_transaction_temporary(form):
    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()
    _tq = 0
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty'    
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code = 'Item code is empty in stock file.'    
    else:
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()                
        _exist = db((db.Stock_Corrections_Transaction_Temporary.item_code == request.vars.item_code) & (db.Stock_Corrections_Transaction_Temporary.ticket_no_id == session.ticket_no_id)).select().first()
        if _id.uom_value == 1:
            form.vars.pieces = 0            
        _tq = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces)
        if _exist:
            form.errors.item_code = 'The same item code already added on the grid.'        
        if _tq == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
        if int(session.stock_quantity_from_id) == 1:
            if _tq > _sf.closing_stock:
                form.errors.quantity = 'Items should not be more than ' + str(_sf.closing_stock) + str(' pieces.')
        if int(session.stock_quantity_from_id) == 2:
            if _tq > _sf.damaged_stock_qty:
                form.errors.quantity = 'Items should not be more than ' + str(_sf.damaged_stock_qty) + str(' pieces.')
        if int(session.stock_quantity_from_id) == 3:
            if _tq > _sf.free_stock_qty:
                form.errors.quantity = 'Items should not be more than ' + str(_sf.quantity) + str(' pieces.')

        form.vars.total_quantity = _tq
        form.vars.item_code_id = _id.id
        form.vars.uom = _id.uom_value

def stock_corrections_transaction_temporary():        
    ctr = 0
    row = []
    _total_amount = 0
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 15),    
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0))
        # Field('average_cost','decimal(10,4)', default = 0),
        # Field('stock_location_from_id','reference Transaction_Item_Category', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')),
        # Field('stock_location_to_id','reference Transaction_Item_Category', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_stock_corrections_transaction_temporary).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'        
        db.Stock_Corrections_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            # stock_location_from_id = form.vars.stock_location_from_id,
            # stock_location_to_id = form.vars.stock_location_to_id,
            ticket_no_id = session.ticket_no_id,
            uom = form.vars.uom,
            total_quantity = form.vars.total_quantity)
        if db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled')"
    elif form.errors:
        # table = TABLE(*[TR(v) for k, v in form.errors.items()])
        response.flash = 'FORM HAS ERROR'
                 
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Action'), _class='bg-danger'))
    for i in db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Stock_Corrections_Transaction_Temporary.ALL, db.Item_Master.ALL, left = db.Item_Master.on(db.Item_Master.item_code == db.Stock_Corrections_Transaction_Temporary.item_code)):         
        ctr += 1       
        # _total_amount += i.Stock_Corrections_Transaction_Temporary.total_cost 
        save_lnk = A(I(_class='fas fa-save'), _title='Save Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Corrections_Transaction_Temporary.id))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Corrections_Transaction_Temporary.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = i.Stock_Corrections_Transaction_Temporary.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction_Temporary.id)})
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(i.Stock_Corrections_Transaction_Temporary.item_code),
            TD(i.Item_Master.item_description.upper()),
            # TD(i.Stock_Corrections_Transaction_Temporary.stock_location_from_id.description),
            # TD(i.Stock_Corrections_Transaction_Temporary.stock_location_to_id.description),
            TD(i.Stock_Corrections_Transaction_Temporary.uom),
            TD(i.Stock_Corrections_Transaction_Temporary.quantity),
            TD(i.Stock_Corrections_Transaction_Temporary.pieces),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],  _class='table', _id = 'tmptbl')                
    return dict(form = form, table = table)

def stock_corrections_transaction_temporary_delete():    
    _id = db(db.Stock_Corrections_Transaction_Temporary.id == request.args(0)).delete()
    response.flash = 'RECORD DELETED'

@auth.requires(lambda: auth.has_membership('ACCOUNT USERS') | auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def stock_corrections_transaction_table():
    row = []
    ctr = 0
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Quantity'),TH('Action'), _class='bg-danger'))
    _query = db((db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)) & (db.Stock_Corrections_Transaction.delete != True)).select(db.Stock_Corrections_Transaction.ALL, db.Item_Master.ALL, orderby = ~db.Stock_Corrections_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Corrections_Transaction.item_code_id))
    for i in _query:         
        ctr += 1             
        if auth.has_membership('ACCOUNT USERS'): # MANOJ
            if _id.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle view')        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', _href = URL('inventory','stock_corrections_transaction_table_edit', args = i.Stock_Corrections_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete',  callback = URL(args = i.Stock_Corrections_Transaction.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction.id)})
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        elif auth.has_membership('ACCOUNT MANAGER'): # JYOTHI
            if _id.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', _href = URL('inventory','stock_corrections_transaction_table_edit', args = i.Stock_Corrections_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete',  callback = URL(args = i.Stock_Corrections_Transaction.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction.id)})
        elif auth.has_membership('ACCOUNT MANAGER'): # ADMIN
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', _href = URL('inventory','stock_corrections_transaction_table_edit', args = i.Stock_Corrections_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete',  callback = URL(args = i.Stock_Corrections_Transaction.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction.id)})
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(i.Stock_Corrections_Transaction.item_code_id.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Stock_Corrections_Transaction.uom),
            TD(card(i.Stock_Corrections_Transaction.item_code_id, i.Stock_Corrections_Transaction.quantity, i.Stock_Corrections_Transaction.uom)),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],  _class='table', _id = 'tblcor')                
    return dict(table = table)    

def validate_stock_corrections_edit(form):
    _id = db(db.Stock_Corrections_Transaction.id == request.args(0)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    form.vars.quantity = _qty

def stock_corrections_transaction_table_edit():
    _id = db(db.Stock_Corrections_Transaction.id == request.args(0)).select().first()
    _sc = db(db.Stock_Corrections.id == _id.stock_corrections_no_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom    
    form = SQLFORM.factory(
        Field('quantity','integer', default = _qty),
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = validate_stock_corrections_edit).accepted:
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id)        
        response.flash = 'RECORD UPDATED'
        redirect(URL('stock_corrections_accounts_view', args = _sc.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('inventory','get_stock_corrections_id', args = _sc.id))
    return dict(form = form, btn_back = btn_back)

def stock_corrections_transaction_table_delete():   
    _id = db(db.Stock_Corrections_Transaction.id == request.args(0)).select().first()
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    session.flash = 'RECORD DELETED'
    response.js = "$('#tblcor').get(0).reload()"

def stk_rpt():
    return locals()

def itm_price():
    form = SQLFORM(db.Item_Prices)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

# ---- Stock File     -----

# ---- Stock Receipt     -----
def gen_str():
    print '\ngen str:>', request.args(0)
    redirect(URL('inventory','gen_rep', request.args(0)))

def gen_rep():
    print '\ngen rep: ', request.args(0)
    return locals()
    
@auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def stock_receipt():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Receipt No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='active'))    
    for n in db(((db.Stock_Request.srn_status_id == 5) | (db.Stock_Request.srn_status_id == 6)) & (db.Stock_Request.archive == 'F')).select(orderby = ~db.Stock_Request.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_receipt_details', args = n.id))
        if n.srn_status_id == 6:
            rec_lnk = A(I(_class='fas fa-receipt'), _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle archive', callback = URL(args = n.id), **{'_data-id':(n.id)})        
            # arch_lnk = A(I(_class='fas fa-archive'), _title='Archive Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback = URL('stock_request_archive', args = n.id))        
        else:
            # edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})            
            rec_lnk = A(I(_class='fas fa-receipt'), _title='Create Stock Receipt and Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle str', callback=URL(args = n.id), **{'_data-id':(n.id)})
            arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        if n.srn_status_id == 5:
            repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            repo_lnk = A(I(_class='fas fa-print'), _title='Print Stock Receipt', _type='button  ', _role='button', _class='btn btn-icon-toggle',_target="blank", _href=URL('inventory','stock_receipt_report', args = n.id))
    
        btn_lnk = DIV(view_lnk, rec_lnk, repo_lnk, arch_lnk)
        if n.stock_receipt_no_id == None:
            _stk_rec = 'None'
        else:
            _stk_rec = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        if n.srn_status_id == 5:
            row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='danger'))
        else:
            row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='success'))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table no-margin table-hover', _id =  'tbl')
    return dict(table = table)

def stock_request_archive():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(archive = T)
   
def validate_stock_receipt(form):
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if form.vars.srn_status_id == 6:        
        stock_receipt_generator()
        # _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()
        # _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRC')).select().first()
        # _skey = _trns_pfx.current_year_serial_key
        # _skey += 1
        # _stk_rcpt.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id)
        # _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        # session.flash = 'SAVING STOCK RECEIVE NO SRC' +str(_skey) + '.'            
        # # transfer stock file from source to destination
        # _stk_fil = db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select()    
        # for srt in _stk_fil:
        #     _stk_file_des = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_destination_id)).select(db.Stock_File.ALL).first()
        #     _stk_file_src = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_source_id)).select(db.Stock_File.ALL).first()            
        #     if _stk_file_des:            
        #         _add = int(int(_stk_file_des.closing_stock) + int(srt.quantity))            
        #         _stk_file_des.update_record(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = _add, last_transfer_qty = srt.quantity, last_transfer_date = request.now)  
        #     else:
        #         db.Stock_File.update_or_insert(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = srt.quantity, last_transfer_qty = srt.quantity, last_transfer_date = request.now)
        #     if _stk_file_src:
        #         _min = int(int(_stk_file_src.closing_stock) - int(srt.quantity))            
        #         _min_or_trn = int(_stk_file_src.stock_in_transit) - int(srt.quantity)
        #         _stk_file_src.update_record(closing_stock = _min, stock_in_transit = _min_or_trn, last_transfer_qty = srt.quantity)    


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
        response.flash = 'STOCK RECEIPT CREATED' 
        # redirect(URL('inventory','stock_receipt'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
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

def create_stock_receipt():
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.accepts(request, formname = None):
        session.flash = 'STOCK RECEIPT CREATED'
        redirect(URL('inventory','stock_receipt'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict()

def stock_transfer_receipt_generate_and_print():
    redirect(URL('inventory','stock_receipt_generator',request.args(0)))    
    print 'gen & rep ', request.args(0)

    
def stock_receipt_generator_():           
    _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()    
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRC')).select().first()
    _skey = _trns_pfx.current_year_serial_key        
    _skey += 1
    
    print _skey, _trns_pfx.id, _stk_rcpt.id
    _stk_rcpt.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id)    
    _trns_pfx.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)


def stock_receipt_generator():           
    _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()    
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRC')).select().first()
    _skey = _trns_pfx.current_year_serial_key        
    _skey += 1
    _stk_rcpt.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id)    
    _trns_pfx.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)
    print 'stock receipt generated'
    # session.flash = 'SAVING STOCK RECEIVE NO SRC' +str(_skey) + '.'            
    # transfer stock file from source to destination

    _stk_fil = db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select()    
    for srt in _stk_fil:
        _stk_file_des = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_destination_id)).select(db.Stock_File.ALL).first()
        _stk_file_src = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_source_id)).select(db.Stock_File.ALL).first()            
        if _stk_file_des:            
            _stk_in_transit = int(_stk_file_des.stock_in_transit) - int(srt.quantity)
            _clo_stk = int(_stk_file_des.closing_stock) + int(srt.quantity)
            _stk_file_des.update_record(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = _clo_stk, stock_in_transit = _stk_in_transit, last_transfer_qty = srt.quantity, last_transfer_date = request.now)  
        else:
            db.Stock_File.update_or_insert(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = _clo_stk, stock_in_transit = _stk_in_transit, last_transfer_qty = srt.quantity, last_transfer_date = request.now)
        if _stk_file_src:
            _clo_stk_in_trn = int(_stk_file_src.closing_stock) - int(srt.quantity)
            _stk_in_trn = int(_stk_file_src.stock_in_transit) + int(srt.quantity)
            _stk_file_src.update_record(closing_stock = _clo_stk_in_trn, stock_in_transit = _stk_in_trn, last_transfer_qty = srt.quantity, last_transfer_date = request.now)  

            # _min = int(int(_stk_file_src.closing_stock) - int(srt.quantity))            
            # _min_or_trn = int(_stk_file_src.stock_in_transit) - int(srt.quantity)
            # _stk_file_src.update_record(closing_stock = _min, stock_in_transit = _min_or_trn, last_transfer_qty = srt.quantity)            


            
    # redirect(URL('inventory','stock_receipt_report',request.args(0)))

##########          Q U E R Y           ##########



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
_style = ParagraphStyle(name='BodyText', fontSize=7)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=90, leftMargin=20, rightMargin=20, bottomMargin=130)#,showBoundary=1)
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
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
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
        # [str(_trn.stock_transfer_approved_by.first_name.upper() + ' ' + _trn.stock_transfer_approved_by.last_name.upper()),'',''],
        # ['Issued by','Receive by', 'Delivered by'],
        # ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))],
        # # ['','- - WAREHOUSE COPY - -',''],
        [merch,''],['',today.strftime("%A %d. %B %Y")]], colWidths=[None])
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
    header = Table([[img]], colWidths='*')
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
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    footer = Table([
        ['','Received by:','','Delivered by:',''],
        ['',str(_stk_req.stock_receipt_approved_by.first_name.upper() + ' ' + _stk_req.stock_receipt_approved_by.last_name.upper()),'','',''],
        ['','Name and Signature','','Name and Signature',''],
        [merch,'','','',''],
        [today.strftime("%A %d. %B %Y, %I:%M%p "),'','','','']], colWidths=[50,'*',50,'*',50])
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
    header = Table([[img]], colWidths='*')
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
            ['STOCK REQUEST NO:',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'STOCK REQUEST DATE:',':',s.Stock_Request.stock_request_date.strftime('%d-%m-%Y')],
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
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total            
        # _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, i.Stock_File.closing_stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str('Remarks: ')+str(i.Stock_Request_Transaction.remarks),        
        i.Item_Master.uom_id.description,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Stock_Request_Transaction.item_code_id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.retail_price,
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

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def stock_transaction_report():
    _id = request.args(0)
    _grand_total = 0    
    ctr = 0
    _total = 0
    for s in db(db.Stock_Request.id == _id).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK TRANSFER'],               
            ['Stock Transfer No',':', str(s.Stock_Request.stock_transfer_no_id.prefix)+str(s.Stock_Request.stock_transfer_no),'', 'Stock Transaction Date',':',str(s.Stock_Request.stock_transfer_date_approved.strftime('%d-%m-%Y'))],
            ['Stock Request No',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stock Request Date',':',str(s.Stock_Request.stock_request_date.strftime('%d-%m-%Y'))],
            ['Stock Transfer From',':',s.Stock_Request.stock_source_id.location_name,'','Stock Transfer To',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department',':',s.Stock_Request.dept_code_id.dept_name,'','','','']]        
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
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)]):
        # for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
        _soh = db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select().first()
        if not _soh:
            _stock = 0
        else:
            _stock = _soh.closing_stock
        ctr += 1
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total        
        _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, _stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks)+str('\n')+str('SOH: ')+str(_stock_on_hand),        
        i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.retail_price,
        # _stock_on_hand,
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

    _pc = db(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0)).select().first()
    if not _pc:
        _ctr = 1
        db.Stock_Request_Transaction_Report_Counter.insert(stock_transfer_no_id = request.args(0), printer_counter = _ctr)
    else:
        _pc.printer_counter += 1
        _ctr = _pc.printer_counter
        db.Stock_Request_Transaction_Report_Counter.update_or_insert(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0), printer_counter = _ctr,updated_on = request.now,updated_by = auth.user_id)

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

@auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_receipt_report():    
    _grand_total = ctr = 0
    # ctr = 00,0
    _total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK RECEIPT'],               
            ['Stock Receipt No',':',str(s.Stock_Request.stock_receipt_no_id.prefix)+str(s.Stock_Request.stock_receipt_no), '','STOCK Receipt DATE:',':',s.Stock_Request.stock_receipt_date_approved.strftime('%d-%m-%Y')],
            ['Stock Transfer No',':',str(s.Stock_Request.stock_transfer_no_id.prefix)+str(s.Stock_Request.stock_transfer_no), '','Stock Transfer Date:',':',s.Stock_Request.stock_transfer_date_approved.strftime('%d-%m-%Y')],
            ['Stock Request No',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stock Request Date:',':',s.Stock_Request.stock_request_date.strftime('%d-%m-%Y')],
            ['Stock Request From', ':',s.Stock_Request.stock_source_id.location_name,'','Stock Request To',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department', ':',s.Stock_Request.dept_code_id.dept_name,'','Remarks:',':',s.Stock_Request.remarks]]
        
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
            # _stock_on_hand,
            locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])    
    trn_tbl = Table(stk_trn, colWidths = [25,55,'*',30,30,30,50,50], repeatRows=1)
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
    _grand_total = 0
    _id = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    for r in db(db.Stock_Adjustment.id == request.args(0)).select():
        stk_adj = [
            ['STOCK ADJUSTMENT'],
            ['Stock Adjustment',':', str(r.stock_adjustment_no_id.prefix)+str(r.stock_adjustment_no),'','Stock Adjustment Date',':',r.stock_adjustment_date.strftime('%d-%m-%Y')],
            ['Department',':', r.dept_code_id.dept_name,'','Location',':',r.location_code_id.location_name],
            ['Adjustment Type',':', r.adjustment_type.description,'','Stock Adjustment Code',':',r.stock_adjustment_code],
            ['Status',':', r.srn_status_id.description],
        ]
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
        ('FONTSIZE',(0,0),(3,0),10),
        ('SPAN',(0,0),(6,0)),
    ]))
    

    stk_adj_trnx = [['#','Item Code','Item Description','Cat.','UOM','Qty','Price','Total']]
    for r in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        
        ctr += 1
        _total = r.Stock_Adjustment_Transaction.quantity * r.Stock_Adjustment_Transaction.price_cost
        _grand_total += _total
        stk_adj_trnx.append([
            ctr,
            r.Stock_Adjustment_Transaction.item_code_id.item_code,
            str(r.Item_Master.brand_line_code_id.brand_line_name) +str('\n') +str(r.Item_Master.item_description),
            r.Stock_Adjustment_Transaction.category_id.mnemonic,
            r.Stock_Adjustment_Transaction.uom,
            # r.Stock_Adjustment_Transaction.quantity,
            card(r.Stock_Adjustment_Transaction.item_code_id, r.Stock_Adjustment_Transaction.quantity,r.Stock_Adjustment_Transaction.uom),
            locale.format('%.3F',r.Stock_Adjustment_Transaction.average_cost or 0, grouping = True),
            locale.format('%.3F',_total or 0, grouping = True)
        ])
    stk_adj_trnx.append(['','','','','','','GRAND TOTAL:',locale.format('%.3F',_grand_total or 0, grouping = True)])
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
    if _id.srn_status_id == 2:
        _approved_by = str(_id.approved_by.first_name.upper()) + ' ' + str(_id.approved_by.last_name.upper())                
    else:
        _approved_by = ''
    _sign = [['',str(_id.created_by.first_name.upper()) + ' ' + str(_id.created_by.last_name.upper()),'',_approved_by,''],
    ['','Requested by:','','Approved by:','']]
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
            ['STOCK ADJUSTMENT:', str(r.stock_adjustment_no_id.prefix)+str(r.stock_adjustment_no),'STOCK ADJUSTMENT DATE:',r.stock_adjustment_date.strftime('%d-%m-%Y')],
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

            head = THEAD(TR(TD('#'),TD('Location Code'),TD('Opening Stock'),TD('Closing Stock'),TD('Stock In Transit'),TD('Provisional Balance'),TD('Free Stock'),TD('Damaged Stock')))
            
            for i in db().select(db.Stock_File.ALL, db.Location.ALL, orderby = db.Location.id, left = db.Stock_File.on((db.Stock_File.location_code_id == db.Location.id) & (db.Stock_File.item_code_id == request.vars.item_code_id))):
                ctr += 1
                _available_balanced = int(i.Stock_File.closing_stock or 0) - int(i.Stock_File.stock_in_transit or 0)
                if _itm_code.uom_value == 1:
                    _os = i.Stock_File.opening_stock or 0
                    _cl = i.Stock_File.closing_stock or 0
                    _st = i.Stock_File.stock_in_transit or 0
                    _av = int(i.Stock_File.closing_stock or 0) - int(i.Stock_File.stock_in_transit or 0)
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

                row.append(TR(TD(ctr),TD(i.Location.location_name),
                TD(_os),
                TD(_cl),
                TD(_st),
                TD(_av),
                TD(_fs),
                TD(_ds))) 
                # TD(i.Stock_File.opening_stock or 0, grouping = True),                
                # TD(i.Stock_File.closing_stock or 0, grouping = True),
                # TD(i.Stock_File.stock_in_transit or 0, grouping = True),
                # TD(_avl_bal or 0, grouping = True)))         
            body = TBODY(*row)
            table = TABLE(*[head, body], _class = 'table')
            return dict(form = form, i_table = i_table, table = table)
    return dict(form = form, table = '', i_table = '')

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
        _rep.append([ctr,
        n.Item_Master.item_code,
        n.Item_Master.supplier_item_ref,        
        n.Item_Master.product_code_id,    
        n.Item_Master.subproduct_code_id.subproduct_name,
        n.Item_Master.group_line_id.group_line_name,
        n.Item_Master.brand_line_code_id.brand_line_name,
        Paragraph(n.Item_Master.brand_cls_code_id.brand_cls_name, style = _style),            
        Paragraph(n.Item_Master.item_description, style = _style),            
        n.Item_Master.uom_value,
        n.Item_Master.uom_id.mnemonic,
        locale.format('%.2F',n.Item_Prices.wholesale_price or 0, grouping = True),
        locale.format('%.2F',n.Item_Prices.retail_price or 0, grouping = True)])
    _rep_tbl = Table(_rep, colWidths=[20,55,80,90,65,65,65,110,'*',30,30,50,50], repeatRows=1)
    # _rep_tbl = Table(_rep, colWidths=(50*mm, 50*mm), rowHeights=(10*mm, 250*mm))
    _rep_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 1)),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(-1,-1),7),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
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