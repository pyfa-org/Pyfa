# shipSHTDmgBonusGF
#
# Used by:
# Ships named like: Incursus (3 of 3)
# Variations of ship: Incursus (3 of 3)
# Ship: Atron
# Ship: Federation Navy Comet
# Ship: Helios
# Ship: Police Pursuit Comet
# Ship: Taranis
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGF") * level)
