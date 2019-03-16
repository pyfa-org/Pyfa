# shipBonusRole4FighterDamageAndHitpoints
#
# Used by:
# Ship: Caiman
# Ship: Komodo
type = "passive"


def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                   src.getModifiedItemAttr("shipBonusRole4"))
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretDamageMultiplier",
                                   src.getModifiedItemAttr("shipBonusRole4"))
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileDamageMultiplier",
                                   src.getModifiedItemAttr("shipBonusRole4"))
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesDamageMultiplier",
                                   src.getModifiedItemAttr("shipBonusRole4"))
