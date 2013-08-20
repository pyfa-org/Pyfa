# Used by:
# Ship: Augoror
# Ship: Osprey
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                  "powerTransferAmount", ship.getModifiedItemAttr("energyTransferAmountBonus"))
