# coding=utf-8

import svc
import blue

from . import EVEModXSvc, ManagerWnd


def init():
    EVEModXSvc.start_service()
    ManagerWnd.RegisterInNeocom()
