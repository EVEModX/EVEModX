# coding=utf-8

"""
    EVEModX Bootstrapper
    Usage: exefile /tools=path/to/bootstrapper.py
"""

import blue
import logmodule

# Start client
__import__('autoexec_%s' % boot.role)


def EVEModX_bootstrap():
    import sys, os

    EVEModX_path = blue.sysinfo.GetUserDocumentsDirectory() + '/EVE/EVEModX/Framework/'

    # TODO: Check EVEModX install
    
    sys.path.append(EVEModX_path)

    while True:
        blue.pyos.synchro.SleepWallclock(1000)
        import __builtin__
        if hasattr(__builtin__, 'sm') and sm.IsServiceRunning('counter'):
            logmodule.general.Log("Initializing EVEModX...", logmodule.LGNOTICE)
            import EVEModX
            EVEModX.init()
            return

logmodule.general.Log("EVEModX bootstrapper loaded, waiting for service manager...", logmodule.LGNOTICE)
import stackless
stackless.tasklet(EVEModX_bootstrap)().run()
