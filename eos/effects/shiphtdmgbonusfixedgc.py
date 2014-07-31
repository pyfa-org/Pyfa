# Used by:
# Ships named like: Thorax (3 of 3)
# Variations of ship: Thorax (3 of 4)
# Ship: Adrestia
# Ship: Arazu
# Ship: Exequror Navy Issue
# Ship: Guardian-Vexor
# Ship: Lachesis
# Ship: Vexor
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC") * level)
