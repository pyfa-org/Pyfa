# commandBurstAoEBonus
#
# Used by:
# Skill: Fleet Command
# Skill: Leadership
# Skill: Wing Command
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "maxRange",
                                  src.getModifiedItemAttr("areaOfEffectBonus") * src.level)
