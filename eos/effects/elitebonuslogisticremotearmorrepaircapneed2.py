# eliteBonusLogisticRemoteArmorRepairCapNeed2
#
# Used by:
# Ship: Guardian
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics")
