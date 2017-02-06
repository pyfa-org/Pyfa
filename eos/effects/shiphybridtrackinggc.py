# shipHybridTrackingGC
#
# Used by:
# Ship: Lachesis
# Ship: Phobos
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
