# shipLargeLaserCapABC1
#
# Used by:
# Ship: Oracle
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC1"),
                                  skill="Amarr Battlecruiser")
