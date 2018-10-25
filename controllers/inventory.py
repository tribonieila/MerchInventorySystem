
# ---- Product Master  -----
def prod_view():

    return dict()

def prod_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Division'),TH('Product Code'),TH('Product Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Division.ALL, db.Product.ALL, left=db.Division.on(db.Division.id == db.Product.div_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _href=URL('prod_edit_form', args = n.Product.id),_type='button', _class='btn btn-icon-toggle', **{'_data-toggle':'tooltip', '_data-placement':'top', '_data-original-title':'View Row'})
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row',_href=URL('prod_edit_form', args = n.Product.id),_type='button  ', _role='button', _class='btn btn-icon-toggle')
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _href=URL('prod_edit_form', args = n.Product.id),_type='button', _class='btn btn-icon-toggle', **{'_data-toggle':'tooltip', '_data-placement':'top', '_data-original-title':'Delete Row'})
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Product.id),TD(n.Division.div_name),TD(n.Product.product_code),TD(n.Product.product_name),TD(n.Product.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover')
    return dict(table=table)

def prod_add_form():
    pre = db(db.Prefix_Data.prefix == 'PRO').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Product.id).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(3,'0')
    ctr_val = pre.prefix+ctr
    form = SQLFORM.factory(
        Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        # Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
        Field('product_name', 'string', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name', error_message = 'Record already exist or empty.')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'NEW RECORD SAVED'
        db.Product.insert(div_code_id=form.vars.div_code_id, product_code = ctr_val, product_name = form.vars.product_name, status_id = form.vars.status_id, created_by = auth.user_id, created_on = request.now)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form, ctr_val=ctr_val)

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
def subprod_mas():
    # pre = db(db.Prefix_Data.prefix == 'SPC').select(db.Prefix_Data.prefix).first()
    # ctr = db(db.SubProduct.id).count()
    # ctr = ctr + 1
    # ctr = str(ctr).rjust(3,'0')
    # ctr_val = pre.prefix + ctr    
    # form = SQLFORM.factory(
    #     Field('subproduct_name','string', requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
    #     Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    # if form.process().accepted:
    #     response.flash = 'RECORD SAVE'
    #     db.SubProduct.insert(
    #         dept_code_id = request.vars.dept_code_id,
    #         product_code_id = request.vars.product_code_id, 
    #         subproduct_code = ctr_val, 
    #         subproduct_name = form.vars.subproduct_name, 
    #         status_id = form.vars.status_id,
    #         created_on = request.now,
    #         created_by = auth.user_id)            
    # elif form.errors:
    #     response.flash = 'ENTRY HAS ERRORS'
    # else:
    #     response.flash = 'PLEASE FILL OUT THE FORM'
    # grid = SQLFORM.grid(db.SubProduct)
    row = []
    thead = THEAD(TR(TH('#'),TH('Product Code'),TH('Product Name'),TH('Sub-Product Code'),TH('Sub-Product Name'),TH('Status'),TH('Action')))
    for n in db(db.SubProduct).select(db.Product.ALL, db.SubProduct.ALL, left=db.Product.on(db.Product.id == db.SubProduct.product_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.SubProduct.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('subprod_edit_form', args = n.SubProduct.id))
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.SubProduct.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.SubProduct.id),TD(n.Product.product_code),TD(n.Product.product_name),TD(n.SubProduct.subproduct_code),TD(n.SubProduct.subproduct_name),TD(n.SubProduct.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover') 
    return dict(table=table)

def subprod_add_form():
    pre = db(db.Prefix_Data.prefix == 'SPC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.SubProduct.id).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(3,'0')
    ctr_val = pre.prefix + ctr    
    form = SQLFORM.factory(
        Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        # Field('dept_code_id','reference Department', label = 'Department',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_name','string', requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.SubProduct.insert(div_code_id = form.vars.div_code_id,        
        product_code_id = form.vars.product_code_id, 
        subproduct_code = ctr_val, 
        subproduct_name = form.vars.subproduct_name, status_id = form.vars.status_id,
        created_on = request.now,created_by = auth.user_id)            
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form, ctr_val = ctr_val)

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
def suplr_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('IB Account'),TH('Purchase Account'),TH('Sales Account'),TH('Department'),TH('Supplier Name'),TH('Contact Person'),TH('Supplier Type'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Master).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#", _title='View Row', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _target="#", _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        addr_lnk = A(I(_class='fas fa-address-card'), _target="#", _title='Address', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_form', args = n.id))
        paym_lnk = A(I(_class='fas fa-list'), _target="#", _title='Payment Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_paymod_form', args = n.id))
        bank_lnk = A(I(_class='fas fa-money-check-alt'),_target="#", _title='Bank Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank', args = n.id))
        # othr_lnk = A(I(_class='fas fa-address-book'),_target="#", _title='Other Address', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        dept_lnk = A(I(_class='fas fa-building'), _target="#",_title='Department', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_dept_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, addr_lnk, paym_lnk, bank_lnk, dept_lnk) 
        row.append(TR(TD(n.id),TD(n.supp_code),TD(n.supplier_ib_account),TD(n.supplier_purchase_account),
        TD(n.supplier_sales_account),TD(n.dept_code_id.dept_name),TD(n.supp_name),
        TD(n.contact_person),TD(n.supplier_type),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover')
    return dict(table = table)

def step1():
    pre = db(db.Prefix_Data.prefix == 'SUP').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Supplier_Master).count()
    session._id = session.renew()
    ctr = ctr + 1
    
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr
    supp_ib_acct_ctr = str(25)+'-'+ctr
    supp_pu_acct_ctr = str(18)+'-'+ctr
    supp_sa_acct_ctr = str(19)+'-'+ctr
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
        Field('purchase_budget', 'decimal(10,2)', default = 0.0),        
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))

    if form.process(keepvalues = True).accepted:
        
        response.flash = 'RECORD SAVE'
        # db.Supplier_Master.insert(dept_code_id = form.vars.dept_code_id,supp_code = ctr_val, supp_name = form.vars.supp_name, supplier_type = form.vars.supplier_type,
        # supplier_ib_account = supp_ib_acct_ctr,supplier_purchase_account = supp_pu_acct_ctr, supplier_sales_account = supp_sa_acct_ctr,
        # contact_person = form.vars.contact_person,address_1 = form.vars.address_1, address_2 = form.vars.address_2,country_id = form.vars.country_id,contact_no = form.vars.contact_no,
        # currency_id = form.vars.currency_id, fax_no = form.vars.fax_no,email_adddress = form.vars.email_address,status_id = form.vars.status_id)
        # redirect(URL('suplr_add_form#second1'))
        #response.js =  "jQuery('#collapseExample').get(0).reload();"
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, ctr_val = ctr_val, supp_ib_acct_ctr = supp_ib_acct_ctr,supp_pu_acct_ctr=supp_pu_acct_ctr,supp_sa_acct_ctr=supp_sa_acct_ctr)      

def step2():

    # supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('other_supplier_name', 'string', length = 50, requires = IS_UPPER()),
        Field('contact_person', 'string', length=30, requires = IS_UPPER()),
        Field('address_1','string', length = 50, requires = IS_UPPER()),
        Field('address_2','string', length = 50, requires = IS_UPPER()),
        Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    
    if form.process(formname = 'step2', keepvalues = True).accepted:
    

        response.flash = session._id
        
        # db.Supplier_Contact_Person.insert(
        #     supplier_id = request.args(0),other_supplier_name = form.vars.other_supplier_name,contact_person = form.vars.contact_person, 
        #     address_1 = form.vars.address_1, address_2 = form.vars.address_2,
        #     country_id = form.vars.country_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = session._id #'ENTRY HAS ERRORS'
        # return jQuery(document).ready(function() { alert('ok') });
    # return dict(form = form, supplier_id = supplier_id.supp_name, table = table)    
    
    
    return dict(form = form)
