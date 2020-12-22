import locale

@auth.requires_login()
def get_stock_transfer_utility_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Receipt No.'),TH('Stock Transfer No.'),TH('Stock Request No.'),TH('Stock Source'),TH('Stock Destination'),TH('Status'),_class='style-accent'))    
    for n in db().select(orderby = ~db.Stock_Receipt.id):
        row.append(TR(
            TD(n.stock_receipt_date_approved.date()),                
            TD(n.stock_receipt_no_id.prefix,n.stock_receipt_no),      
            TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),                
            TD(n.stock_request_no_id.prefix, n.stock_request_no),
            TD(n.stock_source_id.location_code,' - ',n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_code,' - ',n.stock_destination_id.location_name),
            TD(n.srn_status_id.description)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table table-condensed table-hover', _id='tblST')   
    return dict(table = table)

def put_stock_transfer_consolidation():
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    for n in db(db.Stock_Receipt.processed == False).select(orderby = db.Stock_Receipt.id):
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.stock_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 5)).select().first()
        _acct = db(db.Sales_Man.users_id == n.created_by).select().first()
        if not _acct:
            _sales_man = ''
        else:
            _sales_man = _acct.mv_code

        if not _chk: # update consolidated records here
            n.update_record(processed = True)
            
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
                sales_man_code = _sales_man,
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
    response.js = "$('#tblST').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_sales_return_utility_grid():    
    row = []
    head = THEAD(TR(TD('Date'),TD('Sales Return No.'),TD('Department'),TD('Customer'),TD('Location'),TD('Status'),_class='style-warning large-padding text-center'))
    _query = db((db.Sales_Return.status_id == 13) & (db.Sales_Return.processed == False)).select(orderby = ~db.Sales_Return.id)
    for n in _query:
        row.append(TR(
            TD(n.sales_return_date),
            TD(n.transaction_prefix_id.prefix,n.sales_return_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted')),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),            
            TD(n.status_id.required_action)))   
    body = TBODY(*row)     
    table = TABLE(*[head, body], _class = 'table table-condensed table-hover', _id = 'tblSR')
    return dict(table = table)

def put_sales_return_consolidation():
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    for n in db(db.Sales_Return.status_id == 13).select(orderby = db.Sales_Return.id):        
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.sales_return_no)) & (db.Merch_Stock_Header.transaction_type == 4)).select().first()
        if not _chk: # update consolidated records here
            n.update_record(processed = True)
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
    response.js = "$('#tblSR').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_sales_invoice_id():
    form = SQLFORM.factory(
        Field('sales_invoice_no', widget = SQLFORM.widgets.autocomplete(request, db.Sales_Invoice.sales_invoice_no, id_field = db.Sales_Invoice.sales_invoice_no, limitby = (0,10), min_length = 2)))
    if form.accepts(request): 
        if not request.vars.sales_invoice_no:
            response.flash = 'Sales invoice not found.'
        else:
            _id = db(db.Sales_Invoice.sales_invoice_no == request.vars.sales_invoice_no).select().first()
            if _id:                        
                _tax_remarks = ''
                ctr = _total_amount = _total_amount_after_discount = _selective_tax =  _selective_tax_foc = 0
                if _id.sales_invoice_no_prefix_id == None:
                    _sales_invoice_no = _sales_invoice_date = ''            
                else:
                    _sales_invoice_no = _id.sales_invoice_no_prefix_id.prefix,_id.sales_invoice_no
                    _sales_invoice_date = _id.sales_invoice_date_approved

                table = TABLE(TR(
                    TD('Customer Good Receipt No.'),
                    TD(INPUT(_class='form-control',_type='text',_id='customer_good_receipt_no',_name='customer_good_receipt_no')),
                    TD(BUTTON('submit',_class='btn btn-primary',_id='btnSubmit',_type='button')),
                    ),_class='table')
                table += TABLE(TR(TD('Sales Order No'),TD('Sales Order Date'),TD('Delivery Note No'),TD('Delivery Note Date'),TD('Sales Invoice No'),TD('Sales Invoice Date'),TD('Delivery Due Date'),TD('Sales Man'),_class='bg-active'),
                TR(TD(_id.transaction_prefix_id.prefix,_id.sales_order_no),TD(_id.sales_order_date),TD(_id.delivery_note_no_prefix_id.prefix,_id.delivery_note_no),TD(_id.delivery_note_date_approved),TD(_sales_invoice_no),TD(_sales_invoice_date),TD(_id.delivery_due_date),TD(_id.sales_man_id.employee_id.first_name,' ', _id.sales_man_id.employee_id.last_name))
                ,_class='table table-bordered table-condensed')        
                table += TABLE(TR(TD('Department'),TD('Location Source'),TD('Customer'),TD('Remarks'),TD('Status')),
                TR(TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),TD(_id.stock_source_id.location_code, ' - ', _id.stock_source_id.location_name),TD(_id.customer_code_id.account_name,', ',SPAN(_id.customer_code_id.account_code,_class='text-muted')),TD(_id.remarks),TD(_id.status_id.description))
                ,_class='table table-bordered table-condensed')
                row = []
                head = THEAD(TR(TD('#'),TD('Item Code'),TD('Brand Line'),TD('Item Description'),TD('Category'),TD('UOM'),TD('Quantity'),TD('Price/Sel.Tax'),TD('Dis.%'),TD('Net Price'),TD('Total Amount'),_class='bg-primary'))
                for n in db((db.Sales_Invoice_Transaction.sales_invoice_no_id == _id.id) & (db.Sales_Invoice_Transaction.delete == False)).select(db.Sales_Invoice_Transaction.ALL, db.Item_Master.ALL,db.Item_Prices.ALL, orderby = db.Sales_Invoice_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Invoice_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Invoice_Transaction.item_code_id)]):
                    ctr += 1
                    row.append(TR(
                        TD(ctr),
                        TD(n.Item_Master.item_code),
                        TD(n.Item_Master.brand_line_code_id.brand_line_name),
                        TD(n.Item_Master.item_description),
                        TD(n.Sales_Invoice_Transaction.category_id.mnemonic),
                        TD(n.Sales_Invoice_Transaction.uom),
                        TD(card(n.Sales_Invoice_Transaction.item_code_id, n.Sales_Invoice_Transaction.quantity, n.Sales_Invoice_Transaction.uom)),
                        TD(locale.format('%.3F',n.Sales_Invoice_Transaction.price_cost or 0, grouping = True),_align='right'),
                        TD(locale.format('%.2F',n.Sales_Invoice_Transaction.discount_percentage or 0, grouping = True),_align='right'),
                        TD(locale.format('%.3F',n.Sales_Invoice_Transaction.net_price or 0, grouping = True),_align='right'),
                        TD(locale.format('%.3F',n.Sales_Invoice_Transaction.total_amount or 0, grouping = True),_align='right')))
                    _selective_tax += n.Sales_Invoice_Transaction.selective_tax or 0
                    _selective_tax_foc += n.Sales_Invoice_Transaction.selective_tax_foc or 0        
                    if (_selective_tax > 0.0):
                        _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
                    else:
                        _div_tax = ''
                    if (_selective_tax_foc > 0.0):
                        _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
                    else:
                        _div_tax_foc = ''
                    _tax_remarks = PRE(_div_tax + '\n' + ' ' +  _div_tax_foc)                
                    _total_amount += n.Sales_Invoice_Transaction.total_amount
                    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
                foot = TFOOT(
                    TR(TD(_tax_remarks,_colspan='8',_rowspan='3'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right')),    
                    TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
                    TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_total_amount_after_discount or 0, grouping = True), _align = 'right')))                        
                body = TBODY(*row)
                table += TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')                
                return dict(form = form, table = table)                                    
            else:
                table = ''                 
            return dict(form = form, table = table)
    return dict(form = form, table = '')

