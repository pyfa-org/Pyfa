# probeLauncherCPUPercentRoleBonusT3
#
# Used by:
# Ships from group: Strategic Cruiser (4 of 4)
# Ships from group: Tactical Destroyer (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"), "cpu", src.getModifiedItemAttr("roleBonusT3ProbeCPU"))
