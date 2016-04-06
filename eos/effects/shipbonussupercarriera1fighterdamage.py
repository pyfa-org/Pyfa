# shipBonusSupercarrierA1FighterDamage
#
# Used by:
# Ship: Aeon
# Ship: Revenant
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesDamageMultiplier", src.getModifiedItemAttr("shipBonusSupercarrierA1"), skill="Amarr Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileDamageMultiplier", src.getModifiedItemAttr("shipBonusSupercarrierA1"), skill="Amarr Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretDamageMultiplier", src.getModifiedItemAttr("shipBonusSupercarrierA1"), skill="Amarr Carrier")
