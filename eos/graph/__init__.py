# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================


from abc import ABCMeta, abstractmethod


class Graph(metaclass=ABCMeta):

    def __init__(self):
        self.cache = {}

    @abstractmethod
    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        raise NotImplementedError

    def getYForX(self, fit, extraData, x):
        raise NotImplementedError

    def _xIter(self, xRange, xAmount):
        rangeStart, rangeEnd = sorted(xRange)
        # Amount is amount of ranges between points here, not amount of points
        step = (rangeEnd - rangeStart) / xAmount
        if step == 0:
            yield xRange[0]
        else:
            current = rangeStart
            # Take extra half step to make sure end of range is always included
            # despite any possible float errors
            while current <= (rangeEnd + step / 2):
                yield current
                current += step

    def clearCache(self, fitID):
        self.cache.clear()
