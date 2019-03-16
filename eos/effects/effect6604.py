# shipBonusSupercarrierC1FighterDamage
#
# Used by:
# Ship: Revenant
# Ship: Wyvern
type = "passive"


def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityMissilesDamageMultiplier",
                                   src.getModifiedItemAttr("shipBonusSupercarrierC1"), skill="Caldari Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackTurretDamageMultiplier",
                                   src.getModifiedItemAttr("shipBonusSupercarrierC1"), skill="Caldari Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackMissileDamageMultiplier",
                                   src.getModifiedItemAttr("shipBonusSupercarrierC1"), skill="Caldari Carrier")
