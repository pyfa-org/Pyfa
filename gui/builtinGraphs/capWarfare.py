#===============================================================================
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
#===============================================================================

from gui.graph import Graph
import service
from gui.bitmapLoader import BitmapLoader
#from eos.graph.fitDps import FitDpsGraph as FitDps
from eos.graph import Data
import gui.mainFrame
from gnosis.simulations.capacitor import Capacitor

class capWarfareGraph(Graph):
    '''
    propertyAttributeMap = {"angle": "maxVelocity",
                            "distance": "maxRange",
                            "signatureRadius": "signatureRadius",
                            "velocity": "maxVelocity"}

    propertyLabelMap = {"angle": "Target Angle (degrees)",
                        "distance": "Distance to Target (km)",
                        "signatureRadius": "Target Signature Radius (m)",
                        "velocity": "Target Velocity (m/s)"}

    defaults = FitDps.defaults.copy()
    '''

    def __init__(self):
        Graph.__init__(self)
        # self.defaults["time"] = "0-300"
        self.name = "Capacitor Warfare"
        self.capWarfare = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getFields(self):
        #return self.defaults
        return None

    def getLabels(self):
        #return self.propertyLabelMap
        return None

    def getIcons(self):
        '''
        icons = {}
        sAttr = service.Attribute.getInstance()
        for key, attrName in self.propertyAttributeMap.iteritems():
            iconFile = sAttr.getAttributeInfo(attrName).icon.iconFile
            bitmap = BitmapLoader.getBitmap(iconFile, "icons")
            if bitmap:
                icons[key] = bitmap

        return icons
        '''
        return None

    def getPoints(self, fit, fields):
        capacitor_amount = fit.ship.getModifiedItemAttr("capacitorCapacity")
        capacitor_recharge = fit.ship.getModifiedItemAttr("rechargeRate")
        module_list = []

        for module in fit.modules:
            if module.getModifiedItemAttr("capacitorNeed") and getattr(module, 'state', None) == 1:
                capacitor_need = module.getModifiedItemAttr("capacitorNeed")*-1 # Turn drains into negative and boosts to positive
                duration = module.getModifiedItemAttr("duration")
                charges = getattr(module,'numCharges', None)
                reload_time_one = module.getModifiedItemAttr("reloadTime")
                reload_time_two = getattr(module, 'reloadTime', None)
                reactivation_delay = module.getModifiedItemAttr("moduleReactivationDelay")

                reload_time = max(reload_time_one, reload_time_two, reactivation_delay, 0)

                if reload_time == 0 or reload_time == None:
                    reload_time = False

                if charges == 0 or charges == None:
                    if reload_time:
                        # We have a reload time but no charges, so lets give it 1 so it can count down properly.
                        # Most likely comes from a module with a reactivation delay.
                        charges = 1
                    else:
                        charges = False

                if capacitor_need:
                    module_list.append(
                        {
                            'Amount': capacitor_need,
                            'CycleTime': duration,
                            'Charges': charges,
                            'ReloadTime': reload_time,
                        }
                    )

        test = fit.projectedModules
        '''
        for projected_ship in fit.victimOf:
            for projected_ship.source_fit.
            fit
        '''

        return_matrix = Capacitor.capacitor_time_simulator(module_list, capacitor_amount, capacitor_recharge)

        x = []
        y = []
        for tick in return_matrix['Cached Runs']:
            x.append(tick['Current Time']/1000) # Divide by 1000 to give seconds
            y.append(tick['Capacitor Percentage']*100)

        return x, y

capWarfareGraph.register()
