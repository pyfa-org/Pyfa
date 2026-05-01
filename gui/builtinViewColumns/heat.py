# =============================================================================
# 2026 Ansbiget Hild Elarik
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
import math

from gui.bitmap_loader import BitmapLoader
from eos.const import FittingModuleState
from eos.saveddata.fit import Fit
from eos.saveddata.module import Module
from gui.viewColumn import ViewColumn
from service.fit import Fit

import gui.mainFrame

class Thermodynamics():
    def __init__(self, fit):
        self.fit = fit
        self.hgm = fit.ship.getModifiedItemAttr("heatGenerationMultiplier")
        self.harm = self.calcHeatAbsorbtionRateModifier()
        self.slotfactor = self.calcSlotFactor()
        self.simTime = 600

    def getSlotPos(self, mod): # get rack position of mod, 0-7
        rack = []
        for m in self.fit.modules:
            if m.slot == mod.slot:
                rack.insert(0, m)

        for i, m in enumerate(rack):
            if m == mod:
                return i

    def calcHeatAbsorbtionRateModifier(self):
        harm = [0,0,0,0] # 0 is a dummy slot, align with mod.slot constants, 1=low, 2=med, 3=hi, 4=rig, ...

        for mod in self.fit.modules:
            if(mod.state == FittingModuleState.OVERHEATED):
                harm[mod.slot] += mod.getModifiedItemAttr("heatAbsorbtionRateModifier")

        return harm

    def calcSlotFactor(self):
        slots = self.fit.ship.getModifiedItemAttr("hiSlots") + self.fit.ship.getModifiedItemAttr("medSlots") + self.fit.ship.getModifiedItemAttr("lowSlots")
        empty = self.fit.getSlotsFree(3) + self.fit.getSlotsFree(2) + self.fit.getSlotsFree(1) # FittingSlot.HIGH doesn"t work here?
        rigslots = self.fit.getNumSlots(4)

        return (slots - empty) / (slots + rigslots)

    def calcDamageProbability(self, mod, t): # get chance the module is damaged when overheated at time t
        keys = ["", "heatAttenuationLow", "heatAttenuationMed", "heatAttenuationHi"]
        att = self.fit.ship.getModifiedItemAttr(keys[mod.slot], 0.25)
        rackheat = 1 - pow(math.e, (-t * self.hgm * self.harm[mod.slot]))
        slotpos = self.getSlotPos(mod)

        probs = []
        for m in self.fit.modules:
            if (m == mod): continue
            if m.slot == mod.slot:
                if m.state == FittingModuleState.OVERHEATED:
                    i = self.getSlotPos(m)
                    pos = abs(i - slotpos) # get rack distance to other overheated module
                    probs.append(pow(att, pos) * self.slotfactor * rackheat)

        p = 1
        for i in range(0, len(probs)):
            p *= (1 - probs[i])

        selfprob = self.slotfactor * rackheat
        res = selfprob if p == 1 else 1 - p * (1 - selfprob)

        return res

    def calcBurnCycles(self, mod): # estimates the number of cycles a module will OH before it burns out
        speed = mod.getModifiedItemAttr("speed")
        duration = mod.getModifiedItemAttr("duration")
        inc = speed / 1000 if speed else duration / 1000
        t = inc

        fp = [] # failure probabilities
        p = lastp = 0
        while(t < self.simTime):
            p = self.calcDamageProbability(mod, t)
            fp.append(p)

            if f"{p:.5f}" == f"{lastp:.5f}":
                break

            t += inc
            lastp = p

        # http://jsfiddle.net/kkspy/86/
        E = 0 # expected wait to failure
        n = math.ceil(mod.getModifiedItemAttr("hp") / mod.getModifiedItemAttr("heatDamage")) # fault tolerance
        a = [1]

        for i in range(n):
            a.append(0)

        for t, fp_t in enumerate(fp):
            E += (t + 1) * fp_t * a[n - 1]

            for k in range(n - 1, 0, -1):
                a[k] = (1 - fp_t) * a[k] + fp_t * a[k - 1]

            a[0] = (1 - fp_t) * a[0]

        for k in range(n):
            E += (t + 1 + (n - k) * (1 / fp[t])) * a[k]

        return math.floor(E)

class Heat(ViewColumn):
    name = "Heat"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.resizable = False
        self.size = 54
        self.maxsize = self.size * 2
        self.imageId = fittingView.imageList.GetImageIndex("state_overheated_small", "gui")
        self.bitmap = BitmapLoader.getBitmap("state_overheated_small", "gui")
        self.mask = wx.LIST_MASK_IMAGE

    def getText(self, mod):
        if not isinstance(mod, Module) or mod.state != FittingModuleState.OVERHEATED:
            return ""

        thermo = Thermodynamics(Fit.getInstance().getFit(self.mainFrame.getActiveFit()))
        burnCycles = thermo.calcBurnCycles(mod)
        duration = mod.getModifiedItemAttr("duration") / 1000
        speed = mod.getModifiedItemAttr("speed") / 1000
        cycleTime = duration or speed

        t = burnCycles * cycleTime
        s = t % 60
        m = (t / 60) % 60
        h = (t / 3600) % 24
        out = [f"{int(m):02d}", f"{int(s):02d}"]

        if int(h) > 0: # hours is rarely relevant, only show if it is
            out.insert(0, f"{int(h):02d}")

        return ":".join(out) # display as 00:00:00 to vertically align across slot cols consistently

    def getToolTip(self, mod):
        if isinstance(mod, Module) and mod.state == FittingModuleState.OVERHEATED:
            return "Estimated time til burnout" # TODO localize


Heat.register()
