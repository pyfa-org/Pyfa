# caldariShipEwStrengthCB
#
# Used by:
# Ship: Scorpion
type = "passive"


def handler(fit, ship, context):
    for sensorType in ("Gravimetric", "Ladar", "Magnetometric", "Radar"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Electronic Warfare"),
                                      "scan{0}StrengthBonus".format(sensorType),
                                      ship.getModifiedItemAttr("shipBonusCB"), stackingPenalties=True,
                                      skill="Caldari Battleship")
