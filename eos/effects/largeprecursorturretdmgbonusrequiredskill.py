# largePrecursorTurretDmgBonusRequiredSkill
#
# Used by:
# Skill: Large Precursor Weapon
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Precursor Weapon"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
