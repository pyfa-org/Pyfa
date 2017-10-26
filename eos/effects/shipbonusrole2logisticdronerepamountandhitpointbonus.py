# shipBonusRole2LogisticDroneRepAmountAndHitpointBonus
#
# Used by:
# Ship: Loggerhead
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"),
                                    "structureDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"),
                                    "shieldBonus", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"),
                                    "armorDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"),
                                    "armorHP", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"),
                                    "shieldCapacity", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Repair Drone Operation"),
                                    "hp", src.getModifiedItemAttr("shipBonusRole2"))
