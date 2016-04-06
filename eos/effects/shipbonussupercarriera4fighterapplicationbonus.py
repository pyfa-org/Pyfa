# shipBonusSupercarrierA4FighterApplicationBonus
#
# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesExplosionRadius", src.getModifiedItemAttr("shipBonusSupercarrierA4"), skill="Amarr Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileExplosionRadius", src.getModifiedItemAttr("shipBonusSupercarrierA4"), skill="Amarr Carrier")
