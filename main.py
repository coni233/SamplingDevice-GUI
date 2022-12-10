from email.utils import parseaddr
from turtle import color
from PyQt5 import QtCore, QtGui, QtWidgets
import mainGUI
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import xlrd


class demo(QtWidgets.QMainWindow,mainGUI.Ui_MainWindow):
    def __init__(self):
        super(demo, self).__init__()
        self.setupUi(self)

        self.checkBox_Presure.setHidden(False)#压力 不隐藏控件
        self.checkBox_Size.setHidden(False)#速度
        self.checkBox_Depth.setHidden(False)#深度
        self.checkBox_Temperature.setHidden(False)#温度

        self.radioButton_qb.setHidden(True)#全部 隐藏单选按钮控件
        self.radioButton_Presure.setHidden(True)#压力 隐藏控件
        self.radioButton_Size.setHidden(True)#速度
        self.radioButton_Depth.setHidden(True)#深度
        self.radioButton_Temperature.setHidden(True)#温度

        self.radioButton_qb.toggled.connect(self.draw_all)#全部 绑定点击事件
        self.radioButton_Presure.toggled.connect(self.draw_press)#压力 
        self.radioButton_Size.toggled.connect(self.draw_speed)#速度
        self.radioButton_Depth.toggled.connect(self.draw_d)#深度
        self.radioButton_Temperature.toggled.connect(self.draw_t)#温度

        self.checkBox_Depth.setChecked(False)#深度 默认不勾选状态
        self.checkBox_Depth.clicked.connect(self.draw_depth)
        self.checkBox_Temperature.setChecked(False)#温度
        self.checkBox_Temperature.clicked.connect(self.draw_tem)
        self.checkBox_Presure.setChecked(False)#压力
        self.checkBox_Presure.clicked.connect(self.draw_presure)
        self.checkBox_Size.setChecked(False)#尺寸
        self.checkBox_Size.clicked.connect(self.draw_size)
        self.pushButton_openfile.clicked.connect(self.chose_file)
        self.pushButton_openfile_xls.clicked.connect(self.chose_file_xls)
        self.pushButton_xs.clicked.connect(self.showall)
        self.action_shuchu.triggered.connect(self.Shuchu) ########菜单这个方法不太确定，能用
        self.log = 0
        self.xls = 0


    def chose_file(self): #log
        try:
            file,_ = QtWidgets.QFileDialog.getOpenFileNames(self,'选择日志文件','','*.txt')
            self.lineEdit_showpath.setText(file[0])

            with open(file[0]) as f:
                l = f.readlines()

            # with open('./log.txt') as f:
            #     l = f.readlines()


            times = l[0::3]  # 'Time:16:54:10;;Date:2022-10-27;;Week:4\n'
            self.x = []
            for i in times:
                time = i.strip().split('Time:')[1].split(';')[0]  # '16:54:10;;Date:2022-10-27;;Week:4']
                day = i.strip().split('Time:')[1].split(';')[2].split(':')[1]
                merge = day + ' ' + time
                self.x.append(merge)
            #print('33',self.x)

            tempers = l[1::3]
            self.temper_l = []
            for i in tempers:
                temper = i.split(':')[1].strip().replace('℃', '')
                self.temper_l.append(eval(temper))
            #print(self.temper_l)

            depths = l[2::3]
            self.depth_l = []
            for i in depths:
                depth = i.split(':')[1].split(' ')[1]
                self.depth_l.append(eval(depth))
            #print(self.depth_l)

            self.step = int(len(self.x)/7 + 1) #x轴的step


###############################################################写表格
            self.tableWidget.clearContents()
            self.tableWidget.setColumnCount(len(self.x))

    # 写入时间
            t_x = 0
            for i in self.x:
                day_time = QtWidgets.QTableWidgetItem(i)
                day_time.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget.setItem(0,t_x,day_time)
                t_x +=1
    # 写入温度
            t_temper = 0
            for i in self.temper_l:
                day_temper = QtWidgets.QTableWidgetItem(str(i))
                day_temper.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget.setItem(1,t_temper,day_temper)
                t_temper +=1
    # 写入深度
            t_depth = 0
            for i in self.depth_l:
                day_depth = QtWidgets.QTableWidgetItem(str(i))
                day_depth.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget.setItem(2,t_depth,day_depth)
                t_depth +=1


            self.tableWidget.resizeColumnsToContents()
            # self.tableWidget.horizontalHeader().setVisible(False)

            QtWidgets.QMessageBox.information(self.pushButton_openfile, '提示', '读取成功')
            self.log = 1
