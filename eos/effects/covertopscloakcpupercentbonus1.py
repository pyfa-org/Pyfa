# covertOpsCloakCpuPercentBonus1
#
# Used by:
# Ships from group: Covert Ops (5 of 5)
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "cpu", ship.getModifiedItemAttr("eliteBonusCoverOps1"), skill="Covert Ops")
