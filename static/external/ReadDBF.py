import dbf 

db = dbf.Table("/home/larry/Workspace/dbf/Sales_Invoice.dbf")
db.open()
for rec in db:
    print rec.sales_or, rec.sales_date, rec.dept_id, rec.total_amt
print '--- '