if request.env.http_origin:
     response.headers['Access-Control-Allow-Origin'] = request.env.http_origin;
     response.headers['Access-Control-Allow-Methods'] = "POST,GET,OPTIONS";
     response.headers['Access-Control-Allow-Credentials'] = "true";
     response.headers['Access-Control-Allow-Headers'] = "Accept, Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Accept-Encoding";

# from datetime import datetime

# now = datetime.now() # current date and time
import json
def api():
    from gluon.serializers import json
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    def POST(table_name,**vars):
        #return db[table_name].validate_and_insert(**vars)
        #data = gluon.contrib.simplejson.loads(request.body.read())
        return json(db[table_name].validate_and_insert(**vars))
        return dict()
    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)
    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    def OPTIONS(*args,**vars):
        print "OPTION called"
        return True
    return dict(GET=GET,POST=POST,PUT=PUT,DELETE=DELETE,OPTIONS=OPTIONS)

def get_json():
    _data = db().select(db.Item_Master.ALL, db.Department.ALL, orderby = db.Item_Master.id, left = db.Department.on(db.Item_Master.dept_code_id == db.Department.id))
    return XML(response.json(_data))
    
def get_table():
    table = TABLE()
    return dict()

def get_user_sync():
    print("set user's group --- ")
    for n in db().select(orderby = db.auth_group.id):
        _chk = d2(d2.auth_group.id == n.id).select().first()
        if _chk:
            print('update: '), n.id
        else:
            print('insert: '), n.id
    print("set user's authentication --- ")
    for y in db().select(orderby = db.auth_user.id):
        _chk = d2(d2.auth_user.id == y.id).select().first()
        if _chk:
            print('usr up: '), y.id
        else:
            print('usr in: '), y.id
    print("set user's member --- ")
    for z in db().select(orderby = db.auth_membership.id):
        _chk = d2(d2.auth_membership.id == z.id).select().first()
        if _chk:
            print('usr up: '), z.id
        else:
            print('usr in: '), z.id
    

def get_schedule():
    genSched.queue_task('get_consolidation', prevent_drift = True, repeats = 0, period = 120)

def get_version_control():
    grid = SQLFORM.grid(db.Version_Control)
    # print db(db.Version_Control.id == 1).select(db.Version_Control.version_no)
    return dict(grid = grid)

def get_python_script():
    # import dbf 
    # table = dbf.Table('temptable.dbf', 'name C(30); age N(3,0); birth D')
    import os
    fp = os.path.join(request.folder, 'static', 'external/ExportUtil.py')
    os.system('python ' + fp)

def generate():
    
    print '----- '
    # _so = db(db.Sales_Order.status_id == 4).count()
    # for n in db(db.Sales_Order.status_id == 4).select(db.Sales_Order.sales_order_date, orderby = db.Sales_Order.sales_order_date, groupby = db.Sales_Order.sales_order_date):
    #     print ': ', n.sales_order_date, _so
    # from temp
    for n in db().select(orderby = db.Direct_Purchase_Receipt.id):
        n.update_record(processed = False)
    # master stock file
    # for n in db().select(orderby = db.Stock_File.id):
    #     _id = db((db.Stock_File_Temp.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == 1)).select().first()
    #     # n.update_record(closing_stock _id.closing_stock, opening_stock = _id.opening_stock)
    #     if _id:
    #         print _id.closing_stock, n.closing_stock
    # for n in db().select(orderby = db.Merch_Stock_Header.id):
    #     _id = db(db.Sales_Invoice.sales_invoice_no == n.voucher_no).select().first()
    #     _sm = db(db.Sales_Man.id == _id.sales_man_id).select().first()
    #     n.update_record(sales_man_code = _sm.mv_code)
    return dict(table = 'table')

def ResetOrderTransaction():
    for n in db(db.Sales_Order.cancelled_by == 9).select(orderby = db.Sales_Order.id):
        n.update_record(cancelled = False, status_id = 9)
        print 'id: ', n.id
        # _id = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        # if float(_id.retail_price or 0) != float(n.retail_price or 0):
        #     print ': ', n.id, n.item_code_id.item_code, n.retail_price , '- ', _id.retail_price
            # n.update_record(average_cost = float(_id.average_cost or 0))

def merch():
    form = SQLFORM.smartgrid(db.Merch_Stock_Header)
    return dict(form = form)

def put_purchase_receipt_consolidation():
    for n in db(db.Purchase_Receipt.status_id == 21).select(orderby = db.Purchase_Receipt.id):
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.purchase_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()
        if not _chk:            
            print 'insert: ', n.id 
            db.Merch_Stock_Header.insert(
                voucher_no = n.purchase_receipt_no,
                location = n.location_code_id,
                transaction_type = 1, # credit
                transaction_date = n.purchase_receipt_date,
                account = n.supplier_code_id.supp_sub_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount_after_discount,
                discount_percentage = 0,
                discount_added = n.added_discount_amount or 0,                
                supplier_reference_order = n.supplier_reference_order,
                supplier_invoice = n.supplier_invoice,
                exchange_rate = n.exchange_rate,
                landed_cost = n.landed_cost,
                trade_terms_id = n.trade_terms_id,
                other_charges = n.other_charges,
                custom_duty_charges = n.custom_duty_charges,
                stock_destination = n.location_code_id,
                total_selective_tax = n.selective_tax or 0,
                total_selective_tax_foc = 0),                
                # sales_man_code = _em.account_code,
                # batch_code_id = _batch_id.id)           
        else:
            print 'updated: ', n.id
        

