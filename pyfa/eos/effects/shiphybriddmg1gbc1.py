# shipHybridDmg1GBC1
#
# Used by:
# Variations of ship: Brutix (3 of 3)
# Ship: Brutix Serpentis Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC1") * level)
