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

import csv
# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.auxWindow import AuxiliaryFrame
from service.ammoBreakdown import get_ammo_breakdown
from service.fit import Fit

_t = wx.GetTranslation

COL_AMMO_NAME = 0
COL_DAMAGE_TYPE = 1
COL_OPTIMAL = 2
COL_FALLOFF = 3
COL_ALPHA = 4
COL_DPS = 5


class AmmoBreakdownFrame(AuxiliaryFrame):

    def __init__(self, parent):
        super().__init__(parent, title=_t('Ammo Breakdown'), size=(640, 400), resizeable=True)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self._data = []

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.listCtrl = wx.ListCtrl(
            self, wx.ID_ANY,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN
        )
        self.listCtrl.AppendColumn(_t('Ammo Name'), wx.LIST_FORMAT_LEFT, 180)
        self.listCtrl.AppendColumn(_t('Damage Type'), wx.LIST_FORMAT_LEFT, 110)
        self.listCtrl.AppendColumn(_t('Optimal'), wx.LIST_FORMAT_LEFT, 120)
        self.listCtrl.AppendColumn(_t('Falloff'), wx.LIST_FORMAT_LEFT, 120)
        self.listCtrl.AppendColumn(_t('Alpha'), wx.LIST_FORMAT_RIGHT, 90)
        self.listCtrl.AppendColumn(_t('DPS'), wx.LIST_FORMAT_RIGHT, 90)
        mainSizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 5)

        self.emptyLabel = wx.StaticText(self, wx.ID_ANY, _t('No ammo in cargo usable by fitted weapons.'))
        self.emptyLabel.Hide()
        mainSizer.Add(self.emptyLabel, 0, wx.ALL, 10)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.exportBtn = wx.Button(self, wx.ID_ANY, _t('Export…'))
        self.exportBtn.Bind(wx.EVT_BUTTON, self.OnExport)
        btnSizer.Add(self.exportBtn, 0, wx.RIGHT, 5)
        self.copyBtn = wx.Button(self, wx.ID_ANY, _t('Copy to clipboard'))
        self.copyBtn.Bind(wx.EVT_BUTTON, self.OnCopyToClipboard)
        btnSizer.Add(self.copyBtn, 0)
        mainSizer.Add(btnSizer, 0, wx.ALL, 5)

        self.SetSizer(mainSizer)

        self.mainFrame.Bind(GE.FIT_CHANGED, self.OnFitChanged)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.refresh()

    def _get_fit(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        return Fit.getInstance().getFit(fitID)

    def refresh(self):
        fit = self._get_fit()
        self._data = get_ammo_breakdown(fit) if fit else []
        self.listCtrl.DeleteAllItems()
        if not self._data:
            self.listCtrl.Hide()
            self.emptyLabel.Show()
            self.exportBtn.Enable(False)
            self.copyBtn.Enable(False)
        else:
            self.emptyLabel.Hide()
            self.listCtrl.Show()
            for row in self._data:
                idx = self.listCtrl.InsertItem(self.listCtrl.GetItemCount(), row['ammoName'])
                self.listCtrl.SetItem(idx, COL_DAMAGE_TYPE, row['damageType'])
                self.listCtrl.SetItem(idx, COL_OPTIMAL, row['optimal'])
                self.listCtrl.SetItem(idx, COL_FALLOFF, row['falloff'])
                self.listCtrl.SetItem(idx, COL_ALPHA, '{:.1f}'.format(row['alpha']))
                self.listCtrl.SetItem(idx, COL_DPS, '{:.1f}'.format(row['dps']))
            self.exportBtn.Enable(True)
            self.copyBtn.Enable(True)
        self.Layout()

    def OnFitChanged(self, event):
        event.Skip()
        self.refresh()

    def OnClose(self, event):
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.OnFitChanged)
        event.Skip()

    def _get_csv_content(self):
        lines = []
        lines.append([_t('Ammo Name'), _t('Damage Type'), _t('Optimal'), _t('Falloff'), _t('Alpha'), _t('DPS')])
        for row in self._data:
            lines.append([
                row['ammoName'],
                row['damageType'],
                row['optimal'],
                row['falloff'],
                '{:.1f}'.format(row['alpha']),
                '{:.1f}'.format(row['dps']),
            ])
        return lines

    def OnExport(self, event):
        if not self._data:
            return
        fit = self._get_fit()
        defaultFile = 'ammo_breakdown.csv'
        if fit and fit.ship and fit.ship.item:
            defaultFile = '{} - ammo_breakdown.csv'.format(fit.ship.item.name.replace('/', '-'))
        with wx.FileDialog(
                self, _t('Export ammo breakdown'), '', defaultFile,
                _t('CSV files') + ' (*.csv)|*.csv', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            for line in self._get_csv_content():
                writer.writerow(line)
        event.Skip()

    def OnCopyToClipboard(self, event):
        if not self._data:
            return
        lines = self._get_csv_content()
        text = '\n'.join(','.join(str(c) for c in row) for row in lines)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
        event.Skip()