def put_direct_purchase_receipt_consolidation():
    # print 'put_direct_purchase_receipt_consolidation'
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    

    for n in db(db.Direct_Purchase_Receipt.status_id == 21).select(orderby = db.Direct_Purchase_Receipt.id):
        _au = db(db.auth_user.id == n.created_by).select().first()
        _em = db(db.Employee_Master.first_name == _au.first_name).select().first()

        _sm = db(db.Supplier_Master.id == n.supplier_code_id).select().first()
        _ma = db(db.Master_Account.account_code == _sm.supp_code).select().first()
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.purchase_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()
        if not _chk:            
            # print 'insert: ', n.purchase_receipt_no, _ma.account_code
            db.Merch_Stock_Header.insert(
                voucher_no = n.purchase_receipt_no,
                location = n.location_code_id,
                transaction_type = 1, # credit
                transaction_date = n.purchase_receipt_date,
                account = n.supplier_code_id.supp_sub_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount_after_discount,
                discount_percentage = 0,
                discount_added = n.added_discount_amount or 0,                
                supplier_reference_order = n.supplier_reference_order,
                supplier_invoice = n.supplier_invoice,
                exchange_rate = n.exchange_rate,
                landed_cost = n.landed_cost,
                trade_terms_id = n.trade_terms_id,
                other_charges = n.other_charges,
                custom_duty_charges = n.custom_duty_charges,
                stock_destination = n.location_code_id,
                total_selective_tax = n.selective_tax or 0,
                total_selective_tax_foc = 0,                
                sales_man_code = _em.account_code,
                batch_code_id = _batch_id.id)                
            _id = db((db.Merch_Stock_Header.voucher_no == n.purchase_receipt_no) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()
            for x in db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == n.id) & (db.Direct_Purchase_Receipt_Transaction.delete == False)).select():
                _ip = db(db.Item_Prices.item_code_id == x.item_code_id).select().first() 
                _sale_cost_notax_pcs = ((float(x.wholesale_price or 0) / int(x.uom)) * (100 - float(x.discount_percentage or 0))) / 100
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.purchase_receipt_no,
                    location = n.location_code_id,
                    transaction_type = 1,
                    transaction_date = n.purchase_receipt_date,
                    item_code = x.item_code,
                    category_id = x.category_id.mnemonic,
                    uom = x.uom,
                    quantity = x.quantity,
                    average_cost = x.average_cost or 0,
                    price_cost = x.price_cost or 0,
                    sale_cost = x.sale_cost or 0,
                    sale_cost_notax_pcs = _sale_cost_notax_pcs,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax,
                    selective_tax_price = _ip.selective_tax_price,
                    supplier_code = n.supplier_code_id.supp_sub_code,
                    sales_man_code = _em.account_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    price_cost_pcs = x.price_cost_pcs or 0, # convert to pcs 
                    average_cost_pcs = x.average_cost_pcs or 0, # convert to pcs
                    wholesale_price_pcs = x.wholesale_price_pcs or 0, # convert to pcs
                    retail_price_pcs = x.retail_price_pcs or 0, # convert to pcs
                    price_cost_after_discount = x.total_amount or 0)          
            
        else:            
            y = db(db.Merch_Stock_Header.voucher_no == n.purchase_receipt_no).select().first()
            y.update_record(
                voucher_no = n.purchase_receipt_no,
                location = n.location_code_id,
                transaction_type = 1,
                transaction_date = n.purchase_receipt_date,
                account = n.supplier_code_id.supp_sub_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount_after_discount,
                discount_percentage = 0,
                discount_added = n.added_discount_amount or 0,
                supplier_reference_order = n.supplier_reference_order, 
                supplier_invoice = n.supplier_invoice,
                exchange_rate = n.exchange_rate,
                landed_cost = n.landed_cost,
                trade_terms_id = n.trade_terms_id,
                other_charges = n.other_charges,
                custom_duty_charges = n.custom_duty_charges,
                total_selective_tax = n.selective_tax,
                total_selective_tax_foc = 0,
                stock_destination = n.location_code_id,
                sales_man_code = _em.account_code,
                batch_code_id = _batch_id.id)
            for z in db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == n.id) & (db.Direct_Purchase_Receipt_Transaction.delete == False)).select():                                
                _ip = db(db.Item_Prices.item_code_id == z.item_code_id).select().first()
                x = db((db.Merch_Stock_Transaction.merch_stock_header_id == y.id) & (db.Merch_Stock_Transaction.item_code == z.item_code) & (db.Merch_Stock_Transaction.category_id == z.category_id)).select().first()
                # print ' :x-', z.id, x.id        
                x.update_record(
                    merch_stock_header_id = y.id,
                    voucher_no = y.voucher_no,
                    location = y.location,
                    transaction_type = 1,
                    transaction_date = y.transaction_date,
                    item_code = z.item_code,
                    category_id = z.category_id,
                    uom = z.uom,
                    quantity = z.quantity,
                    average_cost = z.average_cost or 0,
                    price_cost = z.price_cost or 0,
                    sale_cost = 0,
                    sale_cost_notax_pcs = 0,
                    discount = z.discount_percentage or 0,
                    wholesale_price = z.wholesale_price or 0,
                    retail_price = z.retail_price or 0,
                    vansale_price = z.vansale_price or 0,
                    tax_amount = z.vat_percentage or 0,
                    selected_tax = z.selective_tax or 0,
                    selective_tax_price = _ip.selective_tax_price,
                    supplier_code = n.supplier_code_id.supp_sub_code,
                    sales_man_code = _em.account_code,
                    dept_code = y.dept_code,
                    stock_destination = y.location,
                    price_cost_pcs = z.price_cost_pcs or 0,
                    average_cost_pcs = z.average_cost_pcs or 0,
                    wholesale_price_pcs = z.wholesale_price_pcs or 0,
                    retail_price_pcs = z.retail_price_pcs or 0,
                    price_cost_after_discount = z.total_amount or 0
                )        



