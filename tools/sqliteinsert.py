import sqlite3
import xlrd
con = sqlite3.connect('../data.db')
data = xlrd.open_workbook('itemcodehxbns.xls')
table = data.sheet_by_index(0)
nrows = table.nrows
print(nrows)
for i in range(nrows):
    row = table.row_values(i)
    print(i)
    #s = con.execute("insert into hxbnsitemscode values ('%s','%s','%s','%s')" % (
    #    i + 1, row[0], row[1],row[2]))
    s=con.execute("UPDATE hxbnsitemscode SET item_id='%s' WHERE name='%s'" %(int(row[2]),row[0]))
    s1 = s

con.commit()
