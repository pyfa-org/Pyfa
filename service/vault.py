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

from logbook import Logger

import eos.db
from service.settings import SettingsProvider

pyfalog = Logger(__name__)

SETTINGS_KEY = "pyfaCurrentVault"
DEFAULT_SETTINGS = {"vaultID": None}


class Vault:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Vault()
        return cls.instance

    def __init__(self):
        self._settings = SettingsProvider.getInstance()

    def getVaultList(self):
        """Return all vaults ordered by sortOrder, then A-Z by name."""
        return eos.db.getVaultList()

    def getCurrentVaultID(self):
        """Return current vault ID from settings. If not set, use first vault (Default)."""
        s = self._settings.getSettings(SETTINGS_KEY, DEFAULT_SETTINGS)
        vid = s["vaultID"]
        if vid is not None:
            return vid
        vaults = eos.db.getVaultList()
        if not vaults:
            return None
        default_id = vaults[0].ID
        self.setCurrentVaultID(default_id)
        return default_id

    def setCurrentVaultID(self, vaultID):
        s = self._settings.getSettings(SETTINGS_KEY, DEFAULT_SETTINGS)
        s["vaultID"] = vaultID
        s.save()

    def getVault(self, vaultID):
        return eos.db.getVault(vaultID)

    def countFitsInVault(self, vaultID):
        return eos.db.countFitsInVault(vaultID)

    def createVault(self, name):
        return eos.db.createVault(name)

    def renameVault(self, vaultID, name):
        eos.db.renameVault(vaultID, name)

    def deleteVault(self, vaultID):
        """Move fits to another vault, then delete. Cannot delete the last remaining vault."""
        vaults = eos.db.getVaultList()
        if len(vaults) <= 1:
            return
        default_id = next((v.ID for v in vaults if v.ID != vaultID), None)
        if default_id is None:
            return
        current = self.getCurrentVaultID()
        eos.db.deleteVault(vaultID, default_id)
        if current == vaultID:
            self.setCurrentVaultID(default_id)

    def moveFitToVault(self, fitID, vaultID):
        eos.db.moveFitToVault(fitID, vaultID)

    def reorderVaults(self, vault_ids_in_order):
        """Persist vault order. vault_ids_in_order is list of vault IDs in display order."""
        eos.db.updateVaultSortOrder(vault_ids_in_order)
