#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import eos.db

class Market():
    instance = None
    FORCED_SHIPS = ("Freiki", "Mimir", "Utu", "Adrestia", "Ibis", "Impairor", "Velator", "Reaper")
    FORCED_GROUPS = ("Rookie ship",)
    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = Market()

        return cls.instance

    def getItems(self, id):
        """
        Get the items contained in the marketGroup with the passed id.
        Returns a list, where each element is a tuple container:
        the id, the name, the icon
        """

        items = []
        group = eos.db.getMarketGroup(id)
        for item in group.items:
            icon = item.icon.iconFile if item.icon else ""
            items.append((item.ID, item.name, icon))

        return items

    def getChildren(self, id):
        """
        Get the children of the group or marketGroup with the passed id.
        Returns a list, where each element is a tuple containing:
        the id, the name, the icon, wether the group has more children.
        """

        group = eos.db.getMarketGroup(id, eager="icon")
        children = []
        for child in group.children:
            icon = child.icon.iconFile if child.icon else ""
            children.append((child.ID, child.name, icon, not child.hasTypes))

        return children

    def getShipRoot(self):
        cat = eos.db.getCategory(6)
        root = []
        for grp in cat.groups:
            if grp.published == 1 or grp.name in self.FORCED_GROUPS:
                root.append((grp.ID, grp.name))

        return root

    def getShipList(self, id):
        ships = []
        grp = eos.db.getGroup(id, eager=("items"))
        for item in grp.items:
            if item.published == 1 or item.name in self.FORCED_SHIPS:
                ships.append((item.ID, item.name, item.race))

        return ships

    def searchShips(self, name):
        results = eos.db.searchItems(name)
        ships = []
        for item in results:
            if item.category.name == "Ship" and (item.published == 1 or item.name in self.FORCED_SHIPS):
                ships.append((item.ID, item.name, item.race))

        return ships

    def getMarketRoot(self):
        """
        Get the root of the market tree.
        Returns a list, where each element is a tuple containing:
        the ID, the name and the icon of the group
        """

        marketGroups = (9, #Modules
                        1111, #Rigs
                        157, #Drones
                        11, #Ammo
                        1112, #Subsystems
                        24) #Implants & Boosters
        root = []
        for id in marketGroups:
            mg = eos.db.getMarketGroup(id, eager="icon")
            root.append((id, mg.name, mg.icon.iconFile if mg.icon else ""))

        return root
