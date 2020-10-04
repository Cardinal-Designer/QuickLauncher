# -*- coding: utf-8 -*-
from PySide2 import QtWidgets,QtGui,QtCore
from PySide2.QtCore import QRect
from Environment import path,dir_mix
from PySide2.QtWidgets import QPushButton
from DataUnCopy import Space
from Environment import Player_path,dir_mix
from config import config
import shutil,os

class VersionCard(QtCore.QObject):
    See_md = QtCore.Signal(str)
    error = QtCore.Signal(str)
    change = QtCore.Signal(str,mode)
    update = QtCore.Signal()
    def __init__(self, Widgets, x, y,Info):
        super().__init__()
        self.Info = Info

        Width = 365
        Height = 50

        self.base = QtWidgets.QWidget(Widgets)
        self.base.setGeometry(QRect(x, y, Width, Height))
        self.base.setObjectName('QWidget_Base')
        self.base.setStyleSheet("QWidget#QWidget_Base{border-radius: 5px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;}")

        self.Label = QtWidgets.QLabel(self.base)
        self.Label.setGeometry(QRect(5, 5, 40, 40))
        self.Pix = QtGui.QPixmap(dir_mix(path,'UI','ExtraImage','cube.svg')).scaled(40, 40)
        self.Label.setPixmap(self.Pix)

        self.Label_TagName = QtWidgets.QLabel(self.base)
        self.Label_TagName.setGeometry(QRect(50, 15, 120, 20))
        self.Label_TagName.setText(self.Info["TagName"])

        self.pushButton_see = QPushButton(self.base)
        self.pushButton_see.setGeometry(QRect(180, 10, 30, 30))
        self.pushButton_see.setStyleSheet('border-radius: 5px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;')
        self.Pix_see = QtGui.QPixmap(dir_mix(path, 'UI', 'ExtraImage', 'see.svg')).scaled(25, 25)
        self.pushButton_see.setIcon(QtGui.QIcon(self.Pix_see))
        self.pushButton_see.setToolTip("查看更新日志")
        self.pushButton_see.clicked.connect(self.see)

        self.pushButton_download = QPushButton(self.base)
        self.pushButton_download.setGeometry(QRect(220, 10, 30, 30))
        self.pushButton_download.setStyleSheet(
            'border-radius: 5px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;')
        self.Pix_download = QtGui.QPixmap(dir_mix(path, 'UI', 'ExtraImage', 'download.svg')).scaled(25, 25)
        self.pushButton_download.setIcon(QtGui.QIcon(self.Pix_download))
        self.pushButton_download.setToolTip("下载该版本")
        self.pushButton_download.clicked.connect(self.download)

        self.pushButton_set = QPushButton(self.base)
        self.pushButton_set.setGeometry(QRect(260, 10, 30, 30))
        self.pushButton_set.setStyleSheet(
            'border-radius: 5px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;')
        self.Pix_set = QtGui.QPixmap(dir_mix(path, 'UI', 'ExtraImage', 'set.svg')).scaled(25, 25)
        self.pushButton_set.setIcon(QtGui.QIcon(self.Pix_set))
        self.pushButton_set.setToolTip("设置该版本为默认")
        self.pushButton_set.clicked.connect(self.setDefault)

        self.pushButton_del = QPushButton(self.base)
        self.pushButton_del.setGeometry(QRect(300, 10, 30, 30))
        self.pushButton_del.setStyleSheet(
            'border-radius: 5px;background-color: rgb(255, 255, 255);border: 1px solid #e1e4e8;')
        self.pushButton_del.setToolTip("删除该版本")
        self.pushButton_del.clicked.connect(self.Delete)
        self.Pix_del = QtGui.QPixmap(dir_mix(path, 'UI', 'ExtraImage', 'del.svg')).scaled(25, 25)
        self.pushButton_del.setIcon(QtGui.QIcon(self.Pix_del))


    def Find(self):
        # 检查是否存在该版本
        if os.path.exists(dir_mix(Player_path,self.Info["TagName"])):
            self.pushButton_set.setEnabled(True)
            self.pushButton_del.setVisible(True)
        else:
            self.pushButton_set.setEnabled(False)
            self.pushButton_del.setVisible(False)

    def Delete(self):
        try:
            shutil.rmtree(dir_mix(Player_path,self.Info["TagName"]))
        except:
            pass
        self.Find()

        if config.config["PlayerVersion"] == self.Info["TagName"]:
            config.config["PlayerVersion"] = "Wrong version"
            config.update()
            self.update.emit()

    def setDefault(self):
        config.config["PlayerVersion"] = self.Info["TagName"]
        config.update()
        self.update.emit()

    def see(self):
        self.See_md.emit(self.Info["TagName"])

    def download(self):
        Tag = self.Info["TagName"]

        self.Text = '<h1>正在下载 :{}</h1>'.format(Tag)

        def Change_Text(Url): # 更新下载文件的Text显示
            self.Text += '\n'
            self.Text += "<p>下载：{}</p>".format(Url)
            self.change.emit(self.Text)

        def end():
            self.Text += '\n'
            self.Text += '<h2>下载完成<h2>'
            self.change.emit(self.Text)
            self.Find()

        Object = Space["jsdelivr_Data"].version(Tag)
        if Object == ValueError:
            self.error.emit("网络错误，无法获取目录结构")
        else:
            Space["jsdelivr_Data"].DownloadUnit.end.connect(end)
            Space["jsdelivr_Data"].DownloadUnit.PackDownload(Object,Tag,dir_mix(Player_path,Tag),Change_Text)




    def show(self):
        for i in self.__dict__:
            try:
                getattr(self, i).show()
            except:
                pass
        self.Find()