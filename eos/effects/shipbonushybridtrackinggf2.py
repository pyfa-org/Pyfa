# shipBonusHybridTrackingGF2
#
# Used by:
# Ships named like: Tristan (2 of 2)
# Ship: Ares
# Ship: Federation Navy Comet
# Ship: Police Pursuit Comet
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                    "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF2") * level)
