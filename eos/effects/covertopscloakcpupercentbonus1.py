# covertOpsCloakCpuPercentBonus1
#
# Used by:
# Ships from group: Covert Ops (5 of 7)
type = "passive"
runTime = "early"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                  "cpu", ship.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")
