db1.define_table('Status', 
    Field('status','string',length=20, requires = [IS_UPPER(), IS_NOT_IN_DB(db1, 'Status.status')]))

db1.define_table('Employee_Status', 
    Field('status','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db1, 'Status.status')]),    
    Field('description','string'))

db1.define_table('Overtime_Status', 
    Field('status','string',length=50, requires = IS_NOT_IN_DB(db1, 'Status.status')),    
    Field('description','string'))

db1.define_table('Leave_Status', 
    Field('status','string',length=50),# requires = IS_NOT_IN_DB(db1, 'Leave_Status.status')),    
    Field('action_required',length=50),
    Field('description','string', length = 50))

db1.define_table('Type_Leave', 
    Field('type_of_leave', 'string',length=50, requires = IS_NOT_IN_DB(db1, 'Type_Leave.type_of_leave')),    
    Field('description','string', length = 50))

db1.define_table('Department',    
    Field('department_code','string', length = 5, label ='Department Code', requires = IS_NOT_IN_DB(db1, 'Department.department_code')),
    Field('department_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db1, 'Department.department_name')]),
    Field('status_id','reference Status', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Status.id,'%(status)s', zero = 'Choose status')))

db1.define_table('Designation',    
    Field('designation_code','string', length = 5, label ='Designation Code', requires = IS_NOT_IN_DB(db1, 'Designation.designation_code')),
    Field('designation_name','string', length = 50, label = 'Designation Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db1, 'Designation.designation_name')]),
    Field('status_id','reference Status', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Status.id,'%(status)s', zero = 'Choose status')))

db1.define_table('Employee_Master',
    Field('title','string',length = 25, requires = IS_IN_SET(['Mr.','Ms.','Mrs.','Mme'], zero = 'Title')),
    Field('first_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]),
    Field('middle_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]),
    Field('last_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]),
    Field('employee_status_id','reference Employee_Status', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Employee_Status.id,'%(status)s', zero = 'Choose status')))

db1.define_table('Labor_Card_Profession',
    Field('labor_card_profession', 'string', length = 50))

db1.define_table('Sponsor',
    Field('sponsor', 'string', length = 50),
    Field('status_id','reference Status', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Status.id,'%(status)s', zero = 'Choose status')))

db1.define_table('Employee_Employment_Details',
    Field('employee_id', 'reference Employee_Master', ondelete = 'NO ACTION', writable = False),
    Field('employee_no', 'integer'),
    Field('account_code', 'string', length = 10),
    Field('department_code_id','reference Department', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Department.id, '%(department_code)s - %(department_name)s', zero = 'Choose Department'), represent = lambda v, r: '' if v is None else v),
    Field('designation_code_id','reference Designation', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Designation.id, '%(designation_code)s - %(designation_name)s', zero = 'Choose Designation')),
    Field('leave_entitlement','string',length=50),
    Field('leave_days_per_year','integer',default=0),
    Field('air_fare','string',length=50),
    Field('date_joined','date', default = request.now),    
    Field('date_last_return','date', default = request.now),
    Field('date_last_ticket','date', default = request.now),
    Field('date_leave_due','date', default = request.now),
    Field('proposed_date','date', default = request.now),
    Field('labor_card_profession_id', 'reference Labor_Card_Profession', ondelete = 'NO ACTION', requires=IS_IN_DB(db1,db1.Labor_Card_Profession.id,'%(labor_card_profession)s',zero='Choose Profession')),
    Field('sector', 'string', length = 50),    
    Field('sponsors_id', 'reference Sponsor',ondelete='NO ACTION',requires=IS_IN_DB(db1,db1.Sponsor.id,'%(sponsor)s',zero='Choose Sponsor')),
    Field('sponsors_occ', 'string', length = 50))

db1.define_table('Employee_Master_Leave_Temporary',
    Field('transaction_no','string',length=25),
    Field('employee_id','reference Employee_Master', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Employee')),    
    Field('application_date', 'date', default = request.now, writable=False),
    Field('from_effective_date','date', default = request.now),
    Field('to_effective_date','date', default = request.now),
    Field('replacement','reference Employee_Master', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Replacement')),    
    Field('type_of_leave_id', 'reference Type_Leave', ondelete = 'NO ACTION',requires = IS_IN_DB(db1, db1.Type_Leave.id,'%(type_of_leave)s', zero = 'Choose Type')),
    Field('duration_leave','integer', default = 0),        
    Field('remarks', 'string'),
    Field('status_id','reference Leave_Status', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Leave_Status.id,'%(status)s', zero = 'Choose status')),
    Field('canceled','boolean',default=False),
    Field('deleted','boolean',default=False))

db1.define_table('Employee_Master_Leave',
    Field('doc_ref_no','string',length=25),
    Field('memo','string',length=25),
    Field('employee_id','reference Employee_Master', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Employee')),    
    Field('application_date', 'date', default = request.now, writable=False),
    Field('from_effective_date','date', default = request.now),
    Field('to_effective_date','date', default = request.now),
    Field('return_date','date',default=request.now),
    Field('replacement','reference Employee_Master', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Replacement')),    
    Field('type_of_leave_id', 'reference Type_Leave', ondelete = 'NO ACTION',requires = IS_IN_DB(db1, db1.Type_Leave.id,'%(type_of_leave)s', zero = 'Choose Type')),
    Field('duration_leave','integer', default = 0),        
    Field('remarks', 'string'),
    Field('status_id','reference Leave_Status', ondelete = 'NO ACTION', requires = IS_IN_DB(db1, db1.Leave_Status.id,'%(status)s', zero = 'Choose status')),
    Field('canceled','boolean',default=False),
    Field('deleted','boolean',default=False))