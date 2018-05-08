# mediumPrecursorTurretDmgBonusRequiredSkill
#
# Used by:
# Skill: Medium Precursor Weapon
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
