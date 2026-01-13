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


# noinspection PyPackageRequirements
import logging
import wx

import gui.display
import gui.globalEvents as GE
from eos.const import FittingHardpoint
from eos.saveddata.targetProfile import TargetProfile
from graphs.style import BASE_COLORS, LIGHTNESSES, STYLES
from graphs.wrapper import SourceWrapper, TargetWrapper
from gui.builtinViewColumns.graphColor import GraphColor
from gui.builtinViewColumns.graphLightness import GraphLightness
from gui.builtinViewColumns.graphLineStyle import GraphLineStyle
from gui.contextMenu import ContextMenu
from service.const import GraphCacheCleanupReason, GraphLightness as GraphLightnessEnum, GraphLineStyle as GraphLineStyleEnum
from service.fit import Fit
from .stylePickers import ColorPickerPopup, LightnessPickerPopup, LineStylePickerPopup

_t = wx.GetTranslation
pyfalog = logging.getLogger(__name__)


def getFitWeaponClass(fit):
    """
    Determine the weapon class of a fit based on its turret or missile type.
    
    Returns: 'energy', 'projectile', 'hybrid', 'exotic', 'vorton', 'missile', or None if no weapons.
    
    Uses module group names instead of loading charges for performance.
    """
    if fit is None:
        return None
    
    # Try activeModulesIter first (more reliable), fall back to modules
    modules = list(fit.activeModulesIter()) if hasattr(fit, 'activeModulesIter') else fit.modules
    
    for mod in modules:
        if mod.isEmpty or mod.item is None:
            continue
        
        # Check turret hardpoints - use module group name to determine type
        if mod.hardpoint == FittingHardpoint.TURRET:
            # Skip mining turrets
            if mod.getModifiedItemAttr('miningAmount'):
                continue
            
            # Get module group name to determine weapon class
            if mod.item.group is None:
                continue
            
            groupName = mod.item.group.name
            
            # Determine weapon class from module group
            if 'Energy' in groupName or 'Laser' in groupName or 'Beam' in groupName or 'Pulse' in groupName:
                return 'energy'
            elif 'Projectile' in groupName or 'Autocannon' in groupName or 'Artillery' in groupName:
                return 'projectile'
            elif 'Hybrid' in groupName or 'Blaster' in groupName or 'Railgun' in groupName:
                return 'hybrid'
            elif 'Entropic' in groupName or 'Disintegrator' in groupName:
                return 'exotic'
            elif 'Vorton' in groupName or 'Arcing' in groupName:
                return 'vorton'
        
        # Check missile hardpoints
        elif mod.hardpoint == FittingHardpoint.MISSILE:
            return 'missile'
    
    return None

