# shipHTDmgBonusfixedGC
#
# Used by:
# Ships named like: Thorax (3 of 3)
# Ships named like: Vexor (3 of 4)
# Ship: Adrestia
# Ship: Arazu
# Ship: Deimos
# Ship: Exequror Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC") * level)
