# shipBonusTitanC5AllDamageBonus
#
# Used by:
# Ship: Leviathan
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "emDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosiveDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "thermalDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "explosiveDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "thermalDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "emDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "thermalDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "emDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "explosiveDamage", src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
