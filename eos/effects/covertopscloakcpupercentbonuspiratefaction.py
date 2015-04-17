# covertOpsCloakCPUPercentBonusPirateFaction
#
# Used by:
# Ship: Astero
# Ship: Prospect
# Ship: Victorieux Luxury Yacht
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                  "cpu", ship.getModifiedItemAttr("shipBonusPirateFaction"))
