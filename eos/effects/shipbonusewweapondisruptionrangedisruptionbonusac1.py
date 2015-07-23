# shipBonusEwWeaponDisruptionRangeDisruptionBonusAC1
#
# Used by:
# Variations of ship: Arbitrator (3 of 3)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "maxRangeBonus", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "falloffBonus", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
