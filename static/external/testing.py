from dbfread import DBF
table = DBF('/home/larry/Workspace/web2py/applications/mtc_inv/static/external/TempTable.dbf', load=True)
print len(table)
# for record in table:
#     print(record)
# OrderedDict([('NAME', 'Alice'), ('BIRTHDATE', datetime.date(1987, 3, 1))])
# OrderedDict([('NAME', 'Bob'), ('BIRTHDATE', datetime.date(1980, 11, 12))])