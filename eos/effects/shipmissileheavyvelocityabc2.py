# shipMissileHeavyVelocityABC2
#
# Used by:
# Ship: Damnation
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusABC2"),
                                    skill="Amarr Battlecruiser")
