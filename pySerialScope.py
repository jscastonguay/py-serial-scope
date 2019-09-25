import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic


qtcreator_file  = "main.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.doTest)

    def doTest(self):
        print("doTest")
        x = np.linspace(0, 20, 100)
        self.graphicsView.plot(np.sin(x))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())