# noinspection PyPackageRequirements
import wx
from logbook import Logger
# noinspection PyPackageRequirements

import gui.globalEvents as GE
import gui.mainFrame
from gui.builtinShipBrowser.categoryItem import CategoryItem
from gui.builtinShipBrowser.fitItem import FitItem
from gui.builtinShipBrowser.shipItem import ShipItem
from service.fit import Fit
from service.market import Market

import gui.builtinShipBrowser.events as events
from gui.builtinShipBrowser.pfWidgetContainer import PFWidgetsContainer
from gui.builtinShipBrowser.navigationPanel import NavigationPanel
from gui.builtinShipBrowser.raceSelector import RaceSelector
from gui.builtinShipBrowser.pfStaticText import PFStaticText

pyfalog = Logger(__name__)


class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=0)

        self._lastWidth = 0
        self._activeStage = 1
        self._lastStage = 0
        self.browseHist = []
        self.lastStage = (0, 0)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.categoryList = []
        self.categoryFitCache = {}

        self._stage1Data = -1
        self._stage2Data = -1
        self._stage3Data = -1
        self._stage3ShipName = ""
        self.fitIDMustEditName = -1
        self.filterShipsWithNoFits = False
        self.recentFits = False

        self.racesFilter = {}

        self.showRacesFilterInStage2Only = True

        for race in self.RACE_ORDER:
            if race:
                self.racesFilter[race] = False

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.navpanel = NavigationPanel(self)
        mainSizer.Add(self.navpanel, 0, wx.EXPAND)

        self.lpane = PFWidgetsContainer(self)
        layout = wx.HORIZONTAL

        self.raceselect = RaceSelector(self, layout=layout, animate=False)
        container = wx.BoxSizer(wx.VERTICAL if layout == wx.HORIZONTAL else wx.HORIZONTAL)

        if layout == wx.HORIZONTAL:
            container.Add(self.lpane, 1, wx.EXPAND)
            container.Add(self.raceselect, 0, wx.EXPAND)
        else:
            container.Add(self.raceselect, 0, wx.EXPAND)
            container.Add(self.lpane, 1, wx.EXPAND)

        mainSizer.Add(container, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show()

        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)
        self.Bind(events.EVT_SB_STAGE2_SEL, self.stage2)
        self.Bind(events.EVT_SB_STAGE1_SEL, self.stage1)
        self.Bind(events.EVT_SB_STAGE3_SEL, self.stage3)
        self.Bind(events.EVT_SB_SEARCH_SEL, self.searchStage)
        self.Bind(events.EVT_SB_IMPORT_SEL, self.importStage)

        self.mainFrame.Bind(GE.FIT_CHANGED, self.RefreshList)

        self.stage1(None)

    def GetBrowserContainer(self):
        return self.lpane

    def RefreshContent(self):
        stage = self.GetActiveStage()
        if stage == 1:
            return
        stageData = self.GetStageData(stage)
        self.navpanel.gotoStage(stage, stageData)

    def RefreshList(self, event):
        stage = self.GetActiveStage()

        if stage in (3, 4, 5):
            self.lpane.RefreshList(True)
        event.Skip()

    def SizeRefreshList(self, event):
        self.Layout()
        self.lpane.Layout()
        self.lpane.RefreshList(True)
        event.Skip()

    def __del__(self):
        pass

    def GetActiveStage(self):
        return self._activeStage

    def GetLastStage(self):
        return self._lastStage

    def GetStageData(self, stage):
        if stage == 1:
            return self._stage1Data
        if stage == 2:
            return self._stage2Data
        if stage == 3:
            return self._stage3Data
        if stage == 4:
            return self.navpanel.lastSearch
        return -1

    def GetStage3ShipName(self):
        return self._stage3ShipName

    def ToggleRacesFilter(self, race):
        if self.racesFilter[race]:
            self.racesFilter[race] = False
        else:
            self.racesFilter[race] = True

    def GetRaceFilterState(self, race):
        return self.racesFilter[race]

    def stage1(self, event):
        self.navpanel.ToggleRecentShips(False, False)
        self._lastStage = self._activeStage
        self._activeStage = 1
        self.lastdata = 0
        self.browseHist = [(1, 0)]

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        sMkt = Market.getInstance()
        sFit = Fit.getInstance()
        self.lpane.ShowLoading(False)

        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()

        pyfalog.debug("Populate ship category list.")
        if len(self.categoryList) == 0:
            # set cache of category list
            self.categoryList = list(sMkt.getShipRoot())
            self.categoryList.sort(key=lambda _ship: _ship.name)

            # set map & cache of fittings per category
            for cat in self.categoryList:
                itemIDs = [x.ID for x in cat.items]
                num = sFit.countFitsWithShip(itemIDs)
                self.categoryFitCache[cat.ID] = num > 0

        for ship in self.categoryList:
            if self.filterShipsWithNoFits and not self.categoryFitCache[ship.ID]:
                continue
            else:
                self.lpane.AddWidget(CategoryItem(self.lpane, ship.ID, (ship.name, 0)))

        self.navpanel.ShowSwitchEmptyGroupsButton(True)

        self.lpane.RefreshList()
        self.lpane.Thaw()
        self.raceselect.RebuildRaces(self.RACE_ORDER)
        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

    RACE_ORDER = [
        "amarr", "caldari", "gallente", "minmatar",
        "sisters", "ore",
        "serpentis", "angel", "blood", "sansha", "guristas", "mordu",
        "jove", "upwell", None
    ]

    def raceNameKey(self, ship):
        return self.RACE_ORDER.index(ship.race), ship.name

    def stage2Callback(self, data):
        if self.GetActiveStage() != 2:
            return
        self.navpanel.ToggleRecentShips(False, False)

        categoryID = self._stage2Data
        ships = list(data[1])
        sFit = Fit.getInstance()

        ships.sort(key=self.raceNameKey)
        racesList = []
        subRacesFilter = {}
        t_fits = 0  # total number of fits in this category

        for ship in ships:
            if ship.race:
                if ship.race not in racesList:
                    racesList.append(ship.race)

        for race, state in self.racesFilter.iteritems():
            if race in racesList:
                subRacesFilter[race] = self.racesFilter[race]

        override = True
        for race, state in subRacesFilter.iteritems():
            if state:
                override = False
                break

        for ship in ships:
            fits = sFit.countFitsWithShip(ship.ID)
            t_fits += fits
            filter_ = subRacesFilter[ship.race] if ship.race else True
            if override:
                filter_ = True

            shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

            if self.filterShipsWithNoFits:
                if fits > 0:
                    if filter_:
                        self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, shipTrait, fits), ship.race))
            else:
                if filter_:
                    self.lpane.AddWidget(ShipItem(self.lpane, ship.ID, (ship.name, shipTrait, fits), ship.race))

        self.raceselect.RebuildRaces(racesList)

        # refresh category cache
        if t_fits == 0:
            self.categoryFitCache[categoryID] = False
        else:
            self.categoryFitCache[categoryID] = True

        self.lpane.ShowLoading(False)

        self.lpane.RefreshList()

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(True)
            self.Layout()

    def stage2(self, event):
        # back = event.back
        # if not back:
        #    self.browseHist.append( (1,0) )

        self._lastStage = self._activeStage
        self._activeStage = 2
        categoryID = event.categoryID
        self.lastdata = categoryID

        self.lpane.ShowLoading()

        self.lpane.RemoveAllChildren()

        sMkt = Market.getInstance()
        sMkt.getShipListDelayed(categoryID, self.stage2Callback)

        self._stage2Data = categoryID

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(True)

    @staticmethod
    def nameKey(info):
        return info[1]

    def stage3(self, event):
        self.navpanel.ToggleRecentShips(False, False)
        self.lpane.ShowLoading(False)

        # If back is False, do not append to history. This could be us calling
        # the stage from previous history, creating / copying fit, etc.
        # We also have to use conditional for search stage since it's last data
        # is kept elsewhere
        if getattr(event, "back", False):
            if self._activeStage == 4 and self.navpanel.lastSearch != "":
                self.browseHist.append((4, self.navpanel.lastSearch))
            else:
                self.browseHist.append((self._activeStage, self.lastdata))

        shipID = event.shipID
        self.lastdata = shipID
        self._lastStage = self._activeStage
        self._activeStage = 3

        sFit = Fit.getInstance()
        sMkt = Market.getInstance()

        ship = sMkt.getItem(shipID)
        categoryID = ship.group.ID

        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()
        fitList = sFit.getFitsWithShip(shipID)

        if len(fitList) == 0:
            stage, data = self.browseHist.pop()
            self.lpane.Thaw()
            self.navpanel.gotoStage(stage, data)
            return

        self.categoryFitCache[categoryID] = True

        self.navpanel.ShowNewFitButton(True)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

        fitList.sort(key=self.nameKey)
        shipName = ship.name

        self._stage3ShipName = shipName
        self._stage3Data = shipID

        shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

        for ID, name, booster, timestamp, notes in fitList:
            self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, shipTrait, name, booster, timestamp, notes), shipID))

        self.lpane.RefreshList()
        self.lpane.Thaw()
        self.raceselect.RebuildRaces(self.RACE_ORDER)

    def searchStage(self, event):

        self.lpane.ShowLoading(False)

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if not event.back:
            if self._activeStage != 4:
                if len(self.browseHist) > 0:
                    self.browseHist.append((self._activeStage, self.lastdata))
                else:
                    self.browseHist.append((1, 0))
            self._lastStage = self._activeStage
            self._activeStage = 4

        sMkt = Market.getInstance()
        sFit = Fit.getInstance()
        query = event.text

        self.lpane.Freeze()

        self.lpane.RemoveAllChildren()
        if query:
            ships = sMkt.searchShips(query)
            fitList = sFit.searchFits(query)

            for ship in ships:
                shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

                self.lpane.AddWidget(
                    ShipItem(self.lpane, ship.ID, (ship.name, shipTrait, len(sFit.getFitsWithShip(ship.ID))),
                             ship.race))

            for ID, name, shipID, shipName, booster, timestamp, notes in fitList:
                ship = sMkt.getItem(shipID)

                if not sMkt.getPublicityByItem(ship):
                    continue

                shipTrait = ship.traits.traitText if (ship.traits is not None) else ""  # empty string if no traits

                self.lpane.AddWidget(FitItem(self.lpane, ID, (shipName, shipTrait, name, booster, timestamp, notes), shipID))
            if len(ships) == 0 and len(fitList) == 0:
                self.lpane.AddWidget(PFStaticText(self.lpane, label=u"No matching results."))
            self.lpane.RefreshList(doFocus=False)
        self.lpane.Thaw()

        self.raceselect.RebuildRaces(self.RACE_ORDER)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()

    def importStage(self, event):
        """
        The import stage handles both displaying fits after importing as well as displaying recent fits. todo: need to
        reconcile these two better into a more uniform function, right now hacked together to get working
        """
        self.lpane.ShowLoading(False)

        self.navpanel.ShowNewFitButton(False)
        self.navpanel.ShowSwitchEmptyGroupsButton(False)

        if getattr(event, "back", False):
            self.browseHist.append((self._activeStage, self.lastdata))

        self._lastStage = self._activeStage
        self._activeStage = 5

        fits = event.fits

        self.lastdata = fits
        self.lpane.Freeze()
        self.lpane.RemoveAllChildren()

        if fits:
            for fit in fits:
                shipItem = fit[3]
                shipTrait = shipItem.traits.traitText if (shipItem.traits is not None) else ""

                self.lpane.AddWidget(FitItem(
                    self.lpane,
                    fit[0],
                    (
                        shipItem.name,
                        shipTrait,
                        fit[1],
                        False,
                        fit[2],
                        fit[4]
                    ),
                    shipItem.ID,
                ))
            self.lpane.RefreshList(doFocus=False)
        self.lpane.Thaw()

        self.raceselect.RebuildRaces(self.RACE_ORDER)

        if self.showRacesFilterInStage2Only:
            self.raceselect.Show(False)
            self.Layout()
