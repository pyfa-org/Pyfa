# Used by:
# Variations of ship: Myrmidon (2 of 2)
# Ship: Astarte
# Ship: Brutix
# Ship: Brutix Serpentis Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGBC2") * level)
