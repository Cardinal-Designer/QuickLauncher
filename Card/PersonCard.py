from PySide2 import QtWidgets,QtGui,QtCore
from PySide2.QtCore import QRect
from Environment import path,dir_mix
from DataUnCopy import Space

class Label_Plus(QtWidgets.QLabel):
    Press = QtCore.Signal()
    def __init__(self,i):
        super(Label_Plus, self).__init__(i)
    def mousePressEvent(self, ev:QtGui.QMouseEvent):
        self.Press.emit()

class PersonCard(QtCore.QObject):
    def __init__(self,Widgets,x,y,Icon,hash_,receive):
        super(PersonCard, self).__init__()
        self.key = False
        self.hash_ = hash_
        self.receive = receive

        Width = 150
        Height = 150

        self.base =QtWidgets.QWidget(Widgets)
        self.base.setGeometry(QRect(x, y, Width, Height))
        self.base.setObjectName('QWidget_Base')
        self.base.setStyleSheet("QWidget#QWidget_Base{border-radius: 10px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;}")
        self.Label = Label_Plus(self.base)

        ImageWidth = 110
        ImageHeight = 110

        Mid = (Height-ImageHeight)/2
        self.Label.setGeometry(QRect(int(Mid), int(Mid) - 10, ImageWidth, ImageHeight))


        self.Pix = QtGui.QPixmap(Icon).scaled(ImageWidth,ImageHeight)
        self.Label.setPixmap(self.Pix)

        self.Label_Name = QtWidgets.QLabel(self.base)
        self.Label_Name.setGeometry(QRect(5, Mid + ImageHeight -5, 140, 20))
        self.Label_Name.setAlignment(QtCore.Qt.AlignHCenter)
        self.Label_Name.setText(self.receive["name"])

        self.Label.Press.connect(self.ChangeState)



    def ChangeState(self):
        if self.key == False:
            self.key = True
            # 表示已经选择
            try:
                Space["select"].add(self.hash_)
            except:
                pass

            self.base.setStyleSheet("QWidget#QWidget_Base{border-radius: 10px;background-color: rgb(255, 255, 255);border: 1px solid #0366d6;}")
        else:
            self.key = False

            try:
                Space["select"].remove(self.hash_)
            except:
                pass

            self.base.setStyleSheet("QWidget#QWidget_Base{border-radius: 10px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;}")

    def show(self):
        for i in self.__dict__:
            try:
                getattr(self, i).show()
            except:
                pass



