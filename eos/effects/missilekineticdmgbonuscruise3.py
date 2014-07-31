# Used by:
# Implants named like: Zainou 'Snapshot' Cruise Missiles CM (6 of 6)
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))
