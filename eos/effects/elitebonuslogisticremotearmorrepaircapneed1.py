# eliteBonusLogisticRemoteArmorRepairCapNeed1
#
# Used by:
# Ship: Oneiros
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics")