class BaseWrapperList(gui.display.Display):

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame
        self._wrappers = []

        self.hoveredRow = None
        self.hoveredColumn = None

        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    @property
    def wrappers(self):
        # Sort fits first, then target profiles
        return sorted(self._wrappers, key=lambda w: not w.isFit)

    # UI-related stuff
    @property
    def defaultTTText(self):
        raise NotImplementedError

    def refreshExtraColumns(self, extraColSpecs):
        baseColNames = set()
        for baseColName in self.DEFAULT_COLS:
            if ":" in baseColName:
                baseColName = baseColName.split(":", 1)[0]
            baseColNames.add(baseColName)
        columnsToRemove = set()
        for col in self.activeColumns:
            if col.name not in baseColNames:
                columnsToRemove.add(col)
        for col in columnsToRemove:
            self.removeColumn(col)
        for colSpec in extraColSpecs:
            self.appendColumnBySpec(colSpec)
        self.refreshView()

    def refreshView(self):
        self.refresh(self.wrappers)

    def updateView(self):
        self.update(self.wrappers)

    # UI event handling
    def OnMouseMove(self, event):
        row, _, col = self.HitTestSubItem(event.Position)
        if row != self.hoveredRow or col != self.hoveredColumn:
            if self.ToolTip is not None:
                self.SetToolTip(None)
            else:
                self.hoveredRow = row
                self.hoveredColumn = col
                if row != -1 and col != -1 and col < self.ColumnCount:
                    item = self.getWrapper(row)
                    if item is None:
                        return
                    tooltip = self.activeColumns[col].getToolTip(item)
                    if tooltip:
                        self.SetToolTip(tooltip)
                    else:
                        self.SetToolTip(None)
                else:
                    self.SetToolTip(self.defaultTTText)
        event.Skip()

    def OnLeaveWindow(self, event):
        self.SetToolTip(None)
        self.hoveredRow = None
        self.hoveredColumn = None
        event.Skip()

    def handleDrag(self, type, fitID):
        if type == 'fit' and not self.containsFitID(fitID):
            sFit = Fit.getInstance()
            fit = sFit.getFit(fitID)
            self.appendItem(fit)
            self.updateView()
            self.graphFrame.draw()

    def OnLeftDown(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            pickers = {
                self.getColIndex(GraphColor): ColorPickerPopup,
                self.getColIndex(GraphLightness): LightnessPickerPopup,
                self.getColIndex(GraphLineStyle): LineStylePickerPopup}
            # In case we had no index for some column, remove None
            pickers.pop(None, None)
            col = self.getColumn(event.Position)
            if col in pickers:
                picker = pickers[col]
                wrapper = self.getWrapper(row)
                if wrapper is not None:
                    win = picker(parent=self, wrapper=wrapper)
                    pos = wx.GetMousePosition()
                    win.Position(pos, (0, 0))
                    win.Popup()
                    return
        event.Skip()

    def OnLineStyleChange(self):
        self.updateView()
        self.graphFrame.draw()

    def OnLeftDClick(self, event):
        row, _ = self.HitTest(event.Position)
        wrapper = self.getWrapper(row)
        if wrapper is None:
            return
        self.removeWrappers([wrapper])

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()
        if keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
            self.removeWrappers(self.getSelectedWrappers())
        event.Skip()

    # Wrapper-related methods
    def getWrapper(self, row):
        if row == -1:
            return None
        try:
            return self.wrappers[row]
        except IndexError:
            return None

    def removeWrappers(self, wrappers):
        wrappers = set(wrappers).intersection(self._wrappers)
        if not wrappers:
            return
        for wrapper in wrappers:
            self._wrappers.remove(wrapper)
        self.updateView()
        for wrapper in wrappers:
            if wrapper.isFit:
                self.graphFrame.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=wrapper.item.ID)
            elif wrapper.isProfile:
                self.graphFrame.clearCache(reason=GraphCacheCleanupReason.profileRemoved, extraData=wrapper.item.ID)
        self.graphFrame.draw()

    def getSelectedWrappers(self):
        wrappers = []
        for row in self.getSelectedRows():
            wrapper = self.getWrapper(row)
            if wrapper is None:
                continue
            wrappers.append(wrapper)
        return wrappers

    def appendItem(self, item):
        raise NotImplemented

    def containsFitID(self, fitID):
        for wrapper in self._wrappers:
            if wrapper.isFit and wrapper.item.ID == fitID:
                return True
        return False

    def containsProfileID(self, profileID):
        for wrapper in self._wrappers:
            if wrapper.isProfile and wrapper.item.ID == profileID:
                return True
        return False

    # Wrapper-related events
    def OnFitRenamed(self, event):
        if self.containsFitID(event.fitID):
            self.updateView()

    def OnFitChanged(self, event):
        if set(event.fitIDs).intersection(w.item.ID for w in self._wrappers if w.isFit):
            self.updateView()

    def OnFitRemoved(self, event):
        wrapper = next((w for w in self._wrappers if w.isFit and w.item.ID == event.fitID), None)
        if wrapper is not None:
            self._wrappers.remove(wrapper)
            self.updateView()

    def OnProfileRenamed(self, event):
        if self.containsProfileID(event.profileID):
            self.updateView()

    def OnProfileChanged(self, event):
        if self.containsProfileID(event.profileID):
            self.updateView()

    def OnProfileRemoved(self, event):
        wrapper = next((w for w in self._wrappers if w.isProfile and w.item.ID == event.profileID), None)
        if wrapper is not None:
            self._wrappers.remove(wrapper)
            self.updateView()

    # Context menu handlers
    def addFit(self, fit):
        if fit is None:
            return
        if self.containsFitID(fit.ID):
            return
        # Ensure fit is fully recalculated before adding to graph
        sFit = Fit.getInstance()
        sFit.recalc(fit)
        self.appendItem(fit)
        self.updateView()
        # Trigger FIT_CHANGED event to refresh all caches and views
        wx.PostEvent(self.graphFrame.mainFrame, GE.FitChanged(fitIDs=(fit.ID,)))

    def getExistingFitIDs(self):
        return [w.item.ID for w in self._wrappers if w.isFit]

    def addFitsByIDs(self, fitIDs):
        sFit = Fit.getInstance()
        addedFitIDs = []
        for fitID in fitIDs:
            if self.containsFitID(fitID):
                continue
            fit = sFit.getFit(fitID)
            if fit is not None:
                # Ensure fit is fully recalculated before adding to graph
                sFit.recalc(fit)
                self.appendItem(fit)
                addedFitIDs.append(fitID)
        self.updateView()
        # Trigger FIT_CHANGED event to refresh all caches and views
        if addedFitIDs:
            wx.PostEvent(self.graphFrame.mainFrame, GE.FitChanged(fitIDs=tuple(addedFitIDs)))


