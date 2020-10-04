# -*- coding:utf-8 -*-
from Environment import root,dir_mix
import json
class ConfigManager():
    def __init__(self):
        self.config = {
            'PlayerVersion':"",
        }

        try:
            with open(dir_mix(root, 'QuickLauncher', 'config.json'), 'r+') as f:
                content = json.loads(f.read())
                self.config = content
        except:
            with open(dir_mix(root, 'QuickLauncher','config.json'),'w+') as f:
                f.write(json.dumps(self.config))

    def update(self):
        try:
            with open(dir_mix(root, 'QuickLauncher','config.json'),'w+') as f:
                f.write(json.dumps(self.config))
        except:
            pass

config = ConfigManager()