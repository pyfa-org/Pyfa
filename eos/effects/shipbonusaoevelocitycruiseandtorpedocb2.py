# shipBonusAoeVelocityCruiseAndTorpedoCB2
#
# Used by:
# Ship: Golem
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(
        lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
        "aoeVelocity", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
