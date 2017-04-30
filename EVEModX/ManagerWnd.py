# coding=utf-8

import carbonui.const as uiconst
import const
import uicontrols
from carbonui.util.bunch import Bunch
from carbonui.primitives.container import Container
from carbonui.control.scrollContainer import ScrollContainer
from eve.client.script.ui.control.themeColored import LineThemeColored

from . import configs

class EVEModXWnd(uicontrols.Window):
    default_caption = 'EVEModX Manager'
    default_minSize = (300, 200)
    default_windowID = 'EVEModX'
    default_iconNum = 'res:/ui/texture/WindowIcons/settings.png'
    def ApplyAttributes(self, attributes):
        uicontrols.Window.ApplyAttributes(self, attributes)
        self.SetTopparentHeight(64)
        self.SetWndIcon(self.default_iconNum)
        uicontrols.WndCaptionLabel(text='EVEModX Manager', parent=self.sr.topParent, align=uiconst.RELATIVE, subcaption='Version: ' + configs.VERSION)
        self.modScroll = ScrollContainer(name='modScroll', parent=self.sr.main, align=uiconst.TOALL, padding=const.defaultPadding, showUnderlay=True)
        sm.GetService('EVEModXSvc').load_mods()
        for mod_name, mod_data in sorted(sm.GetService('EVEModXSvc').mods.iteritems()):
            ModEntry(parent=self.modScroll, data=mod_data)

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


class ModEntry(uicontrols.ContainerAutoSize):
    default_name = 'ModEntry'
    default_align = uiconst.TOTOP
    PADDING_GENERIC = const.defaultPadding * 2

    def ApplyAttributes(self, attributes):
        uicontrols.ContainerAutoSize.ApplyAttributes(self, attributes)
        data = attributes.data
        text = r'<fontsize=18><b>%s</b></fontsize> %s %s, by %s<br><br>%s' % (data.get('display_name', data.get('name')), data.get('name'), data.get('version'), data.get('author'), data.get('description'))
        uicontrols.EveLabelMedium(text=text, parent=self, align=uiconst.TOTOP, padding=const.defaultPadding)
        self.buttonCont = Container(name='buttonCont', parent=self, align=uiconst.TOTOP, height=18, padTop=4)
        for button in data['module'].BUTTONS:
            uicontrols.Button(parent=self.buttonCont, align=uiconst.TORIGHT, label=button[0], func=button[1], args=button[2], padRight=4, hint=button[3])
        LineThemeColored(parent=self, align=uiconst.TOTOP, padTop=4)
