
# ---- Product Master  -----
def prod_view():

    return dict()

def prod_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Department'),TH('Product Code'),TH('Product Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Department.ALL, db.Product.ALL, left=db.Department.on(db.Department.id == db.Product.dept_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _href=URL('prod_edit_form', args = n.Product.id),_type='button', _class='btn btn-icon-toggle', **{'_data-toggle':'tooltip', '_data-placement':'top', '_data-original-title':'View Row'})
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row',_href=URL('prod_edit_form', args = n.Product.id),_type='button  ', _role='button', _class='btn btn-icon-toggle')
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _href=URL('prod_edit_form', args = n.Product.id),_type='button', _class='btn btn-icon-toggle', **{'_data-toggle':'tooltip', '_data-placement':'top', '_data-original-title':'Delete Row'})
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Product.id),TD(n.Department.dept_name),TD(n.Product.product_code),TD(n.Product.product_name),TD(n.Product.status_id.status),TD(btn_lnk)))
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
        Field('product_code','string', default = ctr_val, readable = True,required=False),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
        Field('product_name', 'string', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name', error_message = 'Record already exist or empty.')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'NEW RECORD SAVED'
        db.Product.insert(dept_code_id=form.vars.dept_code_id, product_code = ctr_val, product_name = form.vars.product_name, status_id = form.vars.status_id, created_by = auth.user_id, created_on = request.now)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val=ctr_val)

