# caldariShipEwStrengthCB
#
# Used by:
# Ship: Scorpion
type = "passive"


def handler(fit, ship, context):
    for sensorType in ("Gravimetric", "Ladar", "Magnetometric", "Radar"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                                  (
                                                      "ECM",
                                                      "Burst Jammer",
                                                  ),
                                      "scan{0}StrengthBonus".format(sensorType),
                                      ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
