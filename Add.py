from PySide2 import QtWidgets
from UI.Add import Ui_MainWindow

class Add_windows(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Add Depends")