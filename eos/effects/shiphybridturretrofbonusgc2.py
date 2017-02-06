# shipHybridTurretROFBonusGC2
#
# Used by:
# Ship: Exequror Navy Issue
# Ship: Phobos
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
