# shipBonusAoeVelocityCruiseAndTorpedoCB2
#
# Used by:
# Ships named like: Golem (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonus2CB") * level)
