# shipBonusEwWeaponDisruptionStrengthAC1
#
# Used by:
# Variations of ship: Arbitrator (3 of 3)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "missileVelocityBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeVelocityBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "maxRangeBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "explosionDelayBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeCloudSizeBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "trackingSpeedBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "falloffBonus",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