def prod_edit_form():
    ctr_val = db(db.Product.id == request.args(0)).select().first()
    form = SQLFORM(db.Product, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'        
    elif form.errors:
        response.flash = 'MISSING INFORMATION'        
    else:
        response.flash = 'please update the form'
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
    #     response.flash = 'form accepted'
    #     db.SubProduct.insert(
    #         dept_code_id = request.vars.dept_code_id,
    #         product_code_id = request.vars.product_code_id, 
    #         subproduct_code = ctr_val, 
    #         subproduct_name = form.vars.subproduct_name, 
    #         status_id = form.vars.status_id,
    #         created_on = request.now,
    #         created_by = auth.user_id)            
    # elif form.errors:
    #     response.flash = 'form has errors'
    # else:
    #     response.flash = 'please fill out the form'
    # grid = SQLFORM.grid(db.SubProduct)
    row = []
    thead = THEAD(TR(TH('#'),TH('Product Name'),TH('Product Code'),TH('Sub-Product Name'),TH('Sub-Product Code'),TH('Status'),TH('Action')))
    for n in db(db.SubProduct).select(db.Product.ALL, db.SubProduct.ALL, left=db.Product.on(db.Product.id == db.SubProduct.product_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.SubProduct.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('subprod_edit_form', args = n.SubProduct.id))
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.SubProduct.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        # edit_lnk = A('Edit', _href = URL('subprod_edit_form',args = n.SubProduct.id))
        row.append(TR(TD(n.SubProduct.id),TD(n.Product.product_name),TD(n.Product.product_code),
        TD(n.SubProduct.subproduct_name),TD(n.SubProduct.subproduct_code),TD(n.SubProduct.status_id.status),TD(btn_lnk)))
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
        Field('dept_code_id','reference Department', label = 'Department',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s', zero = 'Choose Product Code')),
        Field('subproduct_name','string', requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.SubProduct.insert(dept_code_id = request.vars.dept_code_id,product_code_id = request.vars.product_code_id, subproduct_code = ctr_val, subproduct_name = form.vars.subproduct_name, status_id = form.vars.status_id,created_on = request.now,created_by = auth.user_id)            
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def subprod_edit_form():
    ctr_val = db(db.SubProduct.id == request.args(0)).select().first()
    form = SQLFORM(db.SubProduct, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form updated'        
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please update the form'
    return dict(form = form, ctr_val = ctr_val.subproduct_code)
    
# ---- Supplier Master  -----
def suplr_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Supplier Name'),TH('Supplier Type'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Master).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#", _title='View Row', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _target="#", _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sply_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        addr_lnk = A(I(_class='fas fa-address-card'), _target="#", _title='Address', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_form', args = n.id))
        paym_lnk = A(I(_class='fas fa-list'), _target="#", _title='Payment Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_paymod_form', args = n.id))
        bank_lnk = A(I(_class='fas fa-money-check-alt'),_target="#", _title='Bank Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        othr_lnk = A(I(_class='fas fa-address-book'),_target="#", _title='Other Address', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        dept_lnk = A(I(_class='fas fa-building'), _target="#",_title='Department', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_dept_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, addr_lnk, paym_lnk, bank_lnk, othr_lnk, dept_lnk) 
        row.append(TR(TD(n.id),TD(n.supp_code),TD(n.supp_name),TD(n.supplier_type),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover')
    return dict(table = table)

def suplr_view_form():    

    return dict()

def suplr_addr_form():     
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('contact_person', 'string', length=30, requires = IS_UPPER()),
        Field('address_1','string', length = 50, requires = IS_UPPER()),
        Field('address_2','string', length = 50, requires = IS_UPPER()),
        Field('country_id','string',label = 'Country',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Supplier_Contact_Person.insert(supplier_id = request.args(0),contact_person = form.vars.contact_person, address_1 = form.vars.address_1, address_2 = form.vars.address_2,country_id = form.vars.country_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form '
    row = []
    thead = THEAD(TR(TH('#'),TH('Contact Person'),TH('Address'),TH('Country'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Contact_Person.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sply_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.contact_person),TD(n.address_1),TD(n.country_id),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, supplier_id = supplier_id.supp_name, table = table)

def suplr_dept_form():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Supplier_Master_Department.insert(supplier_id = request.args(0),dept_code_id = form.vars.dept_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    row = []
    thead = THEAD(TR(TH('#'),TH('Department'),TH('Status'),TH('Action')))  
    for n in db(db.Supplier_Master_Department.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sply_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')                  
    return dict(form = form, supplier_id = supplier_id.supp_name, table = table)

def suplr_paymod_form():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('payment_mode','string',length=30),
        Field('payment_terms','string',length=30),
        Field('currency','string',length=20),
        Field('trade_terms','string',length=20),
        Field('forwarder_air','string',length=20),
        Field('forwarder_sea','string',length=20),
        Field('commodity_code','string',length=10),
        Field('discount_percentage','string',length=10),
        Field('custom_duty_percentage','string',length=10),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Supplier_Payment_Mode.insert(supplier_id = request.args(0),payment_mode = form.vars.payment_mode,payment_terms = form.vars.payment_terms,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    row = []
    thead = THEAD(TR(TH('#'),TH('Payment Mode'),TH('Payment Terms'),TH('Currency'),TH('Trade Terms'),TH('Forwarder Air'),TH('Forwarder Sea'),TH('Payment Mode'),TH('Status'),TH('Action')))  
    for n in db(db.Supplier_Payment_Mode.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sply_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.dept_code_id.dept_name),TD(),TD(),TD(),TD(),TD(),TD(),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')                  
    return dict(form = form, supplier_id = supplier_id.supp_name, table = table)

def suplr_add_group_form():
    pre = db(db.Prefix_Data.prefix == 'SUP').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Supplier_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM(db.Supplier_Master)    
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Supplier_Master.insert(supp_code = form.vars.supp_code,supp_name = form.vars.supp_name)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'     
    spm_form = SQLFORM(db.Supplier_Payment_Mode)
    if spm_form.process().accepted:
        response.flash = 'form accepted'
    elif spm_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, spm_form = spm_form, ctr_val = ctr_val) 

def suplr_add_form():
    pre = db(db.Prefix_Data.prefix == 'SUP').select(db.Prefix_Data.prefix).first()
    ctr = db(db.Supplier_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_val = pre.prefix + ctr
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
        Field('supp_name','string',length=50,requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Supplier_Master.supp_name')]),
        Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL'], zero = 'Choose Type')), # foriegn or local supplier
        Field('contact_person', 'string', length=30, requires = IS_UPPER()),
        Field('address_1','string', length = 50, requires = IS_UPPER()),
        Field('address_2','string', length = 50, requires = IS_UPPER()),    
        Field('country_id','string',label = 'Country',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
        Field('contact_no','string', length=50, requires = IS_UPPER()),
        Field('fax_no','string', length=50, requires = IS_UPPER()),
        Field('email_address','string', length=50, requires = IS_UPPER()),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))    
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Supplier_Master.insert(dept_code_id, form.vars.dept_code_id, supp_code = ctr_val, supp_name = form.vars.supp_name, suppliet_type = form.vars.supplier_type,
        contact_person = form.vars.contact_person,
        address_1 = form.vars.address_1, 
        address_2 = form.vars.address_2,
        country_id = form.vars.country_id,
        contact_no = form.vars.contact_no,
        fax_no = form.vars.fax_no,
        email_adddress = form.vars.email_address,
        status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'  
    return dict(form = form, ctr_val = ctr_val)  

def sply_edit_form():
    ctr_val = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'please fill out the form'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val.supp_code)

# ---- GroupLine Master  -----
def groupline_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Group Line Code'),TH('Group Line Name'),TH('Status'),TH('Actions')))
    query = db(db.GroupLine).select()
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('groupline_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        supp_lnk = A(I(_class='fas fa-store-alt'), _title='Go To Supplier(s)', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='#', _href=URL('sbgplne_lnk', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, supp_lnk)
        row.append(TR(TD(n.id),TD(n.group_line_code),TD(n.group_line_name),TD(n.status_id.status),TD(btn_lnk)))
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
        response.flash = 'form accepted'
        db.GroupLine.insert(supplier_id = form.vars.supplier_id,group_line_code = ctr_val, group_line_name = form.vars.group_line_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val)

def groupline_edit_form():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()
    form = SQLFORM(db.GroupLine, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val.group_line_code)

def sbgplne_lnk():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()    
    _id = db(db.GroupLine.id == request.args(0)).select().first()
    session.id = _id
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Sub_Group_Line.insert(group_line_code_id = ctr_val,supplier_code_id = form.vars.supplier_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

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
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

def sbgplne_lnk_add_form():
    ctr_val = db(db.GroupLine.id == session.id).select().first()
    sub_grp_lne_id = db(db.Sub_Group_Line.group_line_code_id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Sub_Group_Line.insert(group_line_code_id = ctr_val,supplier_code_id = form.vars.supplier_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
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
        response.flash = 'form accepted'
        db.Brand_Line.insert(group_line_id = form.vars.group_line_id,brand_line_code = ctr_val,brand_line_name = form.vars.brand_line_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val)
def brndlne_edit_form():
    ctr_val = db(db.Brand_Line.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Line, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form updated'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'    
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
        response.flash = 'form accepted'
        db.Brand_Classification.insert(brand_line_code_id = form.vars.brand_line_code_id,brand_cls_code = ctr_val,brand_cls_name = form.vars.brand_cls_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def brndclss_edit_form():
    ctr_val = db(db.Brand_Classification.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Classification, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val.brand_cls_code)


# ---- Item Color Master  -----
def itmcol_mas():
    pre = db(db.Prefix_Data.id == 4).select(db.Prefix_Data.prefix).first()
    ctr = db(db.Item_Color).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2, '0')
    ctr_value = pre.prefix + ctr
    # form = SQLFORM(db.Item_Color)
    form = SQLFORM.factory(
        Field('color_code','string',default = ctr_value),
        Field('color_name','string',length=25),
        Field('status_id','reference Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Item_Color.insert(color_code = ctr_value,color_name = form.vars.color_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Item_Color)
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
    ctr_value = pre.prefix + ctr
    form = SQLFORM.factory(
        Field('size_code','string',default = ctr_value),
        Field('size_name','string',length=25),
        Field('status_id','reference Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Item_Size.insert(size_code = form.vars.size_code,size_name = form.vars.size_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    # grid = SQLFORM.grid(db.Item_Size)

    row = []
    thead = THEAD(TR(TH('ID'),TH('Size Code'),TH('Size Name'),TH('Status'),TH()))
    query = db(db.Item_Size).select()
    for n in query:
        # <a class="btn btn-primary" href="#" role="button">Link</a>
        edit = A(SPAN(_class = 'btn btn-primary'),_title="Edit", _href=URL("default",'itmsze_edit_form', args=n.id ))
        btn_lnks = DIV(edit, _class="hidden-sm hidden-xs action-buttons")
        # <button type="button" class="btn btn-primary btn-sm">Small button</button>
        row.append(TR(TD(n.id),TD(n.size_code),TD(n.size_name),TD(n.status_id.status),TD(btn_lnks)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    

    return dict(form=form, grid=table)

def itmsze_edit_form():
    form = SQLFORM(db.Item_Size, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
        # redirect(URL('default','itmsze_mas'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

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
        response.flash = 'form accepted'
        db.Item_Collection.insert(collection_code = form.vars.collection_code,collection_name = form.vars.collection_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
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
        response.flash = 'form accepted'
        # redirect(URL('default','itmcoll_mas'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)
# ---- Made In Master  -----
def mdein_mas():
    form = SQLFORM(db.Made_In)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Made_In)
    return dict(form=form, grid=grid)

# ---- Brand Master      -----
def brand_mas():
    form = SQLFORM(db.brandmas)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)


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
        response.flash = 'form accepted'
        # fnd = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()
        # itm_code = fnd.supp_code[-5:]+'-'+ctr
        # db.Itemmas.insert(supplier_code_id = form.vars.supplier_code_id, item_code = itm_code)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'    

    grid = SQLFORM.grid(db.FMCG_Division)
    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Item Code'),TH('Action')))    
    for n in db(db.FMCG_Division).select():
        edit_lnk = A('Edit', _href = URL('fmcg_edit_form', args = n.id))
        row.append(TR(TD(n.id),TD(n.supplier_code_id.supp_code),TD(n.item_code),TD(edit_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')   
    return dict(form=form, grid = grid)

def fmcg_edit_form():
    form = SQLFORM(db.FMCG_Division, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
        # redirect(URL('fmcg_form'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

def fmcg_grid():
    q_dept = db(db.Department.div_code_id == 2).select()
    form = SQLFORM.factory( 
        # Field('div_code_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('item_code', 'string', length = 15, label = 'Item Code',requires = IS_NOT_IN_DB(db, 'FMCG_Division.item_code')),
        Field('item_description', 'string', length = 35, label = 'Description'),    
        # Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db(db.Department.div_code_id == 2).select(db.Department.dept_code, db.Department.dept_name, db.Department.id),'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
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
        response.flash = 'form accepted'
        # redirect(URL('fmcg_form'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier'),TH('Ref.No.'),TH('Item Code'),TH('Item Description'),TH('Actions',_class='text-right')))
    for f in db(db.FMCG_Division).select():        
        edit_lnk = A('Edit', _href = URL('fmcg_edit_form', args = f.id))
        row.append(TR(TD(f.id),TD(f.supplier_code_id.supp_code),TD(f.ref_no),TD(f.item_code),TD(f.item_description),TD(edit_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table = table)


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
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

def edit_pre_form():
    form = SQLFORM(db.Prefix_Data, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form updated',
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'form has errors'    
    return dict(form = form)

# ---- Division Master       -----
def div_err(form):
    return "jQuery('[href='#tab1']').tab('show');"

def div_mas():    
    grid = SQLFORM.grid(db.Division)
    row = []
    thead = THEAD(TR(TH('#'),TH('Code'),TH('Name'),TH('Status'),TH('Action')))
    for n in db(db.Division).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('div_edit_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('div_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('div_edit_form', args = n.id))
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
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'   
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def div_edit_form():
    ctr_val = db(db.Division.id == request.args(0)).select(db.Division.div_code).first()
    form = SQLFORM(db.Division, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form updated'     
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please update the form'
    return dict(form = form, ctr_val = ctr_val.div_code)

# ---- Department Master  -----
def dept_mas():
    row = []
    thead = THEAD(TR(TH('ID'),TH('Division Code'),TH('Department Code'),TH('Department Name'),TH('Status'),TH('Actions')))    
    for n in db(db.Department).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('dept_edit_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('dept_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('dept_edit_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.div_code_id.div_code),TD(n.dept_code),TD(n.dept_name),TD(n.status_id.status),TD(btn_lnk)))
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
        Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Department.insert(div_code_id = form.vars.div_code_id,dept_code=form.vars.dept_code,dept_name=form.vars.dept_name,status_id=form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def dept_edit_form():
    ctr_val = db(db.Department.id == request.args(0)).select(db.Department.dept_code).first()
    form = SQLFORM(db.Department, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val.dept_code)

# ---- Item Status Master       -----
def stat_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Status.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stat_edit_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stat_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stat_edit_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')
    return dict(table = table)

def stat_add_form():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

def stat_edit_form():
    form = SQLFORM(db.Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'    
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

# ---- Record Status Master  -----
def recst_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Record_Status.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('recst_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table table-hover')
    return dict(table = table)

def recst_add_form():
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form)

def recst_edit_form():
    db.Record_Status.id.readable = False
    form = SQLFORM(db.Record_Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'        
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please update the form'
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
        response.flash = 'form accepted'
        db.Section.insert(section_code = ctr_val,section_name = form.vars.section_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def sec_edit_form():
    ctr_val = db(db.Section.id == request.args(0)).select(db.Section.section_code).first()
    form = SQLFORM(db.Section, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val.section_code)

# ---- Transaction Master -----
def trans_mas():
    form = SQLFORM(db.trnmas)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

# ---- Gender Master   -----
def gndr_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Gender Code'),TH('Gender Name'),TH('Status'),TH('Action')))
    for n in db(db.Gender).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('gndr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
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
        response.flash = 'form accepted'
        db.Gender.insert(gender_code = ctr_val, gender_name = form.vars.gender_name, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def gndr_edit_form():
    ctr_val = db(db.Gender.id == request.args(0)).select(db.Gender.gender_code).first()
    form = SQLFORM(db.Gender, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
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
        response.flash = 'form accepted'
        db.Location_Group.insert(location_group_code = ctr_val, location_group_name = form.vars.location_group_name, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please update the form'
    return dict(form = form, ctr_val = ctr_val)

def locgrp_edit_form():
    ctr_val = db(db.Location_Group.id == request.args(0)).select(db.Location_Group.location_group_code).first()
    form = SQLFORM(db.Location_Group, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please update the form'
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
        response.flash = 'form accepted'
        db.Location.insert(location_code = ctr_val, location_name = form.vars.location_name, location_group_code_id = form.vars.location_group_code_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill up the form'

    return dict(form = form, ctr_val = ctr_val)

def loc_edit_form():
    ctr_val = db(db.Location.id == request.args(0)).select(db.Location.location_code).first()
    form = SQLFORM(db.Location, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please update the form'
    return dict(form = form, ctr_val = ctr_val.location_code)

# ---- Fragrance Type Master  -----  
def frgtype_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Product Code'),TH('Fragrance Code'),TH('Fragrance Name'),TH('Status'),TH('Action')))
    for n in db(db.Fragrance_Type).select():
        edit_lnk = A('Edit', _href=URL('frgtype_edit_form', args = n.id ))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('frgtype_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
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
        Field('product_code_id','reference Product', requires = IS_IN_DB(db(db.Product.dept_code_id == 3), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('fragrance_name','string',length=35, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Fragrance_Type.fragrance_name')]),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Fragrance_Type.insert(product_code_id = form.vars.product_code_id,fragrance_code = ctr_val,fragrance_name = form.vars.fragrance_name,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, ctr_val = ctr_val)

def frgtype_edit_form():
    ctr_val = db(db.Fragrance_Type.id == request.args(0)).select().first()
    form = SQLFORM(db.Fragrance_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form = form, ctr_val = ctr_val.fragrance_code)

# ---- Voucher Master   -----
def vouc_mas():
    form = SQLFORM(db.trnvou)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def testing():
    return locals()

def itm_prcs():
    form = SQLFORM(db.Item_Prices)       
    return dict(form = form)

def fmcg_profile():
    form = SQLFORM(db.FMCG_Division, request.args(0))
    return dict(form = form)
def stk_req_form():

    return locals()

def stk_tns_form():
    
    return locals()

def stk_rcpt_form():
    
    return locals()

def stk_rpt():
    return locals()

