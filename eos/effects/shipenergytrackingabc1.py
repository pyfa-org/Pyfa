# shipEnergyTrackingABC1
#
# Used by:
# Ship: Harbinger Navy Issue

type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusABC1"), skill="Amarr Battlecruiser")