class SourceWrapperList(BaseWrapperList):

    DEFAULT_COLS = (
        'Graph Color',
        'Base Icon',
        'Base Name')

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        fit = Fit.getInstance().getFit(self.graphFrame.mainFrame.getActiveFit())
        if fit is not None:
            self.appendItem(fit)
            self.updateView()

    def appendItem(self, item):
        # Find out least used color
        colorUseMap = {c: 0 for c in BASE_COLORS}
        for wrapper in self._wrappers:
            if wrapper.colorID not in colorUseMap:
                continue
            colorUseMap[wrapper.colorID] += 1

        def getDefaultParams():
            leastUses = min(colorUseMap.values(), default=0)
            for colorID in BASE_COLORS:
                if leastUses == colorUseMap.get(colorID, 0):
                    return colorID
            return None

        colorID = getDefaultParams()
        self._wrappers.append(SourceWrapper(item=item, colorID=colorID))
        
        # Check if we should switch to Pattern mode (for Application Profile graph)
        self._checkAutoSwitchAmmoStyle()

    def _checkAutoSwitchAmmoStyle(self):
        """
        Auto-switch ammo style to Pattern when multiple fits with same weapon class are added.
        
        This helps differentiate between attackers when they use the same ammo types.
        """
        from logbook import Logger
        pyfalog = Logger(__name__)
        
        # Check if ctrlPanel is fully initialized (has ammoStyleSelection)
        ctrlPanel = getattr(self.graphFrame, 'ctrlPanel', None)
        if ctrlPanel is None:
            pyfalog.debug("[AMMO STYLE] ctrlPanel is None")
            return
        if not hasattr(ctrlPanel, 'ammoStyleSelection'):
            pyfalog.debug("[AMMO STYLE] ctrlPanel has no ammoStyleSelection")
            return
        
        # Check if this graph supports segments (Application Profile)
        try:
            view = self.graphFrame.getView()
        except Exception:
            pyfalog.debug("[AMMO STYLE] Failed to get view")
            return
        
        if not getattr(view, 'hasSegments', False):
            pyfalog.debug("[AMMO STYLE] View doesn't have segments")
            return
        
        # Get current ammo style
        currentStyle = ctrlPanel.ammoStyle
        pyfalog.debug(f"[AMMO STYLE] Current style: {currentStyle}")
        
        # Only auto-switch if currently on 'color' mode
        if currentStyle != 'color':
            pyfalog.debug(f"[AMMO STYLE] Not switching - style is {currentStyle}, not 'color'")
            return
        
        # Check if we have 2+ fits with the same weapon class
        weaponClasses = {}
        for wrapper in self._wrappers:
            if not wrapper.isFit:
                continue
            wc = getFitWeaponClass(wrapper.item)
            pyfalog.debug(f"[AMMO STYLE] Fit {wrapper.item.name}: weapon class = {wc}")
            if wc:
                weaponClasses[wc] = weaponClasses.get(wc, 0) + 1
        
        pyfalog.debug(f"[AMMO STYLE] Weapon classes: {weaponClasses}")
        
        # If any weapon class has 2+ fits, switch to pattern mode
        for wc, count in weaponClasses.items():
            if count >= 2:
                pyfalog.debug(f"[AMMO STYLE] Switching to pattern - {wc} has {count} fits")
                ctrlPanel.setAmmoStyle('pattern')
                return
        
        pyfalog.debug("[AMMO STYLE] No conflicts found")

    def _checkAutoSwitchBackToColor(self):
        """
        Auto-switch ammo style back to Color when no more weapon class conflicts exist.
        
        Called after removing a fit to see if we can switch back to color mode.
        """
        # Check if ctrlPanel is fully initialized (has ammoStyleSelection)
        ctrlPanel = getattr(self.graphFrame, 'ctrlPanel', None)
        if ctrlPanel is None:
            return
        if not hasattr(ctrlPanel, 'ammoStyleSelection'):
            return
        
        # Check if this graph supports segments (Application Profile)
        try:
            view = self.graphFrame.getView()
        except Exception:
            return
        
        if not getattr(view, 'hasSegments', False):
            return
        
        # Get current ammo style
        currentStyle = ctrlPanel.ammoStyle
        
        # Only auto-switch if currently on 'pattern' mode
        if currentStyle != 'pattern':
            return
        
        # Check if we still have 2+ fits with the same weapon class
        weaponClasses = {}
        for wrapper in self._wrappers:
            if not wrapper.isFit:
                continue
            wc = getFitWeaponClass(wrapper.item)
            if wc:
                weaponClasses[wc] = weaponClasses.get(wc, 0) + 1
        
        # If no weapon class has 2+ fits anymore, switch back to color mode
        hasConflict = any(count >= 2 for count in weaponClasses.values())
        if not hasConflict:
            ctrlPanel.setAmmoStyle('color')

    def removeWrappers(self, wrappers):
        """Override to check if we should switch back to color mode after removal."""
        super().removeWrappers(wrappers)
        self._checkAutoSwitchBackToColor()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedWrappers()
        mainItem = self.getWrapper(clickedPos)

        itemContext = None if mainItem is None else _t('Fit')
        menu = ContextMenu.getMenu(self, mainItem, selection, ('graphFitList', itemContext), ('graphFitListMisc', itemContext))
        if menu:
            self.PopupMenu(menu)

    @property
    def defaultTTText(self):
        return _t('Drag a fit into this list to graph it')


