# shipEnergyTransferRange1
#
# Used by:
# Ship: Guardian
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