def put_sales_invoice_consolidation_():
    for n in db().select(orderby = db.Sales_Invoice.id):                
        _chk = db(db.Merch_Stock_Header.voucher_no == int(n.sales_invoice_no)).select().first()
        if not _chk:
            print 'insert here: ', n.sales_invoice_no
        else:
            print 'update here: ', n.sales_invoice_no           

def put_sales_invoice_consolidation():    
    print 'def put_sales_invoice_consolidation():    '
    
def put_sales_invoice_consolidation_():    
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    for n in db().select(orderby = db.Sales_Invoice.id):        
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.sales_invoice_no)) & (db.Merch_Stock_Header.transaction_type == 2)).select().first()
        if not _chk: # update consolidated records here
            # print 'insert here: ', n.sales_invoice_no
            n.update_record(processed = True)
            db.Merch_Stock_Header.insert(
                voucher_no = n.sales_invoice_no,
                location = n.stock_source_id,
                transaction_type = 2, # credit
                transaction_date = n.sales_invoice_date_approved,
                account = n.customer_code_id.account_code, # with account name from customer master
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount_after_discount,
                discount_added = n.discount_added or 0,
                total_selective_tax = n.total_selective_tax or 0,
                total_selective_tax_foc = n.total_selective_tax_foc or 0,                
                sales_man_code = n.sales_man_id.mv_code,
                batch_code_id = _batch_id.id)
            _id = db((db.Merch_Stock_Header.voucher_no == n.sales_invoice_no) & (db.Merch_Stock_Header.transaction_type == 2)).select().first()
            for x in db(db.Sales_Invoice_Transaction.sales_invoice_no_id == n.id).select(orderby = db.Sales_Invoice_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.sales_invoice_no,
                    location = n.stock_source_id,
                    transaction_type = _id.transaction_type,
                    transaction_date = n.sales_invoice_date_approved,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,
                    average_cost = x.average_cost or 0,
                    price_cost = x.price_cost or 0,
                    sale_cost = x.sale_cost or 0,
                    sale_cost_notax_pcs = x.sale_cost_notax_pcs,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax,
                    selective_tax_price = x.selective_tax_price,
                    supplier_code = _i.supplier_code_id.supp_code,
                    sales_man_code = n.sales_man_id.mv_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.stock_source_id,
                    price_cost_pcs = x.price_cost_pcs or 0,
                    average_cost_pcs = x.average_cost_pcs or 0,
                    wholesale_price_pcs = x.wholesale_price_pcs or 0,
                    retail_price_pcs = x.retail_price_pcs or 0,
                    price_cost_after_discount = x.price_cost_after_discount or 0)          

