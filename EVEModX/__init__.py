# coding=utf-8

import svc

from . import EVEModXSvc, ManagerWnd

def init():
    EVEModXSvc.start_service()
    ManagerWnd.RegisterInNeocom()