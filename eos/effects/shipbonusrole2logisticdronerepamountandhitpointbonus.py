# shipBonusRole2LogisticDroneRepAmountAndHitpointBonus
#
# Used by:
# Ship: Loggerhead
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                    "structureDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                    "shieldBonus", src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                    "armorDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                    "armorHP", src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                    "shieldCapacity", src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                    "hp", src.getModifiedItemAttr("shipBonusRole2"))
