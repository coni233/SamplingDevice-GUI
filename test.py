'''with open('../log.txt') as f:
    l = f.readlines()
times = l[0::3]
x = []
for i in times:
    time = i.strip().split('Time:')[1].split(';')[2]  # '16:54:10;;Date:2022-10-27;;Week:4']
    print(time)
    day = i.strip().split('Time:')[1].split(';')[2].split(':')[1]
    merge = day + ' ' + time
    x.append(merge)
print('33',x)'''
import os
import xlrd

filename = os.path.abspath('../压力 温度数据格式 .xls')
book = xlrd.open_workbook(filename)
sheets = book.sheets()
print(sheets)  # 所有的表对象
names = book.sheet_names()
print(names)  # 所有的表名
sheet1 = book.sheet_by_index(0)
column_rows = sheet1.nrows  # 行数
print('行数:{}'.format(column_rows))
column_number = sheet1.ncols  # 列数
print('列数:{}'.format(column_number))


time = sheet1.col_values(0)[1:] 
for row in range(len(time)):
    time[row] = str(xlrd.xldate_as_tuple(time[row],0))
#print(time)
'''
time[0] = time[0].strip('(').strip(')').replace(" ", "")
print(time[0].split(',')[0] + ' ' + time[0].split(',')[1] + ' ' + time[0].split(',')[2] + ' ' + time[0].split(',')[3] + ' ' + time[0].split(',')[4] + ' ' + time[0].split(',')[5])
'''

for row in range(0,len(time),6):
    for i in range(6):
        if(i + row >= len(time)):
            break
        #print(time[row+i])
        temp = time[row+i].strip('(').strip(')').replace(" ", "")
        temp = temp.split(',')[0] + '年' + temp.split(',')[1] + '月' + temp.split(',')[2] + '日' + temp.split(',')[3] + '时' + temp.split(',')[4] + '分' + str(i*10) + '秒'  
        time[row+i] = temp
print(time)
press=sheet1.col_values(2)[1:] 
#print(press)
speed=sheet1.col_values(3)[1:] 
#print(speed)