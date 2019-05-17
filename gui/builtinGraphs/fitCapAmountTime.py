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


import gui.mainFrame
from eos.graph.fitCapAmountTime import FitCapAmountTimeGraph as EosGraph
from gui.graph import Graph, XDef, YDef


class FitCapAmountTimeGraph(Graph):

    name = 'Cap Amount vs Time'

    def __init__(self):
        self.eosGraph = EosGraph()
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    @property
    def xDef(self):
        return XDef(handle='time', inputDefault='0-300', inputLabel='Time (seconds)', inputIconID=1392, axisLabel='Time, s')

    @property
    def yDefs(self):
        return [YDef(handle='capAmount', switchLabel='Cap amount', axisLabel='Cap amount, GJ')]

    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        xRange = self.parseRange(xRange)
        return self.eosGraph.getPlotPoints(fit, extraData, xRange, xAmount)


FitCapAmountTimeGraph.register()
