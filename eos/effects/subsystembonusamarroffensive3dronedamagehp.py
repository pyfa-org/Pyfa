# subsystemBonusAmarrOffensive3DroneDamageHP
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "hp", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "armorHP", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "shieldCapacity", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "damageMultiplier", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
