# shipMissileRoFMF2
#
# Used by:
# Ship: Breacher
# Ship: Jaguar
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
