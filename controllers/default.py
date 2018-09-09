# -*- coding: utf-8 -*-

# ---- index page        ----
# @auth.requires_login()
def index():
    response.flash = T("Hello User",language="ar-ar"  )
    return dict(message=T('Welcome to the jungle!'))

# ---- Transaction       -----
def transaction():
    return locals()
# ---- Stock Request     -----
def stock_request():
    return locals()
# ---- Stock Voucher     -----
def stock_voucher():
    return locals()
# ---- Stock Receipt     -----
def stock_receipt():
    return locals()
# ---- Reports           -----
def reports():
    return locals()

# ---- Prefix Master       -----
def pre_mas():
    form = SQLFORM(db.Prefix_Data)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Prefix_Data)
    return dict(form = form, grid = grid)

# ---- Division Master       -----
def stat_mas():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'form accepted'
        # db.Division.insert(Div_Code=form.vars.)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Status)
    return dict(form=form, grid=grid)

# ---- Division Master       -----
def div_mas():
    pre = db(db.Prefix_Data.id == 1).select(db.Prefix_Data.Prefix).first()    
    ctr = db(db.Division.id).count()
    ctr = ctr+1
    ctr = str(ctr).rjust(2, '0')
    ctr_val = pre.Prefix+ctr
    form = SQLFORM.factory(
        Field('div_code','string',default=ctr_val, label="Division Code"),
        Field('div_name','string',length=25, label="Division Name"),
        Field('status_id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        # db.Division.insert(Div_Code=form.vars.)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Division, editable=False, details = True)
    return dict(form=form, grid=grid)

# ---- Department Master  -----
def dept_mas():
    pre = db(db.Prefix_Data.id == 2).select(db.Prefix_Data.Prefix).first()
    ctr = db(db.Department.id).count()
    ctr = ctr+1
    ctr = str(ctr).rjust(2, '0')
    ctr_val = pre.Prefix+ctr
    form = SQLFORM.factory(
        Field('div_code_id', 'reference Division', label='Division Code',requires = IS_IN_DB(db, db.Division.id,'%(Div_Code)s - %(Div_Name)s', zero = 'Choose Division')),
        Field('dept_code', label = 'Department Code', default = ctr_val),
        Field('dept_name','string', label = 'Department Name', requires = IS_UPPER()),
        Field('status_id','reference Status', label = 'Status', requires = IS_IN_DB(db, db.Status.id,'%(Status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.Department.insert(Div_Code_Id = form.vars.div_code_id,Dept_Code=form.vars.dept_code, Dept_Name=form.vars.dept_name)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Department)
    return dict(form=form, grid=grid)

# ---- Product Master  -----
def prod_mas():
    pre = db(db.Prefix_Data.id == 3).select(db.Prefix_Data.Prefix).first()
    ctr = db(db.Product.id).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(2,'0')
    ctr_val = pre.Prefix+ctr
    form = SQLFORM(db.Product)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Product)
    return dict(form=form, grid=grid)

# ---- SubProduct Master  -----
def subprod_mas():
    form = SQLFORM(db.SubProduct)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.SubProduct)
    return dict(form=form, grid=grid)

# ---- GroupLine Master  -----
def groupline_mas():
    ctr = db(db.GroupLine.id).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_value = 'GRL'+ ctr
    form = SQLFORM.factory(
        Field('group_line_code', 'string', default = ctr_value),
        Field('group_line_name', 'string', requires=IS_UPPER()))
    if form.process().accepted:
        response.flash = 'form accepted'
        db.GroupLine.insert(Group_Line_Code = form.vars.group_line_code, Group_Line_Name = form.vars.group_line_name)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.GroupLine)
    return dict(form=form, grid=grid)

# ---- Brand Line Master  -----
def brndlne_mas():
    ctr = db(db.Brand_Line).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')
    ctr_value = 'BRL' + ctr
    form = SQLFORM.factory(
        Field('group_line_code_id', 'reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(Group_Line_Code)s', zero = 'Choose Group Line')),
        Field('brand_line_code', 'string', default = ctr_value),
        Field('brand_line_name', 'string', requires = IS_UPPER()))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Brand_Line)
    return dict(form=form, grid=grid)
# ---- Brand Classification Master  -----
def brndclss_mas():
    form = SQLFORM(db.Brand_Classification)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Brand_Classification)
    return dict(form=form, grid=grid)
# ---- Item Status Master  -----
def itmstat_mas():
    form = SQLFORM(db.Item_Status)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Item_Status)
    return dict(form=form, grid=grid)
# ---- Fragrance Type Master  -----
def frgtype_mas():
    form = SQLFORM(db.Fragrance_Type)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Fragrance_Type)
    return dict(form=form, grid=grid)
    
# ---- Item Color Master  -----
def itmcol_mas():
    form = SQLFORM(db.Item_Color)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Item_Color)
    return dict(form=form, grid=grid)

# ---- Item Color Master  -----
def itmsze_mas():
    form = SQLFORM(db.Item_Size)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Item_Size)
    return dict(form=form, grid=grid)

# ---- Item Color Master  -----
def itmcoll_mas():
    form = SQLFORM(db.Item_Collection)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Item_Collection)
    return dict(form=form, grid=grid)
    
# ---- Made In Master  -----
def mdein_mas():
    form = SQLFORM(db.Made_In)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Made_In)
    return dict(form=form, grid=grid)

# ---- Made In Master  -----
def sec_mas():
    form = SQLFORM(db.Section)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.Section)
    return dict(form=form, grid=grid)

# ---- Item Master       -----
def item_mas():
    form = SQLFORM(db.itemmas)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)
# ---- Brand Master      -----
def brand_mas():
    form = SQLFORM(db.brandmas)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

# ---- Transaction Master -----
def trans_mas():
    form = SQLFORM(db.trnmas)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

# ---- Voucher Master   -----
def vouc_mas():
    form = SQLFORM(db.trnvou)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def testing():
    return locals()
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
