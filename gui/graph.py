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


class Graph(object):
    views = []

    @classmethod
    def register(cls):
        Graph.views.append(cls)

    def __init__(self):
        pass

    def getName(self):
        raise NotImplementedError()

    def allowTargetFits(self):
        return False

    def allowTargetResists(self):
        return False

    def getControlPanel(self, parent, onFieldChanged):
        return None

    def getFields(self):
        return None

    def getLabels(self):
        return None

    def getIcons(self):
        return None

    def getVariableLabels(self, values):
        return None

    def getPoint(self, values, point, fit=None, tgt=None):
        return None

    def getPoints(self, values, fit=None, tgt=None):
        raise NotImplementedError()

# noinspection PyUnresolvedReferences
#from gui.builtinGraphs import fitDps  # noqa: E402, F401
from gui.builtinGraphs import *