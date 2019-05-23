# auth = Auth(db,cas_provider = 'http://127.0.0.1:3000/merch_erp/default/user/cas')

auth = Auth(globals(),db)


# Duplicate Entry error = SAME VALUE ALREADY EXIST OR EMPTY
# error_message = 'Record already exist or empty.'

auth.settings.actions_disabled=['register', 'request_reset_password','retrieve_username']
if request.controller != 'appadmin': auth.settings.actions_disabled +=['register']

db.define_table('Division_Group',
    Field('division_group_name','string',label = 'Division',length = 50, requires = [IS_UPPER(), IS_LENGTH(50), IS_NOT_IN_DB(db,'Division_Group.division_group_name')]))

db.define_table('Department_Group',
    Field('division_group_id','reference Division_Group', ondelete = 'NO ACTION', label = 'Division',requires = IS_IN_DB(db, db.Division_Group.id, '%(division_group_name)s', zero = 'Choose Division')),
    Field('department_group_name','string',label = 'Department', length = 50, requires = [IS_UPPER(), IS_LENGTH(50), IS_NOT_IN_DB(db,'Department_Group.department_group_name')]))

db.define_table('Section_Group',
    Field('department_group_id', 'reference Department_Group', ondelete = 'NO ACTION', label = 'Department', requires = IS_IN_DB(db, db.Department_Group.id,'%(department_group_name)s', zero = 'Choose Department')),
    Field('section_group_name','string',label = 'Section', length = 50, requires = [IS_UPPER(), IS_LENGTH(50), IS_NOT_IN_DB(db, 'Section_Group.section_group_name')]))

db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128),
    Field('last_name', length=128),
    Field('username', unique = True, readable = False),
    Field('email', length=128), # required
    Field('password', 'password', length=512,readable=False, label='Password'), # required
    # Field('division_group_id', 'reference Division_Group', ondelete = 'NO ACTION',label = 'Division',requires = IS_IN_DB(db, db.Division_Group.id, '%(division_group_name)s', zero = 'Choose Division')),
    # Field('department_group_id', 'reference Department_Group', ondelete = 'NO ACTION',label = 'Department', requires = IS_IN_DB(db, db.Department_Group.id,'%(department_group_name)s', zero = 'Choose Department')),
    # Field('section_group_id', 'reference Section_Group', ondelete = 'NO ACTION', label = 'Section', requires = IS_IN_DB(db, db.Section_Group.id,'%(section_group_name)s', zero = 'Choose Section')),
    Field('registration_key', length=512, writable=False, readable=False, default=''),# required
    Field('reset_password_key', length=512,writable=False, readable=False, default=''),# required
    Field('registration_id', length=512, writable=False, readable=False, default=''), format = '%(first_name)s %(last_name)s')# required


# db.auth_user.id.represent = lambda auth_id, row: row.first_name + ' ' + row.last_name
## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
# custom_auth_table.division_id.requires =  IS_IN_DB(db, db.division.id, '%(division)s', zero = 'Choose division')
custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.email.requires =   IS_EMAIL(error_message=auth.messages.invalid_email)

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table
auth.define_tables(username = True)

