# shipLargeLaserDamageBonusABC2
#
# Used by:
# Ship: Oracle
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusABC2"),
                                  skill="Amarr Battlecruiser")
