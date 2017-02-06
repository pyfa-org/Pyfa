# shipLaserTracking2AD2
#
# Used by:
# Ship: Coercer
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
