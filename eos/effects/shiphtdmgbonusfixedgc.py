# Used by:
# Variations of ship: Thorax (3 of 4)
# Variations of ship: Vexor (3 of 4)
# Ship: Adrestia
# Ship: Arazu
# Ship: Exequror Navy Issue
# Ship: Lachesis
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC") * level)