def step3():
    form = SQLFORM.factory(
        Field('trade_terms_id', 'reference Supplier_Trade_Terms', label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')), 
        Field('payment_mode_id', 'reference Supplier_Payment_Mode', label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), 
        Field('payment_terms_id', 'reference Supplier_Payment_Terms', label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), 
        Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('forwarder_id', 'reference Forwarder_Supplier', label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
        Field('commodity_code','string',length=10),
        Field('discount_percentage','string',length=10),
        Field('custom_duty_percentage','string',length=10),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process(formname = 'step3', keepvalues = True).accepted:
        response.flash = 'RECORD SAVE'
        # db.Supplier_Payment_Mode_Details.insert(supplier_id = request.args(0),trade_terms_id = form.vars.trade_terms_id,payment_mode_id = form.vars.payment_mode_id,
        # payment_terms_id = form.vars.payment_terms_id,currency = form.vars.currency,forwarder_id = form.vars.forwarder_id,commodity_code = form.vars.commodity_code,
        # discount_percentage = form.vars.discount_percentage,custom_duty_percentage = form.vars.custom_duty_percentage,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'    
    return dict(form = form)
def step4():
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
    if form.process(formname = 'step4', keepvalues = True).accepted:
        response.flash = 'RECORD SAVE'
        # db.Supplier_Bank.insert(supplier_id = request.args(0),account_no = form.vars.account_no,
        # beneficiary_name = form.vars.beneficiary_name, iban_code = form.vars.iban_code,
        # swift_code = form.vars.swift_code, bank_address = form.vars.bank_address, city= form.vars.city,
        # country_id = form.vars.country_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'     
    return dict(form = form)
def step5():
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')))
        # Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process(formname = 'step5', keepvalues = True).accepted:
        response.flash = 'RECORD SAVE'
        # db.Supplier_Master_Department.insert(supplier_id = request.args(0),dept_code_id = form.vars.dept_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

def suplr_add_form():
    # PREFIX 25- + serial supplier code	25-00001
    # Prefix 18 + serial supplier code	18-00001
    # Prefix 19 + serial supplier code	19-00001

    pre = db(db.Prefix_Data.prefix == 'SUP').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Supplier_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr
    supp_ib_acct_ctr = str(25)+'-'+ctr
    supp_pu_acct_ctr = str(18)+'-'+ctr
    supp_sa_acct_ctr = str(19)+'-'+ctr
    form = SQLFORM.factory(
        # Supplier Master Table
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
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
        # Supplier Contact Person Master Table
        Field('other_supplier_name', 'string', length = 50, requires = IS_UPPER()),
        Field('scp_contact_person', 'string', length=30, requires = IS_UPPER()),
        Field('scp_address_1','string', length = 50, requires = IS_UPPER()),
        Field('scp_address_2','string', length = 50, requires = IS_UPPER()),
        Field('scp_country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('scp_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),    
        # Supplier Payment Mode Details Table
        Field('trade_terms_id', 'reference Supplier_Trade_Terms', label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')), 
        Field('payment_mode_id', 'reference Supplier_Payment_Mode', label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), 
        Field('payment_terms_id', 'reference Supplier_Payment_Terms', label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), 
        Field('spm_currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('forwarder_id', 'reference Forwarder_Supplier', label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
        Field('commodity_code','string',length=10),
        Field('discount_percentage','string',length=10),
        Field('custom_duty_percentage','string',length=10),
        Field('spm_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),    
        # Supplier Bank Table
        Field('account_no', 'string'),
        Field('bank_name', 'string'),
        Field('beneficiary_name', 'string'),
        Field('iban_code', 'string'),
        Field('swift_code', 'string'),
        Field('bank_address', 'string'),
        Field('city', 'string'),
        Field('sb_country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('sb_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        # Supplier Master Department Table
        # Field('smd_dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')))
        

    if form.process(formname = 'form_one', keepvalues = True).accepted:
        
        response.flash = 'NEW RECORD SAVE'
        
        db.Supplier_Master.insert(
            dept_code_id = form.vars.dept_code_id,
            supp_code = ctr_val, 
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
        _id = db(db.Supplier_Master).select(db.Supplier_Master.id).last()
        db.Supplier_Contact_Person.insert(
            supplier_id = _id, 
            other_supplier_name = form.vars.other_supplier_name,
            contact_person = form.vars.scp_contact_person,
            address_1 = form.vars.scp_address_1,
            address_2 = form.vars.scp_address_2,
            country_id = form.vars.scp_country_id,
            status_id = form.vars.scp_status_id)

        db.Supplier_Payment_Mode_Details.insert(
            supplier_id = _id,
            trade_terms_id = form.vars.trade_terms_id,
            payment_mode_id = form.vars.payment_mode_id,
            payment_terms_id = form.vars.payment_terms_id,
            currency = form.vars.spm_currency,
            forwarder_id = form.vars.forwarder_id,
            commodity_code = form.vars.commodity_code,
            discount_percentage = form.vars.discount_percentage,
            custom_duty_percentage = form.vars.custom_duty_percentage,
            status_id = form.vars.spm_status_id)

        db.Supplier_Bank.insert(
            supplier_id = _id,
            account_no = form.vars.account_no,
            beneficiary_name = form.vars.beneficiary_name, 
            iban_code = form.vars.iban_code,
            swift_code = form.vars.swift_code, 
            bank_address = form.vars.bank_address, 
            city= form.vars.city,
            country_id = form.vars.sb_country_id, 
            status_id = form.vars.sb_status_id)
        

    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'



    return dict(form = form, ctr_val = ctr_val, supp_ib_acct_ctr = supp_ib_acct_ctr,supp_pu_acct_ctr=supp_pu_acct_ctr,supp_sa_acct_ctr=supp_sa_acct_ctr)  

def suplr_edit_form():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    # db.Supplier_Master.dept_code_id.writable =False
    ctr_val = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, supplier_id = supplier_id)

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
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    row = []
    thead = THEAD(TR(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Status'),TH('Action'))))
    for n in db(db.Supplier_Bank.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),
        TD(n.swift_code),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, table = table, supplier_id = supplier_id)

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

def suplr_view_form():    

    return dict()

def suplr_addr_form():     
    
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('other_supplier_name', 'string', length = 50, requires = IS_UPPER()),
        Field('contact_person', 'string', length=30, requires = IS_UPPER()),
        Field('address_1','string', length = 50, requires = IS_UPPER()),
        Field('address_2','string', length = 50, requires = IS_UPPER()),
        Field('country_id','string',label = 'Country',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Contact_Person.insert(
            supplier_id = request.args(0),other_supplier_name = form.vars.other_supplier_name,contact_person = form.vars.contact_person, 
            address_1 = form.vars.address_1, address_2 = form.vars.address_2,
            country_id = form.vars.country_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM '
    row = []
    thead = THEAD(TR(TH('#'),TH('Other Supplier Name'),TH('Contact Person'),TH('Address'),TH('Country'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Contact_Person.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.other_supplier_name),TD(n.contact_person),TD(n.address_1),TD(n.country_id.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, supplier_id = supplier_id.supp_name, table = table)

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

def suplr_paymod_form():

    # form = SQLFORM.factory(
    #     Field('trade_terms_id', 'reference Supplier_Trade_Terms', label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')), 
    #     Field('payment_mode_id', 'reference Supplier_Payment_Mode', label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), 
    #     Field('payment_terms_id', 'reference Supplier_Payment_Terms', label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), 
    #     Field('currency', 'string', length = 5, requires = IS_IN_SET(CURRENCY, zero = 'Choose Currency')),
    #     Field('forwarder_id', 'reference Forwarder_Supplier', label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
    #     Field('commodity_code','string',length=10),
    #     Field('discount_percentage','string',length=10),
    #     Field('custom_duty_percentage','string',length=10),
    #     Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    # if form.process().accepted:
    #     response.flash = 'RECORD SAVE'
    #     db.Supplier_Payment_Mode_Details.insert(supplier_id = request.args(0),trade_terms_id = form.vars.trade_terms_id,payment_mode_id = form.vars.payment_mode_id,payment_terms_id = form.vars.payment_terms_id,currency = form.vars.currency,forwarder_id = form.vars.forwarder_id,commodity_code = form.vars.commodity_code,discount_percentage = form.vars.discount_percentage,custom_duty_percentage = form.vars.custom_duty_percentage,status_id = form.vars.status_id)
    # elif form.errors:
    #     response.flash = 'ENTRY HAS ERRORS'
    # else:
    #     response.flash = 'PLEASE FILL OUT THE FORM'
    # row = []
    # thead = THEAD(TR(TH('#'),TH('Trade Terms'),TH('Payment Mode'),TH('Payment Terms'),TH('Currency'),
    # TH('Forwarder'),TH('Commodity'),TH('Discount %'),TH('Custom Duty %'),TH('Status'),TH('Action')))  
    # for n in db(db.Supplier_Payment_Mode_Details.supplier_id == request.args(0)).select():
    #     view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
    #     prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
    #     edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_paymod_edit_form', args = n.id))
    #     dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
    #     btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
    #     row.append(TR(TD(n.id), TD(n.trade_terms_id.trade_terms),TD(n.payment_mode_id.payment_mode),TD(n.payment_terms_id.payment_terms),TD(n.currency_id),
    #     TD(n.forwarder_id.forwarder_name),TD(n.commodity_code),TD(n.discount_percentage),TD(n.custom_duty_percentage),TD(n.status_id.status),TD(btn_lnk)))
    # tbody = TBODY(*row)
    # table = TABLE(*[thead, tbody], _class='table table-striped')         
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Payment_Mode_Details, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'         
    return dict(form = form, supplier_id = supplier_id)

def suplr_paymod_edit_form():
    db.Supplier_Payment_Mode_Details.supplier_id.writable = False
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Payment_Mode_Details, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, supplier_id = supplier_id)

def suplr_add_group_form():
    pre = db(db.Prefix_Data.prefix == 'SUP').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Supplier_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM(db.Supplier_Master)    
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Master.insert(supp_code = form.vars.supp_code,supp_name = form.vars.supp_name)
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

def supp_trd_trms_edit_form():
    form = SQLFORM(db.Supplier_Trade_Terms, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

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

def supp_pay_mode_edit_form():
    form = SQLFORM(db.Supplier_Payment_Mode, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

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
def supp_pay_term_edit_form():
    form = SQLFORM(db.Supplier_Payment_Terms, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

def forw_supp():
    pre = db(db.Prefix_Data.prefix == 'FOR').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Forwarder_Supplier).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2,'0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM.factory(
        Field('forwarder_name','string',length = 50),
        Field('forwarder_type','string',length = 5, requires = IS_IN_SET(['AIR','SEA'], zero = 'Choose Type')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Forwarder_Supplier.insert(forwarder_code = ctr_val,forwarder_name = form.vars.forwarder_name,forwarder_type = form.vars.forwarder_type,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    row = []
    thead = THEAD(TR(TH('#'),TH('Forwarder Code'),TH('Forwarder Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Forwarder_Supplier.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled   ', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('forw_supp_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.forwarder_code),TD(n.forwarder_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form = form, ctr_val = ctr_val,table = table)

def forw_supp_edit_form():
    _fld = db(db.Forwarder_Supplier.id == request.args(0)).select().first()
    form = SQLFORM(db.Forwarder_Supplier, request.args(0), deletable = True)    
    if form.process().accepted:        
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, _fld = _fld)

# ---- GroupLine Master  -----
def groupline_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Supplier Name'),TH('Group Line Code'),TH('Group Line Name'),TH('Status'),TH('Actions')))
    query = db(db.GroupLine).select(db.GroupLine.ALL, db.Supplier_Master.ALL, left = db.Supplier_Master.on(db.Supplier_Master.id == db.GroupLine.supplier_id))
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#'))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('groupline_edit_form', args = n.GroupLine.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#'))
        supp_lnk = A(I(_class='fas fa-paper-plane'), _title='Go To Supplier(s)', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='#', _href=URL('sbgplne_lnk', args = n.GroupLine.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, supp_lnk)
        row.append(TR(TD(n.GroupLine.id),TD(n.Supplier_Master.supp_code),TD(n.Supplier_Master.supp_name),TD(n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.GroupLine.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(table = table)

def groupline_add_form():
    pre = db(db.Prefix_Data.prefix == 'GRL').select(db.Prefix_Data.prefix).first()
    ctr = db(db.GroupLine.id).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM.factory(        
        Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'GroupLine.group_line_name')]),
        Field('supplier_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
        Field('status_id', 'reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.GroupLine.insert(supplier_id = form.vars.supplier_id,group_line_code = ctr_val, group_line_name = form.vars.group_line_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val)

def groupline_edit_form():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()
    form = SQLFORM(db.GroupLine, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.group_line_code)

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
    return dict(form = form, table=table, ctr_val = ctr_val.group_line_code)

def sbgplne_lnk_edit_form():
    form = SQLFORM(db.Sub_Group_Line, request.args(0), deletable= True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

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
def brndlne_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Group Line Code'),TH('Group Line Name'),TH('Brand Line Code'),TH('Brand Line Name'),TH('Status'),TH('Action')))
    query = db(db.Brand_Line).select(db.Brand_Line.ALL, db.GroupLine.ALL, left = db.GroupLine.on(db.Brand_Line.group_line_id == db.GroupLine.id))
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Brand_Line.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brndlne_edit_form', args = n.Brand_Line.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Brand_Line.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        
        row.append(TR(TD(n.Brand_Line.id),TD(n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.Brand_Line.brand_line_code),TD(n.Brand_Line.brand_line_name), TD(n.Brand_Line.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(table=table)

def brndlne_add_form():
    pre = db(db.Prefix_Data.prefix == 'BRL').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Brand_Line).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr    
    form = SQLFORM.factory(
        Field('group_line_id', 'reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')),
        Field('brand_line_code', 'string', default = ctr_val),
        Field('brand_line_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Line.brand_line_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Brand_Line.insert(group_line_id = form.vars.group_line_id,brand_line_code = ctr_val,brand_line_name = form.vars.brand_line_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val)
def brndlne_edit_form():
    ctr_val = db(db.Brand_Line.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Line, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'    
    return dict(form = form, ctr_val = ctr_val.brand_line_code)

# ---- Brand Classification Master  -----
def brndclss_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Group Line Name'),TH('Brand Line Name'),TH('Brand Classficaion Code'),TH('Brand Classification Name'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Classification).select(db.Brand_Classification.ALL, db.Brand_Line.ALL, db.GroupLine.ALL, left = [db.Brand_Line.on(db.Brand_Line.id == db.Brand_Classification.brand_line_code_id), db.GroupLine.on(db.Brand_Line.group_line_id == db.GroupLine.id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Brand_Classification.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brndclss_edit_form', args = n.Brand_Classification.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Brand_Classification.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Brand_Classification.id),TD(n.GroupLine.group_line_name),TD(n.Brand_Line.brand_line_name),TD(n.Brand_Classification.brand_cls_code),TD(n.Brand_Classification.brand_cls_name),TD(n.Brand_Classification.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(table=table)

def brndclss_add_form():
    pre = db(db.Prefix_Data.prefix == 'BRC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Brand_Classification).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5, '0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM.factory(
        Field('group_line_code_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', label = 'Brand Line Code',requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
        Field('brand_cls_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Brand_Classification.insert(brand_line_code_id = form.vars.brand_line_code_id,brand_cls_code = ctr_val,brand_cls_name = form.vars.brand_cls_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form, ctr_val = ctr_val)

def brndclss_edit_form():
    ctr_val = db(db.Brand_Classification.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Classification, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.brand_cls_code)


# ---- Item Color Master  -----
def itmcol_mas():
    pre = db(db.Prefix_Data.id == 4).select(db.Prefix_Data.prefix).first()
    ctr = db(db.Item_Color).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2, '0')
    ctr_value = pre.prefix + ctr
    form = SQLFORM.factory(
        Field('color_code','string',default = ctr_value),
        Field('color_name','string',length=25),
        Field('status_id','reference Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Item_Color.insert(color_code = ctr_value,color_name = form.vars.color_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    row = []
    thead = THEAD(TR(TH('#'),TH('Color Code'),TH('Color Name'),TH('Status'),TH('Action')))    
    for n in db(db.Item_Color).select():
        row.append(TR(TD(n.id),TD(n.color_code),TD(n.color_name),TD(n.status_id.status),TD()))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')     
    return dict(form=form, table=table)

# ---- Item Size Master  -----
def itmsze_mas():
    pre = db(db.Prefix_Data.id == 12).select(db.Prefix_Data.prefix).first()
    ctr = db(db.Item_Size).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(3, '0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM.factory(
        Field('size_name','string',length=25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db, 'Item_Size.size_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Item_Size.insert(size_code = ctr_val ,size_name = form.vars.size_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Size Code'),TH('Size Name'),TH('Status'),TH()))
    query = db(db.Item_Size).select()
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmsze_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.size_code),TD(n.size_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form=form, table=table, ctr_val = ctr_val)

def itmsze_edit_form():
    ctr_val = db(db.Item_Size.id == request.args(0)).select().first()
    form = SQLFORM(db.Item_Size, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        # redirect(URL('default','itmsze_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, ctr_val = ctr_val)

# ---- Item Color Master  -----
def itmcoll_mas():
    pre = db(db.Prefix_Data.id == 3).select(db.Prefix_Data.prefix).first()
    ctr = db(db.Item_Collection).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2,'0')
    ctr_value = pre.prefix + ctr
    # form = SQLFORM(db.Item_Collection)
    form = SQLFORM.factory(
        Field('collection_code','string',default = ctr_value),
        Field('collection_name','string',length=25),
        Field('status_id','reference Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Item_Collection.insert(collection_code = form.vars.collection_code,collection_name = form.vars.collection_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    grid = SQLFORM.grid(db.Item_Collection)
    row = []
    thead = THEAD(TR(TH('#'),TH('Collection Code'),TH('Collection Name'),TH('Status'),TH('Action')))
    query = db(db.Item_Collection).select()
    for n in query:
        # <a class="btn btn-primary" href="#" role="button">Link</a>
        edit = A(SPAN(_class = 'btn btn-primary'),_title="Edit", _href=URL("default",'itmcoll_edit_form', args=n.id ))
        btn_lnks = DIV(edit, _class="hidden-sm hidden-xs action-buttons")
        # <button type="button" class="btn btn-primary btn-sm">Small button</button>
        row.append(TR(TD(n.id),TD(n.collection_code),TD(n.collection_name),TD(n.status_id),TD(btn_lnks)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    

    return dict(form=form, grid=table)

def itmcoll_edit_form():
    form = SQLFORM(db.Item_Collection, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        # redirect(URL('default','itmcoll_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

# ---- Made In Master  -----
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

def mdein_edit_form():
    form = SQLFORM(db.Made_In, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Currency Master  -----
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

def curr_edit_form():
    form = SQLFORM(db.Currency, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Brand Master      -----
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
def itm_typ_mas():  
    form = SQLFORM(db.Item_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Item_Type).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

def itm_type_edit_form():
    form = SQLFORM(db.Item_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Supplier UOM Master      -----
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

def suplr_uom_edit_master():
    form = SQLFORM(db.Supplier_UOM, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

# ---- UOM Master      -----
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

def uom_edit_master():
    form = SQLFORM(db.UOM, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

# ---- Color Master      -----
def col_mas():  
    form = SQLFORM(db.Color_Code)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Color_Code).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('col_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

def col_edit_form():
    form =SQLFORM(db.Color_Code, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)
# ---- ITEM Master Division  -----    
def itm_mas():    

    row = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Int Barcode'),TH('Loc Barcode'),TH('Group Line'),
    TH('Brand Line'),TH('Status'),TH('Actions')))
    for n in db(db.Item_Master).select():        
        # view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', 
        # **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true',
        # '_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Hand-Over Info','_data-content': han_info(h.id)})

        # <button type="button" class="btn btn-secondary" data-container="body" data-toggle="popover" 
        # data-placement="left" data-content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.">Popover on left</button>

        link_lnk = A(I(_class='fas fa-link'), _title='Link Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_link_form', args = n.id))
        view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(link_lnk, view_lnk, prin_lnk,edit_lnk, dele_lnk)
        
        row.append(TR(TD(n.id),TD('ITM'+n.item_code),TD(n.item_description),TD(n.int_barcode),TD(n.loc_barcode),
        TD(n.group_line_id.group_line_name),TD(n.brand_line_code_id.brand_line_name),TD(n.item_status_code_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(table = table)

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
        Field('uom_id', 'reference UOM', requires = IS_IN_DB(db, db.UOM, '%(mnemonic)s - %(description)s', zero = 'Choose UOM Pack Size')),
        Field('supplier_uom_value', 'integer', default =1 ),
        Field('supplier_uom_id', 'reference Supplier_UOM', requires = IS_IN_DB(db, db.Supplier_UOM.id, '%(mnemonic)s - %(description)s', zero = 'Choose Supplier UOM Pack Size') ),
        Field('weight_value', 'integer'),
        Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(mnemonic)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), # saleable/non-saleable
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
        Field('size_code_id','reference Item_Size', default = 1, requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = None)), #widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='')),    
        Field('gender_code_id','reference Gender',  requires = IS_IN_DB(db, db.Gender.id,'%(gender_code)s - %(gender_name)s', zero = None)),
        Field('fragrance_code_id','reference Fragrance_Type',  requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(fragrance_code)s - %(fragrance_name)s', zero = None)),
        Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = None)),
        Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(collection_code)s - %(collection_name)s', zero = 'Choose Collection')),
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
        Field('uom_id', 'reference UOM', default = 1,requires = IS_IN_DB(db, db.UOM, '%(description)s', zero = 'Choose UOM Text')),
        Field('supplier_uom_value', 'integer', default = 1),
        Field('supplier_uom_id', 'reference Supplier_UOM', requires = IS_IN_DB(db, db.Supplier_UOM.id, '%(description)s', zero = 'Choose Supplier UOM') ),
        Field('weight_value', 'integer'),
        Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(description)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(description)s', zero = 'Choose Type')), # saleable/non-saleable
        Field('selective_tax','string'),
        Field('vat_percentage','string'),        
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_name)s', zero = 'Choose Size')),    
        Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(gender_name)s', zero = 'Choose Gender')),
        Field('fragrance_code_id','reference Fragrance_Type', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(fragrance_name)s', zero = 'Choose Fragrance Code')),
        Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = 'Choose Color')),
        Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(collection_name)s', zero = 'Choose Collection')),
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


def itm_edit_form():
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
            TR(TD('Size Code:'), TD(x.size_code_id.size_name, _style = 'text-align: right')),
            TR(TD('Gender:'), TD(x.gender_code_id.gender_name, _style = 'text-align: right')),
            TR(TD('Fragrance Code:'), TD(x.fragrance_code_id.fragrance_name, _style = 'text-align: right')),
            TR(TD('Color:'), TD(x.color_code_id.description, _style = 'text-align: right')),
            TR(TD('Collection:'), TD(x.collection_code_id.collection_name, _style = 'text-align: right')),
            TR(TD('Made In:'), TD(x.made_in_id.description, _style = 'text-align: right')),
            TR(TD('Status:'), TD(x.item_status_code_id.status, _style = 'text-align: right'))])
    table = str(XML(t, sanitize = False))
    return table

def itm_link_form():

    return locals()

def itm_link_profile():
    form = SQLFORM(db.Item_Master, request.args(0))
    return dict(form = form)

# ---- FMCG Division  -----    
def fmcg_form():
    pre = db(db.Prefix_Data.id == 11).select(db.Prefix_Data.prefix).first()
    ctr = db(db.FMCG_Division).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_value = pre.prefix + ctr       
    form = SQLFORM(db.FMCG_Division)
    form = SQLFORM.factory( 
        # Field('div_code_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('item_code', 'string', length = 15, label = 'Item Code',requires = IS_NOT_IN_DB(db, 'FMCG_Division.item_code')),
        Field('item_description', 'string', length = 35, label = 'Description'),    
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        # subproduct
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),

        Field('ref_no', 'string', length = 15, label = 'Reference No',requires = IS_NOT_IN_DB(db, 'FMCG_Division    .ref_no')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
        Field('supplier_item_ref', 'string', length = 15),    
        Field('uom', 'integer'),
        Field('supp_oum', 'integer'),
        Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(gender_code)s - %(gender_name)s', zero = 'Choose Gender')),
        Field('item_status_code_id','reference Status', requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')),
        Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = 'Choose Size')),
        Field('made_in','string',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')))
    if form.process().accepted:        
        response.flash = 'RECORD SAVE'
        # fnd = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()
        # itm_code = fnd.supp_code[-5:]+'-'+ctr
        # db.Itemmas.insert(supplier_code_id = form.vars.supplier_code_id, item_code = itm_code)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'    

    grid = SQLFORM.grid(db.FMCG_Division)
    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Item Code'),TH('Action')))    
    for n in db(db.FMCG_Division).select():
        edit_lnk = A('Edit', _href = URL('fmcg_edit_form', args = n.id))
        row.append(TR(TD(n.id),TD(n.supplier_code_id.supp_code),TD(n.item_code),TD(edit_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')   
    return dict(form=form, grid = grid)

def fmcg_batch_form():
    ctr = db(db.FMCG_Division.id).count()
    ctr = ctr + 1    
    ctr = str(ctr).rjust(5,'0')
    form = SQLFORM.factory(
        Field('item_description', 'string', label = 'Description'),    
        Field('supplier_item_ref', 'string'),    
        Field('uom', 'integer', default = 1),
        Field('supp_oum', 'integer', default = 1),
        Field('weight', 'integer', default = 1),
        Field('dept_code_id','reference Department', default = 2, label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
        Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(gender_code)s - %(gender_name)s', zero = 'Choose Gender')),
        Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = 'Choose Size')),
        Field('made_in','string', requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
        Field('item_status_code_id','reference Status', requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        response.flash = 'NEW RECORD SAVE'
        fnd = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()
        itm_code = fnd.supp_code[-5:]+ctr
        db.FMCG_Division.insert(div_code_id = 2, item_code = itm_code, item_description = form.vars.item_description, dept_code_id = form.vars.dept_code_id, weight = form.vars.weight,
            supplier_code_id = form.vars.supplier_code_id, product_code_id = form.vars.product_code_id, subproduct_code_id = form.vars.subproduct_code_id,
            group_line_id = form.vars.group_line_id, brand_line_code_id = form.vars.brand_line_code_id, brand_cls_code_id = form.vars.brand_cls_code_id,
            section_code_id = form.vars.section_code_id, supplier_item_ref = form.vars.supplier_item_ref, uom = form.vars.uom,
            supp_oum = form.vars.supp_oum, gender_code_id = form.vars.gender_code_id, size_code_id = form.vars.size_code_id, made_in = form.vars.made_in,
            item_status_code_id = form.vars.item_status_code_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)    
    

def fmcg_add_form():
    ctr = db(db.FMCG_Division.id).count()
    ctr = ctr + 1    
    ctr = str(ctr).rjust(5,'0')
    form = SQLFORM.factory(
        Field('item_description', 'string', label = 'Description'),    
        Field('supplier_item_ref', 'string'),    
        Field('int_barcode', 'string', length = 20),     
        Field('loc_barcode', 'string', length = 20),
        Field('uom', 'integer', default = 1),
        Field('supp_oum', 'integer', default = 1),
        Field('weight', 'integer', default = 1),
        Field('dept_code_id','reference Department', default = 3, label = 'Dept Code',requires = IS_IN_DB(db(db.Department.id == 3), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.div_code_id == 2), db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = 'Choose Size')),
        Field('made_in','string', requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
        Field('item_status_code_id','reference Status', default = 1,requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        response.flash = 'NEW RECORD SAVE'
        supl_ctr = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()
        itm_code_ctr = supl_ctr.supp_code[-5:]+ctr
        db.FMCG_Division.insert(div_code_id = 2,item_code = itm_code_ctr, item_description = form.vars.item_description, int_barcode = form.vars.int_barcode, loc_barcode = form.vars.loc_barcode,
            dept_code_id = form.vars.dept_code_id, weight = form.vars.weight,supplier_code_id = form.vars.supplier_code_id, product_code_id = form.vars.product_code_id, subproduct_code_id = form.vars.subproduct_code_id,
            group_line_id = form.vars.group_line_id, brand_line_code_id = form.vars.brand_line_code_id, brand_cls_code_id = form.vars.brand_cls_code_id,
            section_code_id = form.vars.section_code_id, supplier_item_ref = form.vars.supplier_item_ref, uom = form.vars.uom,supp_oum = form.vars.supp_oum, size_code_id = form.vars.size_code_id, made_in = form.vars.made_in,
            item_status_code_id = form.vars.item_status_code_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)


def fmcg_view_form():
    form = db(db.Item_Master.id == request.args(0)).select().first()
    return dict(form = form)

def fmcg_mas():
    q_dept = db(db.Department.div_code_id == 2).select()
    row = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Product Code'),TH('Sub Product'),TH('Group Line'),
    TH('Brand Line'),TH('Status'),TH('Actions')))
    for n in db(db.Item_Master).select():        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('fmcg_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('fmcg_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk,edit_lnk, dele_lnk)
        
        row.append(TR(TD(n.id),TD(n.item_code),TD(n.item_description),TD(n.product_code_id.product_code),TD(n.subproduct_code_id.subproduct_code),
        TD(n.group_line_id.group_line_code),TD(n.brand_line_code_id.brand_line_code),TD(n.item_status_code_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(table = table)


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
def stock_receipt():
    return locals()
# ---- Reports           -----
def reports():
    return locals()

# ------------------------------------------------------------------------------------------
# ----------------------------  S   E   T   T   I   N   G   S  -----------------------------
# ------------------------------------------------------------------------------------------

# ---- Prefix Master       -----
def pre_mas():
    row = []
    thead = THEAD(TR(TH('ID'),TH('Prefix'),TH('Prefix Name'),TH('Action')))
    query = db(db.Prefix_Data).select()
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('edit_pre_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        edit_lnk = A('Edit', _href=URL('edit_pre_form', args=n.id ))
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(table = table)

def pre_add_form():
    form = SQLFORM(db.Prefix_Data)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

def edit_pre_form():
    form = SQLFORM(db.Prefix_Data, request.args(0), deletable = True)
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

def div_mas():    
    grid = SQLFORM.grid(db.Division)
    row = []
    thead = THEAD(TR(TH('#'),TH('Code'),TH('Name'),TH('Status'),TH('Action')))
    for n in db(db.Division).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('div_edit_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('div_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('div_edit_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.div_code),TD(n.div_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')
    return dict(table=table)

def div_add_form():
    pre = db(db.Prefix_Data.prefix == 'DIV').select(db.Prefix_Data.prefix).first()    
    ctr = db(db.Division.id).count()
    ctr = ctr+1
    ctr = str(ctr).rjust(2, '0')
    ctr_val = pre.prefix+ctr
    form = SQLFORM.factory(
        Field('div_name','string', length = 50, label = 'Division Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Division.div_name')]), 
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id, '%(status)s', zero='Choose Status')))
    if form.process().accepted:
        db.Division.insert(div_code = ctr_val, div_name = form.vars.div_name, status_id = form.vars.status_id)
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'   
    return dict(form=form, ctr_val = ctr_val)

def div_edit_form():
    ctr_val = db(db.Division.id == request.args(0)).select(db.Division.div_code).first()
    form = SQLFORM(db.Division, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'     
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, ctr_val = ctr_val.div_code)

# ---- Department Master  -----
def dept_mas(): # change to division name
    row = []
    thead = THEAD(TR(TH('ID'),TH('Division Code'),TH('Division Name'),TH('Department Code'),TH('Department Name'),TH('Status'),TH('Actions')))    
    for n in db().select(db.Department.ALL, db.Division.ALL, left = db.Division.on(db.Division.id == db.Department.div_code_id)):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('dept_edit_form', args = n.Department.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('dept_edit_form', args = n.Department.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('dept_edit_form', args = n.Department.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Department.id),TD(n.Division.div_code),TD(n.Division.div_name),
        TD(n.Department.dept_code),TD(n.Department.dept_name),TD(n.Department.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table=table)

def dept_add_form():
    pre = db(db.Prefix_Data.prefix == 'DEP').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Department.id).count()
    ctr = ctr+1
    ctr = str(ctr).rjust(2, '0')
    ctr_val = pre.prefix+ctr    
    form = SQLFORM.factory(
        Field('div_code_id', 'reference Division', label='Division Code',requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division')),
        Field('dept_code', label = 'Department Code', default = ctr_val),
        Field('dept_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.dept_name')]),
        Field('order_qty', 'integer', default = 40),
        Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'NEW RECORD SAVE'
        db.Department.insert(div_code_id = form.vars.div_code_id,dept_code=ctr_val,dept_name=form.vars.dept_name,status_id=form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form=form, ctr_val = ctr_val)

def dept_edit_form():
    ctr_val = db(db.Department.id == request.args(0)).select(db.Department.dept_code).first()
    form = SQLFORM(db.Department, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form, ctr_val = ctr_val.dept_code)

# ---- Item Status Master       -----
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

def stat_add_form():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

def stat_edit_form():
    form = SQLFORM(db.Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'    
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Record Status Master  -----
def recst_mas():
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Record_Status.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('recst_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table table-hover')
    return dict(form = form, table = table)

def recst_add_form(): # to remove
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

def recst_edit_form():
    db.Record_Status.id.readable = False
    form = SQLFORM(db.Record_Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)


# ---- Made In Master  -----
def sec_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Section Code'),TH('Section Name'),TH('Status'),TH()))    
    for n in db(db.Section).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sec_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.section_code),TD(n.section_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')    
    return dict(table = table)

def sec_add_form():
    pre = db(db.Prefix_Data.prefix == 'SEC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Section).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2,'0')
    ctr_val = pre.prefix + ctr    
    form = SQLFORM.factory(
        Field('section_name','string',length=25, requires = [IS_UPPER(), IS_LENGTH(25), IS_NOT_IN_DB(db, 'Section.section_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Section.insert(section_code = ctr_val,section_name = form.vars.section_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form, ctr_val = ctr_val)

def sec_edit_form():
    ctr_val = db(db.Section.id == request.args(0)).select(db.Section.section_code).first()
    form = SQLFORM(db.Section, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.section_code)

# ---- Transaction Master -----
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
def gndr_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Gender Code'),TH('Gender Name'),TH('Status'),TH('Action')))
    for n in db(db.Gender).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('gndr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled  ', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(n.id),TD(n.gender_code),TD(n.gender_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

def gndr_add_form():
    pre = db(db.Prefix_Data.prefix == 'GNC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Gender).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2,'0')
    ctr_val = pre.prefix + ctr        
    form = SQLFORM.factory(
        Field('gender_name', 'string', length = 10,requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Gender.gender_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Gender.insert(gender_code = ctr_val, gender_name = form.vars.gender_name, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form, ctr_val = ctr_val)

def gndr_edit_form():
    ctr_val = db(db.Gender.id == request.args(0)).select(db.Gender.gender_code).first()
    form = SQLFORM(db.Gender, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.gender_code)

# ---- Location Group Master   -----
def locgrp_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Group Code'),TH('Group Name'),TH('Status'),TH('Action')))
    for n in db(db.Location_Group).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('locgrp_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(n.id),TD(n.location_group_code),TD(n.location_group_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

def locgrp_add_form():
    pre = db(db.Prefix_Data.prefix == 'LGC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Location_Group).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2,'0')
    ctr_val = pre.prefix + ctr 
    form = SQLFORM.factory(
        Field('location_group_name','string',length=50, requires = [IS_UPPER(), IS_LENGTH(50),IS_NOT_IN_DB(db, 'Location_Group.location_group_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status'))) 
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Location_Group.insert(location_group_code = ctr_val, location_group_name = form.vars.location_group_name, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val)

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
def loc_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Location Group Code'),TH('Location Group Name'),TH('Location Code'),TH('Location Name'),TH('Status'),TH('Action')))
    for n in db(db.Location).select(db.Location.ALL, db.Location_Group.ALL, 
    left= db.Location_Group.on(db.Location_Group.id == 3)):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#'))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('loc_edit_form', args = n.Location.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#'))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(
            TD(n.Location.id),
            TD(n.Location_Group.location_group_code),
            TD(n.Location_Group.location_group_name),
            TD(n.Location.location_code),
            TD(n.Location.location_name),
            TD(n.Location.status_id.status),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

def loc_add_form():
    pre = db(db.Prefix_Data.prefix == 'LOC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Location).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(4,'0')
    ctr_val = pre.prefix + ctr        
    form = SQLFORM.factory(
        Field('location_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),
        Field('location_group_code_id','reference Location_Group', label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1,  requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Location.insert(location_code = ctr_val, location_name = form.vars.location_name, location_group_code_id = form.vars.location_group_code_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'please fill up the form'

    return dict(form = form, ctr_val = ctr_val)

def loc_edit_form():
    ctr_val = db(db.Location.id == request.args(0)).select(db.Location.location_code).first()
    form = SQLFORM(db.Location, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.location_code)

# ---- Fragrance Type Master  -----  
def frgtype_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Product Code'),TH('Fragrance Code'),TH('Fragrance Name'),TH('Status'),TH('Action')))
    for n in db(db.Fragrance_Type).select():
        edit_lnk = A('Edit', _href=URL('frgtype_edit_form', args = n.id ))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('frgtype_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        row.append(TR(TD(n.id),TD(n.product_code_id.product_code),TD(n.fragrance_code),TD(n.fragrance_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')        
    return dict(table = table)

def frgtype_add_form():
    pre = db(db.Prefix_Data.prefix == 'FRC').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Fragrance_Type).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(3, '0')
    ctr_val = pre.prefix + ctr        
    form = SQLFORM.factory(
        Field('product_code_id','reference Product', requires = IS_IN_DB(db(db.Product.product_name.startswith('FRAG')), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('fragrance_name','string',length=35, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Fragrance_Type.fragrance_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Fragrance_Type.insert(product_code_id = form.vars.product_code_id,fragrance_code = ctr_val,fragrance_name = form.vars.fragrance_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form, ctr_val = ctr_val)

def frgtype_edit_form():
    ctr_val = db(db.Fragrance_Type.id == request.args(0)).select().first()
    form = SQLFORM(db.Fragrance_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.fragrance_code)

# ---- Voucher Master   -----
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
    _id = 0
    db.Stock_Request.item_status_code_id.writable = False
    db.Stock_Request.stock_request_no.writable = True
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.approved_by.writable = False
    db.Stock_Request.stv_no.writable = False
    db.Stock_Request.stv_date.writable = False
    db.Stock_Request.stv_prepared_by.writable = False
    db.Stock_Request.stv_status.writable = False
    db.Stock_Request.src_no.writable = False
    db.Stock_Request.src_date.writable = False
    db.Stock_Request.src_prepared_by.writable = False
    db.Stock_Request.src_status.writable = False
    db.Stock_Transaction.remarks.writable = False
    # form = SQLFORM.factory(db.Stock_Request, db.Stock_Transaction)
    # if form.accepts(request.vars):
    #     id = db.Stock_Request.insert(**db.Stock_Request._filter_fields(form.vars))
    #     form.vars.stock_request_id=id
    #     id = db.Stock_Transaction.insert(**db.Stock_Transaction._filter_fields(form.vars))
    #     response.flash='Thanks for filling the form'
    
    # form1 = SQLFORM.factory(db.Stock_Request)
    # if form1.accepts(request, formname = None):
        
        
    # form = SQLFORM(db.Stock_Request)
    # if form.process().accepted:
    form = SQLFORM(db.Stock_Transaction)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict()


def testing2():
    row = []
    thead = THEAD(TR(TH('#'),TH('Request Date'),TH('Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Status'),TH('Action')))
    for n in db((db.Stock_Request.stock_request_no.startswith('SRN')) & (db.Stock_Request.requested_by == auth.user)).select():
        tran_lnk = A(I(_class='fas fa-warehouse'), _title='Transaction Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stk_req_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _onclick = "jQuery(show)", _class='btn btn-icon-toggle', _callback =URL('#', args = n.id),**{'_data-id':(n.id)} )
        btn_lnk = DIV(tran_lnk, view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.stock_request_date),TD(n.stock_request_no),TD(n.stock_source_id),TD(n.stock_destination_id.location_name),TD(n.srn_status_id.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')        
    return dict(table = table)    
    
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
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),TD(k.Item_Prices.retail_price, _align='right'),TD(k.Stock_Transaction_Temp.amount, _align='right'),TD(),TD(btn_lnk)))
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
    for n in db(db.Item_Master.dept_code_id == 3).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), 
    db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)]):
        row.append(TR(TD(n.Item_Master.id),TD(n.Item_Master.item_code),TD(n.Item_Master.group_line_id.group_line_name),TD(n.Item_Master.brand_line_code_id.brand_line_name),TD(n.Item_Master.item_description),TD(n.Item_Prices.retail_price),TD(n.Item_Master.uom_value),TD(n.Stock_File.opening_stock),TD(n.Stock_File.stock_in_transit),TD(n.Stock_File.probational_balance)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return table

def stk_req_trns():
    form = SQLFORM(db.Stock_Transaction)
    if form.accepts(request, formname = None):
        return TABLE(*[TR(t.item_code_id) for i in db(db.Stock_Transaction).select(orderby=~db.Stock_Transaction.item_code_id)])
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
def stk_req_form():
    row = []
    thead = THEAD(TR(TH('#'),TH('Request Date'),TH('Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Status'),TH('Action')))
    for n in db((db.Stock_Request.stock_request_no.startswith('SRN')) & (db.Stock_Request.requested_by == auth.user)).select():
        tran_lnk = A(I(_class='fas fa-warehouse'), _title='Transaction Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stk_req_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(tran_lnk, view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.stock_request_date),TD(n.stock_request_no),TD(n.stock_source_id),TD(n.stock_destination_id.location_name),TD(n.srn_status_id.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')        
    return dict(table = table)

def stk_req_val_form(form):
    ctr = db(db.Stock_Request.stock_request_no).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5, '0')
    ctr_val = 'SRN' + ctr            
    form.vars.stock_request_no = ctr_val

def del_item():
    db(db.Stock_Transaction_Temp.id == request.args(0)).delete()
    # response.js =  "$('#tblIC').get(0).reload()" 

def stk_file():
    form = SQLFORM(db.Stock_File)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ERROR'
    return dict(form = form)

def dups(form):
    # _item_code_id = db((db.Stock_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Transaction_Temp.item_code_id == request.vars.item_code_id)).select().first()
    _item_code_id = db(db.Stock_Transaction_Temp.item_code_id == request.vars.item_code_id).select(db.Stock_Transaction_Temp.item_code_id).first()
    if _item_code_id:
        form.errors.item_code_id = ' already exist!'        
    else:
        response.flash = 'inserted'

def itm_view():
    import locale
    row = []
    uom_value = 0
    retail_price_value = 0
    total_pcs = 0    
    ctr = db(db.Stock_Transaction_Temp).count()        
    form = SQLFORM(db.Stock_Transaction_Temp)
    if form.accepts(request, formname=None, onvalidation = dups, hideerror=True):     
        uom = db(db.Item_Master.id == request.vars.item_code_id).select(db.Item_Master.uom_value).first()
        rpv = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select(db.Item_Prices.retail_price).first()
        total_pcs = (int(request.vars.quantity) * int(uom.uom_value)) + int(request.vars.pieces)  
        unit_price = int(rpv.retail_price) / int(uom.uom_value)      
        total_amount_value = int(unit_price) * int(total_pcs)
        _id = db(db.Stock_Transaction_Temp.item_code_id == request.vars.item_code_id).select().first()
        _id.amount = total_amount_value
        _id.update_record()        
        
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        grand_total = db().select(total).first()[total]
                
        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
            ctr += 1            
            edit_lnk = A(SPAN(_class='fas fa-pencil-alt'), _title='Edit Row', callback=URL(args = k.Stock_Transaction_Temp.id), _class='edit')
            dele_lnk = A('Delete', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))
            # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', _href=URL(args = k.Stock_Transaction_Temp.id))
            # dele_lnk = A(SPAN(_class = 'fas fa-trash-alt'), _name='btndel',_title="Delete", callback=URL(args=k.Stock_Transaction_Temp.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id)})
            btn_lnk = DIV(edit_lnk, dele_lnk, _class="hidden-sm action-buttons")
            row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),TD(k.Item_Prices.retail_price, _align='right'),TD(k.Stock_Transaction_Temp.amount, _align='right'),TD(),TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
        return table

    elif form.errors:
        # ctr = 0
        # row = []        
        # head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        # for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        #     ctr += 1            
        #     edit_lnk = A(SPAN(_class='fas fa-pencil-alt'), _title='Edit Row', callback=URL(args = k.Stock_Transaction_Temp.id), _class='edit')
        #     # dele_lnk = A(SPAN(_class = 'fas fa-trash-alt'), _name='btndel',_title="Delete", callback=URL(args=k.Stock_Transaction_Temp.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id)})
        #     dele_lnk = A('Delete', callback=URL('del_item', args = k.Stock_Transaction_Temp.id  ), delete = 'tr')
        #     # dele_lnk = A(SPAN(_class = 'fas fa-trash-alt'), _name='btndel',_title="Delete", callback=URL( args=k.Stock_Transaction_Temp.id),_class='delete')
        #     # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', _href=URL(args = k.Stock_Transaction_Temp.id))
        #     btn_lnk = DIV(edit_lnk, dele_lnk, _class="hidden-sm action-buttons")
        #     row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),TD(k.Item_Prices.retail_price, _align='right'),TD(k.Stock_Transaction_Temp.amount, _align='right'),TD(),TD(btn_lnk)))
        # body = TBODY(*row)
        # foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        # table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
        response.flash = 'item code already exist!'
        table = TABLE(*[TR(k, v) for k, v in form.errors.items()])
        return table

        # return TABLE(*[TR(k, v) for k, v in form.errors.items()])

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

def month_input():
    return dict()

# def month_selector():
#     if not request.vars.month: return ''
#     months = ['January', 'February', 'March', 'April', 'May',
#               'June', 'July', 'August', 'September' ,'October',
#               'November', 'December']
#     month_start = request.vars.month.capitalize()
#     selected = [m for m in months if m.startswith(month_start)]
#     return DIV(*[DIV(k,
#                      _onclick="jQuery('#month').val('%s')" % k,
#                      _onmouseover="this.style.backgroundColor='yellow'",
#                      _onmouseout="this.style.backgroundColor='white'"
#                      ) for k in selected])
def month_selector():
    if not request.vars.month:
        return ''
    pattern = request.vars.month.capitalize() + '%'
    selected = [row.name for row in db(db.month.name.like(pattern)).select()]
    return ''.join([DIV(k,
                 _onclick="jQuery('#month').val('%s')" % k,
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white'"
                 ).xml() for k in selected])    

def itm_select():
    if not request.vars.item_code_id:
        return ''
    pattern = request.vars.item_code_id.capitalize() + '%'
    selected = [row.item for row in db(db.Item_Master.item_code.like(pattern)).select()]
    return ''.join([DIV(k,
                 _onclick="jQuery('#month').val('%s')" % k,
                 _onmouseover="this.style.backgroundColor='yellow'",
                 _onmouseout="this.style.backgroundColor='white'"
                 ).xml() for k in selected])

def stk_req_add_form():    
    import datetime
    ctr = db(db.Stock_Request.stock_request_no).count()
    ctr = ctr + 1    
    ctr = str(ctr).rjust(5, '0')
    ctr_val = 'SRN' + ctr                
    form = SQLFORM.factory(        
        Field('stock_request_date', 'date', default = datetime.date.today()),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
        Field('stock_due_date','date', default = datetime.date.today()),
        Field('remarks','string'),
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'reference Transaction_Item_Category', default = 4, requires = IS_IN_DB(db((db.Transaction_Item_Category.mnemonic != 'E') & (db.Transaction_Item_Category.mnemonic != 'S')), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')),
        Field('srn_status_id','reference Stock_Status', default = 3, requires = IS_IN_DB(db(db.Stock_Status.id == 3), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))

    if form.process().accepted:  
        response.flash = 'RECORD SAVE'       
        # db.Stock_Request.insert(
        #     stock_request_no = ctr_val,
        #     stock_request_date = datetime.date.today(),
        #     stock_due_date = form.vars.stock_due_date,
        #     dept_code_id = form.vars.dept_code_id,
        #     stock_source_id = form.vars.stock_source_id,
        #     stock_destination_id = form.vars.stock_destination_id,
        #     srn_status_id = form.vars.srn_status_id,
        #     requested_by = auth.user_id,
        #     remarks = form.vars.remarks)
        # _id = db(db.Stock_Request).select().last()

    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form,  ctr_val = ctr_val)


def data():
    

    # if not session.m or len(session.m)==10: session.m=[]
    if request.vars.q: session.m.append(request.vars.q)
    session.m.sort()
    return TABLE(*[TR(v) for v in session.m]).xml()



def validate_tail(form):
    response.flash = 'SAVE FIRST HEAD'
def dept_code_id_json():
    dept = db(db.Department).select()
    return dict(dept = dept)

def stk_req_edit_form():
    db.Stock_Request.stv_no.writable = False
    db.Stock_Request.stv_date.writable = False
    db.Stock_Request.stv_prepared_by.writable = False
    db.Stock_Request.stv_status.writable = False
 
    db.Stock_Request.src_no.writable = False
    db.Stock_Request.src_date.writable = False
    db.Stock_Request.src_prepared_by.writable = False
    db.Stock_Request.src_status.writable = False

    db.Stock_Request.stv_no.readable = False
    db.Stock_Request.stv_date.readable = False
    db.Stock_Request.stv_prepared_by.readable = False
    db.Stock_Request.stv_status.readable = False
 
    db.Stock_Request.src_no.readable = False
    db.Stock_Request.src_date.readable = False
    db.Stock_Request.src_prepared_by.readable = False
    db.Stock_Request.src_status.readable = False    

    form = SQLFORM(db.Stock_Request, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)
# ---- Stock Transaction Master   -----
def stk_trn_add_form():
    return dict()
def stk_tns_form():
    row = []
    thead = THEAD(TR(TH('#'),TH('Transaction No'),TH('Transaction Date'),TH('Prepared By'),TH('Status'),TH('Action')))
    for n in db((db.Stock_Request.stv_no.startswith('STN')) & (db.Stock_Request.requested_by == db.auth_user)).select(db.Stock_Request.ALL):
   
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stk_tns_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        row.append(TR(TD(n.id),TD(n.stv_no),TD(n.stv_date),TD(n.stv_prepared_by),TD(n.stv_status),TD(btn_lnk)))
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

def stk_rpt():
    return locals()

def itm_price():
    form = SQLFORM(db.Item_Prices)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)
def register_person():
    # create an insert form from the table
    form = SQLFORM(db.person).process()

    # if form correct perform the insert
    if form.accepted:
        response.flash = 'new record inserted'

    # and get a list of all persons
    records = SQLTABLE(db().select(db.person.ALL),headers='fieldname:capitalize')

    return dict(form=form, records=records)
def register_product():
    form = SQLFORM(db.product).process()
    if form.accepted:
        response.flash = 'new record inserted'
    records = SQLTABLE(db().select(db.product.ALL),
                       upload = URL('download'), # allows pics preview
                       headers='fieldname:capitalize')
    return dict(form=form, records=records)

def buy():
    form = SQLFORM.factory(
        Field('buyer_id',requires=IS_IN_DB(db,db.person.id,'%(name)s')),
        Field('product_id',requires=IS_IN_DB(db,db.product.id,'%(name)s')),
        Field('quantity','integer',requires=IS_INT_IN_RANGE(1,100))).process()
    if form.accepted:
        # get previous purchase for same product
        purchase = db((db.purchase.buyer_id == form.vars.buyer_id)&
            (db.purchase.product_id==form.vars.product_id)).select().first()

        if purchase:
            # if list contains a record, update that record
            purchase.update_record(
                quantity = purchase.quantity+form.vars.quantity)
        else:
            # self insert a new record in table
            db.purchase.insert(buyer_id=form.vars.buyer_id,
                               product_id=form.vars.product_id,
                               quantity=form.vars.quantity)
        response.flash = 'product purchased!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    # now get a list of all purchases
    records = SQLTABLE(db(purchased).select(),headers='fieldname:capitalize')
    return dict(form=form, records=records)
