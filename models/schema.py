# auth = Auth(db,cas_provider = 'http://127.0.0.1:3000/merch_erp/default/user/cas')
# db = DAL('mssql4://username:password@localhost/test', pool_size=0)

db = DAL('postgres://root:admin@localhost:5432/mpc_inv', pool_size=0)
# Field('division_id', 'reference division', readable = False, writable = False, requires = IS_IN_DB(db, db.division.id, '%(division)s', zero = 'Choose division')),
# Field('division', requires = IS_UPPER(), label = 'Division'),format = '%(division)s')

db.define_table('Status',
    Field('Status','string',length=20, requires = IS_UPPER()),format = '%(Status)s')

db.define_table('Division',
    Field('Div_Code','string', length = 5, label = 'Division Code'),
    Field('Div_Name','string', length = 50, label = 'Division Name'), 
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')), format = '%(Div_Code)s')

db.define_table('Department',
    Field('Div_Code_Id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(Div_Code)s - %(Div_Name)s', zero = 'Choose Division'), label='Division Code'),
    Field('Dept_Code','string', length = 5, label ='Department Code'),
    Field('Dept_Name','string', length = 50, label = 'Department Name'),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')),format = '%(Dept_Code)s')

db.define_table('Product',
    Field('Dept_Code_Id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(Dept_Code)s - %(Dept_Name)s', zero = 'Choose Department')),
    Field('Product_Code','string', length = 10),
    Field('Product_Name', 'string', length = 50, requires = IS_UPPER()),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')),format = '%(Product_Code)s')

db.define_table('SubProduct',
    Field('Product_Code_Id','reference Product', requires = IS_IN_DB(db, db.Product.id, '%(Product_Code)s', zero = 'Choose Product Code')),
    Field('Subproduct_Code','string', length = 10),
    Field('Subproduct_Name','string', length = 50),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')), format = '%(Subproduct_Code)s')

db.define_table('GroupLine',
    Field('Group_Line_Code','string',length=8),
    Field('Group_Line_Name', 'string', length=50, requires=IS_UPPER()),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')), format = '%(Group_Line_Code)s')

db.define_table('Brand_Line',
    Field('Group_Line_Code_Id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(Group_Line_Code)s', zero = 'Choose Group Line')),
    Field('Brand_Line_Code','string',length=8),
    Field('Brand_Line_Name','string',length=50),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')), format = '%(Brand_Line_Code)s')

db.define_table('Brand_Classification',
    Field('Brand_Line_Code_Id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id, '%(Brand_Line_Code)s', zero= 'Choose Brand Line')),
    Field('Brand_Cls_Code','string', length=8),
    Field('Brand_Cls_Name','string',length=50),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')), format = '%(Brand_Cls_Code)s')

db.define_table('Item_Status',
    Field('Item_Status_Code','string',length=5),
    Field('Item_Status_Type','string',length=15))

db.define_table('Fragrance_Type',
    Field('Product_Code_Id','reference Product', requires = IS_IN_DB(db, db.Product.id, '%(Product_Code)s', zero = 'Choose Product Code')),
    Field('Fragrance_Code','string',length=6),
    Field('Fragrance_Name','string',length=35),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))

db.define_table('Item_Color',
    Field('Color_Code','string',length=5),
    Field('Color_Name','string',length=25),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))

db.define_table('Item_Size',
    Field('Size_Code','string',length=10),
    Field('Size_Name','string',length=25),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))

db.define_table('Item_Collection',
    Field('Collection_Code','string',length=5),
    Field('Collection_Name','string',length=25),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))

db.define_table('Made_In',
    Field('Made_In_Name','string', length=30, requires=IS_IN_SET(COUNTRIES)),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))

