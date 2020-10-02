# -*- coding:utf-8 -*-
from Quick import *
import sys

app = QtWidgets.QApplication(sys.argv)

graphics = Quick()
graphics.show()

sys.exit(app.exec_())