# shipCruiseAndTorpedoVelocityBonusCB3
#
# Used by:
# Ships named like: Golem (4 of 4)
# Ship: Widow
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3") * level)
