# auth = Auth(db,cas_provider = 'http://127.0.0.1:3000/merch_erp/default/user/cas')
# db = DAL('mssql4://username:password@localhost/test', pool_size=0)
# db = DAL('mssql://SA:M3rch@2018@localhost/master?DRIVER={FreeTDS}')
# db = DAL('mssql4://SA:M3rch@2018@localhost,1433/mpc_inv', pool_size = 0)

# db = DAL("mssql4://SA:M3rch2018@localhost:1433/M3rchDB?driver={ODBC Driver 17 for SQL Server}") # production
# db = DAL("mssql4://SA:M3rch2018@localhost:1433/M3rchDB_Test?driver={ODBC Driver 17 for SQL Server}") # testing
# db = DAL("mssql4://SA:M3rch2018@localhost:1433/M3rchDB_Deve?driver={ODBC Driver 17 for SQL Server}") # development

db = DAL('postgres://postgres:admin@localhost:5432/mpc_inv', pool_size=0)

# Field('division_id', 'reference division', readable = False, writable = False, requires = IS_IN_DB(db, db.division.id, '%(division)s', zero = 'Choose division')),
# Field('division', requires = IS_UPPER(), label = 'Division'),format = '%(division)s')
# import pyodbc
# server = 'localhost'
# database = 'SampleDB'
# username = 'SA' 
# password = 'M3rch@2018'
# # cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
# db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
auth = Auth(globals(),db)


# Duplicate Entry error = SAME VALUE ALREADY EXIST OR EMPTY
# error_message = 'Record already exist or empty.'

auth.settings.actions_disabled=['register', 'request_reset_password','retrieve_username']
if request.controller != 'appadmin': auth.settings.actions_disabled +=['register']
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128),
    Field('last_name', length=128),
    Field('username', unique = True, readable = False),
    Field('email', length=128), # required
    Field('password', 'password', length=512,readable=False, label='Password'), # required
    Field('registration_key', length=512, writable=False, readable=False, default=''),# required
    Field('reset_password_key', length=512,writable=False, readable=False, default=''),# required
    Field('registration_id', length=512, writable=False, readable=False, default=''))# required

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
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(status)s')

