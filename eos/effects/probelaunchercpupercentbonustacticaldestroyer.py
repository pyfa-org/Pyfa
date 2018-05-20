# probeLauncherCPUPercentBonusTacticalDestroyer
#
# Used by:
# Ships from group: Tactical Destroyer (4 of 4)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                  "cpu", ship.getModifiedItemAttr("roleBonusT3ProbeCPU"))
