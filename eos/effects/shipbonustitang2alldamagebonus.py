# shipBonusTitanG2AllDamageBonus
#
# Used by:
# Ship: Komodo
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "explosiveDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "emDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "emDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "explosiveDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "emDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "explosiveDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
