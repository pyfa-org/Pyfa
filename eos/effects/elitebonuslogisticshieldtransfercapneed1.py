# eliteBonusLogisticShieldTransferCapNeed1
#
# Used by:
# Ship: Basilisk
# Ship: Etana
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics")