db.define_table('Status', # Item Master
    Field('status','string',length=20, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(status)s')

db.define_table('Record_Status',
    Field('status','string',length=20, requires = [IS_LENGTH(20),IS_UPPER(), IS_NOT_IN_DB(db, 'Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(status)s')

db.define_table('Prefix_Data',        
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('serial_key', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

db.define_table('Division',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code','string', length = 5, label = 'Division Code', writable = False, requires = IS_NOT_IN_DB(db, 'Division.div_code')),
    Field('div_name','string', length = 50, label = 'Division Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Division.div_name')]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(div_code)s')

db.define_table('Department',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code_id', 'reference Division', ondelete = 'NO ACTION', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('dept_code','string', length = 5, label ='Department Code', writable = False, requires = IS_NOT_IN_DB(db, 'Department.dept_code')),
    Field('dept_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.dept_name')]),
    Field('order_qty', 'integer', default = 40),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(dept_code)s')

db.define_table('Transaction_Prefix',    
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('current_year_serial_key', 'integer'),
    Field('previous_year_serial_key', 'integer', writable = False),
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

db.define_table('Product',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    # Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('div_code_id', 'reference Division', ondelete = 'NO ACTION', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('product_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_code')]), # Field 
    Field('product_name', 'string', length = 50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(product_code)s')

db.define_table('SubProduct',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code_id', 'reference Division', ondelete = 'NO ACTION', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('product_code_id','reference Product', ondelete = 'NO ACTION', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
    Field('subproduct_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_code')]),
    # Field('dept_code_id','reference Department', label = 'Department',requires = IS_IN_DB(db(db.Department.status_id == 1), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('subproduct_name','string', length = 50, requires = [IS_UPPER(),IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(subproduct_code)s')

db.define_table('Made_In',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Currency',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Currency_Exchange',
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id, '%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('exchange_rate_value', 'decimal(10,2)', default = 0),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Forwarder_Supplier',
    Field('forwarder_code','string',length = 5, writable = False),
    Field('forwarder_name','string',length = 50),
    Field('forwarder_type','string',length = 5, requires = IS_IN_SET(['AIR','SEA'], zero = 'Choose Type')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'forwarder_code')

db.define_table('Supplier_Master',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
    Field('supp_code','string', length=10, writable = False),
    Field('supp_sub_code','string', length=10, writable = True, requires = IS_LENGTH(10)),
    Field('supp_name','string',length=50,requires = [IS_UPPER(), IS_LENGTH(50),IS_NOT_IN_DB(db, 'Supplier_Master.supp_name')]),
    Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL'], zero = 'Choose Type')), # foriegn or local supplier
    Field('contact_person', 'string', length=30, requires = IS_UPPER()),
    Field('address_1','string', length = 100, requires = [IS_UPPER(), IS_LENGTH(100)]),
    Field('address_2','string', length = 100, requires = [IS_UPPER(), IS_LENGTH(100)]),
    Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('contact_no','string', length=50, requires = IS_UPPER()),
    Field('fax_no','string', length=50, requires = IS_UPPER()),
    Field('email_address','string', length=50, requires = IS_EMAIL(error_message='invalid email!')),
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('purchase_budget', 'decimal(10,2)'),
    Field('supplier_ib_account','string',length = 10, writable = False),
    Field('supplier_purchase_account', 'string', length = 10, writable = False),
    Field('supplier_sales_account', 'string', length = 10, writable = False),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(supp_code)s')

db.define_table('Supplier_Bank',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),    
    Field('bank_name', 'string'),
    Field('account_no', 'string', length = 50),
    Field('bank_name', 'string', length = 50),
    Field('beneficiary_name', 'string', length = 50),
    Field('iban_code', 'string', length = 50),
    Field('swift_code', 'string', length = 50),
    Field('bank_address', 'string', length = 50),
    Field('city', 'string', length = 50),
    Field('country_id','reference Made_In', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Master_Department',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(supp_code)s')

db.define_table('Supplier_Contact_Person',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('other_supplier_name', 'string', length = 50, requires = [IS_UPPER(), IS_LENGTH(50)]),
    Field('contact_person', 'string', length=30, requires = [IS_UPPER(), IS_LENGTH(30)]),
    Field('address_1','string', length = 50, requires = [IS_UPPER(), IS_LENGTH(50)]),
    Field('address_2','string', length = 50, requires = [IS_UPPER(), IS_LENGTH(50)]),
    Field('country_id','reference Made_In', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Forwarders',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('forwarder_code_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Forwarder_Supplier.id, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder' )),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Trade_Terms',
    Field('trade_terms', 'string', length = 25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Trade_Terms.trade_terms')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'trade_terms')

db.define_table('Supplier_Payment_Mode',
    Field('payment_mode','string', length = 25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Payment_Mode.payment_mode')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'payment_mode')

db.define_table('Supplier_Payment_Terms',
    Field('payment_terms','string', length = 25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Payment_Terms.payment_terms')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'payment_terms')

db.define_table('Supplier_Payment_Mode_Details',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),
    Field('payment_mode_id', 'reference Supplier_Payment_Mode', ondelete = 'NO ACTION',label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), #'string', length = 25, requires = IS_IN_SET(['LC','TELEX TRANSFER'], zero = 'Choose Payment Mode')),
    Field('payment_terms_id', 'reference Supplier_Payment_Terms', ondelete = 'NO ACTION',label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), #'string', length = 25, requires = IS_IN_SET(['LC','45 DAYS'], zero = 'Choose Payment Mode')),
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('forwarder_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION',label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
    Field('commodity_code','string',length=10),
    Field('discount_percentage','string',length=10),
    Field('custom_duty_percentage','string',length=10),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Bank_Details',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('trade_terms_id', 'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),
    Field('payment_mode_id', 'string', length = 25, requires = IS_IN_SET(['LC','TELEX TRANSFER'], zero = 'Choose Payment Mode')),
    Field('payment_terms_id', 'string', length = 25, requires = IS_IN_SET(['LC','45 DAYS'], zero = 'Choose Payment Mode')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('GroupLine',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('group_line_code','string',length=8, writable = False),
    Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'GroupLine.group_line_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False),format = '%(group_line_code)s')

db.define_table('Brand_Line',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('brand_line_code','string',length=8, writable = False),
    Field('brand_line_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Line.brand_line_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

db.define_table('Brand_Line_Department',
    Field('brand_line_code_id','reference Brand_Line', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

db.define_table('Sub_Group_Line',
    Field('group_line_code_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
    Field('supplier_code_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(group_line_code)s')

# msg.flash = Incomplete Informatin
db.define_table('Brand_Classification',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')), #ERROR - * Field should not be empty
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('brand_line_code_id','reference Brand_Line', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
    Field('brand_cls_code','string', length=8, writable = False),
    Field('brand_cls_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_cls_code)s')

db.define_table('Brand_Classificatin_Department',
    Field('brand_cls_code_id','reference Brand_Classification',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

db.define_table('Fragrance_Type',        
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Color',    
    Field('color_name','string',length=25, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Color.color_name')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Size',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Collection',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Section',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('section_code','string',length=5, writable = False),
    Field('section_name','string',length=50, requires = [IS_UPPER(), IS_LENGTH(25), IS_NOT_IN_DB(db, 'Section.section_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Location_Group',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('location_group_code', 'string', length=10,writable = False),
    Field('location_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location_Group.location_group_name')]),
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user,ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_group_code)s')

db.define_table('Location_Sub_Group',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('location_sub_group_code','string',length=10, writable =False),
    Field('location_sub_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location_Sub_Group.location_sub_group_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

db.define_table('Location',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('location_group_code_id','reference Location_Group', ondelete = 'NO ACTION',label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),    
    Field('location_sub_group_id','reference Location_Sub_Group', ondelete = 'NO ACTION',label = 'Location Sub-Group Code', requires = IS_IN_DB(db, db.Location_Sub_Group.id, '%(location_sub_group_code)s - %(location_sub_group_name)s', zero = 'Choose Location Sub-Group')),
    Field('location_code','string',length=10, writable =False),
    Field('location_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),    
    Field('stock_adjustment_code', 'string', length = 10),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')
    
db.define_table('Gender',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(gender_code)s')
    
db.define_table('Item_Type',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('UOM',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

# to remove in db schema
db.define_table('Supplier_UOM',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Weight',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Transaction_Item_Category',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user,ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Color_Code',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Master',
    Field('item_code', 'string', length = 15, label = 'Item Code',writable = False, readable = True, requires = [IS_LENGTH(15),IS_NOT_IN_DB(db, 'Item_Master.item_code')]),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
    Field('item_description_ar', 'string', length = 50, label = 'Arabic Name', requires = [IS_LENGTH(50), IS_UPPER()]),
    Field('supplier_item_ref', 'string', length = 20, requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
    Field('int_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
    Field('loc_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
    Field('purchase_point', 'integer', default = 40),
    Field('ib', 'decimal(10,2)', default = 0),
    Field('uom_value', 'integer'),    
    Field('uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose UOM Pack Size')),
    Field('supplier_uom_value', 'integer'),
    Field('supplier_uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose UOM Pack Size')),
    Field('weight_value', 'integer'),
    Field('weight_id', 'reference Weight', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Weight.id, '%(mnemonic)s', zero = 'Choose Weight')),
    Field('type_id', 'reference Item_Type',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Item_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), # saleable/non-saleable => item_type_id    
    Field('selectivetax','decimal(10,2)', default = 0, label = 'Selective Tax'),    
    Field('vatpercentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),    
    Field('division_id', 'reference Division', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
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
    Field('item_status_code_id','reference Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'item_code')
# editing item_master freeze division_id, item-code, uom, 

db.define_table('Stock_Status',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('required_action','string', length = 50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Stock_Required_Action',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Stock_Request',       
    Field('stock_request_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('stock_request_no', 'integer', default = 0, writable = False),
    Field('stock_request_date', 'date', default = request.now),
    Field('stock_due_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('stock_destination_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),    
    Field('total_amount','decimal(10,2)', default = 0),
    Field('srn_status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('stock_request_date_approved','date'),
    Field('stock_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),

    # represent = lambda id, r: db.department(id).name if id else '',
    Field('stock_transfer_no_id', 'reference Transaction_Prefix',ondelete = 'NO ACTION', writable = False),    
    Field('stock_transfer_no', 'integer', writable = False),
    Field('stock_transfer_date_approved', 'date', writable = False),
    Field('stock_transfer_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    
    Field('stock_receipt_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_receipt_no', 'integer', writable = False),    
    Field('stock_receipt_date_approved', 'date', writable = False),
    Field('stock_receipt_approved_by', 'reference auth_user',ondelete = 'NO ACTION', writable = False),

    Field('ticket_no', 'string', length = 10, writable = False, requires = [IS_LENGTH(10),IS_UPPER(), IS_NOT_IN_DB(db, 'Stock_Request.ticket_no')]),
    Field('archive','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'stock_request_no')

db.define_table('Stock_Request_Transaction',    
    Field('stock_request_id', 'reference Stock_Request', ondelete = 'NO ACTION',readable = False), #writable = False), #requires = IS_IN_DB(db, db.Stock_Request.id, '%(stock_request_no)s')),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION'), #requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),    
    Field('category_id', 'reference Transaction_Item_Category',ondelete = 'NO ACTION'), 
    Field('quantity', 'integer', default = 0),
    Field('uom','integer', default = 0),
    Field('average_cost','decimal(10,4)', default =0),
    Field('price_cost', 'decimal(10,4)', default = 0 ),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('remarks','string', length = 50),
    Field('delete', 'boolean', default = False),
    Field('ticket_no_id', 'string', length = 10, writable = False, readable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

db.define_table('Stock_Transaction_Temp',    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code'))),
    Field('item_code', 'string',length = 25),
    Field('stock_source_id', 'reference Location',ondelete = 'NO ACTION'),
    Field('stock_destination_id', 'reference Location',ondelete = 'NO ACTION'),
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default =0),
    Field('qty', 'integer', default =0),
    Field('price_cost', 'decimal(10, 4)', default = 0),
    Field('category_id', 'reference Transaction_Item_Category',ondelete = 'NO ACTION'), 
    # compute = lambda p: p['regular_maintenance'] + p['accident_repair'] + p['statutory_expenses'] + p['spare_parts']
    Field('amount','decimal(10,2)', default = 0, compute = lambda p: p['qty'] * p['price_cost']),
    Field('remarks','string'),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

    # Field('uom','integer', default =0),
    # Field('price_cost', 'decimal(10,2)',default = 0),
    # Field('wholesale_price', 'decimal(10,2)', default = 0),
    # Field('retail_price', 'decimal(10,2)',default = 0),    

db.define_table('Stock_File',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
    Field('opening_stock', 'integer', default = 0),
    Field('closing_stock', 'integer', default = 0),
    Field('previous_year_closing_stock', 'integer', default = 0),
    Field('stock_in_transit', 'integer', default = 0),
    Field('free_stock_qty', 'integer', default = 0),
    Field('reorder_qty', 'integer', default = 0), 
    Field('last_transfer_qty', 'integer', default = 0),
    Field('probational_balance','integer', default = 0),
    Field('damaged_stock_qty', 'integer', default = 0),
    Field('last_transfer_date', 'datetime', default = request.now),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Adjustment_Type',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Merch_Stock_Transaction',
    Field('voucher_no','string', length = 15), # 10 length
    Field('location_code', 'string', length = 10),   # from location master
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8
    Field('transaction_date', 'date'), # from date of transaction
    Field('account', 'string', length = 10), #adjustment code, customer code, supplier code. etc...
    Field('item_code', 'string', length = 15), # item master
    Field('uom', 'integer'), # from transaction
    Field('quantity', 'integer'), # from transaction
    Field('average_cost','decimal(10,6)', default = 0), # average cost
    Field('price_cost', 'decimal(10,6)', default = 0), # pieces
    Field('sale_cost','decimal(10,6)', default = 0), # after discount
    Field('discount', 'integer', default = 0), # normal discount from pos
    Field('wholesale_price', 'decimal(10,2)', default = 0), # from item prices
    Field('retail_price', 'decimal(10,2)', default = 0), # from item prices
    Field('vansale_price', 'decimal(10,2)', default = 0), # from item prices
    Field('tax_amount', 'decimal(10,2)', default = 0), # in sales
    Field('selected_tax','integer'), # in sales
    Field('sales_lady_code', 'string',length = 10), # sales, pos
    Field('supplier_code','string', length = 10), # from item code
    Field('dept_code','string', length = 20)) # from item master

db.define_table('Stock_Adjustment',
    Field('stock_adjustment_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_adjustment_no','integer'),
    Field('stock_adjustment_date', 'date', default = request.now),
    Field('stock_adjustment_code','string', length = 10),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
    Field('adjustment_type', 'reference Adjustment_Type', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Adjustment_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('total_amount','decimal(10,4)', default = 0),    
    Field('srn_status_id','reference Stock_Status', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('approved_by', 'reference auth_user', writable = False),
    Field('date_approved', 'datetime'),
    Field('archive','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Adjustment_Transaction',
    Field('stock_adjustment_no_id','reference Stock_Adjustment',ondelete = 'NO ACTION',writable = False, requires = IS_IN_DB(db, db.Stock_Adjustment.id, '%(stock_adjustment_no)s', zero = 'Choose Adjustment No')),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),    
    Field('stock_adjustment_date', 'date', default = request.now),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('delete', 'boolean', default = False),
    # Field('total_cost','decimal(10,4)', default = 0, compute = lambda p: (p['average_cost'] / p['uom']) * p['quantity']), # remove 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))
       
db.define_table('Stock_Adjustment_Transaction_Temp',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION'),
    Field('item_code', 'string', length = 25),    
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('uom', 'integer'),
    Field('total_quantity', 'integer', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('total_cost','decimal(10,4)', default = 0),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False))

db.define_table('Item_Prices',
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
    Field('reorder_qty', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Type',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Corrections',
    Field('stock_corrections_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_corrections_no','integer', writable = False),
    Field('stock_corrections_date', 'date', default = request.now, writable = False),    
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
    Field('stock_quantity_from_id', 'reference Stock_Type', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Stock_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('stock_quantity_to_id', 'reference Stock_Type', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Stock_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('status_id','reference Stock_Status', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('remarks', 'string', length = 50),
    Field('approved_by', 'reference auth_user', writable = False),
    Field('date_approved', 'datetime', writable = False),
    Field('archive','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Corrections_Transaction',
    Field('stock_corrections_no_id','reference Stock_Corrections',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),    
    Field('stock_corrections_date', 'date', default = request.now),
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('delete', 'boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))
       
db.define_table('Stock_Corrections_Transaction_Temporary',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION'),
    Field('item_code', 'string', length = 25),        
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('uom', 'integer'),
    Field('total_quantity', 'integer', default = 0),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False))


#---------- S   A   L   E   S   S c h e m a ----------

db.define_table('Customer_Category', # hypermarket, restaurant
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Customer_Account_Type',# cash, credit, bill
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Customer_Group_Code',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Customer',
    Field('customer_account_no','string',length = 15),
    Field('customer_group_code_id', 'reference Customer_Group_Code', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Customer_Group_Code.id,'%(description)s', zero = 'Choose Group Code')), 
    Field('customer_name','string', length = 50),
    Field('customer_category_id', 'reference Customer_Category', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Customer_Category.id,'%(description)s', zero = 'Choose Category')), 
    Field('customer_account_type', 'reference Customer_Account_Type', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Customer_Account_Type.id,'%(description)s', zero = 'Choose Account Type')), 
    # Field('account_type', ), account receivable
    Field('po_box_no', 'integer'),
    Field('unit_no', 'integer'),
    Field('building_no', 'integer'),
    Field('street_no', 'integer'),
    Field('zone', 'integer'),
    Field('telephone_no','string',length = 25),
    Field('fax_no','string',length = 25),
    Field('email_address','string', length = 50),
    Field('area_name','string', length = 25),
    Field('state','string', length = 50),
    Field('country','string', length = 50),
    Field('sponsor_name','string', length = 50),
    # Field('sponsor_id','string', length = 50),
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'customer_account_no')

db.define_table('Customer_Contact_Person',
    Field('customer_id', 'reference Customer', ondelete = 'NO ACTION',writable = False),
    Field('contact_person','string', length = 50),
    Field('contact_number','string',length = 25),
    Field('position','string', length = 50),
    Field('email_address','string',length = 25),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'contact_person')

db.define_table('Customer_Credit_Limit',
    Field('customer_id', 'reference Customer', ondelete = 'NO ACTION', writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION'),
    Field('credit_limit_amount','decimal(10,2)'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'customer_account_no')

db.define_table('Customer_Bank_Detail', 
    Field('customer_id', 'reference Customer', ondelete = 'NO ACTION', writable = False),        
    Field('account_no', 'string', length = 50),
    Field('bank_name', 'string', length = 50),
    Field('beneficiary_name', 'string', length = 50),
    Field('iban_code', 'string', length = 50),
    Field('swift_code', 'string', length = 50),
    Field('bank_address', 'string', length = 50),
    Field('city', 'string', length = 50),
    Field('country_id','reference Made_In', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Man',
    Field('employee_id','string', length = 10),
    Field('name','string', length = 25),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'employee_id')

db.define_table('Sales_Order',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_order_no', 'integer', default = 0, writable = False),
    Field('sales_order_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Customer', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Customer.id, '%(customer_account_no)s - %(customer_name)s', zero = 'Choose Customer')),    
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(10,4)', default = 0),    
    Field('total_amount_after_discount','decimal(10,4)', default = 0),    
    Field('total_selective_tax', 'decimal(10,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(10,2)', default = 0),
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure
    Field('total_vat_amount', 'decimal(10,2)', default = 0),
    Field('sales_order_date_approved','date', writable = False),
    Field('sales_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),

    Field('delivery_note_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('delivery_note_no', 'integer', writable = False),
    Field('delivery_note_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('delivery_note_date_approved','date', writable = False),

    Field('sales_invoice_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_invoice_no', 'integer', writable = False),    
    Field('sales_invoice_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('sales_invoice_date_approved','date', writable = False),
    
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Sales_Man.id, '%(name)s', zero = 'Choose Salesman')),   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('archives', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'sales_order_no')
 
db.define_table('Sales_Order_Transaction',
    Field('sales_order_no_id','reference Sales_Order',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('sale_cost', 'decimal(10,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),            
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Order_Transaction_Temporary',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', writable = False),        
    Field('item_code', 'string', length = 25),        
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('price_cost','decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('taxable_value','decimal(10,2)', default = 0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),  
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax FOC'),  
    Field('tax_percentage','decimal(10,2)', default = 0),
    Field('tax_amount','decimal(10,2)', default = 0),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION'),
    Field('remarks','string'),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Return',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_return_no', 'integer', default = 0, writable = False),
    Field('sales_return_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Customer', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Customer.id, '%(customer_account_no)s - %(customer_name)s', zero = 'Choose Customer')),    
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(10,4)', default = 0),    
    Field('total_amount_after_discount','decimal(10,4)', default = 0),    
    Field('total_selective_tax', 'decimal(10,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(10,2)', default = 0),
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure
    Field('total_vat_amount', 'decimal(10,2)', default = 0),
    Field('sales_return_date_approved','date', writable = False),
    Field('sales_return_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),    
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Sales_Man.id, '%(name)s', zero = 'Choose Salesman')),   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('archives', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'sales_order_no')
 
db.define_table('Sales_Return_Transaction',
    Field('sales_return_no_id','reference Sales_Order',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('sale_cost', 'decimal(10,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),            
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Return_Transaction_Temporary',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', writable = False),        
    Field('item_code', 'string', length = 25),        
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('price_cost','decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('taxable_value','decimal(10,2)', default = 0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),  
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax FOC'),  
    Field('tax_percentage','decimal(10,2)', default = 0),
    Field('tax_amount','decimal(10,2)', default = 0),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')),     
    Field('remarks','string'),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

db.define_table('Master_Account',
    Field('account_code','string', length = 15),
    Field('account_name','string', length = 50))

db.define_table('Obsolescence_Stocks',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('obsolescence_stocks_no', 'integer', default = 0, writable = False),
    Field('obsolescence_stocks_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_type_id','reference Stock_Type', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Type.id,'%(description)s', zero = 'Choose Stock Type')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('account_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Customer')),    
    Field('total_amount','decimal(10,4)', default = 0),    
    Field('total_amount_after_discount','decimal(10,4)', default = 0),    
    Field('total_selective_tax', 'decimal(10,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(10,2)', default = 0),
    Field('total_vat_amount', 'decimal(10,2)', default = 0),
    Field('obsolescence_stocks_date_approved','date', writable = False),
    Field('obsolescence_stocks_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('archives', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'sales_order_no')
 
db.define_table('Obsolescence_Stocks_Transaction',
    Field('obsolescence_stocks_no_id','reference Sales_Order',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),            
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('sale_cost', 'decimal(10,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),            
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Obsolescence_Stocks_Transaction_Temporary',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', writable = False),        
    Field('item_code', 'string', length = 25),        
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('price_cost','decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('taxable_value','decimal(10,2)', default = 0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),  
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax FOC'),  
    Field('tax_percentage','decimal(10,2)', default = 0),
    Field('tax_amount','decimal(10,2)', default = 0),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')),     
    Field('remarks','string'),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

db.define_table('Delivery_Note',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('delivery_note_no', 'integer', default = 0, writable = False),
    Field('delivery_note_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Customer', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Customer.id, '%(customer_account_no)s - %(customer_name)s', zero = 'Choose Customer')),    
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    # Field('total_amount','decimal(10,2)', default = 0),
    Field('remarks', 'string'),
    Field('sales_invoice_no', 'integer', writable = False),    
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION'),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'delivery_note_no')
 
db.define_table('Delivery_Note_Transaction',
    Field('delivery_note_id'),    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Invoice',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_invoice_no', 'integer', default = 0, writable = False),
    Field('sales_invoice_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Customer', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Customer.id, '%(customer_account_no)s - %(customer_name)s', zero = 'Choose Customer')),    
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(10,2)', default = 0),    
    Field('sales_order_date_approved','date'),
    Field('sales_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),
    Field('sales_order_no', 'integer',  writable = False),    
    Field('delivery_note_id','integer', writable = False),
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION'),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'sales_invoice_no')
 
db.define_table('Sales_Invoice_Transaction',
    Field('sales_invoice_no_id','reference Sales_Invoice',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('sale_cost', 'decimal(10,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),    
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

#---------- S   A   L   E   S   S c h e m a ----------


#---------- P  R  O  C  U  R  E  M  E  N  T  S c h e m a -------

db.define_table('Purchase_Request',       
    Field('purchase_request_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_request_no', 'integer', writable = False),
    Field('purchase_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_request_date_approved','date', writable = False),
    Field('purchase_request_date', 'date', default = request.now, writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),
    Field('estimated_time_of_arrival', 'date', default = request.now),
    Field('total_amount','decimal(15,4)', default = 0),    
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('insured', 'boolean', default = False),
    Field('foreign_currency_value','decimal(10,2)', default = 0),
    Field('local_currency_value','decimal(10,2)', default = 0),
    Field('exchange_rate','decimal(10,2)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', writable = False), #requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('remarks', 'text'),
    
    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'integer', writable = False),
    Field('purchase_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_date_approved','date', writable = False),
        
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
        
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_request_no')

db.define_table('Purchase_Request_Transaction_Temporary',    
    Field('item_code', 'string', length = 25),   
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(15,6)', default = 0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('average_cost','decimal(15,4)', default = 0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),            
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Request_Transaction',
    Field('purchase_request_no_id','reference Purchase_Request',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(15,6)', default = 0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('average_cost','decimal(15,4)', default = 0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),            
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Order',       
    Field('purchase_request_no_id', 'reference Purchase_Request', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'integer', writable = False),
    Field('purchase_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_date_approved','date', writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),
    Field('estimated_time_of_arrival', 'date', default = request.now),
    Field('total_amount','decimal(15,4)', default = 0),    
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('insured', 'boolean', default = False),
    Field('insurance_letter_reference', 'string', length = 50),
    Field('foreign_currency_value','decimal(10,2)', default = 0),
    Field('local_currency_value','decimal(10,2)', default = 0),
    Field('exchange_rate','decimal(10,2)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', writable = False), #requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('remarks', 'text'),                   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('selected','boolean', default = False, writable = False), 
    Field('consolidated','boolean', default = False, writable = False),
    Field('partial','boolean', default = False, writable = False), 
    Field('received','boolean', default = False, writable = False),
    Field('archives', 'boolean', default = False, writable = False), 
     
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_order_no')

db.define_table('Purchase_Order_Transaction',
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('receive_quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('difference_quantity', 'integer', default = 0),
    Field('price_cost', 'decimal(15,6)', default = 0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('average_cost','decimal(15,4)', default = 0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('delete', 'boolean', default = False),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Receipt_Warehouse_Consolidated',        
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('draft','boolean', default = True),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

db.define_table('Purchase_Receipt_Ordered_Warehouse_Consolidated',    
    Field('purchase_receipt_no_id','reference Purchase_Receipt_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),       
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),    
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'purchase_order_no_id')

db.define_table('Purchase_Receipt_Transaction_Consolidated', 
    Field('purchase_receipt_no_id','reference Purchase_Receipt_Ordered_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),              
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # qty consolidated
    Field('uom','integer', default = 0),        
    Field('purchase_ordered_quantity', 'integer', default = 0), # ordered consolidated
    Field('difference_quantity', 'integer', default = 0),
    # delete
    Field('price_cost', 'decimal(15,6)', default = 0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('average_cost','decimal(15,4)', default = 0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    # delete
    Field('delete', 'boolean', default = False),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),                
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Receipt_Transaction_Consolidated_New_Item', 
    Field('purchase_receipt_no_id','reference Purchase_Receipt_Ordered_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),                     
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code', 'string', length = 25), 
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('delete', 'boolean', default = False),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),                
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('new_item','boolean', default = False),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Receipt',    
    Field('purchase_receipt_no_id_consolidated','reference Purchase_Receipt_Ordered_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),                 
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),    
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('total_amount','decimal(15,4)', default = 0),    # total net amount
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('exchange_rate','decimal(10,6)', default = 0, required = True),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('landed_cost','decimal(10,6)', default = 0),
    Field('other_charges','decimal(10,6)', default = 0),    
    Field('custom_duty_charges','decimal(10,6)', default = 0),    
    # Field('exchange_rate','decimal(10,6)', default = 0.0),
    Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),
    Field('supplier_invoice','string', length = 25),
    Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('supplier_account_code_description', 'string', length = 50),
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', writable = False), #requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    # Field('remarks', 'text'),                   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    # Field('selected','boolean', default = False), 
    # Field('consolidated','boolean', default = False),
    # Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

db.define_table('Purchase_Receipt_Transaction',
    Field('purchase_receipt_no_id_consolidated','reference Purchase_Receipt_Ordered_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),                 
    Field('purchase_receipt_no_id','reference Purchase_Receipt',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # manoj
    Field('receive_quantity','integer', default = 0), # hakim
    Field('uom','integer', default = 0),    
    Field('difference_quantity', 'integer', default = 0), # diff
    Field('price_cost', 'decimal(15,6)', default = 0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('average_cost','decimal(15,4)', default = 0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    # Field('discount_percentage', 'decimal(10,2)',default =0),
    # Field('net_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('excessed','boolean',default = False),
    Field('remarks','string', length = 50),
    Field('delete', 'boolean', default = False),    

    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),

    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Direct_Purchase_Receipt',    
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_order_no', 'string', length = 25),    
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),    
    Field('supplier_reference_order','string', length = 25),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('total_amount','decimal(15,4)', default = 0),    # total net amount
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('exchange_rate','decimal(10,6)', default = 0, required = True),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('landed_cost','decimal(10,6)', default = 0),
    Field('other_charges','decimal(10,6)', default = 0),    
    Field('custom_duty_charges','decimal(10,6)', default = 0),        
    Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),
    Field('supplier_invoice','string', length = 25),
    Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('supplier_account_code_description', 'string', length = 50),
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', writable = False), #requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),    
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

db.define_table('Direct_Purchase_Receipt_Transaction',
    Field('purchase_receipt_no_id','reference Direct_Purchase_Receipt',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # manoj
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(15,6)', default = 0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('average_cost','decimal(15,4)', default = 0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('excessed','boolean',default = False),
    Field('remarks','string', length = 50),
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Insurance_Master',    
    Field('insurance_name','string', length = 50),
    Field('contact_person','string', legnth = 50),
    Field('address','string',length = 50),
    Field('city','string',length = 25),
    Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False), format = 'insurance_name')

db.define_table('Insurance_Details',    
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),
    Field('insurance_master_id','reference Insurance_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Insurance_Master.id, '%(insurance_name)s', zero = 'Choose Insurance')),
    Field('subject','string', length = 50),
    Field('description', 'string', length = 50),
    Field('payment_terms', 'string', length = 50),
    Field('partial_shipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Partial Shipment')),
    Field('transhipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Transhipment')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False))

# db.define_table('Purchase_Receipt_Transaction', #Purchase_Receipt_Transaction_Accounts
#     Field('purchase_order_no_id','reference Purchase_Receipt_Ordered_Consolidated',ondelete = 'NO ACTION',writable = False),
#     Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
#     Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
#     Field('uom','integer', default = 0),    
#     Field('quantity','integer', default = 0),        
#     Field('purchase_ordered_quantity', 'integer', default = 0),
#     Field('price_cost', 'decimal(15,6)', default = 0),
#     Field('delete', 'boolean', default = False),   
#     Field('selected','boolean', default = False), 
#     Field('consolidated','boolean', default = False), 
#     Field('partial','boolean', default = False), 
#     Field('received','boolean', default = False),
#     Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
#     Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
#     Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
#     Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

# db.define_table('Purchase_Receipt_Transaction_Header',
#     Field('location_code', 'integer'),    
#     Field('trn_type', 'integer'),
#     Field('trn_date','date'),
#     Field('purchase_receipt_number','integer'),
#     Field('supp_code', 'string',length=8),
#     Field('total_amount','decimal(10,2)'),
#     Field('discount_percentage','decimal(10,2)'),
#     Field('discount_amount','decimal(10,2)'),
#     Field('other_charges','decimal(10,2)'),
#     Field('po_group_ref','string',length=8),
#     Field('lc_number','string', length=20),
#     Field('supp_invoice_no','string',length=10),
#     Field('exchange_rate','decimal(10,2)'),
#     Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
#     Field('landed_cost_rate','decimal(10,2)'),
#     Field('po_type','integer'),
#     Field('remarks','text'),
#     Field('status','string',length=10),
#     Field('print_counter'))

db.define_table('PO_Group',
    Field('po_group_refno','string', length=10),
    Field('po_number','string',length=10))

# db.define_table('Purchase_Receipt_Transaction_Details',
#     Field('purchase_receipt_number','string',length=10),
#     Field('item_code','string',length=15),
#     Field('price_cost','decimal(10,2)'),
#     Field('qty','integer'),
#     Field('uom','integer'),
#     Field('item_category','string',length=1),
#     Field('average_cost','decimal(10,2)'),
#     Field('wholesale_price','decimal(10,2)'),
#     Field('retail_price','decimal(10,2)'),
#     Field('net_price','decimal(10,2)'),
#     Field('received_date','date'),
#     Field('status','string',length=10))

# db.define_table('Purchase_Order_Transaction_Header',
#     Field('po_number', 'string',length=10),
#     Field('po_date','date'),
#     Field('supp_code','string',length=10),
#     Field('po_amount','decimal(10,2)'),
#     Field('discount_percentage','decimal(10,2)'),
#     Field('discount_amount','decimal(10,2)'),
#     Field('po_tprobational_balanceype','string',length=10),
#     Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
#     Field('eta','string',length=10),
#     Field('purchase_request_no','string',length=10))

# db.define_table('Purchase_Order_Transaction_Details',
#     Field('po_number','string',length=10),
#     Field('item_code','string',length=10),
#     Field('supp_price','decimal(10,2)'),
#     Field('quantity','integer'),
#     Field('uom','integer'),
#     Field('item_category','string',length=10),
#     Field('qty_received','integer'))

db.define_table('Batch_Order_Transaction',
    Field('item_code','string',length=10),
    Field('supp_price','decimal(10,2)'),
    Field('landed_cost','decimal(10,2)'),
    Field('qty','integer'),
    Field('date_ordered','date'))



#---------- P  R  O  C  U  R  E  M  E  N  T  S c h e m a -------


db.define_table('Stock_Request_Transaction_Report_Counter',
    Field('stock_transfer_no_id', 'reference Stock_Request'),
    Field('printer_counter', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

db.define_table('Sales_Order_Transaction_Report_Counter',
    Field('sales_order_transaction_no_id', 'reference Sales_Order'),
    Field('printer_counter', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

db.define_table('Sales_Invoice_Transaction_Report_Counter',
    Field('sales_invoice_transaction_no_id', 'reference Sales_Order'),
    Field('printer_counter', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

db.define_table('Sales_Return_Transaction_Report_Counter',
    Field('sales_return_transaction_no_id', 'reference Sales_Return'),
    Field('printer_counter', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

db.define_table('Stock_Issue_Transaction_Report_Counter',
    Field('stock_issue_transaction_no_id', 'reference Obsolescence_Stocks'),
    Field('printer_counter', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

#---------- C O M M U N I C A T I O N  S c h e m a -------

db.define_table('Communication_Tranx_Prefix',    
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('serial_key', 'integer', default = 0),
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

db.define_table('Incoming_Mail',
    Field('mail_prefix_no_id','reference Communication_Tranx_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('incoming_mail_no', 'string', length = 25, writable = False),
    Field('mail_date','date', default = request.now),
    Field('mail_sender','string', length = 50),
    Field('mail_subject','string', length = 50),
    Field('attached','upload'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Outgoing_Mail',    
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),
    Field('insurance_master_id','reference Insurance_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Insurance_Master.id, '%(insurance_name)s', zero = 'Choose Insurance')),
    Field('mail_prefix_no_id','reference Communication_Tranx_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('outgoing_mail_no', 'string', length = 25, writable = False),
    Field('mail_date','date', default = request.now),
    Field('mail_sender','string', length = 50),
    Field('mail_addressee','string', length = 50),
    Field('mail_subject','string', length = 50),
    Field('postage','decimal(10,2)', default = 0),    
    Field('attached','upload'),
    Field('print_process', 'boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Circular',
    Field('circular_prefix_no_id','reference Communication_Tranx_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('circular_no','string', length = 25, writable = False),
    Field('circular_date','date', default = request.now),
    Field('circular_addressee', 'string', length = 50),    
    Field('circular_subject','string', legnth = 50),
    Field('attached','upload'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Memorandum',
    Field('memorandum_prefix_no_id','reference Communication_Tranx_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('memorandum_no','string', length = 25, writable = False),
    Field('memorandum_date','date', default = request.now),
    Field('memorandum_from', 'string', length = 50),
    Field('memorandum_to', 'string', length = 50),
    Field('memorandum_subject','string', legnth = 50),
    Field('attached','upload'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Fax',
    Field('fax_prefix_no_id','reference Communication_Tranx_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('fax_no','string', length = 25, writable = False),
    Field('fax_date','date', default = request.now),
    Field('fax_from', 'string', length = 50),
    Field('fax_to', 'string', length = 50),
    Field('fax_subject','string', legnth = 50),
    Field('attached','upload'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

from num2words import num2words

def amt2words(amount, currency='riyals', change='dirhams', precision=2):
    change_amt = (amount - int(amount))*pow(10, precision)
    words = '{main_amt} {main_word}'.format(
        main_amt=num2words(int(amount)),
        main_word=currency,
    )
    if change_amt > 0:
        words += ' and {change_amt} {change_word}'.format(
        change_amt=num2words(change_amt),
        change_word=change,
    )
    return words

# i.number_to_words(49)

# from num2words import num2words

# test = 23.25

# intpart,decimalpart = int(test), test-int(test) 
# print(num2words(intpart).replace('-', ' ') + ' and ' + str( int(decimalpart * (10 ** (len(str(decimalpart)) - 2)))) +  ' cent')