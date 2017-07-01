# coding=utf-8

"""
    EVEModX Bootstrapper
    Usage: exefile /tools=path/to/bootstrapper.py
"""
import sys, os

import blue
import service
import logmodule

# Start client
__import__('autoexec_%s' % boot.role)

FRAMEWORK_PATH = blue.sysinfo.GetUserDocumentsDirectory() + '/EVE/EVEModX/EVEModX.zip'

def EVEModX_bootstrap():
    if os.path.isfile(FRAMEWORK_PATH):
        sys.path.append(FRAMEWORK_PATH)
        start_framework()
    else:
        install_framework()
    
def install_framework():
    import requests
    framework_info = requests.get(r'https://repo.evemodx.com/api/framework/info')
    print framework_info.json()
    # TODO: Install Framework
    
def start_framework():
    import __builtin__
    while not hasattr(__builtin__, 'sm') or sm.state != service.SERVICE_RUNNING:
        blue.pyos.synchro.SleepWallclock(1000)

    logmodule.general.Log("Initializing EVEModX...", logmodule.LGNOTICE)
    import EVEModX
    EVEModX.init()


import stackless
stackless.tasklet(EVEModX_bootstrap)().run()