@auth.requires_login()
def get_sales_invoice_utility_grid():
    row = []
    head = THEAD(TR(TD('Date'),TD('Sales Invoice No.'),TD('Delivery Note No.'),TD('Sales Order No.'),TD('Department'),TD('Customer'),TD('Location Source'),TD('Status'),_class='style-warning large-padding text-center'))
    _query = db(db.Sales_Invoice.processed == False).select(orderby = ~db.Sales_Invoice.id)
    for n in _query:  

        _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
        _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})

        _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
        _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})

        _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
        _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(TD(n.sales_invoice_date_approved),TD(_inv),TD(_note),TD(_sales),TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ', SPAN(n.customer_code_id.account_code,_class='text-muted')),TD(n.stock_source_id.location_name),TD(n.status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover table-condensed',_id='tblSI')
    return dict(table = table)    

def put_sales_invoice_consolidation():    
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    for n in db(db.Sales_Invoice.processed == False).select(orderby = db.Sales_Invoice.id):        
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

    response.js = "$('#tblSI').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_direct_purchase_utility_grid():
    row = []
    head = THEAD(TR(TD('Date'),TD('Purchase Receipt No.'),TD('Transaction Date'),TD('Transaction No.'),TD('Department'),TD('Supplier Code'),TD('Location'),TD('Status'),_class='style-primary'))    
    for n in db((db.Direct_Purchase_Receipt.status_id == 21) & (db.Direct_Purchase_Receipt.processed == False)).select(orderby = ~db.Direct_Purchase_Receipt.id):
        row.append(TR(
            TD(n.purchase_receipt_date),
            TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
            TD(n.transaction_date),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ', SPAN(n.supplier_code_id.supp_sub_code, _class='text-muted')),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),            
            TD(n.status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover table-condensed',_id='tblDPr')
    return dict(table = table)

def put_direct_purchase_consolidation():
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()
    for n in db((db.Direct_Purchase_Receipt.status_id == 21) & (db.Direct_Purchase_Receipt.processed == False)).select():
        _au = db(db.auth_user.id == n.created_by).select().first()
        _em = db(db.Employee_Master.first_name == _au.first_name).select().first()    
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.purchase_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()        
        if not _chk:
            n.update_record(processed = True)
            db.Merch_Stock_Header.insert(
                voucher_no = n.purchase_receipt_no,
                location = n.location_code_id,
                transaction_type = 1,
                transaction_date = n.purchase_receipt_date,
                account = n.supplier_code_id.supp_sub_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount_after_discount,
                discount_added = n.added_discount_amount,
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

    response.js = "$('#tblDPr').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_utility_grid():

    return dict()
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

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
        return str('{:,}'.format(int(_stock))) + ' - ' + str(_pieces)  + '/' + str(int(_item.uom_value))        