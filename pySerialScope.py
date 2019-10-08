

import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
try:
    import Queue
except:
    import queue as Queue
import sys, time, serial

SER_TIMEOUT = 0.1                   # Timeout for serial Rx
baudrate    = 115200                # Default baud rate
portname    = "COM5"                # Default port name

qtcreator_file  = "main.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


# Thread to handle incoming and outgoing serial data
class SerialThread(QtCore.QThread):
    signalData = QtCore.pyqtSignal(int)
    def __init__(self, portname, baudrate): # Initialise with serial port details
        QtCore.QThread.__init__(self)
        self.portname, self.baudrate = portname, baudrate
        self.txq = Queue.Queue()
        self.running = True
 
    # JSC: ce sera appelé par une slot provenant du GUI
    def ser_out(self, s):                   # Write outgoing data to serial port if open
        self.txq.put(s)                     # ..using a queue to sync with reader thread
         
    def ser_in(self, s):                    # Write incoming serial data to screen
        
        # --- ATTENTION ---
        # JSC: C'est ici que je dois ajouter le code pour faire afficher des données
        #      Lire ceci: https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
        #      ou plutôt ceci: https://python-forum.io/Thread-Thread-Signal
        #display(s)
        self.signalData.emit(s)
        pass
         
    def run(self):                          # Run serial reader thread
        print("Opening %s at %u baud" % (self.portname, self.baudrate))
        try:
            self.ser = serial.Serial(self.portname, self.baudrate, timeout=SER_TIMEOUT)
            time.sleep(SER_TIMEOUT*1.2)
            self.ser.flushInput()
        except:
            self.ser = None
        if not self.ser:
            print("Can't open port")
            self.running = False
        while self.running:
            #s = self.ser.read(self.ser.in_waiting or 1)
            s = self.ser.readline()
            if s:                                       # Get data from serial port
                self.ser_in(int(s))                     # ..and convert to string
                #print("Data Rx")
            if not self.txq.empty():
                txd = str(self.txq.get())               # If Tx data in queue, write to serial port
                self.ser.write(txd)
        if self.ser:                                    # Close serial port when thread finished
            self.ser.close()
            self.ser = None


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.doTest)
        self.serialThread = SerialThread(portname, baudrate)
        self.serialThread.signalData.connect(self.rxData)
        self.serialThread.start()

    def doTest(self):
        print("doTest")
        x = np.linspace(0, 20, 100)
        self.graphicsView.plot(np.sin(x))

    def rxData(self, data):
        print("rxData: {}".format(data))
        d = np.array([1000, data, 1023])
        self.graphicsView.plot(d)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