db.define_table('Section',
    Field('Section_Code','string',length=5),
    Field('Section_Name','string',length=15),
    Field('Status_Id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))

db.define_table('Prefix_Data',
    Field('Prefix_Name','string', length = 30, requires = IS_UPPER()),
    Field('Prefix', length = 10, requires = IS_UPPER()), format = '%(Prefix)s')
    
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

db.define_table('po_group',
    Field('po_group_refno','string', length=10),
    Field('po_number','string',length=10))

db.define_table('purchase_receipt_transaction_details',
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

db.define_table('purchase_order_transaction_header',
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

db.define_table('purchase_order_transaction_details',
    Field('po_number','string',length=10),
    Field('item_code','string',length=10),
    Field('supp_price','decimal(10,2)'),
    Field('quantity','integer'),
    Field('uom','integer'),
    Field('item_category','string',length=10),
    Field('qty_received','integer'))

db.define_table('batch_order_transaction',
    Field('item_code','string',length=10),
    Field('supp_price','decimal(10,2)'),
    Field('landed_cost','decimal(10,2)'),
    Field('qty','integer'),
    Field('date_ordered','date'))

db.define_table('supplier_master',
    Field('supp_code','string', length=10),
    Field('supp_name','string',length=50),
    Field('country','string',length=30),
    Field('payment_mode','string',length=30),
    Field('payment_terms','string',length=30),
    Field('currency','string',length=20),
    Field('trade_terms','string',length=20),
    Field('forwarder_air','string',length=20),
    Field('forwarder_sea','string',length=20),
    Field('commodity_code','string',length=10),
    Field('discount_percentage','string',length=10),
    Field('custom_duty_percentage','string',length=10),format='%(supp_code)s')

db.define_table('gender',
    Field('gender_type', 'string', length = 10,requires = IS_UPPER()),format='%(gender_type)s')
    
db.define_table('itemmas',
    Field('Item_Code', 'string', length = 10, label = 'Item Code',requires = IS_NOT_IN_DB(db, 'itemmas.Item_Code')),
    Field('Ref_No', 'string', length = 15, label = 'Reference No',requires = IS_NOT_IN_DB(db, 'itemmas.Ref_No')),
    Field('Section_Code', 'string', length = 15),
    Field('Supplier_Item_Ref', 'string', length = 15),
    Field('Item_Description', 'string', length = 35, label = 'Description'),
    Field('supplier_code_id', 'reference supplier_master', label = 'Supplier Code', requires = IS_IN_DB(db, db.supplier_master.id,'%(supp_code)s', zero = 'Choose Supplier Code')),
    Field('Mr_Cost', 'decimal(10,2)', default = 0),
    Field('Ave_Cost', 'decimal(10,2)', default = 0),
    Field('Mr_Lndcost', 'decimal(10,2)', default =0),
    Field('Currency', 'string', length = 5, requires = IS_IN_SET(CURRENCY, zero = 'Choose Currency')),
    Field('Size_Code', 'string', length = 10),
    Field('UOM', 'integer'),
    Field('Supp_OUM', 'integer'),
    Field('Op_Avcost', 'decimal(10,2)', default = 0),
    Field('Last_Issdt', 'date', default = request.now),
    Field('Price_Wsch', 'decimal(10,2)', label = 'Price', default = 0),
    Field('Price_Rtch', 'decimal(10,2)',default = 0),
    Field('Price_Vnch', 'decimal(10,2)',default =0),
    Field('Created_On', 'date', default = request.now),
    Field('Created_By', 'date',default = request.now),
    Field('Reorder_Qty', 'integer', default = 0),
    Field('Bar_Code', 'string', length = 20),
    Field('Dept_Code_Id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(Dept_Code)s', zero = 'Choose Department')),
    Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(Product_Code)s - %(Product_Name)s', zero = 'Choose Product Code')),
    Field('sub_product_code_id','reference SubProduct', requires = IS_IN_DB(db, db.SubProduct.id,'%(Subproduct_Code)s', zero = 'Choose Sub-Product')),
    Field('Group_Line_Code_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(Group_Line_Code)s', zero = 'Choose Group Line Code')),
    Field('Brand_Line_Code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(Brand_Line_Code)s', zero = 'Choose Brand Line')),
    Field('Brand_Cls_Code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(Brand_Cls_Code)s', zero = 'Choose Brand Classification')),
    Field('Gender_Code_id','reference gender', requires = IS_IN_DB(db, db.gender.id,'%(gender_type)s', zero = 'Choose Gender')),
    Field('Item_Status_Code','reference Status', requires = IS_IN_DB(db, db.Status.id, '%(Status)s', zero = 'Choose Status')),
    Field('Fragrance_Code','string'),
    Field('Color_Code','string'),
    Field('Size_Code','string'),
    Field('Collection_Code','string'),
    Field('Made_In','string',length=25, requires = IS_IN_SET(COUNTRIES, zero = 'Choose Country')))