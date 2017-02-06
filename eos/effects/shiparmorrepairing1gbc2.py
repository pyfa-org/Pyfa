# shipArmorRepairing1GBC2
#
# Used by:
# Variations of ship: Myrmidon (2 of 2)
# Ship: Astarte
# Ship: Brutix
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGBC2"),
                                  skill="Gallente Battlecruiser")
