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
        disk = c+':'
        if os.path.isdir(disk):
            disk_list.append(disk)
    return disk_list
 
def monitor_usbdisk(disk_list):
    while True:
        usb_disk = get_disklist()[-1]
        if  usb_disk not in disk_list:
            print('Warning : USB disk be insert on ',usb_disk)
            #break
        time.sleep(5)
 
if __name__ == '__main__':
    monitor_usbdisk(get_disklist())