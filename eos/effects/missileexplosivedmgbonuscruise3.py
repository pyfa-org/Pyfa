# Used by:
# Implants named like: Missiles CM (6 of 6)
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "explosiveDamage",container.getModifiedItemAttr("damageMultiplierBonus"))
