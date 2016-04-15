import xlrd
import sys
fname = sys.argv[1]
print repr(fname)
bk = xlrd.open_workbook(fname)

a = bk.sheets()[0]


nrows = a.nrows
ncols = a.ncols
print nrows, ncols

def log(s):
    for i in s.splitlines():
        print 'userlog("""', i, '""")'
for i in range(0, nrows):
    for j in range(0, ncols):
        s = a.cell_value(i,j)
#        if s.strip() != '':
#        log(s)
        print '+++', s, '++++'
