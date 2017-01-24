# commandBurstReloadTimeBonus
#
# Used by:
# Skill: Command Burst Specialist
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"),
                                  "reloadTime",
                                  src.getModifiedItemAttr("reloadTimeBonus") * lvl)
