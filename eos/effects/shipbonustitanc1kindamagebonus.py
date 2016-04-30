# shipBonusTitanC1KinDamageBonus
#
# Used by:
# Ship: Leviathan
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "kineticDamage", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "kineticDamage", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "kineticDamage", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