def put_sales_return_consolidation():        
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    for n in db(db.Sales_Return.status_id == 13).select(orderby = db.Sales_Return.id):        
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.sales_return_no)) & (db.Merch_Stock_Header.transaction_type == 4)).select().first()
        if not _chk: # update consolidated records here
            # print 'insert here: ', n.sales_invoice_no
            db.Merch_Stock_Header.insert(
                voucher_no = n.sales_return_no,
                location = n.location_code_id,
                stock_destination = n.location_code_id,
                transaction_type = 4, # credit
                transaction_date = n.sales_return_date,
                account = n.customer_code_id.account_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount_after_discount,
                discount_added = n.discount_added or 0,
                total_selective_tax = n.total_selective_tax or 0,
                total_selective_tax_foc = n.total_selective_tax_foc or 0,                
                sales_man_code = n.sales_man_id.mv_code,
                batch_code_id = _batch_id.id)
            _id = db((db.Merch_Stock_Header.voucher_no == int(n.sales_return_no)) & (db.Merch_Stock_Header.transaction_type == 4)).select().first()
            for x in db(db.Sales_Return_Transaction.sales_return_no_id == n.id).select(orderby = db.Sales_Return_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.sales_return_no,
                    location = n.location_code_id,
                    transaction_type = _id.transaction_type,
                    transaction_date = n.sales_return_date,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,
                    average_cost = x.average_cost or 0,
                    price_cost = x.price_cost or 0,
                    sale_cost = x.sale_cost or 0,
                    sale_cost_notax_pcs = x.sale_cost_notax_pcs or 0,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax or 0,
                    selective_tax_price = x.selective_tax_price or 0,
                    supplier_code = _i.supplier_code_id.supp_code,
                    sales_man_code = n.sales_man_id.mv_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    price_cost_pcs = x.price_cost_pcs or 0,
                    average_cost_pcs = x.average_cost_pcs or 0,
                    wholesale_price_pcs = x.wholesale_price_pcs or 0,
                    retail_price_pcs = x.retail_price_pcs or 0,
                    price_cost_after_discount = x.price_cost_after_discount or 0)               

def put_stock_transfer_consolidation_():       
    for n in db().select(orderby = db.Stock_Receipt.id):
        print 'h:', n.id
        for x in db(db.Stock_Receipt_Transaction.stock_receipt_no_id == n.id).select():
            print '      t:', x.id

def put_stock_transfer_consolidation():        
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    for n in db().select(orderby = db.Stock_Receipt.id):        
        print n.created_by
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.stock_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 5)).select().first()
        if not _chk: # update consolidated records here
            _acct = db(db.Sales_Man.users_id == n.created_by).select().first()
            # account field => from master account
            # location source => from master account
            # location destination => from master account
            db.Merch_Stock_Header.insert(
                voucher_no = n.stock_receipt_no,
                location = n.stock_source_id,
                stock_destination = n.stock_destination_id,
                transaction_type = 5, # credit
                transaction_date = n.stock_receipt_date_approved,
                account = n.stock_destination_id.location_code, #_acct.employee_id.first_name, # replace to location code with location name column
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount,
                discount_added = 0,
                total_selective_tax = 0,
                total_selective_tax_foc = 0,                
                sales_man_code = _acct.mv_code,
                batch_code_id = _batch_id.id)
            _id = db((db.Merch_Stock_Header.voucher_no == int(n.stock_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 5)).select().first()
            for x in db(db.Stock_Receipt_Transaction.stock_receipt_no_id == n.id).select(orderby = db.Stock_Receipt_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.stock_receipt_no,
                    location = n.stock_source_id,
                    transaction_type = _id.transaction_type,
                    transaction_date = n.stock_receipt_date_approved,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,                                        
                    price_cost = x.price_cost or 0,
                    sale_cost = x.sale_cost or 0,
                    # sale_cost_notax_pcs = x.sale_cost_notax_pcs or 0,
                    discount = 0,
                    average_cost = x.average_cost or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    # tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax or 0,
                    # selective_tax_price = x.selective_tax_price or 0,
                    
                    supplier_code = _i.supplier_code_id.supp_code,
                    sales_man_code = _acct.mv_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.stock_destination_id,

                    price_cost_pcs = x.price_cost_pcs or 0,
                    average_cost_pcs = x.average_cost_pcs or 0,
                    wholesale_price_pcs = x.wholesale_price_pcs or 0,
                    retail_price_pcs = x.retail_price_pcs or 0,

                    price_cost_after_discount = x.total_amount or 0)               
  
@auth.requires_login()
def admin():
    return dict()

def direct_purchase():
    return dict()

def obsolescence_of_stock():
    return dict()

def stock_adjustment():
    return dict()

def stock_corrections():
    return dict()

def stock_transfer():
    return dict()

def sales_return():
    return dict()

def sales_invoice():
    return dict()


def put_obsolescence_of_stock_consolidation(): # validated
    # print 'put_obsolescence_of_stock_consolidation'
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    

    for n in db(db.Obsolescence_Stocks.status_id == 24).select():
        # print 'id: ', n.id, n.obsolescence_stocks_no, n.obsolescence_stocks_date, n.dept_code_id, n.stock_type_id, n.location_code_id,
        # n.account_code_id, n.total_amount, n.total_amount_after_discount, n.total_selective_tax, n.total_selective_tax_foc,
        # n.total_vat_amount, n.obsolescence_stocks_date_approved, n.obsolescence_stocks_approved_by,n.remarks, n.status_id
        _s = db((db.Employee_Master.first_name == n.created_by.first_name) & (db.Employee_Master.last_name == n.created_by.last_name)).select().first()
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.obsolescence_stocks_no)) & (db.Merch_Stock_Header.transaction_type == 10)).select().first()
        if not _chk:
            db.Merch_Stock_Header.insert(
                voucher_no = n.obsolescence_stocks_no,
                location = n.location_code_id,
                transaction_type = 10,
                transaction_date = n.obsolescence_stocks_date,
                account = n.account_code_id.account_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount,
                total_selective_tax = n.total_selective_tax,
                total_selective_tax_foc = n.total_selective_tax_foc,
                stock_destination = n.location_code_id,
                sales_man_code = _s.account_code,
                batch_code_id = _batch_id.id)
            _id = db(db.Merch_Stock_Header.voucher_no == n.obsolescence_stocks_no).select().first()
            for y in db(db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == n.id).select():                
                # print '=>      id: ', y.id, y.item_code_id,y.category_id,y.quantity,y.uom,y.price_cost,y.total_amount,y.average_cost,y.sale_cost,
                # y.wholesale_price, y.retail_price,y.vansale_price,y.net_price,y.selective_tax,y.selective_tax_foc,y.vat_percentage
                _i = db(db.Item_Master.id == y.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == y.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id=_id.id,
                    voucher_no = n.obsolescence_stocks_no,
                    location =n.location_code_id,
                    transaction_type = 10,
                    transaction_date= n.obsolescence_stocks_date,
                    item_code = y.item_code_id.item_code,
                    category_id=y.category_id,
                    uom=y.uom,
                    quantity=y.quantity,
                    average_cost=y.average_cost,
                    price_cost=y.price_cost,
                    sale_cost= y.sale_cost,
                    sale_cost_notax_pcs=0,
                    discount=0,
                    wholesale_price=_p.wholesale_price,
                    retail_price=_p.retail_price,
                    vansale_price=0,
                    tax_amount=0,
                    selected_tax=0,
                    price_cost_after_discount=0,
                    sales_man_code=_s.account_code,
                    price_cost_pcs=_p.average_cost / y.uom,
                    average_cost_pcs=_p.average_cost / y.uom,
                    wholesale_price_pcs=_p.wholesale_price / y.uom,
                    retail_price_pcs=_p.retail_price / y.uom,
                    selective_tax_price= _p.selective_tax_price,
                    supplier_code=_i.supplier_code_id.supp_code,
                    dept_code=n.dept_code_id,
                    stock_destination=n.location_code_id,
                )
                #     y.item_code_id,
                #     y.category_id,
                #     y.quantity,
                #     y.uom,
                #     y.price_cost,
                #     y.total_amount,
                #     y.average_cost,
                #     y.sale_cost,
                #     y.wholesale_price, 
                #     y.retail_price,
                #     y.vansale_price,
                #     y.net_price,
                #     y.selective_tax,
                #     y.selective_tax_foc,
                #     y.vat_percentage
                # )
