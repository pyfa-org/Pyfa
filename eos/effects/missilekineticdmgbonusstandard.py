# Used by:
# Implants named like: Zainou 'Snapshot' Light Missiles LM (6 of 6)
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))
