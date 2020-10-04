# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore
from UI.Add import Ui_MainWindow
from Card import VersionCard
from config import config
from Api.jsdelivr import jsdelivr
from MarkdownToHtml import ToHtml
from DataUnCopy import Space, Add
import requests
import json


class FindVersion(QtCore.QThread):
    Create = QtCore.Signal(str)
    error = QtCore.Signal(str)

    def __init__(self):
        super(FindVersion, self).__init__()
        Add('jsdelivr_Data')
        Space["jsdelivr_Data"] = jsdelivr('show',self.error)

    def run(self) -> None:
        self.Tags = Space["jsdelivr_Data"].tags()
        if self.Tags == ValueError:
            self.error.emit("网络异常，无法取得源的应答")

        for i in self.Tags:
            Info = {
                'TagName': i,
            }

            self.Create.emit(json.dumps(Info))


class Update_info(QtCore.QThread):
    error = QtCore.Signal(str)
    change = QtCore.Signal(str)

    def __init__(self):
        super(Update_info, self).__init__()
        self.Tag = None

    def A_Sentence(self):
        try:
            Url = 'https://v1.hitokoto.cn/?c=d'
            content = json.loads(requests.get(Url, timeout=5).text)

            Html = '''
            <h2>[一言]<h2>
            <h3 align="center">'''+content["hitokoto"]+'''</h3>
            <h4 align="right">—— '''+content['from_who']+'''「'''+content["from"]+'''」</h4>
            '''

            self.change.emit(Html)
        except:
            pass

    def run(self) -> None:
        if self.Tag == 'A_Sentence':
            self.A_Sentence()
            return

        Url = "https://api.github.com/repos/Cardinal-Designer/show/releases/tags/" + self.Tag
        try:
            content = json.loads(requests.get(Url, timeout=5).text)
            html = ToHtml(content["body"])
            self.change.emit(html)
        except:
            self.error.emit('网络超时')


class Add_windows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Add Depends")
        self.Key = False
        self.N = 0
        self.List = {}

        self.Update_info = Update_info()
        self.Update_info.error.connect(self.error)
        self.Update_info.change.connect(self.Change)

        self.Find = FindVersion()
        self.Find.error.connect(self.error)
        self.Find.Create.connect(self.Create)

    def show(self):
        super().show()
        self.Update_Text('A_Sentence')
        self.Update()

        if self.Key == False:
            self.Key = True
            print(self.Key)
            self.Find.start()


    def Update(self):
        self.lineEdit_PlayerVersion.setText(config.config['PlayerVersion'])

    def error(self, text):
        QtWidgets.QMessageBox.warning(self, 'error', text, QtWidgets.QMessageBox.Yes)

    def Create(self, Info_):
        Info = json.loads(Info_)
        self.N += 1

        y = 5 + 50 * (self.N - 1)

        hash_ = hash(Info_)
        self.List[hash_] = VersionCard(self.scrollAreaWidgetContents, 5, y, Info)
        self.List[hash_].See_md.connect(self.Update_Text)
        self.List[hash_].error.connect(self.error)
        self.List[hash_].change.connect(self.Change_Append)
        self.List[hash_].update.connect(self.Update)
        self.List[hash_].show()

        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(390, y + 70))

    def Update_Text(self, Tag):
        self.Update_info.terminate()
        self.Update_info.Tag = Tag
        self.Update_info.start()

    def Change(self, html):
        self.textBrowser.setHtml(html)

    def Change_Append(self,text,Move):
        self.textBrowser.append(text)
        if Move:
            self.textBrowser.moveCursor(QtWidgets.QTextBrowser.textCursor().End)
