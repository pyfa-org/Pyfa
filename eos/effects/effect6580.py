# shipBonusRole2LogisticDroneRepAmountBonus
#
# Used by:
# Ships from group: Force Auxiliary (5 of 6)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"), "structureDamageAmount",
                                 src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"), "armorDamageAmount",
                                 src.getModifiedItemAttr("shipBonusRole2"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"), "shieldBonus",
                                 src.getModifiedItemAttr("shipBonusRole2"))
