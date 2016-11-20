# dreadnoughtShipBonusLaserRofA2
#
# Used by:
# Ship: Revelation
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusA2"),
                                  skill="Amarr Dreadnought")
