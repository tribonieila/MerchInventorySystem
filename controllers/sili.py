def labuyo():
    form = SQLFORM(db.auth_user, request.args(0))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    row = []
    head = THEAD(TR(TH('#'),TH('First Name'),TH('Last Name'),TH('Email'),TH('Action',_class='sorting_disabled')))
    for u in db().select(db.auth_user.ALL):
        # pr_v = A(I(_class = 'fa fa-print bigger-130 blue'), _title="Print", _target='blank', _href=URL("Reports","AdvertisementReport", args=u.auth_user.id, extension = False))
        # edit = A(I(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL('sili','tagagamit_form', args = u.auth_user.id, extension = False))
        # btn_lnks = DIV(pr_v, edit, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(
            TD(u.id),
            TD(u.first_name.upper()),
            TD(u.last_name.upper()),
            TD(u.email.lower()),
            TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped')
    grid = SQLFORM.grid(db.auth_user, user_signature=False, csv = False, create = True, searchable = True, showbuttontext = False, links = '')
    # response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Welcome '), 'to our latest Users on Fleet Management System.', _class='white'),_class='alert alert-success')
    return dict(form = form, table = table)

def haba():
    form = SQLFORM(db.auth_group, request.args(0))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    
    grid = SQLFORM.grid(db.auth_group)
    head = THEAD(TR(TH('#'),TH()))
    return dict(form = form, table = grid)


def pansigang():
    form = SQLFORM(db.auth_membership, request.args(0))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    grid = SQLFORM.grid(db.auth_membership)
    return dict(form = form, table = grid)