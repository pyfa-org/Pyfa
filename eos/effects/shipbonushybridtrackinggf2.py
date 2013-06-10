# Used by:
# Ship: Ares
# Ship: Federation Navy Comet
# Ship: Tristan
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                    "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF2") * level)
