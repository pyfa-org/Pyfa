# shipECMScanStrengthBonusCF
#
# Used by:
# Variations of ship: Griffin (3 of 3)
type = "passive"


def handler(fit, ship, context):
    for type in ("Gravimetric", "Ladar", "Radar", "Magnetometric"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scan{0}StrengthBonus".format(type),
                                      ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
