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


class StatsView(object):
    views = {}

    def __init__(self):
        pass

    @classmethod
    def register(cls):
        StatsView.views[cls.name] = cls

    @classmethod
    def getView(cls, name):
        return cls.views[name]

    def populatePanel(self, panel):
        raise NotImplementedError()

    def getHeaderText(self, fit):
        raise NotImplementedError()

    def refreshPanel(self, fit):
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
from gui.builtinStatsViews import (  # noqa: E402, F401
    resourcesViewFull,
    resistancesViewFull,
    firepowerViewFull,
    miningyieldViewFull,
    capacitorViewFull,
    rechargeViewFull,
    targetingMiscViewMinimal,
    priceViewFull,
    priceViewMinimal,
    outgoingViewFull,
    outgoingViewMinimal,
)
