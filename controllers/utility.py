def get_utility_grid():

    return dict()

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
        row.append(TR(TD(n.sales_invoice_date_approved.date()),TD(_inv),TD(_note),TD(_sales),TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ', SPAN(n.customer_code_id.account_code,_class='text-muted')),TD(n.stock_source_id.location_name),TD(n.status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover table-condensed',_id='tblSI')
    return dict(table = table)    

def put_sales_invoice_consolidation():    
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
    response.js = "$('#tblSI').get(0).reload(), toastr['success']('Record Consolidated')"