# Used by:
# Variations of ship: Ferox (2 of 2)
# Ship: Ferox Guristas Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCBC1") * level)
