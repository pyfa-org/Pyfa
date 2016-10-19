# shipSETTrackingBonusAF
#
# Used by:
# Ship: Retribution
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