##################################################################################################################画图
            self.checkBox_Presure.setHidden(False)#压力 不隐藏控件
            self.checkBox_Size.setHidden(False)#速度
            self.checkBox_Depth.setHidden(False)#深度
            self.checkBox_Temperature.setHidden(False)#温度

            self.radioButton_qb.setHidden(True)#全部 隐藏单选按钮控件
            self.radioButton_Presure.setHidden(True)#压力 隐藏控件
            self.radioButton_Size.setHidden(True)#速度
            self.radioButton_Depth.setHidden(True)#深度
            self.radioButton_Temperature.setHidden(True)#温度
            
            self.checkBox_Temperature.setChecked(True) #默认勾选
            self.checkBox_Depth.setChecked(True)
            self.checkBox_Temperature.setEnabled(True)
            self.checkBox_Depth.setEnabled(True)
            self.checkBox_Presure.setEnabled(False)
            self.checkBox_Size.setEnabled(False)

            if self.checkBox_Temperature.isChecked() and self.checkBox_Depth.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_tandd(self)
        except:
            QtWidgets.QMessageBox.warning(self.pushButton_openfile,'警告','未选择文件或文件格式有误')

    def draw_tem(self): #勾选框温度
        try:

            if self.checkBox_Temperature.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_t(self)
            if self.checkBox_Temperature.isChecked() and self.checkBox_Depth.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_tandd(self)
            if self.checkBox_Depth.isChecked() and self.checkBox_Temperature.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_d(self)
            if self.checkBox_Depth.isChecked() == False and self.checkBox_Temperature.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
        except:
            QtWidgets.QMessageBox.warning(self.checkBox_Temperature,'警告','未选择文件或文件格式有误')


    def draw_depth(self): #勾选框深度
        try:
            if self.checkBox_Depth.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_d(self)
            if self.checkBox_Temperature.isChecked() and self.checkBox_Depth.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_tandd(self)
            if self.checkBox_Depth.isChecked() == False and self.checkBox_Temperature.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_t(self)
            if self.checkBox_Depth.isChecked() == False and self.checkBox_Temperature.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
        except:
            QtWidgets.QMessageBox.warning(self.checkBox_Depth,'警告','未选择文件或文件格式有误')


    def draw_tandd(self): #画温度和深度
        plt.close()
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.plot(self.x, self.temper_l,color='b')
        plt.plot(self.x, self.depth_l,color='r')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['温度','深度'],loc=0)
        plt.xticks(self.x[::self.step], self.x[::self.step], rotation=0, fontsize=8)
        plt.scatter(self.x, self.temper_l,color='b',alpha=0.2) #生成点
        plt.scatter(self.x, self.depth_l,color='r',alpha=0.2)
        plt.xlabel('时间',fontsize=10)
        plt.grid() #显示网格
        # plt.show()
        self.canvas.draw()
    
    def draw_t(self): #只画温度
        plt.close()#防止点太多次了占用内存
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.plot(self.x, self.temper_l,color='b')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['温度'],loc=0)
        plt.xticks(self.x[::self.step], self.x[::self.step], rotation=0, fontsize=8)
        plt.scatter(self.x, self.temper_l,color='b',alpha=0.2)
        plt.xlabel('时间',fontsize=10)
        plt.ylabel('温度',fontsize=10)
        plt.grid()
        # plt.show()
        self.canvas.draw()

    def draw_d(self): #只画深度
        plt.close()
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.plot(self.x, self.depth_l,color='r')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['深度'],loc=0)
        plt.xticks(self.x[::self.step], self.x[::self.step], rotation=0, fontsize=8)
        plt.scatter(self.x, self.depth_l,color='r',alpha=0.2)
        plt.xlabel('时间',fontsize=10)
        plt.ylabel('深度',fontsize=10)
        plt.grid()
        # plt.show()
        self.canvas.draw()


    def chose_file_xls(self):#xls
        try:
            file_xls,_ = QtWidgets.QFileDialog.getOpenFileNames(self,'选择表格文件','','*.xls')
            self.lineEdit_showpath.setText(file_xls[0])

            with xlrd.open_workbook(file_xls[0]) as excel:
                sheet = excel.sheet_by_index(0) #工作薄
                column_rows = sheet.nrows  # 行数
                column_number = sheet.ncols  # 列数
                self.time_xls = sheet.col_values(0)[1:] 
                for row in range(len(self.time_xls)):
                    self.time_xls[row] = str(xlrd.xldate_as_tuple(self.time_xls[row],0))
                for row in range(0,len(self.time_xls),6): ###一会要改，索引会溢出
                    for i in range(6):
                        if(i + row >= len(self.time_xls)):
                            break
                        temp = self.time_xls[row+i].strip('(').strip(')').replace(" ", "")
                        temp = temp.split(',')[0] + '-' + temp.split(',')[1] + '-' + temp.split(',')[2] + ' ' + temp.split(',')[3] + ':' + temp.split(',')[4] + ':' + str(i*10) 
                        self.time_xls[row+i] = temp
                #print(self.time_xls)
                self.press_xls = sheet.col_values(2)[1:] 
                #print(self.press_xls)
                self.speed_xls = sheet.col_values(3)[1:] 
                #print(self.speed_xls)

                self.step2 = int(len(self.time_xls)/7 + 1)

