# shipBonusForceAuxiliaryRole2LogisticDroneBonus
#
# Used by:
# Ships from group: Force Auxiliary (4 of 4)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"), "structureDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"), "armorDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"), "shieldBonus", src.getModifiedItemAttr("shipBonusRole2"))
