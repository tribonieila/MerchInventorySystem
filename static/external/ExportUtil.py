# from datetime import date
import pyodbc 
import dbf 

server = '128.1.2.2' 
database = 'm3rch_inv_db' 
username = 'SA' 
password = 'M3rch2018' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Sample select query
cursor.execute("SELECT * FROM Sales_Invoice;") 
row = cursor.fetchone() 
# while row: 
#     print(row[1])
#     row = cursor.fetchone()

print '****'
table = dbf.Table('/home/larry/Workspace/dbf/Sales_Invoice.dbf', 'sales_or C(25); sales_date D; dept_id N(1,0); total_amt N(12,2)')

print('db definition created with field names:', table.field_names)

table.open(mode=dbf.READ_WRITE)

while row:
    for rec in ((str(row[2]),dbf.Date(row[3]),str(row[4]),row[9]),):
        table.append(rec)
    row = cursor.fetchone()

print ('records added:')
for record in table:
    print (record)
    print ('-----')

table.close()

# table.open(mode=dbf.READ_WRITE)

# table.add_fields('telephone C(10)')

# telephones = {'John Doe': '1234', 'Ethan Furman': '2345', 'Jane Smith': '3456', 'John Adams': '4567'}
# for record in table:
#     with record as r:
#         r.telephone = telephones[r.name.strip()]

# print ('updated records')
# for record in table:
#     print (record)
#     print ('-----')