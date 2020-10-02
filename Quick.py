# -*- coding:utf-8 -*-
from PySide2 import QtWidgets, QtCore
from UI.Mainwindow import Ui_MainWindow
from Environment import Package_path, dir_mix
from DataUnCopy import Space, Add
from PySide2.QtCore import Signal
from Add import Add_windows
from Card import PersonCard
import math, json, os

def message_info(type, title, msgs):
    msg = {
        'type': type,
        'title': title,
        'msg': msgs
    }
    return json.dumps(msg)
    # 包装message数据


class ReadConfig(QtCore.QThread):
    Create = Signal(str,str)
    def __init__(self):
        super(ReadConfig, self).__init__()

    def run(self) -> None:
        Path = None  # 图包父目录
        Child_path = None  # 图包文件夹目录名[list]
        # 遍历图包目录
        for paths, child_path, j in os.walk(Package_path):
            Path = paths
            Child_path = child_path
            break

        now_Process = None
        try:
            for pkg_name in Child_path:
                now_Process = pkg_name
                config_file = dir_mix(
                    Path,
                    pkg_name,
                    'config.json'
                )
                # 合并多段数据 组成config文件的目录数据

                with open(config_file, 'r', encoding='utf-8') as f:
                    Package_root = dir_mix(Path,pkg_name)
                    cover =  dir_mix(Package_root,json.loads(f.read())["cover"])
                    self.Create.emit(Package_root,cover)

        except:
            self.message.emit(message_info(type='wrong', title='error', msgs='包：[' + now_Process + ']异常'))
            # 回调，发送出错的包的名称



class Quick(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Quick, self).__init__()
        self.Add_window = Add_windows()
        self.setupUi(self)
        self.setStyleSheet("QWidget#centralwidget{background-color: rgb(255, 255, 255);}")
        self.scrollAreaWidgetContents.setStyleSheet("QWidget#scrollAreaWidgetContents{background-color: rgb(255, 255, 255);}")
        self.setWindowTitle("QuickLauncher")
        self.N = 0  # 初始为0，在第一次调用Create时候会加1

        # Add('configs')
        # Space['configs'] = []
        # Add('pkg_root')
        # Space['pkg_root'] = []
        # 创建跨组件共享变量

        self.Card = {}
        self.Card_List = []

    def show(self) -> None:
        super().show()
        self.FindPackage = ReadConfig()
        self.FindPackage.Create.connect(self.Create)
        self.FindPackage.start()

    def Create(self,Package_root,Icon):
        self.N += 1

        w = (self.N - 1) % 5

        x = w * (150 + 6)

        l = math.ceil(self.N / 5)
        y = (l > 0) * (l - 1) * 150 + 6 * (l > 0) * (l - 1)

        hash_ = hash(Package_root)

        self.Card[hash_] = PersonCard(self.scrollAreaWidgetContents, x, y,Icon)
        self.Card[hash_].show()

        l = math.ceil(self.N / 5)
        L = (l > 0) * (l - 1) * 150 + 6 * (l > 0) * (l - 1) + 300
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(780, L))

    def AddDepends(self):
        self.Add_window.show()

    def RunAll(self):
        pass
