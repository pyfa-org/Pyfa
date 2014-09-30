# shipBonusAoeVelocityCruiseMissilesMB2
#
# Used by:
# Ship: Typhoon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusMB2") * level)
