# shipBonusTitanG1KinThermDamageBonus
#
# Used by:
# Ship: Komodo
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "kineticDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "kineticDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