class TargetWrapperList(BaseWrapperList):

    DEFAULT_COLS = (
        'Graph Lightness',
        'Graph Line Style',
        'Base Icon',
        'Base Name')

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        self.appendItem(TargetProfile.getIdeal())
        self.updateView()

    def getFilteredDefaultCols(self):
        """Return default columns filtered based on current ammo style.
        
        For the Application Profile graph (hasSegments=True):
        - 'color' mode: Ammo determines line color, so hide Lightness (show Line Style only)
        - 'pattern' mode: Ammo determines line pattern, so hide Line Style (show Lightness only)
        - 'none' mode: Show both columns
        
        For other graphs, always show both columns.
        """
        view = self.graphFrame.getView()
        hasSegments = getattr(view, 'hasSegments', False)
        
        if not hasSegments:
            return self.DEFAULT_COLS
        
        ammoStyle = self.graphFrame.ctrlPanel.ammoStyle
        
        if ammoStyle == 'color':
            # Color mode: ammo color differentiates, use line style for targets
            return tuple(c for c in self.DEFAULT_COLS if c != 'Graph Lightness')
        elif ammoStyle == 'pattern':
            # Pattern mode: ammo pattern differentiates, use lightness for targets
            return tuple(c for c in self.DEFAULT_COLS if c != 'Graph Line Style')
        else:
            # None mode: show both
            return self.DEFAULT_COLS

    def refreshDefaultColumns(self):
        """Refresh the default columns based on current ammo style.
        
        Rebuilds all columns in correct order to maintain proper column positions.
        """
        filteredCols = self.getFilteredDefaultCols()
        
        # Get base names of columns that should be shown
        colNamesToShow = set()
        for colName in filteredCols:
            if ":" in colName:
                colName = colName.split(":", 1)[0]
            colNamesToShow.add(colName)
        
        # Check if we need to make any changes
        currentStyleCols = [col.name for col in self.activeColumns 
                           if col.name in ('Graph Lightness', 'Graph Line Style')]
        targetStyleCols = [c for c in ('Graph Lightness', 'Graph Line Style') if c in colNamesToShow]
        
        if currentStyleCols == targetStyleCols:
            # No changes needed
            return
        
        # Save any extra columns (non-default columns added by the view)
        extraCols = [col.name for col in self.activeColumns 
                    if col.name not in ('Graph Lightness', 'Graph Line Style', 'Base Icon', 'Base Name')]
        
        # Remove ALL columns
        while self.activeColumns:
            self.removeColumn(self.activeColumns[0])
        
        # Re-add columns in correct order using filtered defaults
        for colName in filteredCols:
            self.appendColumnBySpec(colName)
        
        # Re-add any extra columns
        for colName in extraCols:
            self.appendColumnBySpec(colName)
        
        self.refreshView()

    def appendItem(self, item):
        # Find least used line style and least used lightness independently
        # This ensures both properties iterate even when only one is visible
        
        # Count line style usage
        lineStyleUseMap = {s: 0 for s in STYLES}
        for wrapper in self._wrappers:
            if wrapper.lineStyleID in lineStyleUseMap:
                lineStyleUseMap[wrapper.lineStyleID] += 1
        
        # Count lightness usage
        lightnessUseMap = {l: 0 for l in LIGHTNESSES}
        for wrapper in self._wrappers:
            if wrapper.lightnessID in lightnessUseMap:
                lightnessUseMap[wrapper.lightnessID] += 1
        
        # Find least used line style
        leastLineStyleUses = min(lineStyleUseMap.values(), default=0)
        lineStyleID = None
        for sid in STYLES:
            if lineStyleUseMap.get(sid, 0) == leastLineStyleUses:
                lineStyleID = sid
                break
        
        # Find least used lightness
        leastLightnessUses = min(lightnessUseMap.values(), default=0)
        lightnessID = None
        for lid in LIGHTNESSES:
            if lightnessUseMap.get(lid, 0) == leastLightnessUses:
                lightnessID = lid
                break
        
        self._wrappers.append(TargetWrapper(item=item, lightnessID=lightnessID, lineStyleID=lineStyleID))

    def removeWrappers(self, wrappers):
        """Override to reset remaining target to default style when only one remains."""
        # Call parent implementation
        wrappers = set(wrappers).intersection(self._wrappers)
        if not wrappers:
            return
        for wrapper in wrappers:
            self._wrappers.remove(wrapper)
        
        # If only one target remains, reset it to default styles
        if len(self._wrappers) == 1:
            remaining = self._wrappers[0]
            remaining.lightnessID = GraphLightnessEnum.normal
            remaining.lineStyleID = GraphLineStyleEnum.solid
        
        self.updateView()
        for wrapper in wrappers:
            if wrapper.isFit:
                self.graphFrame.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=wrapper.item.ID)
            elif wrapper.isProfile:
                self.graphFrame.clearCache(reason=GraphCacheCleanupReason.profileRemoved, extraData=wrapper.item.ID)
        self.graphFrame.draw()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedWrappers()
        mainItem = self.getWrapper(clickedPos)

        itemContext = None if mainItem is None else _t('Target')
        menu = ContextMenu.getMenu(self, mainItem, selection, ('graphTgtList', itemContext), ('graphTgtListMisc', itemContext))
        if menu:
            self.PopupMenu(menu)

    def OnResistModeChanged(self, event):
        if set(event.fitIDs).intersection(w.item.ID for w in self._wrappers if w.isFit):
            self.updateView()

    @property
    def defaultTTText(self):
        return _t('Drag a fit into this list to have your fits graphed against it')

    # Context menu handlers
    def addProfile(self, profile):
        if profile is None:
            return
        if self.containsProfileID(profile.ID):
            return
        self.appendItem(profile)
        self.updateView()
        self.graphFrame.draw()
