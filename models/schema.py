
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
    Field('stock_adjustment_account', 'string', length = 10), # stock adjustment account
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
    Field('exchange_rate_value', 'decimal(10,4)', default = 0),
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
    Field('supp_name','string',requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Supplier_Master.supp_name')]),
    Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL'], zero = 'Choose Type')), # foriegn or local supplier
    Field('contact_person', 'string'),
    Field('address_1','string'),
    Field('address_2','string'),
    Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('contact_no','string'),
    Field('fax_no','string'),
    Field('email_address','string',  requires = IS_EMAIL(error_message='invalid email!')),
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
    Field('account_no', 'string'),
    Field('bank_name', 'string'),
    Field('beneficiary_name', 'string'),
    Field('iban_code', 'string'),
    Field('swift_code', 'string'),
    Field('bank_address', 'string'),
    Field('city', 'string'),
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
    Field('other_supplier_name', 'string'),
    Field('contact_person', 'string'),
    Field('contact_no','string'),
    Field('fax_no','string'),
    Field('email_address','string',  requires = IS_EMAIL(error_message='invalid email!')),
    Field('address_1','string'),
    Field('address_2','string'),
    Field('country_id','reference Made_In', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Forwarders', # not used
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION', label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('forwarder_code_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Forwarder_Supplier.id, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder' )),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Supplier_Trade_Terms',
    Field('trade_terms', 'string', requires = [IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Trade_Terms.trade_terms')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'trade_terms')

db.define_table('Supplier_Payment_Mode',
    Field('payment_mode','string', requires = [IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Payment_Mode.payment_mode')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'payment_mode')

db.define_table('Supplier_Payment_Terms',
    Field('payment_terms','string',requires = [IS_UPPER(),IS_NOT_IN_DB(db,'Supplier_Payment_Terms.payment_terms')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'payment_terms')

db.define_table('Supplier_Payment_Mode_Details',
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',label = 'Supplier', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier')),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),
    Field('payment_mode_id', 'reference Supplier_Payment_Mode', ondelete = 'NO ACTION',label = 'Payment Mode', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode'))), #'string', length = 25, requires = IS_IN_SET(['LC','TELEX TRANSFER'], zero = 'Choose Payment Mode')),
    Field('payment_terms_id', 'reference Supplier_Payment_Terms', ondelete = 'NO ACTION',label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), #'string', length = 25, requires = IS_IN_SET(['LC','45 DAYS'], zero = 'Choose Payment Mode')),
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('forwarder_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION',label = 'Forwarder', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder'))),
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
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s, %(supp_sub_code)s', zero =  'Choose Supplier')),
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
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
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
    Field('brand_cls_name','string',length=100, requires = [IS_LENGTH(100),IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
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
    Field('stock_adjustment_code', 'string', length = 10), # stock adjustment account
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

db.define_table('User_Location',
    Field('user_id', db.auth_user, ondelete = 'NO ACTION'),
    Field('location_code_id', 'reference Location', ondelete='NO ACTION', requires=IS_IN_DB(db, db.Location.id,'%(location_code)s %(location_name)s',zero='Choose Location')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

db.define_table('Back_Office_User',
    Field('user_id', db.auth_user, ondelete = 'NO ACTION'),
    Field('department_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),        
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section'),('A','Food/Non-Food Section')],zero ='Choose Section')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

db.define_table('Sales_Manager_User',
    Field('user_id', db.auth_user, ondelete = 'NO ACTION'),
    Field('department_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),        
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section'),('A','Food/Non-Food Section')],zero ='Choose Section')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

db.define_table('User_Department',
    Field('user_id', db.auth_user, ondelete = 'NO ACTION'),
    Field('department_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),    
    Field('van_sales','boolean',label ='Van Sales',default=False),
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
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
    Field('item_code', 'string', length = 15, label = 'Item Code'), #requires = [IS_LENGTH(15),IS_NOT_IN_DB(db, 'Item_Master.item_code')]),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
    Field('item_description_ar', 'string', length = 50, label = 'Arabic Name', requires = [IS_LENGTH(50), IS_UPPER()]),
    Field('supplier_item_ref', 'string', length = 20), #requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
    Field('int_barcode', 'string', length = 20), #requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
    Field('loc_barcode', 'string', length = 20), #requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
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
    Field('product_code_id','reference Product', ondelete = 'NO ACTION',label = 'Product Code',requires = IS_EMPTY_OR(IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code'))),
    Field('subproduct_code_id', 'reference SubProduct', ondelete = 'NO ACTION',label = 'SubProduct', requires = IS_EMPTY_OR(IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct'))),
    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_EMPTY_OR(IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code'))),
    Field('brand_line_code_id','reference Brand_Line', ondelete = 'NO ACTION',requires = IS_EMPTY_OR(IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line'))),
    Field('brand_cls_code_id','reference Brand_Classification',ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification'))),
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

db.define_table('Stock_File',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('item_code','string',length=25),
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
    Field('opening_stock', 'integer', default = 0),
    Field('closing_stock', 'integer', default = 0),
    Field('previous_year_closing_stock', 'integer', default = 0),
    Field('stock_in_transit', 'integer', default = 0),
    Field('order_in_transit', 'integer', default = 0), 
    Field('free_stock_qty', 'integer', default = 0),    
    Field('reorder_qty', 'integer', default = 0), 
    Field('last_transfer_qty', 'integer', default = 0),
    Field('probational_balance','integer', default = 0),
    Field('damaged_stock_qty', 'integer', default = 0),
    Field('last_transfer_date', 'datetime', default = request.now),
    Field('pos_stock', 'integer', default = 0), # from stock receipt
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Card_Movement',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', writable = False),
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION', writable = False),    
    Field('type','string', length = 10),
    Field('transaction_no','integer', default = 0),
    Field('date_approved', 'date', default = request.now),
    Field('category_description', 'string', length = 25),
    Field('quantity_in', 'integer', default = 0),
    Field('quantity_out', 'integer', default = 0),
    Field('quantity_balanced', 'integer', default = 0),
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

db.define_table('Dbf_Batch_Table',
    Field('batch_code','string',length=25),    
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False),format = 'batch_code')

db.define_table('Stock_Header_Consolidation',
    Field('transaction_no','string',length = 25), # 25 length
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8    
    Field('customer_code_id','string',length=50),    # create normal
    Field('transaction_date', 'date'), # from date of transaction
    Field('account', 'string', length = 10), #adjustment code, customer code, supplier code. etc...
    Field('total_amount','decimal(20,6)', default = 0),
    Field('discount_percentage','decimal(20,6)', default = 0),
    Field('discount_added','decimal(20,6)', default = 0),
    Field('total_selective_tax','decimal(20,6)', default = 0),
    Field('total_selective_tax_foc','decimal(20,6)', default = 0),
    Field('stock_destination','reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
    Field('batch_code_id','reference Dbf_Batch_Table',ondelete='NO ACTION',requires = IS_IN_DB(db,db.Dbf_Batch_Table.id,'%()s',zero = 'Choose Batch Code')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Transaction_Consolidation',
    Field('transaction_no_id','reference Stock_Header_Consolidation',ondelete='NO ACTION',requires = IS_IN_DB(db,db.Stock_Header_Consolidation.id,'%(transaction_no)s',zero='Choose Transaction')),    
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8
    Field('transaction_date', 'date'), # from date of transaction    
    Field('item_code', 'string', length = 25), # item master
    Field('category_id', 'reference Transaction_Item_Category',ondelete = 'NO ACTION'), 
    Field('uom', 'integer'), # from transaction
    Field('quantity', 'integer'), # from transaction
    Field('average_cost','decimal(20,6)', default = 0), # average cost
    Field('price_cost', 'decimal(20,6)', default = 0), # pieces
    Field('sale_cost','decimal(20,6)', default = 0), # after discount
    Field('discount', 'integer', default = 0), # normal discount from pos
    Field('wholesale_price', 'decimal(20,2)', default = 0), # from item prices
    Field('retail_price', 'decimal(20,2)', default = 0), # from item prices
    Field('vansale_price', 'decimal(20,2)', default = 0), # from item prices
    Field('tax_amount', 'decimal(20,2)', default = 0), # in sales
    Field('selected_tax','decimal(20,2)'), # in sales
    Field('sales_lady_code', 'string',length = 10), # sales, pos
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_destination', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Merch_Stock_Header',
    Field('voucher_no','integer'), # 10 length
    Field('location', 'integer'),   # from location master
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8
    Field('transaction_date', 'date'), # from date of transaction
    Field('account', 'string', length = 10), #adjustment code, customer code, supplier code. etc...
    Field('dept_code','integer'), # from item master
    Field('total_amount','decimal(20,6)', default = 0),    
    Field('total_amount_after_discount','decimal(20,6)', default = 0),        
    Field('discount_percentage','decimal(20,6)', default = 0),
    Field('discount_added','decimal(20,6)', default = 0),

    Field('supplier_reference_order','string', length = 25),    
    Field('supplier_invoice','string', length = 25),    
    Field('exchange_rate','decimal(20,6)', default = 0, required = True),    
    Field('landed_cost','decimal(20,6)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  # ()=> order type 'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),        
    Field('other_charges','decimal(20,6)', default = 0),    
    Field('custom_duty_charges','decimal(20,6)', default = 0),    

    Field('total_selective_tax','decimal(20,6)', default = 0),
    Field('total_selective_tax_foc','decimal(20,6)', default = 0),
    Field('stock_destination','integer'),
    Field('sales_man_code','string',length=15),    
    Field('batch_code_id','reference Dbf_Batch_Table',ondelete='NO ACTION'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Merch_Stock_Transaction',
    Field('merch_stock_header_id','reference Merch_Stock_Header',ondelete='NO ACTION',requires = IS_IN_DB(db,db.Merch_Stock_Header.id,'%(voucher_no)s',zero='Choose Transaction')),
    Field('voucher_no','string',length=25), # 10 length
    Field('location', 'integer'),   # from location master
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8
    Field('transaction_date', 'date'), # from date of transaction    
    Field('item_code', 'string', length = 15), # item master
    Field('category_id','string', lenght=10), # n-normal, p-promotional
    Field('uom', 'integer'), # from transaction
    Field('quantity', 'integer'), # from transaction
    Field('average_cost','decimal(20,6)', default = 0), # average cost
    Field('price_cost', 'decimal(20,6)', default = 0), # pieces
    Field('sale_cost','decimal(20,6)', default = 0), # after discount
    Field('sale_cost_notax_pcs', 'decimal(20,6)', default = 0), # sales cost without tax
    Field('discount', 'integer', default = 0), # normal discount from pos
    Field('wholesale_price', 'decimal(20,6)', default = 0), # from item prices
    Field('retail_price', 'decimal(20,6)', default = 0), # from item prices
    Field('vansale_price', 'decimal(20,6)', default = 0), # from item prices
    Field('tax_amount', 'decimal(20,2)', default = 0), # in sales
    Field('selected_tax','decimal(20,2)', default = 0), # in sales
    Field('price_cost_after_discount','decimal(20,2)', default = 0), # included in sales invoice transaction
    Field('sales_man_code','string',length=15),
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.
    Field('selective_tax_price','decimal(20,2)', default = 0), # from item_prices
    # Field('sales_lady_code', 'string',length = 10), # sales, pos
    Field('supplier_code','string', length = 10), # from item code
    Field('dept_code','integer'), # from item master
    Field('stock_destination','integer'), # destination of stock transfer
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Master_Account',
    Field('account_code','string', length = 15),
    Field('account_name','string', length = 50),    
    Field('master_account_type_id','string',length=25,requires = IS_IN_SET([('A', 'A - Accounts'), ('C', 'C - Customer'), ('E', 'E - Employee'),('S','S - Supplier'),('SAC','SAC - Stock Adjustment Code'),('OOS','OOS - Obselensce Of Stock')],zero='Choose Account Type')), #Customer,Accounts,Supplier,Employees    
    Field('stock_adjustment_account', 'string'), # stock adjustment account
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Adjustment',
    Field('stock_adjustment_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_adjustment_no','integer'),
    Field('transaction_no', 'integer', default = 0, writable = False),
    Field('transaction_date', 'date', default=request.now),
    Field('stock_adjustment_date', 'date', default = request.now),
    Field('stock_adjustment_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Account Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Account')),    # create normal    
    Field('stock_adjustment_code','string', length = 10),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),    
    Field('adjustment_type', 'reference Adjustment_Type', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Adjustment_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('total_amount','decimal(10,4)', default = 0),    
    Field('srn_status_id','reference Stock_Status', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('approved_by', 'reference auth_user', writable = False),
    Field('date_approved', 'datetime'),
    Field('total_selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'), # outer
    Field('archive','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

# Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))

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
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'), # outer
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax FOC'), # outer
    Field('delete', 'boolean', default = False),
    Field('total_amount','decimal(20,6)', default = 0),    
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
    Field('price_cost','decimal(10,4)',default=0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('total_cost','decimal(10,4)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'), # outer
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'), # outer
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False))

db.define_table('Item_Prices',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
    Field('item_code','string',length=25),
    Field('most_recent_cost', 'decimal(16,4)', default = 0),
    Field('average_cost', 'decimal(16,4)', default = 0),
    Field('most_recent_landed_cost', 'decimal(16,4)', default = 0),
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('opening_average_cost', 'decimal(16,4)', default = 0),
    Field('last_issued_date', 'date', default = request.now),
    Field('wholesale_price', 'decimal(16,2)', default = 0),
    Field('retail_price', 'decimal(16,2)',default = 0),
    Field('vansale_price', 'decimal(16,2)',default =0),
    Field('selective_tax_percentage','decimal(16,2)',default=0),
    Field('selective_tax_price','decimal(16,2)',default=0),
    Field('vat_percentage','decimal(16,2)',default=0),
    Field('vat_price','decimal(16,2)',default=0), # tax amount?
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
    Field('transaction_no','integer', writable = False),
    Field('transaction_date', 'date', writable = False),    
    Field('total_amount','decimal(20,6)', default = 0),
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
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('total_amount','decimal(20,6)', default = 0),
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
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
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

db.define_table('Customer_Classification', # hypermarket, restaurant
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

db.define_table('Customer_Group_Code',# assets, receivable, payables, journals
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Area_Name',
    Field('area_name', 'string',length=50),
    Field('zone_no','integer'),    
    Field('municipality','string',legnth=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False),format='area_name')

db.define_table('Customer',
    Field('customer_account_no','string',length = 15),
    Field('customer_group_code_id', 'reference Customer_Group_Code', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Customer_Group_Code.id,'%(description)s', zero = 'Choose Group Code'))), 
    Field('customer_name','string', length = 50),
    Field('customer_category_id', 'reference Customer_Category', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Customer_Category.id,'%(description)s', zero = 'Choose Category'))), 
    Field('customer_account_type', 'reference Customer_Account_Type', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Customer_Account_Type.id,'%(description)s', zero = 'Choose Account Type')), 
    Field('parent_outlet','string',length=50),
    Field('department_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),    
    Field('cr_no','string',length=25),
    Field('po_box_no', 'integer'),    
    Field('unit_no', 'integer'),
    Field('building_no', 'integer'),
    Field('street_no', 'integer'),
    Field('zone', 'integer'),
    Field('area_name_id','reference Area_Name', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Area_Name.id,'%(area_name)s', zero = 'Choose Area Name'))), 
    Field('area_name','string', length = 150),
    Field('state','string', length = 50),
    Field('country','string', length = 50),
    Field('telephone_no','string',length = 25),
    Field('mobile_no','string',length = 25),
    Field('fax_no','string',length = 25),
    Field('email_address','string', length = 50),
    Field('contact_person','string',length = 25),
    Field('longtitude','string',length=50),
    Field('latitude','string',length=50),
    
    Field('outlet_category','string',length=50),
    Field('outlet_type','string',length=50),
    Field('outlet_classification','string',length=50),

    Field('sponsor_name','string', length = 50),    
    Field('sponsor_contact_no','string', length = 50),
    ## upload files to fill in here (5 fields)
    
    Field('cr_license','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),
    Field('guarantee','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),    
    Field('customer_form','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),    
    Field('sponsor_id','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),
    
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

db.define_table('Employee_Master',
    Field('account_code', 'string', length = 10),
    Field('title','string',length = 25, requires = IS_IN_SET(['Mr.','Ms.','Mrs.','Mme'], zero = 'Title')),    
    Field('first_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]),
    Field('middle_name','string',length = 50),
    Field('last_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'customer_account_no')

db.define_table('Sales_Man',
    Field('users_id', db.auth_user, ondelete = 'NO ACTION'),
    Field('mv_code','string',length=25),    
    Field('employee_id','reference Employee_Master', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Employee'))),    
    Field('van_sales','boolean',label ='Van Sales',default=False),
    Field('section_id','string',length=25,requires = IS_EMPTY_OR(IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section'))),
    Field('parent_outlet','string',length=50),
    Field('department_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_EMPTY_OR(IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty'))),    
    Field('location_code_id', 'reference Location', ondelete='NO ACTION', requires=IS_EMPTY_OR(IS_IN_DB(db, db.Location.id,'%(location_code)s %(location_name)s',zero='Choose Location'))),
    Field('cr_no','string',length=25),
    Field('po_box_no', 'integer'),    
    Field('unit_no', 'integer'),
    Field('building_no', 'integer'),
    Field('street_no', 'integer'),
    Field('zone', 'integer'),
    Field('area_name_id','reference Area_Name', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Area_Name.id,'%(area_name)s', zero = 'Choose Area Name'))), 
    Field('area_name','string', length = 150),
    Field('state','string', length = 50),
    Field('country','string', length = 50),
    Field('telephone_no','string',length = 25),
    Field('mobile_no','string',length = 25),
    Field('fax_no','string',length = 25),
    Field('email_address','string', length = 50),
    Field('contact_person','string',length = 25),
    Field('longtitude','string',length=50),
    Field('latitude','string',length=50),    
    Field('outlet_category','string',length=50),
    Field('outlet_type','string',length=50),
    Field('outlet_classification','string',length=50),
    Field('sponsor_name','string', length = 50),
    Field('sponsor_id','string', length = 50),
    Field('sponsor_contact_no','string', length = 50),   
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Man_Customer',
    Field('sales_man_id','reference Sales_Man',ondelete='NO ACTION',requires = IS_IN_DB(db, db.Sales_Man.id,'%(mv_code)s', zero = 'Choose Sales Man')),
    Field('users_id', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False),
    Field('master_account_type_id','string',length=25,requires = IS_IN_SET([('A', 'A - Accounts'), ('C', 'C - Customer'), ('E', 'E - Employee'),('S','S - Supplier')],zero='Choose Account Type')), #Customer,Accounts,Supplier,Employees
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Order',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_order_no', 'integer', default = 0, writable = False),
    Field('sales_order_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Customer')),    # create normal
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(20,2)', default = 0),    
    Field('total_amount_after_discount','decimal(20,2)', default = 0),    
    Field('total_selective_tax', 'decimal(20,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(20,2)', default = 0),
    Field('discount_added','decimal(10,2)', default = 0),
    Field('total_vat_amount', 'decimal(20,2)', default = 0),
    Field('sales_order_date_approved','datetime', writable = False),
    Field('sales_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),

    Field('delivery_note_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('delivery_note_no', 'integer', writable = False),
    Field('delivery_note_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('delivery_note_date_approved','datetime', writable = False),

    Field('sales_invoice_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_invoice_no', 'integer', writable = False),    
    Field('sales_invoice_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('sales_invoice_date_approved','datetime', writable = False),
    
    Field('cancelled','boolean',default = False),
    Field('cancelled_by','reference auth_user',ondelete='NO ACTION',writable=False),
    Field('cancelled_on', 'datetime', default=request.now, writable = False, readable = False),
    
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
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
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer with tax
    Field('packet_price_cost', 'decimal(20,6)', default = 0), # per packet with tax
    Field('total_amount','decimal(20,2)', default = 0),
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,6)', default = 0), # pcs
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),
    Field('vansale_price', 'decimal(20,2)',default =0),
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('net_price', 'decimal(20,2)',default =0),
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('packet_selective_tax','decimal(20,6)', default = 0, label = 'Selective Tax'), # packet
    Field('packet_selective_tax_foc','decimal(20,6)', default = 0, label = 'Selective Tax'), # packet
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),            
    Field('delete', 'boolean', default = False),    
    Field('discounted','boolean',default=False),
    Field('discount_added','decimal(10,2)', default = 0),
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
    Field('price_cost','decimal(20,6)', default = 0),
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('total_amount','decimal(20,2)', default = 0),
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('net_price', 'decimal(20,2)',default =0),
    Field('taxable_value','decimal(20,2)', default = 0),
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'),  
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax FOC'),  
    Field('tax_percentage','decimal(20,2)', default = 0),
    Field('tax_amount','decimal(20,2)', default = 0),
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
    Field('customer_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Customer')),        
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(20,2)', default = 0),    
    Field('total_amount_after_discount','decimal(20,2)', default = 0),    
    Field('total_selective_tax', 'decimal(20,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(20,2)', default = 0),
    Field('discount_added', 'decimal(10,2)',default =0), # on hold structure
    Field('total_vat_amount', 'decimal(20,2)', default = 0),
    
    Field('sales_return_date_approved','date', writable = False),
    Field('sales_return_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),

    Field('sales_manager_id', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False), #approve/reject
    Field('sales_manager_date','datetime',update=request.now, writable = False, readable = True),

    Field('warehouse_id', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),#approve/reject
    Field('warehouse_date','datetime',update=request.now, writable = False, readable = True),

    Field('accounts_id', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),#approve/reject
    Field('accounts_date','datetime',update=request.now, writable = False, readable = True),

    Field('remarks', 'string'),   
    Field('section_id','string',length=25,requires = IS_EMPTY_OR(IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section'))),
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Sales_Man.id, '%(name)s', zero = 'Choose Salesman')),   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('archives', 'boolean', default = False),    
    Field('processed','boolean',default=False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Return_Transaction',
    Field('sales_return_no_id','reference Sales_Return',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer with tax
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,6)', default = 0), # packet
    Field('sale_cost_notax_pcs', 'decimal(20,6)', default = 0), # sales cost without tax
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),
    
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs. without tax
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.without tax   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.without tax
    
    Field('price_cost_after_discount','decimal(20,2)'), 
    Field('vansale_price', 'decimal(20,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),

    Field('discounted','boolean',default=False),
    Field('discount_added','decimal(10,2)', default = 0),
    Field('net_price', 'decimal(20,2)',default =0),
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_price','decimal(20,2)', default = 0, label = 'Selective Tax'), # from item_prices
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),            
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
    Field('price_cost','decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
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
    Field('transaction_no', 'integer', default = 0, writable = False),
    Field('transaction_date', 'date', default=request.now, writable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'sales_order_no')
 
db.define_table('Obsolescence_Stocks_Transaction',
    Field('obsolescence_stocks_no_id','reference Obsolescence_Stocks',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),            
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(10,4)', default = 0),
    Field('sale_cost', 'decimal(10,6)', default = 0),
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
    Field('price_cost','decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
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
    Field('sales_order_no', 'integer', default = 0, writable = False),
    Field('sales_order_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Customer')),    # create normal
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(20,2)', default = 0),    
    Field('total_amount_after_discount','decimal(20,2)', default = 0),    
    Field('total_selective_tax', 'decimal(20,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(20,2)', default = 0),
    # Field('discount_percentage', 'decimal(20,2)',default =0), # on hold structure
    Field('discount_added','decimal(10,2)', default = 0),
    Field('total_vat_amount', 'decimal(20,2)', default = 0),
    Field('sales_order_date_approved','datetime', writable = False),
    Field('sales_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),
    Field('delivery_note_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('delivery_note_no', 'integer', writable = False),
    Field('delivery_note_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('delivery_note_date_approved','datetime', writable = False),
    Field('sales_invoice_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_invoice_no', 'integer', writable = False),    
    Field('sales_invoice_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('sales_invoice_date_approved','datetime', writable = False),
    Field('cancelled','boolean',default = False),
    Field('cancelled_by','reference auth_user',ondelete='NO ACTION',writable=False),
    Field('cancelled_on', 'datetime', default=request.now, writable = False, readable = False),

    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Sales_Man.id, '%(name)s', zero = 'Choose Salesman')),   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('archives', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'sales_order_no')
 
db.define_table('Delivery_Note_Transaction',
    Field('delivery_note_id','reference Delivery_Note',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer
    Field('packet_price_cost', 'decimal(20,6)', default = 0), # per packet
    Field('total_amount','decimal(20,2)', default = 0),
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,6)', default = 0), # packet
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),

    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('average_cost_pcs','decimal(20,4)', default = 0), # per pcs.   
    Field('wholesale_price_pcs', 'decimal(20,2)', default = 0), # per pcs.
    Field('retail_price_pcs', 'decimal(20,2)',default = 0), # per pcs.
        
    Field('vansale_price', 'decimal(20,2)',default =0),
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('net_price', 'decimal(20,2)',default =0),
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('packet_selective_tax','decimal(20,6)', default = 0, label = 'Selective Tax'), # packet
    Field('packet_selective_tax_foc','decimal(20,6)', default = 0, label = 'Selective Tax'), # packet
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),            
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Sales_Invoice',       
    Field('transaction_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_order_no', 'integer', default = 0, writable = False),
    Field('sales_order_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('customer_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_code)s - %(account_name)s', zero = 'Choose Customer')),    # create normal
    Field('customer_order_reference','string', length = 25),
    Field('delivery_due_date', 'date', default = request.now),
    Field('total_amount','decimal(20,2)', default = 0),    
    Field('total_amount_after_discount','decimal(20,2)', default = 0),    
    Field('total_selective_tax', 'decimal(20,2)', default = 0),
    Field('total_selective_tax_foc', 'decimal(20,2)', default = 0),
    # Field('discount_percentage', 'decimal(20,2)',default =0), # on hold structure
    Field('discount_added','decimal(10,2)', default = 0),
    Field('total_vat_amount', 'decimal(20,2)', default = 0),
    Field('sales_order_date_approved','datetime', writable = False),
    Field('sales_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),

    Field('delivery_note_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('delivery_note_no', 'integer', writable = False),
    Field('delivery_note_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('delivery_note_date_approved','datetime', writable = False),

    Field('sales_invoice_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('sales_invoice_no', 'integer', writable = False),    
    Field('sales_invoice_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('sales_invoice_date_approved','datetime', writable = False),

    Field('cancelled','boolean',default = False),
    Field('cancelled_by','reference auth_user',ondelete='NO ACTION',writable=False),
    Field('cancelled_on', 'datetime', default=request.now, writable = False, readable = False),
    
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Sales_Man.id, '%(name)s', zero = 'Choose Salesman')),   
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('archives', 'boolean', default = False),    
    Field('processed','boolean',default=False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))
 
db.define_table('Sales_Invoice_Transaction',
    Field('sales_invoice_no_id','reference Sales_Invoice',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer with tax
    Field('packet_price_cost', 'decimal(20,6)', default = 0), # per packet with tax
    Field('total_amount','decimal(20,2)', default = 0),
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,6)', default = 0), # packet
    Field('sale_cost_notax_pcs', 'decimal(20,6)', default = 0), # sales cost without tax
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),
    Field('vansale_price', 'decimal(20,2)',default =0),
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('net_price', 'decimal(20,2)',default =0),
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs. without tax
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.without tax   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.without tax
    Field('price_cost_after_discount','decimal(20,2)'), 
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer    
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('selective_tax_price','decimal(20,2)', default = 0, label = 'Selective Tax'), # from item_prices
    Field('packet_selective_tax','decimal(20,6)', default = 0, label = 'Selective Tax'), # packet
    Field('packet_selective_tax_foc','decimal(20,6)', default = 0, label = 'Selective Tax'), # packet
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),            
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('upddocument_register_grid_processated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

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
    Field('stock_request_pre_date_approved', 'datetime', writable = False),
    Field('stock_request_pre_approved_by', 'reference auth_user',ondelete = 'NO ACTION', writable = False),

    Field('stock_request_date_approved','datetime',writable=False),
    Field('stock_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),    

    Field('stock_transfer_no_id', 'reference Transaction_Prefix',ondelete = 'NO ACTION', writable = False),    
    Field('stock_transfer_no', 'integer', writable = False),
    Field('stock_transfer_date_approved', 'date', writable = False),
    Field('stock_transfer_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('stock_transfer_dispatched_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('stock_transfer_dispatched_date','datetime', writable = False),
    Field('stock_receipt_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_receipt_no', 'integer', writable = False),    
    Field('stock_receipt_date_approved', 'date', writable = False),
    Field('stock_receipt_approved_by', 'reference auth_user',ondelete = 'NO ACTION', writable = False),
    Field('ticket_no', 'string', length = 10, writable = False, requires = [IS_LENGTH(10),IS_UPPER(), IS_NOT_IN_DB(db, 'Stock_Request.ticket_no')]),
    Field('archive','boolean', default = False),
    Field('cancelled','boolean',default = False),
    Field('cancelled_by','reference auth_user',ondelete='NO ACTION',writable=False),
    Field('cancelled_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'stock_request_no')

db.define_table('Stock_Request_Transaction',    
    Field('stock_request_id', 'reference Stock_Request', ondelete = 'NO ACTION',readable = False), #writable = False), #requires = IS_IN_DB(db, db.Stock_Request.id, '%(stock_request_no)s')),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('total_amount','decimal(20,2)', default = 0),
    Field('unit_price', 'decimal(20,2)',default =0), # _prc.retail_price + _prc.selective_tax,+
    
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer with tax
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs. without tax
    Field('sale_cost', 'decimal(20,6)', default = 0), # packet/outer/carton
    Field('sale_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.without tax   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.without tax  
    
    Field('average_cost','decimal(20,4)', default = 0),    
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),    
    Field('vansale_price', 'decimal(20,2)',default =0),
    
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer    
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),    
    Field('remarks','string', length = 50),        
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

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
    Field('amount','decimal(10,2)', default = 0, compute = lambda p: p['qty'] * p['price_cost']),
    Field('remarks','string'),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Transfer',       
    Field('stock_request_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('stock_request_no', 'integer', default = 0, writable = False),
    Field('stock_request_date', 'date', default = request.now),
    Field('stock_due_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('stock_destination_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),    
    Field('total_amount','decimal(10,2)', default = 0),
    Field('srn_status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('stock_request_date_approved','datetime',writable=False),
    Field('stock_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),    
    Field('stock_transfer_no_id', 'reference Transaction_Prefix',ondelete = 'NO ACTION', writable = False),    
    Field('stock_transfer_no', 'integer', writable = False),
    Field('stock_transfer_date_approved', 'datetime', writable = False),
    Field('stock_transfer_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('stock_transfer_dispatched_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('stock_transfer_dispatched_date','datetime', writable = False),
    Field('stock_receipt_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_receipt_no', 'integer', writable = False),    
    Field('stock_receipt_date_approved', 'datetime', writable = False),
    Field('stock_receipt_approved_by', 'reference auth_user',ondelete = 'NO ACTION', writable = False),   
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'stock_request_no')

db.define_table('Stock_Transfer_Transaction',    
    Field('stock_transfer_no_id', 'reference Stock_Transfer', ondelete = 'NO ACTION',readable = False), 
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('total_amount','decimal(20,2)', default = 0),
    Field('unit_price', 'decimal(20,2)',default =0), # _prc.retail_price + _prc.selective_tax,+
    
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer with tax
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs. without tax
    Field('sale_cost', 'decimal(20,6)', default = 0), # packet/outer/carton
    Field('sale_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.without tax   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.without tax  
    
    Field('average_cost','decimal(20,4)', default = 0),    
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),    
    Field('vansale_price', 'decimal(20,2)',default =0),
    
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer    
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),    
    Field('remarks','string', length = 50),        
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Stock_Receipt',       
    Field('stock_request_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('stock_request_no', 'integer', default = 0, writable = False),
    Field('stock_request_date', 'date', default = request.now),
    Field('stock_due_date', 'date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('stock_source_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('stock_destination_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),    
    Field('total_amount','decimal(10,2)', default = 0),
    Field('srn_status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('stock_request_date_approved','datetime',writable=False),
    Field('stock_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('remarks', 'string'),    
    Field('stock_transfer_no_id', 'reference Transaction_Prefix',ondelete = 'NO ACTION', writable = False),    
    Field('stock_transfer_no', 'integer', writable = False),
    Field('stock_transfer_date_approved', 'datetime', writable = False),
    Field('stock_transfer_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('stock_transfer_dispatched_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('stock_transfer_dispatched_date','datetime', writable = False),
    Field('stock_receipt_no_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),
    Field('stock_receipt_no', 'integer', writable = False),    
    Field('stock_receipt_date_approved', 'datetime', writable = False),
    Field('stock_receipt_approved_by', 'reference auth_user',ondelete = 'NO ACTION', writable = False),   
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('processed','boolean',default=False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'stock_request_no')

db.define_table('Stock_Receipt_Transaction',    
    Field('stock_receipt_no_id', 'reference Stock_Receipt', ondelete = 'NO ACTION',readable = False), #writable = False), #requires = IS_IN_DB(db, db.Stock_Request.id, '%(stock_request_no)s')),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('total_amount','decimal(20,2)', default = 0),
    Field('unit_price', 'decimal(20,2)',default =0), # _prc.retail_price + _prc.selective_tax,+
    
    Field('price_cost', 'decimal(20,6)', default = 0), # per outer with tax
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs. without tax
    Field('sale_cost', 'decimal(20,6)', default = 0), # packet/outer/carton
    Field('sale_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.without tax   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.without tax
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.without tax  
    
    Field('average_cost','decimal(20,4)', default = 0),    
    Field('wholesale_price', 'decimal(20,2)', default = 0),
    Field('retail_price', 'decimal(20,2)',default = 0),    
    Field('vansale_price', 'decimal(20,2)',default =0),
    
    Field('selective_tax','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer    
    Field('selective_tax_foc','decimal(20,2)', default = 0, label = 'Selective Tax'), # outer
    Field('vat_percentage','decimal(20,2)', default = 0, label = 'Vat Percentage'),    
    Field('remarks','string', length = 50),        
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
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_sub_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),    
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),
    Field('estimated_time_of_arrival', 'date', default = request.now), #requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'), minimum=datetime.date(2008, 1, 1),error_message='must be YYYY-MM-DD!')),    
    Field('total_amount','decimal(15,4)', default = 0),    
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('total_amount_invoiced','decimal(15,4)', default = 0),    # account invoiced
    Field('added_discount_amount_invoiced', 'decimal(10,3)',default =0), # account invoiced
    Field('total_amount_after_discount_invoiced','decimal(15,4)', default = 0), # account invoiced
    Field('insured', 'boolean', default = False),
    Field('foreign_currency_value','decimal(10,3)', default = 0),
    Field('local_currency_value','decimal(10,3)', default = 0),
    Field('exchange_rate','decimal(10,4)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure    
    Field('added_discount_amount', 'decimal(10,3)',default =0), # on hold structure    
    Field('currency_id','reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('remarks', 'string'),
    Field('remarks_created_by',db.auth_user,ondelete='NO ACTION',writable=False,readable=False),

    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'integer', writable = False),
    Field('purchase_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_date_approved','date', writable = False),
    Field('purchase_order_date','date', writable = False),
        
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('purchase_receipt_date','date', writable = False),
    Field('supplier_account_code','string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('supplier_account_code_description','string', length = 50),
    Field('supplier_invoice','string', length = 25),

    Field('landed_cost','decimal(10,6)', default = 0),
    Field('other_charges','decimal(10,6)', default = 0),    
    Field('custom_duty_charges','decimal(10,6)', default = 0),        
    Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),

    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('submitted','boolean', default = False),
    Field('posted','boolean', default = False),
    Field('draft','boolean', default = True),
    Field('selected','boolean', default = False), 

    Field('consolidated','boolean', default = False),
    Field('save_as_draft','boolean', default = False), # manoj save as draft
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('proforma_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),    
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
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
    Field('uom','integer', default = 0),    
    Field('total_pieces','integer', default = 0),        
    Field('price_cost', 'decimal(20,6)', default = 0),        
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,2)',default =0),
    Field('total_amount','decimal(15,6)', default = 0),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Request_Transaction',
    Field('purchase_request_no_id','reference Purchase_Request',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code','string', length = 50),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # quantity requested
    Field('quantity_ordered','integer', default = 0), # quantity ordered
    Field('quantity_received','integer', default = 0), # quantity received/warehouse
    Field('quantity_invoiced','integer', default = 0), # quantity invoiced/accounts
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('price_cost_invoiced', 'decimal(20,6)', default = 0),
    Field('net_price_invoiced', 'decimal(20,6)', default = 0), # invoiced    
    Field('discount_percentage_invoiced', 'decimal(10,2)',default =0), # invoiced
    Field('total_amount_invoiced','decimal(20,6)', default = 0), # invoiced
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,4)', default = 0),
    Field('wholesale_price', 'decimal(10,4)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,3)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('production_date', 'date'),
    Field('expiration_date', 'date'),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False), #warehouse processed
    Field('delete', 'boolean', default = False),    
    Field('delete_receipt', 'boolean', default = False),    
    Field('delete_invoiced', 'boolean', default = False),    
    Field('item_remarks', 'string'),
    Field('partial','boolean', default = False), #warehouse processed
    Field('new_item','boolean', default=False),    
    Field('quantity_ordered_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_received_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_invoiced_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Order',    
    Field('purchase_request_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_request_no', 'integer', writable = False),
    Field('purchase_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_request_date_approved','date', writable = False),
    Field('purchase_request_date', 'date', default = request.now, writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_sub_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),    
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),
    Field('estimated_time_of_arrival', 'date', default = request.now), #requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'), minimum=datetime.date(2008, 1, 1),error_message='must be YYYY-MM-DD!')),
    Field('total_amount','decimal(15,4)', default = 0),    
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('insured', 'boolean', default = False),
    Field('foreign_currency_value','decimal(10,3)', default = 0),
    Field('local_currency_value','decimal(10,3)', default = 0),
    Field('exchange_rate','decimal(10,4)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure    
    Field('added_discount_amount', 'decimal(10,3)',default =0), # on hold structure    
    Field('currency_id','reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('remarks', 'string'),
    Field('remarks_created_by',db.auth_user,ondelete='NO ACTION',writable=False,readable=False),

    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'integer', writable = False),
    Field('purchase_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_date_approved','date', writable = False),
    Field('purchase_order_date','date', writable = False),

    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('purchase_receipt_date','date', writable = False),
    Field('supplier_account_code','string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('supplier_account_code_description','string', length = 50),
    Field('supplier_invoice','string', length = 25),

    Field('landed_cost','decimal(10,6)', default = 0),
    Field('other_charges','decimal(10,6)', default = 0),    
    Field('custom_duty_charges','decimal(10,6)', default = 0),        
    Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),

    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('submitted','boolean', default = False),
    Field('posted','boolean', default = False),
    Field('draft','boolean', default = True),
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('proforma_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),    
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_order_no')


db.define_table('Purchase_Order_Transaction',
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code','string', length = 50),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # quantity requested
    Field('quantity_ordered','integer', default = 0), # quantity ordered
    Field('quantity_received','integer', default = 0), # quantity received/warehouse
    Field('quantity_invoiced','integer', default = 0), # quantity invoiced/accounts
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,4)', default = 0),
    Field('wholesale_price', 'decimal(10,4)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,3)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('production_date', 'date'),
    Field('expiration_date', 'date'),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),            
    Field('delete', 'boolean', default = False),    
    Field('item_remarks', 'string'),
    Field('partial','boolean', default = False), 
    Field('new_item','boolean', default=False),
    Field('quantity_ordered_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_received_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_invoiced_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

# pending table
db.define_table('Purchase_Receipt_Warehouse_Consolidated',        
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('draft','boolean', default = True),
    Field('received','boolean',default=False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')
# pending table
db.define_table('Purchase_Receipt_Ordered_Warehouse_Consolidated',    
    Field('purchase_receipt_no_id','reference Purchase_Receipt_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),       
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),    
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('delete', 'boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'purchase_order_no_id')
# pending table
db.define_table('Purchase_Receipt_Transaction_Consolidated', 
    Field('purchase_receipt_no_id','reference Purchase_Receipt_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),              
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('new_item_code', 'string', length = 25), 
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer',default=0), # qty consolidated
    Field('invoiced_quantity','integer',default=0),
    Field('difference_quantity','integer',default=0),
    Field('uom','integer', default = 0),        
    Field('purchase_ordered_quantity', 'integer', default = 0), # ordered consolidated    
    Field('production_date', 'date'),
    Field('expiration_date', 'date'),
    # delete
    Field('price_cost', 'decimal(15,6)', default = 0), 
    Field('total_amount','decimal(15,6)', default = 0), #compute = lambda r: (r['price_cost'] / r['uom']) * r['quantity']),
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
    Field('new_item','boolean', default = False),
    Field('item_remarks','string'),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db(db.Stock_Status.id == 18), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))
# pending table
db.define_table('Purchase_Receipt_Transaction_Consolidated_New_Item', 
    Field('purchase_receipt_no_id','reference Purchase_Receipt_Warehouse_Consolidated',ondelete = 'NO ACTION',writable = False),                     
    Field('supplier_item_ref', 'string', length = 20), #requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code', 'string', length = 25), 
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0),
    Field('pieces','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('uom','integer', default = 0),    
    Field('production_date', 'date', request.now),
    Field('expiration_date', 'date', request.now),
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
    Field('new_item','boolean', default = False),
    Field('skip','boolean', default = False),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Receipt',            
    Field('purchase_request_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_request_no', 'integer', writable = False),
    Field('purchase_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_request_date_approved','date', writable = False),
    Field('purchase_request_date', 'date', default = request.now, writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_sub_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),    
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),
    Field('estimated_time_of_arrival', 'date', default = request.now), #requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'), minimum=datetime.date(2008, 1, 1),error_message='must be YYYY-MM-DD!')),
    Field('total_amount','decimal(15,4)', default = 0),    
    Field('total_amount_after_discount','decimal(15,4)', default = 0),    
    Field('insured', 'boolean', default = False),
    Field('foreign_currency_value','decimal(10,3)', default = 0),
    Field('local_currency_value','decimal(10,3)', default = 0),
    Field('exchange_rate','decimal(10,4)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure    
    Field('added_discount_amount', 'decimal(10,3)',default =0), # on hold structure    
    Field('currency_id','reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('remarks', 'string'),
    Field('remarks_created_by',db.auth_user,ondelete='NO ACTION',writable=False,readable=False),

    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'integer', writable = False),
    Field('purchase_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_date_approved','date', writable = False),
    Field('purchase_order_date','date', writable = False),
        
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('purchase_receipt_date','date', writable = False),
    Field('supplier_account_code','string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('supplier_account_code_description','string', length = 50),
    Field('supplier_invoice','string', length = 25),

    Field('landed_cost','decimal(10,6)', default = 0),
    Field('other_charges','decimal(10,6)', default = 0),    
    Field('custom_duty_charges','decimal(10,6)', default = 0),        
    Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),

    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('submitted','boolean', default = False),
    Field('posted','boolean', default = False),
    Field('draft','boolean', default = True),
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('proforma_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),    
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

db.define_table('Purchase_Receipt_Transaction',    
    Field('purchase_receipt_no_id','reference Purchase_Receipt',ondelete = 'NO ACTION',writable = False),    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code','string', length = 50),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # quantity requested
    Field('quantity_ordered','integer', default = 0), # quantity ordered
    Field('quantity_received','integer', default = 0), # quantity received/warehouse
    Field('quantity_invoiced','integer', default = 0), # quantity invoiced/accounts
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(20,4)', default = 0),
    Field('sale_cost', 'decimal(20,4)', default = 0),
    Field('wholesale_price', 'decimal(10,4)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(10,3)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('old_average_cost','decimal(15,4)', default = 0), # get the old average cost
    Field('old_landed_cost','decimal(10,6)', default = 0), # get the old landed cost
    Field('production_date', 'date'),
    Field('expiration_date', 'date'),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),            
    Field('delete', 'boolean', default = False),    
    Field('item_remarks', 'string'),
    Field('partial','boolean', default = False), 
    Field('new_item','boolean', default=False),
    Field('quantity_ordered_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_received_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_invoiced_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Batch_Cost', # Except short and excess
    Field('purchase_receipt_no_id','reference Purchase_Receipt',ondelete = 'NO ACTION',writable = False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('purchase_receipt_date', 'datetime', default = request.now), # from purchase receipt date
    Field('batch_cost', 'decimal(10,2)', default = 0), # landed  cost
    Field('supplier_price','decimal(15,6)', default = 0), # invoice price from manoj     
    Field('batch_quantity', 'integer', default = 0), # manoj
    Field('batch_production_date','date', default = request.now), # hakim entry
    Field('batch_expiry_date','date', default = request.now), # hakim entry
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Direct_Purchase_Receipt',  
    Field('transaction_no', 'integer', default = 0, writable = False),
    Field('transaction_date', 'datetime', default=request.now, writable = False),
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_date', 'date', writable = False),    
    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'string', length = 25, requires=IS_NOT_EMPTY() ),    
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),    
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),    
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),        
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', default = 4, requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('total_amount','decimal(20,6)', default = 0, writable = False),    # total net amount
    Field('total_amount_after_discount','decimal(20,6)', default = 0, writable = False),    
    Field('exchange_rate','decimal(20,6)', default = 0, required = True),    
    Field('landed_cost','decimal(20,6)', default = 0),
    Field('other_charges','decimal(20,6)', default = 0),    
    Field('custom_duty_charges','decimal(20,6)', default = 0),        
    Field('selective_tax','decimal(20,6)', default = 0.0, label = 'Selective Tax'),
    Field('supplier_invoice','string', length = 25),    
    Field('supplier_account_code_description', 'string'),
    Field('added_discount_amount', 'decimal(10,3)',default =0), # on hold structure
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),    
    Field('remarks', 'string'),    
    Field('received','boolean', default = False, writable = False),
    Field('archives', 'boolean', default = False, writable = False),   
    Field('posted_by','reference auth_user', ondelete='NO ACTION', writable = False),
    Field('date_posted','datetime',default=request.now),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

db.define_table('Direct_Purchase_Receipt_Transaction',    
    Field('purchase_receipt_no_id','reference Direct_Purchase_Receipt',ondelete = 'NO ACTION',writable = False),    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code', 'string', length = 25), 
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # manoj
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('net_price', 'decimal(20,6)',default =0),
    Field('discount_percentage', 'decimal(20,6)',default =0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(20,6)', default = 0),
    Field('sale_cost', 'decimal(20,2)', default = 0),
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('landed_cost','decimal(20,6)', default = 0),    
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.
    Field('location_code_id','reference Location', ondelete = 'NO ACTION', writable = False),
    Field('transaction_type','integer', default = 1),
    Field('transaction_date', 'datetime', default=request.now, writable = False),
    Field('supplier_reference_order','string', length = 25),
    Field('delete', 'boolean', default = False),  
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))
# LANDED COST	AVERAGE COST	DISCOUNT PERCENTAGE	LOCATION	PURCHASE RECEIPT NO.	TRANSACTION DATE	TRANSACTION TYPE

db.define_table('Direct_Purchase_Receipt_Transaction_Temporary',    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code', 'string', length = 25), 
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # manoj
    Field('pieces','integer', default = 0),    
    Field('uom','integer', default = 0),
    Field('total_pieces','integer', default = 0),
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('net_price', 'decimal(20,2)',default =0),
    Field('discount_percentage', 'decimal(20,2)',default =0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Purchase_Return',
    Field('transaction_no','integer', default = 0, writable = False),
    Field('transaction_date','date', default=request.now),
    Field('purchase_return_no_prefix_id','reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_return_no','integer', default = 0, writable = False),
    Field('purchase_return_date','date', default = request.now),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    # Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('adjustment_type', 'reference Adjustment_Type', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Adjustment_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('total_amount','decimal(20,2)', default = 0),
    Field('remarks','string'),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('purchase_return_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_return_date_approved','date', writable = False),

    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False), format = 'insurance_name')

db.define_table('Purchase_Return_Transaction',
    Field('transaction_no_id','reference Purchase_Return',ondelete='NO ACTION',writable=False),
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer',default=0),
    Field('uom','integer',default=0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('price_cost','decimal(15,6)',default=0),
    Field('average_cost','decimal(15,4)', default = 0),   
    Field('wholesale_price', 'decimal(10,2)', default = 0),
    Field('retail_price', 'decimal(10,2)',default = 0),
    Field('vansale_price', 'decimal(10,2)',default =0),
    Field('sale_cost', 'decimal(15,2)', default = 0),
    Field('selective_tax','decimal(10,2)', default = 0, label = 'Selective Tax'),
    Field('delete','boolean',default=False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False), format = 'insurance_name')

db.define_table('Purchase_Return_Transaction_Temporary',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION', writable = False),        
    Field('item_code','string',length=25),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer',default=0),
    Field('uom','integer',default=0),
    Field('pieces','integer',default=0),
    Field('total_pieces','integer',default=0),
    Field('price_cost','decimal(10,6)', default = 0),
    Field('total_amount','decimal(10,6)', default = 0),
    Field('average_cost','decimal(10,6)', default = 0),
    Field('ticket_no_id', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False), format = 'insurance_name')

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
    # Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_no','string',length = 25, writable = False),
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

db.define_table('Document_Register',           
    Field('document_register_no', 'string', length = 25),
    Field('document_register_date', 'date'),    
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('supplier_reference_order','string', length = 25),
    Field('invoice_no', 'string', length = 25),
    Field('invoice_date', 'date'),
    Field('estimated_time_of_arrival', 'date'),
    Field('total_amount_in_qr','decimal(15,4)', default = 0),    
    Field('invoice_amount','decimal(15,4)', default = 0),    
    Field('ib_amount','decimal(15,4)', default = 0),    
    Field('exchange_rate','decimal(10,2)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('freight_currency_id', 'reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('freight_amount', 'decimal(10,2)', default = 0),
    Field('bank', 'string',length = 25),                   
    Field('payment_category','string', length = 25),
    Field('bank_reference_no_1','string',length = 25),
    Field('bank_reference_no_2','string',length = 25),
    Field('lc_no','string', legnth = 25),
    Field('lc_expiring_date','date'),
    Field('cil_no', 'string', length = 25),
    Field('forwarder_supplier_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Forwarder_Supplier.id, '%(forwarder_name)s',zero = 'Choose Forwareder')),
    Field('courier','string', length = 25),
    Field('payment_terms','string',length = 25),
    Field('due_date','date'),
    Field('descriptions', 'string', length = 25),
    Field('payment_voucher','string', length = 25),
    Field('payment_voucher_date', 'date'),
    Field('paid', 'boolean', default = False),
    Field('category', 'string', length = 25),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'document_register_no')

db.define_table('Document_Register_Details',           
    Field('document_register_no_id', 'reference Document_Register', ondelete = 'NO ACTION', writable = False),
    Field('details','string'),        
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_order_no')

db.define_table('Document_Register_Purchase_Order',           
    Field('document_register_no_id', 'reference Document_Register', ondelete = 'NO ACTION', writable = False),
    Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),        
    Field('purchase_order_no','string',length=25),        
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_order_no')


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

db.define_table('Delivery_Note_Transaction_Report_Counter',
    Field('delivery_note_transaction_no_id', 'reference Delivery_Note'),
    Field('printer_counter', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', writable = False, readable = False),
    Field('updated_by', db.auth_user,ondelete = 'NO ACTION', writable = False, readable = False))

db.define_table('Sales_Invoice_Transaction_Report_Counter',
    Field('sales_invoice_transaction_no_id', 'reference Sales_Invoice'),
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
    # Field('purchase_order_no_id','reference Purchase_Order',ondelete = 'NO ACTION',writable = False),
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

db.define_table('Version_Control',
    Field('version_no','string',length=25),
    Field('version_date','date'),
    Field('module_name','string',length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),    
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Daily_Activity',
    Field('transaction','string',length=50),
    Field('activities','string'),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),    
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False))
#---------------------------------------------------------
# db.define_table('General_Ledger',

# )
# Department
# Type
# Ref_Date
# Account_code
# Description
# Credit
# Debit
# Due_Date
# Amount Paid
# Status
# FlgPost 
# Person 
# Entry_Date
# AccsRef
# BankCode
# CCENT
# LOCCENT
# ACCT_COD2
# TRNTYPE
db.define_table('Monthly_Stocks',
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('month_january','integer',default=0),
    Field('month_february','integer',default=0),
    Field('month_march','integer',default=0),
    Field('month_april','integer',default=0),
    Field('month_may','integer',default=0),
    Field('month_june','integer',default=0),
    Field('month_july','integer',default=0),
    Field('month_august','integer',default=0),
    Field('month_september','integer',default=0),
    Field('month_october','integer',default=0),
    Field('month_november','integer',default=0),
    Field('month_december','integer',default=0),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))


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

# genSched.queue_task(
#     'get_consolidation', 
#     prevent_drift = True, 
#     start_time=request.now,
#     repeats = 1, 
#     period = 120)

# scheduler.queue_task('reporting_percentages', prevent_drift = True, repeats = 1, period = 120)

# python web2py.py -a admin -K mtc_inv -X

# 86400 seconds/24 hours
# i.number_to_words(49)

# from num2words import num2words

# test = 23.25

# intpart,decimalpart = int(test), test-int(test) 
# print(num2words(intpart).replace('-', ' ') + ' and ' + str( int(decimalpart * (10 ** (len(str(decimalpart)) - 2)))) +  ' cent')

# for n in d2().select(d2.Employee_Master.ALL, d2.Employee_Employment_Details.ALL, orderby = d2.Employee_Master.id, left = d2.Employee_Employment_Details.on(d2.Employee_Employment_Details.employee_id == d2.Employee_Master.id)):
#     _id = db(db.Employee_Master.id == n.Employee_Master.id).select().first()
#     if _id:        
#         _id.update_record(account_code=n.Employee_Employment_Details.account_code, title = n.Employee_Master.title, first_name=n.Employee_Master.first_name,middle_name=n.Employee_Master.middle_name,last_name=n.Employee_Master.last_name)
#     else:        
#         db.Employee_Master.insert(account_code=n.Employee_Employment_Details.account_code, title = n.Employee_Master.title, first_name=n.Employee_Master.first_name,middle_name=n.Employee_Master.middle_name,last_name=n.Employee_Master.last_name)

# # master_account_type_id #Customer,Accounts,Supplier,Employees    
# for n in db().select(orderby = db.Customer.id): # Customer
#     _id = db(db.Master_Account.account_code == n.customer_account_no).select().first()
#     if _id:
#         _id.update_record(account_code=n.customer_account_no, account_name=n.customer_name, master_account_type_id='C')
#     else:
#         db.Master_Account.insert(account_code = n.customer_account_no, account_name=n.customer_name,master_account_type_id='C')

# for n in db().select(orderby = db.Supplier_Master.id): # Suppliers
#     _id = db(db.Master_Account.account_code == n.supp_code).select().first()
#     if _id:
#         _id.update_record(account_code=n.supp_code, account_name=n.supp_name, master_account_type_id='S')
#     else:
#         db.Master_Account.insert(account_code = n.supp_code, account_name=n.supp_name,master_account_type_id='S')

# for n in db().select(orderby = db.Employee_Master.id):
#     _id = db(db.Master_Account.account_code == n.account_code).select().first()
#     _str = str(n.title) + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)
#     if _id:
#         _id.update_record(account_code=n.account_code, account_name=_str, master_account_type_id='E') 
#     else:
#         db.Master_Account.insert(account_code = n.account_code, account_name=_str,master_account_type_id='E') 

# for n in db().select(orderby = db.Sales_Man.id):
#     _id = db(db.Master_Account.account_code == n.mv_code).select().first()
#     _str = str(n.employee_id.first_name) + ' ' + str(n.employee_id.middle_name) + ' ' + str(n.employee_id.last_name)
#     if _id:
#         _id.update_record(account_code=n.mv_code, account_name=_str,master_account_type_id='A')
#     else:
#         db.Master_Account.insert(account_code=n.mv_code, account_name=_str,master_account_type_id='A')