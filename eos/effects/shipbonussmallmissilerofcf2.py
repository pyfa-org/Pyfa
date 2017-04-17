# shipBonusSmallMissileRoFCF2
#
# Used by:
# Ship: Buzzard
# Ship: Hawk
# Ship: Pacifier
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
