# coding=utf-8

import os, os.path

import blue
import logmodule
import service
import svc

class EVEModXSvc(service.Service):
    __guid__ = 'svc.EVEModXSvc'
    __servicename__ = 'svc.EVEModXSvc'
    __notifyevents__ = []
    __displayname__ = 'EVEModX Core Service'

    def Run(self, *args):
        service.Service.Run(self, *args)
        self.mods = {}

    def load_mods(self):
        EVEModX_Modules_path = blue.sysinfo.GetUserDocumentsDirectory() + '/EVE/EVEModX/Mods/'
        mod_names = []
        # TODO: Check zip packages
        for name in os.listdir(EVEModX_Modules_path):
            if name not in self.mods.keys():
                if os.path.isfile(EVEModX_Modules_path + name + '/__init__.py'):
                    mod_names.append(name)
        for mod_name in mod_names:
            try:
                self.mods[mod_name] = __import__(mod_name)
            except:
                logmodule.general.Log('EVEModX: Import %s Error' % mod_name, logmodule.LGNOTICE)



def start_service():
    svc.EVEModXSvc = EVEModXSvc
    sm.StartService('EVEModXSvc')