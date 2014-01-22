# Used by:
# Ship: Basilisk
# Ship: Etana
# Ship: Guardian
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                  "power", ship.getModifiedItemAttr("powerTransferPowerNeedBonus"))
