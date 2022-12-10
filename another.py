from PyQt5 import QtCore, QtGui, QtWidgets
import anotherGUI
import sys
import os
import string

class shuchu(QtWidgets.QMainWindow,anotherGUI.Ui_Form):
    def __init__(self):
        super(shuchu, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.INI_file)
        #self.statusBar.addPermanentWidget(self.label_3, 0)   #将label控件放进状态栏
        self.Timer=QtCore.QTimer()   #自定义QTimer类
        self.Timer.start(500)  #每1s运行一次
        self.Timer.timeout.connect(self.updateTime)   #与updateTime函数连接

    def INI_file(self):
        time=str(self.doubleSpinBox.value())
        #print(time)
        disk_list = []
        for c in string.ascii_uppercase:
            disk = c+':/'
            if os.path.isdir(disk):
                disk_list.append(disk)
        j = 0
        for i in disk_list:
            if os.path.exists(os.path.join(i,"ahfu2el253sdf235lfsnpiov9.txt")):
                j = j + 1
                path = os.path.join(i, "INI.txt")
        if j == 1:
            try:
                with open(path,'w+') as file:
                    file.write(time)
                    QtWidgets.QMessageBox.information(None,'提示','文件保存成功')
            except:
                QtWidgets.QMessageBox.warning(None,'警告','没有成功保存！！！')
        elif j == 0:
            QtWidgets.QMessageBox.warning(None,'警告','未检测到tf卡，请检测tf卡根目录是否存在“ahfu2el253sdf235lfsnpiov9.txt”文件')
        else:
            QtWidgets.QMessageBox.warning(None,'警告','检测到多张tf卡，请手动选择位置')
            filepath, type = QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", "./INI.txt" ,'txt(*.txt)')
            try:
                with open(filepath,'w+') as file:
                    file.write(time)
                    QtWidgets.QMessageBox.information(None,'提示','文件保存成功')
            except:
                QtWidgets.QMessageBox.warning(None,'警告','没有成功保存！！！')

    def updateTime(self):
        time=QtCore.QDateTime.currentDateTime()    #获取现在的时间
        timeplay=time.toString('yyyy-MM-dd hh:mm:ss dddd')   #设置显示时间的格式
        self.label_3.setText(timeplay)  # 设置label_3控件显示的内容


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = shuchu()
    window.show()
    sys.exit(app.exec_())