def put_stock_correction_consolidation(): # validated    
    for n in db(db.Stock_Corrections.status_id == 16).select():        
        db.Merch_Stock_Header.insert(
            voucher_no = n.stock_corrections_no,
            location = n.location_code_id,
            transaction_type = 8,
            transaction_date = n.stock_corrections_date,
            # account = n.,
            dept_code = n.dept_code_id,
            total_amount = n.total_amount,
            total_amount_after_discount = 0,
            discount_percentage = 0,
            discount_added = 0,
            total_selective_tax = 0,
            # total_selective_tax_foc = 0,
            # stock_destination = n.,
            # sales_man_code = n.,
            # batch_code_id = n.,
        )
        _id = db(db.Merch_Stock_Header.voucher_no == n.stock_corrections_no).select().first()
        for y in db(db.Stock_Corrections_Transaction.stock_corrections_no_id == n.id).select():
            print '          insert: ', y.id
            db.Merch_Stock_Transaction.insert(
                merch_stock_header_id = _id.id,
                voucher_no = _id.voucher_no,
                # location,transaction_type,transaction_date,item_code,category_id,uom,quantity,average_cost,price_cost,
                # sale_cost,sale_cost_notax_pcs,discount,wholesale_price,retail_price,vansale_price,tax_amount,selected_tax,price_cost_after_discount,
                # sales_man_code,price_cost_pcs,average_cost_pcs,wholesale_price_pcs,retail_price_pcs,selective_tax_price,supplier_code,
                # dept_code,stock_destination
            )

