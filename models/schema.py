# auth = Auth(db,cas_provider = 'http://127.0.0.1:3000/merch_erp/default/user/cas')
# db = DAL('mssql4://username:password@localhost/test', pool_size=0)
# db = DAL('mssql://SA:M3rch@2018@localhost/master?DRIVER={FreeTDS}')
# db = DAL('mssql4://SA:M3rch@2018@localhost,1433/mpc_inv', pool_size = 0)
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
    Field('status','string',length=20, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Status.status')]),
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
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(dept_code)s')

db.define_table('Product',
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('product_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_code')]), # Field 
    Field('product_name', 'string', length = 50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name')]),
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(product_code)s')

db.define_table('SubProduct',
    Field('subproduct_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_code')]),
    Field('dept_code_id','reference Department', label = 'Department',requires = IS_IN_DB(db(db.Department.status_id == 1), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s', zero = 'Choose Product Code')),
    Field('subproduct_name','string', length = 50, requires = [IS_UPPER(),IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
    Field('status_id','reference Record_Status', label = 'Status', requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(subproduct_code)s')

db.define_table('Supplier_Master',
    Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
    Field('supp_code','string', length=10, writable = False),
    Field('supp_name','string',length=50,requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Supplier_Master.supp_name')]),
    Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL'], zero = 'Choose Type')), # foriegn or local supplier
    Field('contact_person', 'string', length=30, requires = IS_UPPER()),
    Field('address_1','string', length = 50, requires = IS_UPPER()),
    Field('address_2','string', length = 50, requires = IS_UPPER()),    
    Field('country_id','string',label = 'Country',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
    Field('contact_no','string', length=50, requires = IS_UPPER()),
    Field('fax_no','string', length=50, requires = IS_UPPER()),
    Field('email_address','string', length=50, requires = IS_UPPER()),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(supp_code)s')

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
    Field('contact_person', 'string', length=30, requires = IS_UPPER()),
    Field('address_1','string', length = 50, requires = IS_UPPER()),
    Field('address_2','string', length = 50, requires = IS_UPPER()),
    Field('country_id','string',label = 'Country',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Payment_Mode',
    Field('supplier_id', 'reference Supplier_Master', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('payment_mode','string',length=30),
    Field('payment_terms','string',length=30),
    Field('currency','string',length=20),
    Field('trade_terms','string',length=20),
    Field('forwarder_air','string',length=20),
    Field('forwarder_sea','string',length=20),
    Field('commodity_code','string',length=10),
    Field('discount_percentage','string',length=10),
    Field('custom_duty_percentage','string',length=10),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))
    
db.define_table('GroupLine',
    Field('supplier_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('group_line_code','string',length=8, writable = False),
    Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'GroupLine.group_line_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format = '%(group_line_code)s')

db.define_table('Sub_Group_Line',
    Field('group_line_code_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
    Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(group_line_code)s')

db.define_table('Brand_Line',
    Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')),
    Field('brand_line_code','string',length=8, writable = False),
    Field('brand_line_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Line.brand_line_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

# msg.flash = Incomplete Informatin
db.define_table('Brand_Classification',
    Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')), #ERROR - * Field should not be empty
    Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
    Field('brand_cls_code','string', length=8, writable = False),
    Field('brand_cls_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False), format = '%(brand_cls_code)s')


db.define_table('Fragrance_Type',
    Field('product_code_id','reference Product', requires = IS_IN_DB(db, db.Product.id, '%(product_code)s', zero = 'Choose Product Code')),
    Field('fragrance_code','string',length=6, writable = False),
    Field('fragrance_name','string',length=35, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Fragrance_Type.fragrance_name')]),
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
    Field('size_name','string',length=25, requires = IS_UPPER()),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Collection',
    Field('collection_code','string',length=5, writable = False),
    Field('collection_name','string',length=25, requires = IS_UPPER()),
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
    Field('location_group_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Location_Group.location_group_name')]),
    Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False),format='%(location_group_code)s')

db.define_table('Location',
    Field('location_group_code_id','reference Location_Group', label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),
    Field('location_code','string',length=10, writable =False),
    Field('location_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),
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
    Field('item_status_code_id','reference Status', requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')),
    Field('fragrance_code_id','reference Fragrance_Type', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(fragrance_code)s - %(fragrance_name)s', zero = 'Choose Fragrance Code')),
    Field('color_code_id','string', length=10, requires = IS_IN_SET(COLOR, zero = 'Choose Color')),
    Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(size_code)s - %(size_name)s', zero = 'Choose Size')),
    Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(collection_code)s - %(collection_name)s', zero = 'Choose Collection')),
    Field('made_in','string',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
    Field('created_on', 'date', default = request.now),
    Field('created_by', 'date',default = request.now))

db.define_table('FMCG_Division',
    Field('div_code_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
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
    Field('made_in','string',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, update=auth.user_id, writable = False, readable = False))

db.define_table('Item_Prices',
    Field('item_code_id', 'reference Itemmas'),
    Field('mr_cost', 'decimal(10,2)', default = 0),
    Field('ave_cost', 'decimal(10,2)', default = 0),
    Field('mr_lndcost', 'decimal(10,2)', default =0),
    Field('currency', 'string', length = 5, requires = IS_IN_SET(CURRENCY, zero = 'Choose Currency')),
    Field('op_avcost', 'decimal(10,2)', default = 0),
    Field('last_issdt', 'date', default = request.now),
    Field('price_wsch', 'decimal(10,2)', label = 'Price', default = 0),
    Field('price_rtch', 'decimal(10,2)',default = 0),
    Field('price_vnch', 'decimal(10,2)',default =0),
    Field('reorder_qty', 'integer', default = 0))


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
    Field('currency','string',length=5),
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
    Field('currency','string',length=10),
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