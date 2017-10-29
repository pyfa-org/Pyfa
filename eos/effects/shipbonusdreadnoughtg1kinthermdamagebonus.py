# shipBonusDreadnoughtG1KinThermDamageBonus
#
# Used by:
# Ship: Caiman
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "kineticDamage",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "kineticDamage",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
