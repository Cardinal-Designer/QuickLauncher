# -*- coding: utf-8 -*-
import requests,os,json
from PySide2 import QtCore


class jsdelivr():
    def __init__(self, package,error):
        self.base = 'https://cdn.jsdelivr.net/gh/Cardinal-Designer/PackageCube/'
        self.root = self.base + package
        self.download = 'https://cdn.jsdelivr.net/gh/'
        self.download_url = "https://cdn.jsdelivr.net/gh/Cardinal-Designer/" + package
        self.DownloadUnit = Download_Unit(package)
        self.DownloadUnit.error.connect(error)

    def tags(self):
        try:
            return json.loads(requests.get(self.root + '/' + 'Origin.json',timeout = 3).text)["versions"]
        except:
            return ValueError

    def version(self,Tag):
        try:
            return json.loads(requests.get(self.root + '/' + Tag +'.json',timeout = 3).text)
        except:
            return ValueError

class Download_Unit(QtCore.QThread):
    end = QtCore.Signal()
    error = QtCore.Signal(str)
    def __init__(self,package):
        super().__init__()
        self.download_url = "https://cdn.jsdelivr.net/gh/Cardinal-Designer/" + package
        self.key = False

    def PackDownload(self, Object, Tag, path, callback=None):
        if self.key:
            self.error.emit("心急吃不了热豆腐！")
            return
        self.Object = Object
        self.Tag = Tag
        self.path = path
        self.callback = callback
        self.start()

    def run(self):
        self.key = True
        Pass_directory = [".idea"]

        work = self.Object["files"]
        if os.name == 'nt':
            Replace = '\\'
        else:
            Replace = '/'

        def find(root, w):
            for p in w:

                Path = root + '/' + p["name"]

                if p["type"] == "directory":
                    if p["name"] in Pass_directory:
                        continue

                    try:
                        os.makedirs(self.path + Path.replace('/', Replace))
                    except:
                        pass

                    find(Path, p["files"])
                if p["type"] == "file":
                    url = self.download_url + "@" + self.Tag + Path
                    if not self.callback == None:
                        self.callback(url)

                    with open(self.path + Path.replace('/', Replace), 'wb+') as f:
                        req = requests.get(url).content
                        f.write(req)

        find('', work)
        self.key = False
        self.end.emit()
