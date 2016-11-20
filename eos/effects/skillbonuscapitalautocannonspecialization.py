# skillBonusCapitalAutocannonSpecialization
#
# Used by:
# Skill: Capital Autocannon Specialization
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Autocannon Specialization"),
                                  "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
