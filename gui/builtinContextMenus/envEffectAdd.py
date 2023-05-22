import re
from collections import OrderedDict
from itertools import chain

# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.market import Market

_t = wx.GetTranslation


class Group:

    def __init__(self):
        self.groups = OrderedDict()
        self.items = []

    def sort(self):
        self.groups = OrderedDict((k, self.groups[k]) for k in sorted(self.groups))
        for group in self.groups.values():
            group.sort()
        self.items.sort(key=lambda e: e.shortName)


class Entry:

    def __init__(self, itemID, name, shortName):
        self.itemID = itemID
        self.name = name
        self.shortName = shortName


class AddEnvironmentEffect(ContextMenuUnconditional):
    # CCP doesn't currently provide a mapping between the general Environment, and the specific environment effect
    # (which can be random when going into Abyssal space). This is how we currently define it:
    # environment type: specific type name prefix
    abyssal_mapping = {
        'caustic_toxin_weather': 47862,  # Exotic Particle Storm
        'darkness_weather': 47863,  # Dark Matter Field
        'infernal_weather': 47864,  # Plasma Firestorm
        'electric_storm_weather': 47865,  # Electrical Storm
        'xenon_gas_weather': 47866,  # Gamma-Ray Afterglow
    }

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == "projected"

    def getText(self, callingWindow, itmContext):
        return _t("Add Environmental Effect")

    def _addGroup(self, parentMenu, name):
        id = ContextMenuUnconditional.nextID()
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleSelection, menuItem)
        return menuItem

    def _addEffect(self, parentMenu, typeID, name):
        id = ContextMenuUnconditional.nextID()
        self.idmap[id] = typeID
        menuItem = wx.MenuItem(parentMenu, id, name)
        parentMenu.Bind(wx.EVT_MENU, self.handleSelection, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        self.idmap = {}
        data = self.getData()
        msw = "wxMSW" in wx.PlatformInfo

        def makeMenu(data, parentMenu):
            menu = wx.Menu()
            for group_name in data.groups:
                menuItem = self._addGroup(rootMenu if msw else parentMenu, group_name)
                subMenu = makeMenu(data.groups[group_name], menu)
                menuItem.SetSubMenu(subMenu)
                menu.Append(menuItem)
            for entry in data.items:
                menuItem = self._addEffect(rootMenu if msw else parentMenu, entry.itemID, entry.shortName)
                menu.Append(menuItem)
            menu.Bind(wx.EVT_MENU, self.handleSelection)
            return menu

        sub = makeMenu(data, rootMenu)
        return sub

    def handleSelection(self, event):
        # Skip events ids that aren't mapped

        swObj = self.idmap.get(event.Id, False)
        if not swObj:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        self.mainFrame.command.Submit(cmd.GuiAddProjectedModuleCommand(fitID, swObj))

    def getData(self):
        data = Group()
        data.groups[_t('Metaliminal Storm')] = self.getEffectBeacons(
            _t('ContextMenu|ProjectedEffectManipulation|Electrical'),
            _t('ContextMenu|ProjectedEffectManipulation|Exotic'),
            _t('ContextMenu|ProjectedEffectManipulation|Gamma'),
            _t('ContextMenu|ProjectedEffectManipulation|Plasma'),
            extra_garbage=(
                _t('ContextMenu|ProjectedEffectManipulation|Metaliminal'),
                _t('ContextMenu|ProjectedEffectManipulation|Storm'),
                _t('ContextMenu|ProjectedEffectManipulation|Matter'),
                _t('ContextMenu|ProjectedEffectManipulation|Ray'),
                _t('ContextMenu|ProjectedEffectManipulation|Firestorm')))
        data.groups[_t('Wormhole')] = self.getEffectBeacons(
            _t('ContextMenu|ProjectedEffectManipulation|Black Hole'),
            _t('ContextMenu|ProjectedEffectManipulation|Cataclysmic Variable'),
            _t('ContextMenu|ProjectedEffectManipulation|Magnetar'),
            _t('ContextMenu|ProjectedEffectManipulation|Pulsar'),
            _t('ContextMenu|ProjectedEffectManipulation|Red Giant'),
            _t('ContextMenu|ProjectedEffectManipulation|Wolf Rayet'))
        data.groups[_t('Abyssal Weather')] = self.getAbyssalWeather()
        data.groups[_t('Sansha Incursion')] = self.getEffectBeacons(
            _t('ContextMenu|ProjectedEffectManipulation|Sansha Incursion'))
        data.groups[_t('Triglavian Invasion')] = self.getInvasionBeacons()
        return data

    def getEffectBeacons(self, *groups, extra_garbage=()):
        """
        Get dictionary with system-wide effects
        """
        compacted = len(groups) <= 1
        sMkt = Market.getInstance()

        # Container for system-wide effects
        data = Group()

        # Stuff we don't want to see in names
        garbages = [
            _t('ContextMenu|ProjectedEffectManipulation|System Effects'),
            _t('ContextMenu|ProjectedEffectManipulation|Effects')]
        garbages.extend(extra_garbage)

        # Get group with all the system-wide beacons
        grp = sMkt.getGroup("Effect Beacon")

        # Cycle through them
        for beacon in sMkt.getItemsByGroup(grp):
            # Check if it belongs to any valid group
            for group in groups:
                # Check beginning of the name only
                if re.search(group, beacon.name):
                    # Get full beacon name
                    beaconname = beacon.name
                    for garbage in garbages:
                        beaconname = re.sub(garbage, "", beaconname)
                    beaconname = re.sub(" {2,}", " ", beaconname).strip()
                    # Get short name
                    shortname = re.sub(group, "", beacon.name)
                    for garbage in garbages:
                        shortname = re.sub(garbage, "", shortname)
                    shortname = re.sub(" {2,}", " ", shortname).strip()
                    # Get group name
                    groupname = group
                    for garbage in garbages:
                        groupname = re.sub(garbage, "", groupname)
                    groupname = re.sub(" {2,}", " ", groupname).strip()
                    # Add stuff to dictionary
                    if compacted:
                        container = data.items
                    else:
                        container = data.groups.setdefault(groupname, Group()).items
                    container.append(Entry(beacon.ID, beaconname, shortname))
                    # Break loop on 1st result
                    break
        data.sort()
        return data

    def getAbyssalWeather(self):
        sMkt = Market.getInstance()
        data = Group()

        environments = {x.ID: x for x in sMkt.getGroup("Abyssal Environment").items}
        items = chain(
                sMkt.getGroup("MassiveEnvironments").items,
                sMkt.getGroup("Non-Interactable Object").items)
        for beacon in items:
            if not beacon.isType('projected'):
                continue
            type = self.__class__.abyssal_mapping.get(beacon.name[0:-2], None)
            type = environments.get(type, None)
            if type is None:
                continue
            subdata = data.groups.setdefault(type.name, Group())
            display_name = "{} {}".format(type.name, beacon.name[-1:])
            subdata.items.append(Entry(beacon.ID, display_name, display_name))
        data.sort()

        # Localized abyssal hazards
        items = sMkt.getGroup("Abyssal Hazards").items
        if items:
            subdata = data.groups.setdefault(_t('Localized'), Group())
            for beacon in sMkt.getGroup("Abyssal Hazards").items:
                if not beacon.isType('projected'):
                    continue
                groups = (_t('Bioluminescence'), _t('Tachyon'), _t('Filament'))
                for group in groups:
                    if re.search(group, beacon.customName):
                        key = group
                        break
                else:
                    continue

                subsubdata = subdata.groups.setdefault(key, Group())
                subsubdata.items.append(Entry(beacon.ID, beacon.customName, beacon.customName))
            subdata.sort()

        # PVP weather
        data.items.append(Entry(49766, _t('PvP Weather'), _t('PvP Weather')))

        return data

    def getDestructibleBeacons(self):
        data = Group()
        sMkt = Market.getInstance()
        for item in sMkt.getItemsByGroup(sMkt.getGroup('Destructible Effect Beacon')):
            if not item.isType('projected'):
                continue
            data.items.append(Entry(item.ID, item.name, item.name))
        data.sort()
        return data

    def getInvasionBeacons(self):
        data = self.getDestructibleBeacons()
        # Turnur weather
        item = Market.getInstance().getItem(74002)
        data.items.append(Entry(item.ID, item.name, item.name))
        return data


AddEnvironmentEffect.register()
