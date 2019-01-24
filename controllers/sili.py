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