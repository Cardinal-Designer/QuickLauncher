# -*- coding:utf-8 -*-
from PySide2 import QtWidgets, QtCore
from UI.Mainwindow import Ui_MainWindow
from Environment import Package_path, dir_mix,wrapper_path,Player_path
from DataUnCopy import Space, Add
from PySide2.QtCore import Signal
from Add import Add_windows
from Card import PersonCard
from config import config
import subprocess
import math, json, os

class ReadConfig(QtCore.QThread):
    Create = Signal(str)
    error = Signal(str)
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
                    content = json.loads(f.read())
                    Package_root = dir_mix(Path, pkg_name)

                    To = {
                        "Package_root" : Package_root,
                        "cover" : dir_mix(Package_root, content["cover"]),
                        "name" : content["Name"],
                        "Description" : content["Description"]
                    }

                    self.Create.emit(json.dumps(To))

        except:
            self.error.emit('包：[' + now_Process + ']异常')
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

        Add('select')
        Space['select'] = set()
        #创建跨组件共享变量

        self.Card = {}
        self.Card_List = {}

    def show(self) -> None:
        super().show()
        self.FindPackage = ReadConfig()
        self.FindPackage.error.connect(self.error)
        self.FindPackage.Create.connect(self.Create)
        self.FindPackage.start()

    def error(self,text):
        QtWidgets.QMessageBox.warning(self, 'error', text, QtWidgets.QMessageBox.Yes)

    def Create(self,content):
        receive = json.loads(content)
        Package_root = receive["Package_root"]
        Icon = receive["cover"]
        self.N += 1

        w = (self.N - 1) % 5

        x = w * (150 + 6)

        l = math.ceil(self.N / 5)
        y = (l > 0) * (l - 1) * 150 + 6 * (l > 0) * (l - 1)

        hash_ = hash(Package_root)
        self.Card_List[hash_] = Package_root
        self.Card[hash_] = PersonCard(self.scrollAreaWidgetContents, x, y,Icon,hash_,receive)
        self.Card[hash_].show()

        l = math.ceil(self.N / 5)
        L = (l > 0) * (l - 1) * 150 + 6 * (l > 0) * (l - 1) + 300
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(780, L))



    def AddDepends(self):
        self.Add_window.show()

    def RunAll(self):
        v = config.config['PlayerVersion']
        if v == 'Wrong version' or not v:
            QtWidgets.QMessageBox.warning(self, 'error', '没有找到show组件，请点击右下角加号图包进行安装', QtWidgets.QMessageBox.Yes)
        elif not self.Card_List:
            QtWidgets.QMessageBox.warning(self, 'error', '没有图包，自行添加', QtWidgets.QMessageBox.Yes)
        elif not Space['select']:
            QtWidgets.QMessageBox.warning(self, 'error', '没有选择图包', QtWidgets.QMessageBox.Yes)
        else:
            choose = QtWidgets.QMessageBox.information(self, 'Success', '一切就绪', QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.Yes)
            if choose == QtWidgets.QMessageBox.StandardButton.Yes:
                for i in Space['select']:
                    subprocess.Popen([wrapper_path,dir_mix(Player_path,v),self.Card_List[i]])

