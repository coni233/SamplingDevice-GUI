from PyQt5 import QtCore, QtGui, QtWidgets
import anotherGUI
import sys

class shuchu(QtWidgets.QMainWindow,anotherGUI.Ui_Form):
    def __init__(self):
        super(shuchu, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.INI_file)

    def INI_file(self):
        dateTime=str(self.dateTimeEdit.dateTime())
        dateTime=dateTime.strip('PyQt5.QtCore.QDateTime')[1:-1]
        dateTime=dateTime.replace(" ", "")
        douhao=dateTime.rindex(',')
        dateTime=dateTime[0:douhao]
        hz=str(self.spinBox.value())
        print(dateTime)
        print(hz)
        filepath, type = QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", "./INI.txt" ,'txt(*.txt)')
        try:
            with open(filepath,'w+') as file:
                file.write(dateTime+'\n')
                file.write(hz)
                QtWidgets.QMessageBox.information(None,'提示','文件保存成功')
        except:
            QtWidgets.QMessageBox.warning(None,'警告','没有成功保存！！！')




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = shuchu()
    window.show()
    sys.exit(app.exec_())