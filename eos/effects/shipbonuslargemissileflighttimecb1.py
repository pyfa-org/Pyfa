# shipBonusLargeMissileFlightTimeCB1
#
# Used by:
# Ship: Marshal
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosionDelay",
                                    src.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "explosionDelay",
                                    src.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
