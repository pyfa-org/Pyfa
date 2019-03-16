# shipBonusHybridTrackingGF2
#
# Used by:
# Ship: Ares
# Ship: Federation Navy Comet
# Ship: Pacifier
# Ship: Tristan
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
