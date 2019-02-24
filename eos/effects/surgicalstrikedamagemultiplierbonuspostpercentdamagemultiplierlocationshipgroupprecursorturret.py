# surgicalStrikeDamageMultiplierBonusPostPercentDamageMultiplierLocationShipGroupPrecursorTurret
#
# Used by:
# Skill: Surgical Strike
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Precursor Weapon",
                                  "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
