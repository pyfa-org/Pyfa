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

import itertools


class Graph(object):
    def __init__(self, fit, function, data=None):
        self.fit = fit
        self.data = {}
        if data is not None:
            for name, d in data.items():
                self.setData(Data(name, d))

        self.function = function

    def clearData(self):
        self.data.clear()

    def setData(self, data):
        self.data[data.name] = data

    def getIterator(self):
        pointNames = []
        pointIterators = []
        for data in self.data.values():
            pointNames.append(data.name)
            pointIterators.append(data)

        return self._iterator(pointNames, pointIterators)

    def _iterator(self, pointNames, pointIterators):
        for pointValues in itertools.product(*pointIterators):
            point = {}
            for i in range(len(pointValues)):
                point[pointNames[i]] = pointValues[i]

            yield point, self.function(point)


class Data(object):
    def __init__(self, name, dataString, step=None):
        self.name = name
        self.step = step
        self.data = self.parseString(dataString)

    def parseString(self, dataString):
        if not isinstance(dataString, str):
            return Constant(dataString),

        dataList = []
        for data in dataString.split(";"):
            if isinstance(data, str) and "-" in data:
                # Dealing with a range
                dataList.append(Range(data, self.step))
            else:
                dataList.append(Constant(data))

        return dataList

    def __iter__(self):
        for data in self.data:
            for value in data:
                yield value

    def isConstant(self):
        return len(self.data) == 1 and self.data[0].isConstant()


class Constant(object):
    def __init__(self, const):
        if isinstance(const, str):
            self.value = None if const == "" else float(const)
        else:
            self.value = const

    def __iter__(self):
        yield self.value

    @staticmethod
    def isConstant():
        return True


class Range(object):
    def __init__(self, string, step):
        start, end = string.split("-")
        self.start = float(start)
        self.end = float(end)
        self.step = step

    def __iter__(self):
        current = start = self.start
        end = self.end
        step = self.step or (end - start) / 50.0
        i = 1
        while current < end:
            current = start + i * step
            i += 1
            yield current

    @staticmethod
    def isConstant():
        return False
