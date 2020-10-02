import requests,os,json


class jsdelivr():
    def __init__(self, package):
        self.base = 'https://cdn.jsdelivr.net/gh/Cardinal-Designer/PackageCube/'
        self.root = self.base + package
        self.download = 'https://cdn.jsdelivr.net/gh/'
        self.download_url = "https://cdn.jsdelivr.net/gh/Cardinal-Designer/" + package

    def tags(self):
        try:
            return json.loads(requests.get(self.root + '/' + 'Origin.json').text)["versions"]
        except:
            return ValueError

    def version(self,Tag):
        try:
            return json.loads(requests.get(self.root + '/' + Tag +'.json').text)
        except:
            pass

    def PackDownload(self, Object, Tag, path, callback=None):
        Pass_directory = [".idea"]

        work = Object["files"]
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
                        os.makedirs(path + Path.replace('/', Replace))
                    except:
                        pass

                    find(Path, p["files"])
                if p["type"] == "file":
                    url = self.download_url + "@" + Tag + Path
                    if not callback == None:
                        callback(url)

                    with open(path + Path.replace('/', Replace), 'wb+') as f:
                        req = requests.get(url).content
                        f.write(req)

        find('', work)
