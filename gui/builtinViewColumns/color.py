# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx

from graphs.wrapper import SourceWrapper
from gui.viewColumn import ViewColumn


class LineColor(ViewColumn):

    name = 'Color'

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 16
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_TEXT

    def getText(self, stuff):
        if isinstance(stuff, SourceWrapper):
            return ''
        return ''

    def getToolTip(self, stuff):
        if isinstance(stuff, SourceWrapper):
            return 'Change line color'
        return ''


LineColor.register()
