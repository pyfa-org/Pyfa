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


from collections import OrderedDict

import gui.mainFrame
from eos.graph.fitShieldAmountVsTime import FitShieldAmountVsTimeGraph as EosGraph
from .base import FitGraph, XDef, YDef


class FitShieldAmountVsTimeGraph(FitGraph):

    name = 'Shield Amount vs Time'

    def __init__(self):
        super().__init__()
        self.eosGraph = EosGraph()
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    @property
    def xDef(self):
        return XDef(inputDefault='0-300', inputLabel='Time (seconds)', inputIconID=1392, axisLabel='Time, s')

    @property
    def yDefs(self):
        axisLabel = 'Shield amount, {}'.format('EHP' if self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective else 'HP')
        return OrderedDict([('shieldAmount', YDef(switchLabel='Shield amount', axisLabel=axisLabel, eosGraph='eosGraph'))])

    def redrawOnEffectiveChange(self):
        return True


FitShieldAmountVsTimeGraph.register()
