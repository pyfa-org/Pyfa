type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"), "structureDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"), "armorDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"), "shieldBonus", src.getModifiedItemAttr("shipBonusRole2"))
