import sqlite3
import os
import xlrd
con = sqlite3.connect('../data.db')
data = xlrd.open_workbook('itemcodeddt.xls')
table = data.sheet_by_index(0)
nrows = table.nrows
print(nrows)
for i in range(nrows):
    row = table.row_values(i)
    print(i)
    s = con.execute("insert into ddtitemscode values ('%s','%s','%s')" % (
        i + 1, row[0], row[1]))
    s1 = s

con.commit()
