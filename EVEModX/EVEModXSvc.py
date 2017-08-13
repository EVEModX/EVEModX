# coding=utf-8

import os, os.path
import sys
import json

import blue
import logmodule
import service
import svc
import uthread

from . import settings


class EVEModXSvc(service.Service):
    __guid__ = 'svc.EVEModXSvc'
    __servicename__ = 'svc.EVEModXSvc'
    __notifyevents__ = []
    __displayname__ = 'EVEModX Core Service'

    def Run(self, *args):
        service.Service.Run(self, *args)
        sys.path.append(settings.MODS_PATH)
        self.mods = {}
        uthread.new(self.load_mods)

    def load_mods(self):
        for name in os.listdir(settings.MODS_PATH):
            # TODO: Check zip packages
            if (os.path.isdir(settings.MODS_PATH + name) and
                    os.path.isfile(settings.MODS_PATH + name + '/__init__.py') and
                    os.path.isfile(settings.MODS_PATH + name + '/info.json')):
                if name not in self.mods.keys():
                    try:
                        info = json.load(open(settings.MODS_PATH + name + '/info.json', 'r'), encoding="utf-8")
                    except:
                        logmodule.general.Log('EVEModX: Parsing info.json failed: %s' % name, logmodule.LGNOTICE)
                    if info and info.get('name') == name:
                        try:
                            module = __import__(name)
                            self.mods[name] = Mod(info, module)
                            if hasattr(module, 'EXEC_ON_START') and callable(module.EXEC_ON_START):
                                uthread.new(module.EXEC_ON_START)
                        except ImportError:
                            logmodule.general.Log('EVEModX: Importing module failed: %s' % name, logmodule.LGNOTICE)
                        except Exception as e:
                            logmodule.general.Log('EVEModX: Importing module failed: %s' % e, logmodule.LGNOTICE)


def start_service():
    svc.EVEModXSvc = EVEModXSvc
    sm.StartService('EVEModXSvc')


class Mod:
    def __init__(self, info, module):
        self.module = module
        self.display_name = info.get('display_name', info.get('name'))
        self.name = info.get('name')
        self.version = info.get('version')
        self.author = info.get('author')
        self.description = info.get('description')
