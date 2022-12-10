'''
Pyhon 监视U盘插入并告警
'''
import time
import os
import shutil
import string
 
def get_disklist():
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c+':/'
        if os.path.isdir(disk):
            disk_list.append(disk)
    print(disk_list)
    #f = os.path.exists('C:/ahfu2el253sdf235lfsnpiov9.txt')
    #print(f)
    j = 0
    for i in disk_list:
        if os.path.exists(os.path.join(i, "ahfu2el253sdf235lfsnpiov9.txt")):
            j = j + 1
            path = os.path.join(i, "INI.txt")
    print(j)
    print(path)
    return path
 
if __name__ == '__main__':
    get_disklist()