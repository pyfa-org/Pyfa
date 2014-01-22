# Used by:
# Implants named like: 'Snapshot' RD (6 of 6)
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))
