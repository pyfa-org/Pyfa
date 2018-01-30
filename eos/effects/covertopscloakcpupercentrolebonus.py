# covertOpsCloakCPUPercentRoleBonus
#
# Used by:
# Ships from group: Expedition Frigate (2 of 2)
# Ship: Astero
# Ship: Enforcer
# Ship: Pacifier
# Ship: Victor
# Ship: Victorieux Luxury Yacht
# Ship: Virtuoso
type = "passive"
runTime = "early"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                  "cpu", ship.getModifiedItemAttr("shipBonusRole7"))
