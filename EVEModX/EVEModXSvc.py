# coding=utf-8

import os, os.path
import sys
import json

import blue
import logmodule
import service
import svc

from . import configs

class EVEModXSvc(service.Service):
    __guid__ = 'svc.EVEModXSvc'
    __servicename__ = 'svc.EVEModXSvc'
    __notifyevents__ = []
    __displayname__ = 'EVEModX Core Service'

    def Run(self, *args):
        service.Service.Run(self, *args)
        sys.path.append(configs.MODS_PATH)
        self.mods = {}

    def load_mods(self):
        for name in os.listdir(configs.MODS_PATH):
            # TODO: Check zip packages
            if os.path.isdir(configs.MODS_PATH + name):
                if os.path.isfile(configs.MODS_PATH + name + '/__init__.py') and os.path.isfile(configs.MODS_PATH + name + '/info.json'):
                    if name not in self.mods.keys():
                        try:
                            info = json.load(open(configs.MODS_PATH + name + '/info.json', 'r'), encoding="utf-8")
                        except:
                            logmodule.general.Log('EVEModX: Parsing info.json failed: %s' % name, logmodule.LGNOTICE)
                        if info and info.get('name') == name:
                            try:
                                info['module'] =  __import__(name)
                                self.mods[name] = info
                            except ImportError:
                                logmodule.general.Log('EVEModX: Importing module failed: %s' % name, logmodule.LGNOTICE)
                            except Exception as e:
                                logmodule.general.Log('EVEModX: Importing module failed: %s' % e, logmodule.LGNOTICE)


def start_service():
    svc.EVEModXSvc = EVEModXSvc
    sm.StartService('EVEModXSvc')