db.define_table('Record_Status',
    Field('status','string',length=20, requires = [IS_LENGTH(20),IS_UPPER(), IS_NOT_IN_DB(db, 'Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(status)s')

db.define_table('Prefix_Data',
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

db.define_table('Division',
    Field('div_code','string', length = 5, label = 'Division Code', writable = False, requires = IS_NOT_IN_DB(db, 'Division.div_code')),
    Field('div_name','string', length = 50, label = 'Division Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Division.div_name')]), 
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(div_code)s')

db.define_table('Department',
    Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('dept_code','string', length = 5, label ='Department Code', writable = False, requires = IS_NOT_IN_DB(db, 'Department.dept_code')),
    Field('dept_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.dept_name')]),
    Field('order_qty', 'integer', default = 40),
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(dept_code)s')


db.define_table('Product',
    # Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('product_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_code')]), # Field 
    Field('product_name', 'string', length = 50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name')]),
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(product_code)s')

db.define_table('SubProduct',
    Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
    Field('subproduct_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_code')]),
    # Field('dept_code_id','reference Department', label = 'Department',requires = IS_IN_DB(db(db.Department.status_id == 1), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('subproduct_name','string', length = 50, requires = [IS_UPPER(),IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(subproduct_code)s')

db.define_table('Made_In',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Currency',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Supplier_Master',
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
    Field('supp_code','string', length=10, writable = False),
    Field('supp_sub_code','string', length=10, writable = False),
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
    Field('supplier_ib_account','string',length = 10, writable = False),
    Field('supplier_purchase_account', 'string', length = 10, writable = False),
    Field('supplier_sales_account', 'string', length = 10, writable = False),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(supp_code)s')

db.define_table('Supplier_Bank',
    Field('supplier_id', 'reference Supplier_Master', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),    Field('bank_name', 'string'),
    Field('account_no', 'string'),
    Field('bank_name', 'string'),
    Field('beneficiary_name', 'string'),
    Field('iban_code', 'string'),
    Field('swift_code', 'string'),
    Field('bank_address', 'string'),
    Field('city', 'string'),
    Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Master_Department',
    Field('supplier_id', 'reference Supplier_Master', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(supp_code)s')

db.define_table('Supplier_Contact_Person',
    Field('supplier_id', 'reference Supplier_Master', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('other_supplier_name', 'string', length = 50, requires = [IS_UPPER(), IS_LENGTH(50)]),
    Field('contact_person', 'string', length=30, requires = [IS_UPPER(), IS_LENGTH(30)]),
    Field('address_1','string', length = 50, requires = [IS_UPPER(), IS_LENGTH(50)]),
    Field('address_2','string', length = 50, requires = [IS_UPPER(), IS_LENGTH(50)]),
    Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Trade_Terms',
    Field('trade_terms', 'string', length = 25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Trade_Terms.trade_terms')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'trade_terms')

db.define_table('Supplier_Payment_Mode',
    Field('payment_mode','string', length = 25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Payment_Mode.payment_mode')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'payment_mode')

db.define_table('Supplier_Payment_Terms',
    Field('payment_terms','string', length = 25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Payment_Terms.payment_terms')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'payment_terms')

db.define_table('Forwarder_Supplier',
    Field('forwarder_code','string',length = 5, writable = False),
    Field('forwarder_name','string',length = 50),
    Field('forwarder_type','string',length = 5, requires = IS_IN_SET(['AIR','SEA'], zero = 'Choose Type')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'forwarder_code')

db.define_table('Supplier_Payment_Mode_Details',
    Field('supplier_id', 'reference Supplier_Master', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),
    Field('payment_mode_id', 'reference Supplier_Payment_Mode', label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), #'string', length = 25, requires = IS_IN_SET(['LC','TELEX TRANSFER'], zero = 'Choose Payment Mode')),
    Field('payment_terms_id', 'reference Supplier_Payment_Terms', label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), #'string', length = 25, requires = IS_IN_SET(['LC','45 DAYS'], zero = 'Choose Payment Mode')),
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('forwarder_id', 'reference Forwarder_Supplier', label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
    Field('commodity_code','string',length=10),
    Field('discount_percentage','string',length=10),
    Field('custom_duty_percentage','string',length=10),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Bank_Details',
    Field('supplier_id', 'reference Supplier_Master', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('trade_terms_id', 'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),
    Field('payment_mode_id', 'string', length = 25, requires = IS_IN_SET(['LC','TELEX TRANSFER'], zero = 'Choose Payment Mode')),
    Field('payment_terms_id', 'string', length = 25, requires = IS_IN_SET(['LC','45 DAYS'], zero = 'Choose Payment Mode')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

# db.define_table('Supplier_Bank_')
db.define_table('GroupLine',
    Field('supplier_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('group_line_code','string',length=8, writable = False),
    Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'GroupLine.group_line_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(group_line_code)s')

db.define_table('Brand_Line',
    Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')),
    Field('brand_line_code','string',length=8, writable = False),
    Field('brand_line_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Line.brand_line_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

db.define_table('Sub_Group_Line',
    Field('group_line_code_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
    Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(group_line_code)s')


# msg.flash = Incomplete Informatin
db.define_table('Brand_Classification',
    Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')), #ERROR - * Field should not be empty
    Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
    Field('brand_cls_code','string', length=8, writable = False),
    Field('brand_cls_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(brand_cls_code)s')


db.define_table('Fragrance_Type',
    Field('product_code_id','reference Product', requires = IS_IN_DB(db(db.Product.product_name.startswith('FRAG')), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
    Field('fragrance_code','string',length=6, writable = False),
    Field('fragrance_name','string',length=35, requires = [IS_LENGTH(35),IS_UPPER(), IS_NOT_IN_DB(db, 'Fragrance_Type.fragrance_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Color',
    Field('color_code','string',length=5, writable = False),
    Field('color_name','string',length=25),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Size',
    Field('size_code','string',length=10, writable = False),
    Field('size_name','string',length=25, requires = [IS_LENGTH(25),IS_UPPER(),IS_NOT_IN_DB(db, 'Item_Size.size_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Collection',
    Field('collection_code','string',length=5, writable = False),
    Field('collection_name','string',length=25, requires = [IS_LENGTH(25),IS_UPPER()]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Section',
    Field('section_code','string',length=5, writable = False),
    Field('section_name','string',length=25, requires = [IS_UPPER(), IS_LENGTH(25), IS_NOT_IN_DB(db, 'Section.section_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Location_Group',
    Field('location_group_code', 'string', length=10,writable = False),
    Field('location_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location_Group.location_group_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(location_group_code)s')

db.define_table('Location_Sub_Group',
    Field('location_group_code_id','reference Location_Group', label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),
    Field('location_code','string',length=10, writable =False),
    Field('location_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

db.define_table('Location',
    Field('location_group_code_id','reference Location_Group', label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),
    Field('location_code','string',length=10, writable =False),
    Field('location_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(location_code)s')
    

db.define_table('Gender',
    Field('gender_code','string',length=10, writable = False),
    Field('gender_name', 'string', length = 10,requires = [IS_UPPER(), IS_LENGTH(10), IS_NOT_IN_DB(db, 'Gender.gender_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(gender_code)s')
    
db.define_table('Itemmas',
    Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('item_code', 'string', length = 15, label = 'Item Code',requires = IS_NOT_IN_DB(db, 'Itemmas.item_code')),
    Field('ref_no', 'string', length = 15, label = 'Reference No',requires = IS_NOT_IN_DB(db, 'Itemmas.ref_no')),
    Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
    Field('supplier_item_ref', 'string', length = 15),
    Field('item_description', 'string', length = 35, label = 'Description'),    
    Field('uom', 'integer'),
    Field('supp_oum', 'integer'),
    Field('bar_code', 'string', length = 20),
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
    Field('sub_product_code_id','reference SubProduct', requires = IS_IN_DB(db, db.SubProduct.id,'%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose Sub-Product')),
    Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
    Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
    Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
    Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(gender_code)s - %(gender_name)s', zero = 'Choose Gender')),
    Field('item_status_code_id','reference Status', requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose  Status')),
    Field('fragrance_code_id','reference Fragrance_Type', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(fragrance_code)s - %(fragrance_name)s', zero = 'Choose Fragrance Code')),
    Field('color_code_id','string', length=10, requires = IS_IN_SET(COLOR, zero = 'Choose Color')),
    Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = 'Choose Size')),
    Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(collection_code)s - %(collection_name)s', zero = 'Choose Collection')),
    Field('made_in','string',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
    Field('created_on', 'date', default = request.now),
    Field('created_by', 'date',default = request.now))

db.define_table('Item_Type',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('UOM',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Supplier_UOM',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Weight',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Transaction_Item_Category',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Color_Code',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Item_Master',
    Field('item_code', 'string', length = 15, label = 'Item Code',writable = False, readable = True, requires = [IS_LENGTH(15),IS_NOT_IN_DB(db, 'Item_Master.item_code')]),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
    Field('item_description_ar', 'string', length = 50, label = 'Arabic Name', requires = [IS_LENGTH(50), IS_UPPER()]),
    Field('supplier_item_ref', 'string', length = 20, requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
    Field('int_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
    Field('loc_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
    Field('purchase_point', 'integer', default = 40),
    Field('uom_value', 'integer'),    
    Field('uom_id', 'reference UOM', requires = IS_IN_DB(db, db.UOM, '%(mnemonic)s - %(description)s', zero = 'Choose UOM Pack Size')),
    Field('supplier_uom_value', 'integer'),
    Field('supplier_uom_id', 'reference Supplier_UOM', requires = IS_IN_DB(db, db.Supplier_UOM.id, '%(mnemonic)s - %(description)s', zero = 'Choose Supplier UOM Pack Size') ),
    Field('weight_value', 'integer'),
    Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(mnemonic)s', zero = 'Choose Weight')),
    Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), # saleable/non-saleable => item_type_id
    Field('selective_tax','string', length = 25),
    Field('vat_percentage','string', length = 25),    
    Field('division_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
    Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
    Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
    Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
    Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
    Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
    Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = 'Choose Size')),    
    Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(gender_code)s - %(gender_name)s', zero = 'Choose Gender')),
    Field('fragrance_code_id','reference Fragrance_Type', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(fragrance_code)s - %(fragrance_name)s', zero = 'Choose Fragrance Code')),
    Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = 'Choose Color')),
    Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(collection_code)s - %(collection_name)s', zero = 'Choose Collection')),
    Field('made_in_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(description)s', zero = 'Choose Country')),
    Field('item_status_code_id','reference Status', requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'item_code')
# editing item_master freeze division_id, item-code, uom, 

db.define_table('Stock_Status',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Stock_Request',    
    Field('stock_request_no', 'string', label = 'Stock Request No',writable = False, readable = True, requires = IS_NOT_IN_DB(db, 'Stock_Request.stock_request_no')),
    Field('stock_request_date', 'date', default = request.now),
    Field('stock_due_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),    
    Field('total_amount','integer'),
    Field('requested_by', db.auth_user, default = auth.user_id, writable = False),
    Field('srn_status_id','reference Stock_Status', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),
    Field('approved_by',db.auth_user, default = auth.user_id, writable = False),
    Field('remarks', 'text'),
    Field('stv_no', 'string', label = 'Stock Transaction No',writable = False, readable = True, requires = IS_NOT_IN_DB(db, 'Stock_Request.stv_no')),
    Field('stv_date', 'date', default = request.now),
    Field('stv_prepared_by','string'),
    Field('stv_status',db.auth_user, default = auth.user_id, writable = False),

    Field('src_no', 'string', label = 'Stock Receipt No',writable = False, readable = True, requires = IS_NOT_IN_DB(db, 'Stock_Request.src_no')),
    Field('src_date', 'date', default = request.now),
    Field('src_prepared_by',db.auth_user, default = auth.user_id, writable = False),
    Field('src_status','string'),
    
    Field('item_status_code_id','reference Status', default = 1, requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = 'stock_request_no')


db.define_table('Stock_Request_Transaction',
    Field('stock_request_id', 'reference Stock_Request'), #writable = False), #requires = IS_IN_DB(db, db.Stock_Request.id, '%(stock_request_no)s')),
    Field('item_code_id', 'reference Item_Master'), #requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('category_id'),
    Field('quantity','integer'),
    Field('uom','integer'),
    Field('price_cost', 'decimal(10,2)',default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    # Field('pieces','integer'),
    Field('remarks','text'),

    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Request_Temp',
    Field('stock_request_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
    Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
    Field('stock_due_date','date', default = request.now),
    Field('remarks','string'),
    Field('requested_by', db.auth_user, default = auth.user_id, writable = False),
    Field('srn_status_id','reference Stock_Status', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    
db.define_table('Stock_Transaction_Temp',
    Field('item_code_id', 'reference Item_Master'), #requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default =0),
    Field('uom','integer', default =0),
        # Field('total_amount','decimal(10,2)', represent = lambda value, row: locale.format('%.2F', value or 0, grouping = True),
        # compute = lambda p: p['regular_maintenance'] + p['accident_repair'] + p['statutory_expenses'] + p['spare_parts']),

    # Field('total_pieces','integer', compute = lambda p: p['quantity'] * p['uom'] + p['pieces']), 
    Field('price_cost', 'decimal(10,2)',default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),    
    Field('category_id', 'reference Transaction_Item_Category', requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')), 
    Field('amount','decimal(10,2)', default =0),
    # Field('total_amount','decimal(10,2)', represent = lambda  value, row: locale.format('%.2F', value or 0, grouping = True), compute = lambda r: r['quantity'] * r['pieces'] * r['amount']),
    Field('remarks','text'),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False))

transact = (db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id) & (db.Stock_Request_Temp.requested_by == db.Stock_Transaction_Temp.created_by)
db.define_table('post', Field('your_message', 'text'))
db.post.your_message.requires = IS_NOT_EMPTY()
# ITEM_CODE
# LOCATION_CODE
# OPENING_STOCK
# CLOSING_STOCK
# STOCK_INTRANSIT
# FREE_STOCKQTY
# REORDER_QTY

db.define_table('month', Field('name'))

db.define_table('Stock_File',
    Field('item_code_id', 'reference Item_Master', requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('location_code_id', 'reference Location', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s', zero = 'Choose Location Code')),
    Field('opening_stock', 'integer', default = 0),
    Field('closing_stock', 'integer', default = 0),
    Field('stock_in_transit', 'integer', default = 0),
    Field('free_stock_qty', 'integer', default = 0),
    Field('reorder_qty', 'integer', default = 0),
    Field('probational_balance','integer', default = 0))

db.define_table('Item_Prices',
    Field('item_code_id', 'reference Item_Master', requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('most_recent_cost', 'decimal(10,2)', default = 0),
    Field('average_cost', 'decimal(10,2)', default = 0),
    Field('most_recent_landed_cost', 'decimal(10,2)', default =0),
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('opening_average_cost', 'decimal(10,2)', default = 0),
    Field('last_issued_date', 'date', default = request.now),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('reorder_qty', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))


### PROCUREMENT SYSTEMS
  
db.define_table('Purchase_Receipt_Transaction_Header',
    Field('location_code', 'integer'),    
    Field('trn_type', 'integer'),
    Field('trn_date','date'),
    Field('purchase_receipt_number','integer'),
    Field('supp_code', 'string',length=8),
    Field('total_amount','decimal(10,2)'),
    Field('discount_percentage','decimal(10,2)'),
    Field('discount_amount','decimal(10,2)'),
    Field('other_charges','decimal(10,2)'),
    Field('po_group_ref','string',length=8),
    Field('lc_number','string', length=20),
    Field('supp_invoice_no','string',length=10),
    Field('exchange_rate','decimal(10,2)'),
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('landed_cost_rate','decimal(10,2)'),
    Field('po_type','integer'),
    Field('remarks','text'),
    Field('status','string',length=10),
    Field('print_counter'))

db.define_table('PO_Group',
    Field('po_group_refno','string', length=10),
    Field('po_number','string',length=10))

db.define_table('Purchase_Receipt_Transaction_Details',
    Field('purchase_receipt_number','string',length=10),
    Field('item_code','string',length=15),
    Field('price_cost','decimal(10,2)'),
    Field('qty','integer'),
    Field('uom','integer'),
    Field('item_category','string',length=1),
    Field('average_cost','decimal(10,2)'),
    Field('wholesale_price','decimal(10,2)'),
    Field('retail_price','decimal(10,2)'),
    Field('net_price','decimal(10,2)'),
    Field('received_date','date'),
    Field('status','string',length=10))

db.define_table('Purchase_Order_Transaction_Header',
    Field('po_number', 'string',length=10),
    Field('po_date','date'),
    Field('supp_code','string',length=10),
    Field('po_amount','decimal(10,2)'),
    Field('discount_percentage','decimal(10,2)'),
    Field('discount_amount','decimal(10,2)'),
    Field('po_type','string',length=10),
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('eta','string',length=10),
    Field('purchase_request_no','string',length=10))

db.define_table('Purchase_Order_Transaction_Details',
    Field('po_number','string',length=10),
    Field('item_code','string',length=10),
    Field('supp_price','decimal(10,2)'),
    Field('quantity','integer'),
    Field('uom','integer'),
    Field('item_category','string',length=10),
    Field('qty_received','integer'))

db.define_table('Batch_Order_Transaction',
    Field('item_code','string',length=10),
    Field('supp_price','decimal(10,2)'),
    Field('landed_cost','decimal(10,2)'),
    Field('qty','integer'),
    Field('date_ordered','date'))

####### sample ##########
db.define_table('person',
    Field('name'),
    Field('email'),
    format = '%(name)s')

# ONE (person) TO MANY (products)

db.define_table('product',
    Field('seller_id',db.person),
    Field('name'),
    Field('description', 'text'),
    Field('picture', 'upload', default=''),
    format = '%(name)s')

# MANY (persons) TO MANY (purchases)

db.define_table('purchase',
    Field('buyer_id', db.person),
    Field('product_id', db.product),
    Field('quantity', 'integer'),
    format = '%(quantity)s %(product_id)s -> %(buyer_id)s')

purchased = (db.person.id==db.purchase.buyer_id)&(db.product.id==db.purchase.product_id)

db.person.name.requires = IS_NOT_EMPTY()
db.person.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'person.email')]
db.product.name.requires = IS_NOT_EMPTY()
db.purchase.quantity.requires = IS_INT_IN_RANGE(0, 10)

