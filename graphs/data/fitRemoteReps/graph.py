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


from graphs.data.base import FitGraph, XDef, YDef, Input


class FitRemoteRepsGraph(FitGraph):

    # UI stuff
    internalName = 'remoteRepsGraph'
    name = 'Remote Repairs'
    xDefs = [
        XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km')),
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's'))]
    yDefs = [
        YDef(handle='rps', unit='HP/s', label='Repair speed'),
        YDef(handle='total', unit='HP', label='Total repaired')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=None, defaultRange=(0, 80), secondaryTooltip='When set, uses repairing ship\'s exact RR stats at a given time\nWhen not set, uses attacker\'s RR stats as shown in stats panel of main window'),
        Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=None, defaultRange=(0, 100), mainTooltip='Distance between the repairing ship and the target, as seen in overview (surface-to-surface)', secondaryTooltip='Distance between the repairing ship and the target, as seen in overview (surface-to-surface)')]
    srcExtraCols = ()

    # Calculation stuff
    _normalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v * 1000}
    _limiters = {'time': lambda src, tgt: (0, 2500)}
    _getters = {}
    _denormalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v / 1000}
