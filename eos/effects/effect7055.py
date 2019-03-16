# shipLargeWeaponsDamageBonus
#
# Used by:
# Ship: Praxis
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "explosiveDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosiveDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "explosiveDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusRole7"))
