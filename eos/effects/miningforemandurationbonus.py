# miningForemanDurationBonus
#
# Used by:
# Skill: Mining Foreman
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
