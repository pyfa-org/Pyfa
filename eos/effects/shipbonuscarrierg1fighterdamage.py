type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesDamageMultiplier", src.getModifiedItemAttr("shipBonusCarrierG1"), skill="Gallente Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretDamageMultiplier", src.getModifiedItemAttr("shipBonusCarrierG1"), skill="Gallente Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileDamageMultiplier", src.getModifiedItemAttr("shipBonusCarrierG1"), skill="Gallente Carrier")
