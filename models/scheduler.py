from gluon.scheduler import Scheduler

def get_consolidation():
    print 'get_consolidation: ', request.now
    for n in db().select(orderby = db.Sales_Order.id):
        print 'id: ', n.id    

genSched = Scheduler(db, tasks = dict(get_consolidation = get_consolidation))