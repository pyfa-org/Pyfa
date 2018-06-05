from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from service.market import Market
from service.fit import Fit
from service.settings import ContextMenuSettings
from itertools import chain
import re


class WhProjector(ContextMenu):

    # CCP doesn't currently provide a mapping between the general Environment, and the specific environment effect
    # (which can be random when going into Abyssal space). This is how we currently define it:
    # environment type: specific type name previx
    abyssal_mapping = {
        'caustic_toxin_weather': 47862,  # Exotic Particle Storm
        'darkness_weather': 47863,  # Dark Matter Field
        'infernal_weather': 47864,  # Plasma Firestorm
        'electric_storm_weather': 47865,  # Electrical Storm
        'xenon_gas_weather': 47866,  # Gamma-Ray Afterglow
    }

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('whProjector'):
            return False

        return srcContext == "projected"

    def getText(self, itmContext, selection):
        return "Add Environmental Effect"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False

        # Wormholes

        self.idmap = {}
        sub = wx.Menu()

        wormhole_item = wx.MenuItem(sub, wx.ID_ANY, "Wormhole")
        wormhole_menu = wx.Menu()
        wormhole_item.SetSubMenu(wormhole_menu)
        sub.Append(wormhole_item)

        effdata = self.getEffectBeacons()
        self.buildMenu(effdata, wormhole_menu, rootMenu, msw)

        # Incursions

        effdata = self.getEffectBeacons(incursions=True)
        self.buildMenu(effdata, sub, rootMenu, msw)

        # Abyssal Weather

        abyssal_item = wx.MenuItem(sub, wx.ID_ANY, "Abyssal Weather")
        abyssal_menu = wx.Menu()
        abyssal_item.SetSubMenu(abyssal_menu)
        sub.Append(abyssal_item)

        effdata = self.getAbyssalWeather()
        self.buildMenu(effdata, abyssal_menu, rootMenu, msw)

        # Localized Weather

        local_item = wx.MenuItem(sub, wx.ID_ANY, "Localized")
        local_menu = wx.Menu()
        local_item.SetSubMenu(local_menu)
        sub.Append(local_item)

        effdata = self.getLocalizedEnvironments()
        self.buildMenu(effdata, local_menu, rootMenu, msw)

        return sub

    def handleSelection(self, event):
        # Skip events ids that aren't mapped

        swObj, swName = self.idmap.get(event.Id, (False, False))
        if not swObj and not swName:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.project(fitID, swObj)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def buildMenu(self, data, local_menu, rootMenu, msw):
        for swType in sorted(data):
            subItem = wx.MenuItem(local_menu, wx.ID_ANY, swType)
            grandSub = wx.Menu()
            subItem.SetSubMenu(grandSub)
            local_menu.Append(subItem)

            for swData in sorted(data[swType], key=lambda tpl: tpl[2]):
                wxid = ContextMenu.nextID()
                swObj, swName, swClass = swData
                self.idmap[wxid] = (swObj, swName)
                grandSubItem = wx.MenuItem(grandSub, wxid, swClass)
                if msw:
                    rootMenu.Bind(wx.EVT_MENU, self.handleSelection, grandSubItem)
                else:
                    grandSub.Bind(wx.EVT_MENU, self.handleSelection, grandSubItem)
                grandSub.Append(grandSubItem)

    def getEffectBeacons(self, incursions=False):
        """
        Get dictionary with system-wide effects
        """
        sMkt = Market.getInstance()

        # todo: rework this
        # Container for system-wide effects
        effects = {}

        # Expressions for matching when detecting effects we're looking for
        if incursions:
            validgroups = ("Incursion ship attributes effects",)
        else:
            validgroups = ("Black Hole Effect Beacon",
                           "Cataclysmic Variable Effect Beacon",
                           "Magnetar Effect Beacon",
                           "Pulsar Effect Beacon",
                           "Red Giant Beacon",
                           "Wolf Rayet Effect Beacon")

        # Stuff we don't want to see in names
        garbages = ("Effect", "Beacon", "ship attributes effects")

        # Get group with all the system-wide beacons
        grp = sMkt.getGroup("Effect Beacon")

        # Cycle through them
        for beacon in sMkt.getItemsByGroup(grp):
            # Check if it belongs to any valid group
            for group in validgroups:
                # Check beginning of the name only
                if re.match(group, beacon.name):
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
                    if groupname not in effects:
                        effects[groupname] = set()
                    effects[groupname].add((beacon, beaconname, shortname))
                    # Break loop on 1st result
                    break

        return effects

    def getAbyssalWeather(self):
        sMkt = Market.getInstance()

        environments = {x.ID: x for x in sMkt.getGroup("Abyssal Environment").items}
        items = chain(sMkt.getGroup("MassiveEnvironments").items, sMkt.getGroup("Non-Interactable Object").items)

        effects = {}

        for beacon in items:
            if not beacon.isType('projected'):
                continue

            type = self.__class__.abyssal_mapping.get(beacon.name[0:-2], None)
            type = environments.get(type, None)
            if type is None:
                continue

            if type.name not in effects:
                effects[type.name] = set()

            display_name = "{} {}".format(type.name, beacon.name[-1:])
            effects[type.name].add((beacon, display_name, display_name))

        return effects

    def getLocalizedEnvironments(self):
        sMkt = Market.getInstance()

        grp = sMkt.getGroup("Abyssal Hazards")

        effects = dict()

        for beacon in grp.items:
            if not beacon.isType('projected'):
                continue
            # Localized effects, currently, have a name like "(size) (type) Cloud"
            # Until this inevitably changes, do a simple split
            name_parts = beacon.name.split(" ")

            key = name_parts[1].strip()
            if key not in effects:
                effects[key] = set()

            effects[key].add((beacon, beacon.name, beacon.name))

        return effects


WhProjector.register()
