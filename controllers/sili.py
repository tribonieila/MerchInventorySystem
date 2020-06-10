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
            print 'update: ', n.Sales_Order.id
        else:
            print 'insert: ', n.Sales_Order.id
        #     db.Stock_Header_Consolidation.insert(
        #         transaction_no = n.sales_invoice_no,
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
    