def get_sync_note():
    # print 'get_sync_note'
    for n in db(db.Sales_Order.status_id == 8).select(orderby = db.Sales_Order.id):        
        db.Delivery_Note.insert(
            transaction_prefix_id = n.transaction_prefix_id,
            sales_order_no = n.sales_order_no,
            sales_order_date = n.sales_order_date,
            dept_code_id = n.dept_code_id,
            stock_source_id = n.stock_source_id,
            customer_code_id = n.customer_code_id,
            customer_order_reference = n.customer_order_reference,
            delivery_due_date = n.delivery_due_date,
            total_amount = n.total_amount,
            total_amount_after_discount = n.total_amount_after_discount,
            total_selective_tax = n.total_selective_tax,
            total_selective_tax_foc = n.total_selective_tax_foc,
            discount_percentage = n.discount_percentage,
            total_vat_amount = n.total_vat_amount,
            sales_order_date_approved = n.sales_order_date_approved,
            sales_order_approved_by = n.sales_order_approved_by,
            remarks = n.remarks,
            delivery_note_no_prefix_id = n.delivery_note_no_prefix_id,
            delivery_note_no = n.delivery_note_no,
            delivery_note_approved_by = n.delivery_note_approved_by,
            delivery_note_date_approved = n.delivery_note_date_approved,
            section_id = n.section_id,
            sales_man_id = n.sales_man_id,
            status_id = n.status_id)        
        _dn = db(db.Delivery_Note.sales_order_no == n.sales_order_no).select().first()
        for x in db((db.Sales_Order_Transaction.sales_order_no_id == n.id) & (db.Sales_Order_Transaction.delete == False)).select():
            db.Delivery_Note_Transaction.insert(
                delivery_note_id = int(_dn.id),
                item_code_id = x.item_code_id,
                category_id = x.category_id,
                quantity = x.quantity,
                uom = x.uom,
                price_cost  = x.price_cost,
                packet_price_cost = x.packet_price_cost,
                total_amount = x.total_amount,
                average_cost = x.average_cost,
                sale_cost = x.sale_cost,
                wholesale_price = x.wholesale_price,
                retail_price = x.retail_price,
                vansale_price = x.vansale_price,
                discount_percentage = x.discount_percentage,
                net_price = x.net_price,
                selective_tax = x.selective_tax,
                selective_tax_foc = x.selective_tax_foc,
                packet_selective_tax = x.packet_selective_tax,
                packet_selective_tax_foc = x.packet_selective_tax_foc,
                vat_percentage = x.vat_percentage)                
                # print '        ', x.id, x.sales_order_no_id

