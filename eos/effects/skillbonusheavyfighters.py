# skillBonusHeavyFighters
#
# Used by:
# Skill: Heavy Fighters
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Fighters"), "fighterAbilityMissilesDamageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Fighters"), "fighterAbilityAttackMissileDamageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Fighters"), "fighterAbilityAttackTurretDamageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
