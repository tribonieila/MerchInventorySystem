# -*- coding: utf-8 -*-

# ---- index page        ----
# @auth.requires(lambda: auth.has_membership('ROOT'))
@auth.requires_login()
# @auth.requires_membership('ROOT')
def index():
    response.flash = T("Welcome to MERCH - ERP",language="ar-ar"  )
    return dict(message=T('Welcome to MERCH - ERP'))

# ---- administrative task        ----
def resetstock():
    for x in db().select(db.Stock_File.ALL):
        x.update_record(opening_stock = 10000, closing_stock = 10000, stock_in_transit = 0, probational_balance = 0, last_transfer_qty = 0, damaged_stock_qty = 0, free_stock_qty = 0)
    return locals()

def resettawar():
    for x in db((db.Stock_File.item_code_id == 1) & (db.Stock_File.location_code_id == 2)).select():
        x.update_record(opening_stock = 0, closing_stock = 0)
    return locals()
    
def init_stock():
    for i in db().select(db.Item_Master.ALL, orderby = db.Item_Master.id):        
        if db((db.Stock_File.item_code_id == i.id) & (db.Stock_File.location_code_id == 2)).select().first():
            print 'in stock:: ', i.item_code
        else:            
            # print 'no stock:: ', i.item_code
            db.Stock_File.insert(item_code_id = i.id, location_code_id = 2, opening_stock = 0, closing_stock = 0, previous_year_closing_stock = 0, stock_in_transit = 0, free_stock_qty = 0, reorder_qty = 0, last_transfer_qty = 0, probational_balance = 0, damaged_stock_qty = 0 )
            

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
