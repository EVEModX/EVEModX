# coding=utf-8

import service
import svc

class EVEModXSvc(service.Service):
    __guid__ = 'svc.EVEModXSvc'
    __servicename__ = 'svc.EVEModXSvc'
    __notifyevents__ = []
    __displayname__ = 'EVEModX Core Service'

    def Run(self, *args):
        service.Service.Run(self, *args)

def start_service():
    svc.EVEModXSvc = EVEModXSvc
    sm.StartService('EVEModXSvc')