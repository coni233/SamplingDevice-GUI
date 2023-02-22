with open('../log_g.txt') as f:
    l = f.readlines()
times = l[0::5]
x = []
for i in times:
    time = i.strip().split('Time:')[1].split(';')[0]  # 16:54:10
    day = i.strip().split('Time:')[1].split(';')[2].split(':')[1]
    merge = day + ' ' + time
    x.append(merge)


tempers = l[1::5]
temper_l = []
for i in tempers:
    try:
        temper = i.split(':')[1].strip().replace('℃', '')
        temper_l.append(eval(temper))
    except:
        temper_l.append(None)

depths_1 = l[3::5]
depth_l1 = []
for i in depths_1:
    depth = i.split(':')[1].split(' ')[1]
    depth_l1.append(eval(depth))
print(depth_l1)

depths_2 = l[4::5]
depth_l2 = []
for i in depths_2:
    depth = i.split(':')[1].split(' ')[1]
    depth_l2.append(eval(depth))
print(depth_l2)
