# coding=utf-8

import carbonui.const as uiconst
from eve.client.script.ui.control.eveWindow import Window

class EVEModXWnd(Window):
    default_caption = 'EVEModX Manager'
    default_minSize = (300, 200)
    default_windowID = 'EVEModX'
    default_iconNum = 'res:/ui/texture/WindowIcons/settings.png'
    def ApplyAttributes(self, attributes):
        Window.ApplyAttributes(self, attributes)

def OpenEVEModXWindow():
    EVEModXWnd.Open()

OpenEVEModXWindow.nameString = u"EVEModX"
OpenEVEModXWindow.descriptionString = u"Open EVEModX Manager"

def RegisterInNeocom():
    from eve.client.script.ui.shared.neocom.neocom import neocomCommon, neocomSvc
    from carbonui.services.command import CommandService, CommandMapping
    import util

    def MonkeyPatchForCmdSvc(func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            ret.append(CommandMapping(OpenEVEModXWindow, (uiconst.VK_CONTROL, uiconst.VK_MENU, uiconst.VK_SHIFT, uiconst.VK_N), isLocked=True))
            return ret
        return wrapper

    CommandService.SetDefaultShortcutMappingCORE = MonkeyPatchForCmdSvc(CommandService.SetDefaultShortcutMappingCORE)
    neocomSvc.BTNDATARAW_BY_ID['EVEModXWindow'] = neocomSvc.BtnDataRaw(cmdName='OpenEVEModXWindow', wndCls=EVEModXWnd)
    neocomSvc.RAWDATA_EVEMENU.append(util.KeyVal(label='EVEModX', btnType=neocomCommon.BTNTYPE_CMD, id='EVEModXWindow', children=None))
