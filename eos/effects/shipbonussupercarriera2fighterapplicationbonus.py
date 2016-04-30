# shipBonusSupercarrierA2FighterApplicationBonus
#
# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesExplosionVelocity", src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileExplosionVelocity", src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
