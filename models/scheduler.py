from gluon.scheduler import Scheduler

def get_consolidation():
    print 'get_consolidation: ', request.now
    for n in db().select(orderby = db.Sales_Order.id):
        print 'id: ', n.id    

def reporting_percentages():
    time.sleep(5)
    print '50%'
    time.sleep(5)
    print '!clear!100%'
    return 1

genSched = Scheduler(db, tasks = dict(
    get_consolidation = get_consolidation
    ))
