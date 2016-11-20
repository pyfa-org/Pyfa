# shipBonusMediumEnergyTurretTrackingAC2
#
# Used by:
# Ship: Fiend
# Ship: Phantasm
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
