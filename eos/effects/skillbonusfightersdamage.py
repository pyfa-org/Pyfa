# skillBonusFightersDamage
#
# Used by:
# Skill: Fighters
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackTurretDamageMultiplier",
                                   src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityMissilesDamageMultiplier",
                                   src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackMissileDamageMultiplier",
                                   src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
