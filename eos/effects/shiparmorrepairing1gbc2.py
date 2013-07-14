# Used by:
# Variations of ship: Brutix (3 of 4)
# Ship: Myrmidon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGBC2") * level)
