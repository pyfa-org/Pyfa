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

import config
import wx
_t = wx.GetTranslation

try:
    versionString = "{0}".format(config.getVersion())
except NameError:
    # is caught in case we run test and there are no config values initialized
    versionString = "0.0"

licenses = (
    _t("pyfa is released under GNU GPLv3 - see included LICENSE file"),
    _t("All EVE-Online related materials are property of CCP hf."),
    _t("Silk Icons Set by famfamfam.com - Creative Commons Attribution 2.5 License"),
    _t("Fat Cow Icons by fatcow.com - Creative Commons Attribution 3.0 License")
)
developers = (
    "blitzmann \tSable Blitzmann (maintainer)",
    "cncfanatics \tSakari Orisi (retired)",
    "DarkPhoenix \tKadesh Priestess (retired)",
    "Darriele \t\tDarriele (retired)",
    "Ebag333 \t\tEbag Trescientas"
)
credits = (
    "Entity (Entity) \tCapacitor calculations / EVEAPI python lib / Reverence",
    "Aurora \t\tMaths",
    "Corollax (Aamrr) \tVarious EOS / pyfa improvements",
    "Dreae (Dreae)\tPyCrest")
description = (
    _t("Pyfa (the Python Fitting Assistant) is an open-source standalone application able to "
    "create and simulate fittings for EVE-Online SciFi MMORPG with a very high degree of "
    "accuracy. Pyfa can run on all platforms where Python and wxWidgets are supported.")
)
