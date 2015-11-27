# eliteBonusLogisticEnergyTransferCapNeed2
#
# Used by:
# Ship: Basilisk
# Ship: Etana
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics Cruisers")