###############################################################写表格
                self.tableWidget.clearContents()
                self.tableWidget.setColumnCount(len(self.time_xls))

        # 写入时间
                t_time_xls = 0
                for i in self.time_xls:
                    day_time = QtWidgets.QTableWidgetItem(i)
                    day_time.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.tableWidget.setItem(0,t_time_xls,day_time)
                    t_time_xls +=1
        # 写入压力
                t_press_xls = 0
                for i in self.press_xls:
                    day_temper = QtWidgets.QTableWidgetItem(str(i))
                    day_temper.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.tableWidget.setItem(3,t_press_xls,day_temper)
                    t_press_xls +=1
        # 写入尺寸（速度）
                t_speed_xsl = 0
                for i in self.speed_xls:
                    day_depth = QtWidgets.QTableWidgetItem(str(i))
                    day_depth.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.tableWidget.setItem(4,t_speed_xsl,day_depth)
                    t_speed_xsl +=1


                self.tableWidget.resizeColumnsToContents()
                # self.tableWidget.horizontalHeader().setVisible(False)

                QtWidgets.QMessageBox.information(self.pushButton_openfile_xls, '提示', '读取成功')
                self.xls = 1
    ##################################################################################################################画图
                self.checkBox_Presure.setHidden(False)#压力 不隐藏控件
                self.checkBox_Size.setHidden(False)#速度
                self.checkBox_Depth.setHidden(False)#深度
                self.checkBox_Temperature.setHidden(False)#温度

                self.radioButton_qb.setHidden(True)#全部 隐藏单选按钮控件
                self.radioButton_Presure.setHidden(True)#压力 隐藏控件
                self.radioButton_Size.setHidden(True)#速度
                self.radioButton_Depth.setHidden(True)#深度
                self.radioButton_Temperature.setHidden(True)#温度
                
                self.checkBox_Presure.setChecked(True)#压力
                self.checkBox_Size.setChecked(True)#速度
                self.checkBox_Presure.setEnabled(True)#压力
                self.checkBox_Size.setEnabled(True)#速度
                self.checkBox_Depth.setEnabled(False)#深度
                self.checkBox_Temperature.setEnabled(False)#温度
                if self.checkBox_Presure.isChecked() and self.checkBox_Size.isChecked():
                    for i in range(self.horizontalLayout.count()):
                        self.horizontalLayout.itemAt(i).widget().deleteLater()
                    demo.draw_pressandspeed(self)
        
        
        except:
            QtWidgets.QMessageBox.warning(self.pushButton_openfile_xls,'警告','未选择文件或文件格式有误')


    def draw_pressandspeed(self):#画压力和速度
        plt.close()
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.plot(self.time_xls, self.press_xls,color='g')
        plt.plot(self.time_xls, self.speed_xls,color='y')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['压力','速度'],loc=0)
        #plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(50))
        plt.xticks(self.time_xls[::self.step2], self.time_xls[::self.step2], rotation=0, fontsize=8)
        plt.scatter(self.time_xls, self.press_xls,color='g',alpha=0.2)
        plt.scatter(self.time_xls, self.speed_xls,color='y',alpha=0.2)
        plt.xlabel('时间',fontsize=10)
        plt.grid()
        # plt.show()
        self.canvas.draw()

    def draw_press(self):#画压力
        plt.close()
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.plot(self.time_xls, self.press_xls,color='g')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['压力'],loc=0)
        plt.xticks(self.time_xls[::self.step2], self.time_xls[::self.step2], rotation=0, fontsize=8)
        plt.scatter(self.time_xls, self.press_xls,color='g',alpha=0.2)
        plt.xlabel('时间',fontsize=10)
        plt.ylabel('压力',fontsize=10)
        plt.grid()
        # plt.show()
        self.canvas.draw()

    def draw_speed(self):#画速度
        plt.close()
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.plot(self.time_xls, self.speed_xls,color='y')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['速度'],loc=0)
        plt.xticks(self.time_xls[::self.step2], self.time_xls[::self.step2], rotation=0, fontsize=8)
        plt.scatter(self.time_xls, self.speed_xls,color='y',alpha=0.2)
        plt.xlabel('时间',fontsize=10)
        plt.ylabel('速度',fontsize=10)
        plt.grid()
        # plt.show()
        self.canvas.draw()
    
    def draw_presure(self):#勾选框
        try:

            if self.checkBox_Presure.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_press(self)
            if self.checkBox_Presure.isChecked() and self.checkBox_Size.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_pressandspeed(self)
            if self.checkBox_Size.isChecked() and self.checkBox_Presure.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_speed(self)
            if self.checkBox_Size.isChecked() == False and self.checkBox_Presure.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
        except:
            QtWidgets.QMessageBox.warning(self.checkBox_Presure,'警告','未选择文件或文件格式有误')



    def draw_size(self):#勾选框
        try:

            if self.checkBox_Size.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_speed(self)
            if self.checkBox_Size.isChecked() and self.checkBox_Presure.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_pressandspeed(self)
            if self.checkBox_Presure.isChecked() and self.checkBox_Size.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_press(self)
            if self.checkBox_Presure.isChecked() == False and self.checkBox_Size.isChecked() ==False:
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
        except:
            QtWidgets.QMessageBox.warning(self.checkBox_Size,'警告','未选择文件或文件格式有误')

    
    def draw_all(self):#画四个子图
        plt.close()
        for i in range(self.horizontalLayout.count()): #清空画布
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.figure = plt.figure(dpi=80, figsize=(1, 1))  # 画板  facecolor='#FFD7C4',
        self.canvas = FigureCanvas(self.figure)  # 画布
        self.horizontalLayout.addWidget(self.canvas)
        plt.subplot(2, 2, 1)#子图1
        plt.plot(self.x, self.temper_l,color='b')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['温度'],loc=0)
        plt.ylabel('温度',fontsize=10)
        plt.xticks(self.x[::self.step*2], self.x[::self.step*2], rotation=0, fontsize=8)#x轴要更稀疏
        plt.grid()
        plt.subplot(2, 2, 2)#子图2
        plt.plot(self.x, self.depth_l,color='r')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['深度'],loc=0)
        plt.ylabel('深度',fontsize=10)
        plt.xticks(self.x[::self.step*2], self.x[::self.step*2], rotation=0, fontsize=8)#x轴要更稀疏
        plt.grid()
        plt.subplot(2, 2, 3)#子图3
        plt.plot(self.time_xls, self.press_xls,color='g')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['压力'],loc=0)
        plt.xticks(self.time_xls[::self.step2*2], self.time_xls[::self.step2*2], rotation=0, fontsize=8)
        plt.xlabel('时间',fontsize=10)
        plt.ylabel('压力',fontsize=10)
        plt.grid()
        plt.subplot(2, 2, 4)#子图4
        plt.plot(self.time_xls, self.speed_xls,color='y')
        plt.rcParams['font.sans-serif']=['Microsoft Yahei']#matplotlib不支持中文，得这样   
        plt.legend(labels=['速度'],loc=0)
        plt.xticks(self.time_xls[::self.step2*2], self.time_xls[::self.step2*2], rotation=0, fontsize=8)
        plt.xlabel('时间',fontsize=10)
        plt.ylabel('速度',fontsize=10)
        plt.grid()
        self.canvas.draw()

    
    def showall(self):#显示全部的按钮
        if self.log==1 and self.xls==1:
            self.checkBox_Presure.setHidden(True)#压力 隐藏控件
            self.checkBox_Size.setHidden(True)#速度
            self.checkBox_Depth.setHidden(True)#深度
            self.checkBox_Temperature.setHidden(True)#温度

            self.radioButton_qb.setHidden(False)#全部 显示单选按钮控件
            self.radioButton_Presure.setHidden(False)#压力 显示控件
            self.radioButton_Size.setHidden(False)#速度
            self.radioButton_Depth.setHidden(False)#深度
            self.radioButton_Temperature.setHidden(False)#温度

            self.radioButton_qb.setChecked(True)

            if self.radioButton_qb.isChecked():
                for i in range(self.horizontalLayout.count()):
                    self.horizontalLayout.itemAt(i).widget().deleteLater()
                demo.draw_all(self)

        elif self.log==1 and self.xls==0:
            QtWidgets.QMessageBox.warning(self.pushButton_xs,'警告','需要先打开xls文件')
        elif self.log==0 and self.xls==1:
            QtWidgets.QMessageBox.warning(self.pushButton_xs,'警告','需要先打开txt文件')
        else:
            QtWidgets.QMessageBox.warning(self.pushButton_xs,'警告','需要先打开txt文件和xls文件')

    def Shuchu(self): #确认开机采样时间和频率的
        import another
        self.one = another.shuchu()
        self.one.show()

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) #适配高分辨率
    app = QtWidgets.QApplication(sys.argv)
    window = demo()
    window.show()
    sys.exit(app.exec_())