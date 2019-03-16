# shipBonusAoeVelocityCruiseMissilesMB2
#
# Used by:
# Ship: Typhoon
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusMB2"),
                                    skill="Minmatar Battleship")