def get_sync_all():    
    for n in db(db.Sales_Order.status_id == 7).select(orderby = db.Sales_Order.id):#, left = db.Sales_Order.on(db.Sales_Order.id == db.Sales_Order_Transaction.sales_order_no_id)):
        db.Sales_Invoice.insert(
            transaction_prefix_id = n.transaction_prefix_id,
            sales_order_no = n.sales_order_no,
            sales_order_date = n.sales_order_date,
            dept_code_id = n.dept_code_id,
            stock_source_id = n.stock_source_id,
            customer_code_id = n.customer_code_id,
            customer_order_reference = n.customer_order_reference,
            delivery_due_date = n.delivery_due_date,
            total_amount = n.total_amount,
            total_amount_after_discount = n.total_amount_after_discount,
            total_selective_tax = n.total_selective_tax,
            total_selective_tax_foc = n.total_selective_tax_foc,
            discount_percentage = n.discount_percentage,
            total_vat_amount = n.total_vat_amount,
            sales_order_date_approved = n.sales_order_date_approved,
            sales_order_approved_by = n.sales_order_approved_by,
            remarks = n.remarks,
            delivery_note_no_prefix_id = n.delivery_note_no_prefix_id,
            delivery_note_no = n.delivery_note_no,
            delivery_note_approved_by = n.delivery_note_approved_by,
            delivery_note_date_approved = n.delivery_note_date_approved,
            sales_invoice_no_prefix_id = n.sales_invoice_no_prefix_id,
            sales_invoice_no = n.sales_invoice_no,
            sales_invoice_approved_by = n.sales_invoice_approved_by,
            sales_invoice_date_approved = n.sales_invoice_date_approved,
            section_id = n.section_id,
            sales_man_id = n.sales_man_id,
            status_id = n.status_id)            
        db.Delivery_Note.insert(
            transaction_prefix_id = n.transaction_prefix_id,
            sales_order_no = n.sales_order_no,
            sales_order_date = n.sales_order_date,
            dept_code_id = n.dept_code_id,
            stock_source_id = n.stock_source_id,
            customer_code_id = n.customer_code_id,
            customer_order_reference = n.customer_order_reference,
            delivery_due_date = n.delivery_due_date,
            total_amount = n.total_amount,
            total_amount_after_discount = n.total_amount_after_discount,
            total_selective_tax = n.total_selective_tax,
            total_selective_tax_foc = n.total_selective_tax_foc,
            discount_percentage = n.discount_percentage,
            total_vat_amount = n.total_vat_amount,
            sales_order_date_approved = n.sales_order_date_approved,
            sales_order_approved_by = n.sales_order_approved_by,
            remarks = n.remarks,
            delivery_note_no_prefix_id = n.delivery_note_no_prefix_id,
            delivery_note_no = n.delivery_note_no,
            delivery_note_approved_by = n.delivery_note_approved_by,
            delivery_note_date_approved = n.delivery_note_date_approved,
            sales_invoice_no_prefix_id = n.sales_invoice_no_prefix_id,
            sales_invoice_no = n.sales_invoice_no,
            sales_invoice_approved_by = n.sales_invoice_approved_by,
            sales_invoice_date_approved = n.sales_invoice_date_approved,
            section_id = n.section_id,
            sales_man_id = n.sales_man_id,
            status_id = n.status_id)     
        _si = db(db.Sales_Invoice.sales_order_no == n.sales_order_no).select().first()           
        _dn = db(db.Delivery_Note.sales_order_no == n.sales_order_no).select().first()
        for x in db((db.Sales_Order_Transaction.sales_order_no_id == n.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
            db.Sales_Invoice_Transaction.insert(
                sales_invoice_no_id = int(_si.id),
                item_code_id = x.item_code_id,
                category_id = x.category_id,
                quantity = x.quantity,
                uom = x.uom,
                price_cost  = x.price_cost,
                packet_price_cost = x.packet_price_cost,
                total_amount = x.total_amount,
                average_cost = x.average_cost,
                sale_cost = x.sale_cost,
                wholesale_price = x.wholesale_price,
                retail_price = x.retail_price,
                vansale_price = x.vansale_price,
                discount_percentage = x.discount_percentage,
                net_price = x.net_price,
                selective_tax = x.selective_tax,
                selective_tax_foc = x.selective_tax_foc,
                packet_selective_tax = x.packet_selective_tax,
                packet_selective_tax_foc = x.packet_selective_tax_foc,
                vat_percentage = x.vat_percentage,
                delete = x.delete)
            db.Delivery_Note_Transaction.insert(
                delivery_note_id = int(_dn.id),
                item_code_id = x.item_code_id,
                category_id = x.category_id,
                quantity = x.quantity,
                uom = x.uom,
                price_cost  = x.price_cost,
                packet_price_cost = x.packet_price_cost,
                total_amount = x.total_amount,
                average_cost = x.average_cost,
                sale_cost = x.sale_cost,
                wholesale_price = x.wholesale_price,
                retail_price = x.retail_price,
                vansale_price = x.vansale_price,
                discount_percentage = x.discount_percentage,
                net_price = x.net_price,
                selective_tax = x.selective_tax,
                selective_tax_foc = x.selective_tax_foc,
                packet_selective_tax = x.packet_selective_tax,
                packet_selective_tax_foc = x.packet_selective_tax_foc,
                vat_percentage = x.vat_percentage,
                delete = x.delete)                

def labuyo():
    form = SQLFORM(db.auth_user)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    head = THEAD(TR(TH('#'),TH('First Name'),TH('Last Name'),TH('Role'),TH('Email'),TH('Action',_class='sorting_disabled')))
    for u in db().select(db.auth_user.ALL, db.auth_membership.ALL, db.auth_group.ALL, orderby = db.auth_user.id, 
    left = [db.auth_membership.on(db.auth_membership.user_id == db.auth_user.id),db.auth_group.on(db.auth_group.id == db.auth_membership.group_id)]):
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('labuyo_edit_form', args = u.auth_user.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = u.auth_user.id))
        btn_lnks = DIV(edit_lnk, dele_lnk, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(u.auth_user.id),TD(u.auth_user.first_name.upper()),TD(u.auth_user.last_name.upper()),TD(u.auth_group.role),TD(u.auth_user.email.lower()),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped')    
    return dict(form = form, table = table)

def labuyo_edit_form():
    form =SQLFORM(db.auth_user, request.args(0))
    if form.process().accepted:
        session.flash = 'FORM UPDATED'
        redirect(URL('sili','labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def haba():
    row = []
    form = SQLFORM(db.auth_group)
    if form.process().accepted:
        response.flash = 'FORM ACCEPTED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'        

    head = THEAD(TR(TH('#'),TH('Role'),TH('Description'),TH('Action')))
    for n in db().select(db.auth_group.ALL, orderby = db.auth_group.id):
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('haba_edit_form.html', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnks = DIV(edit_lnk, dele_lnk, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(n.id),TD(n.role.upper()),TD(n.description.upper()),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

def haba_edit_form():
    form = SQLFORM(db.auth_group, request.args(0))
    if form.process().accepted:
        session.flash = 'FORM UPDATED'
        redirect(URL('labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'        
    return dict(form = form)    

def pansigang():
    row = []
    form = SQLFORM(db.auth_membership)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
        
    head = THEAD(TR(TH('#'),TH('User'),TH('Group'),TH('Action')))
    for n in db(db.auth_membership).select():
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('pansigang_edit_form.html', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnks = DIV(edit_lnk, dele_lnk, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(n.id),TD(n.user_id.first_name.upper(), ' ', n.user_id.last_name.upper()),TD(n.group_id.role),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

def pansigang_edit_form():
    form = SQLFORM(db.auth_membership, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def division_group():
    # form = SQLFORM(db.Division_Group)
    # if form.process().accepted:
    #     response.flash = 'RECORD SAVE'
    # elif form.errors:
    #     response.flash = 'FORM HAS ERROR'
    table = SQLFORM.grid(db.Division_Group)
    return dict(table = table)

def department_group():
    # form = SQLFORM(db.Department_Group)
    # if form.process().accepted:
    #     response.flash = 'RECORD SAVE'
    # elif form.errors:
    #     response.flash = 'FORM HAS ERROR'
    table = SQLFORM.grid(db.Department_Group)
    return dict(table = table)

def section_group():
    # form = SQLFORM(db.Section_Group)
    # if form.process().accepted:
    #     response.flash = 'RECORD SAVE'
    # elif form.errors:
    #     response.flash = 'FORM HAS ERROR'
    table = SQLFORM.grid(db.Section_Group)
    return dict(table = table)

def section_tools():
    for n in db().select(db.Stock_File.ALL):
        _closing_stock = n.closing_stock
        # print _closing_stock
        n.update_record(stock_in_transit = 0, order_in_transit = 0,probational_balance = _closing_stock)
    return dict()

def get_stock_file_grid():    
    return dict(grid = SQLFORM.grid(db.Stock_File))

def get_item_price_grid():
    return dict(grid = SQLFORM.grid(db.Item_Prices))

def get_sales_order_utility():    
    _qty = _stk_in_transit = _stk_in_probati = 0
    for n in db(db.Sales_Order.status_id == 4).select(db.Sales_Order_Transaction.item_code_id, db.Sales_Order.stock_source_id, groupby = db.Sales_Order_Transaction.item_code_id | db.Sales_Order.stock_source_id, left = db.Sales_Order_Transaction.on(db.Sales_Order_Transaction.sales_order_no_id == db.Sales_Order.id)):
        _sum = db.Sales_Order_Transaction.quantity.sum()
        _qty = db((db.Sales_Order_Transaction.item_code_id == n.Sales_Order_Transaction.item_code_id) & (db.Sales_Order_Transaction.delete == False)).select(_sum).first()[_sum]        
        _stk = db((db.Stock_File.location_code_id == n.Sales_Order.stock_source_id) & (db.Stock_File.item_code_id == n.Sales_Order_Transaction.item_code_id)).select().first()
        _stk_in_transit = -abs(_qty)
        _stk_in_probati = _stk.closing_stock - abs(_qty)
        _stk.update_record(stock_in_transit = _stk_in_transit, probational_balance = _stk_in_probati)            
    return dict()

def get_sales_order_in_temporary_utility():    
    _qty = _stk_in_transit = _stk_in_probati = 0
    for n in db().select(db.Sales_Order_Transaction_Temporary.ALL):
        for y in db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select():            
            _stk_in_transit = y.stock_in_transit - -abs(n.total_pieces)
            _stk_in_probati = y.closing_stock - abs(_stk_in_transit)
            y.update_record(stock_in_transit=_stk_in_transit, probational_balance=_stk_in_probati)
            db(db.Sales_Order_Transaction_Temporary.id == n.id).delete()
    return dict()

def get_sales_order_sync(): #  transaction 3
    print '-- ', request.now
    for n in db(db.Sales_Order.status_id == 7).select(orderby = db.Sales_Order.id, left = db.Sales_Order.on(db.Sales_Order.id == db.Sales_Order_Transaction.sales_order_no_id)):
        # print 'id: ', n.Sales_Order.sales_order_no,n.Sales_Order_Transaction.sales_order_no_id
        _chk_sal = db(db.Stock_Header_Consolidation.transaction_no == n.Sales_Order.sales_order_no).select().first()
        if _chk_sal:
            print 'update: ', n.Sales_Order.id, n.Sales_Order.stock_source_id
            db.Stock_Header_Consolidation.update(
                transaction_no = n.Sales_Order.sales_order_no,
                location_code_id = n.Sales_Order.stock_source_id
            )
        else:
            print 'insert: ', n.Sales_Order.id
            db.Stock_Header_Consolidation.insert(
                transaction_no = n.Sales_Order.sales_order_no)
        #         location_code_id = x,
        #         transaction_type = x,
        #         customer_code_id = x,
        #         transaction_date = x,
        #         account = x,
        #         total_amount = x,
        #         discount_percentage = x,
        #         discount_added = x,
        #         total_selective_tax = x,
        #         total_selective_tax_foc = x,
        #         stock_destination = x,
        #         batch_code_id = x)
        #     _stk_head = db().select(db.Stock_Header_Consolidation.ALL).select().last()

        #     for y in db(db.Stock_Transaction_Consolidation.transaction_no_id != _stk_head.id).select():
        #         db.Stock_Transaction_Consolidation.insert(
        #             transaction_no_id = _stk_head.id,
        #             location_code_id = _stk_head.location_code_id,
        #             transaction_type = x,
        #             transaction_date = x,
        #             item_code = x,


        #         )
    return dict()

    # 1 GRV
    # 2 CREDIT
    # 3 CASH   
    # 4 SALES retrun  
    # 5 STV 
    # 6 STOCK ADJUSTMENT -
    # 7 STOCK ADJUSTMENT + 
    