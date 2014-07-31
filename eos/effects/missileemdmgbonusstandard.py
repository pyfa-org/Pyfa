# Used by:
# Implants named like: Zainou 'Snapshot' Light Missiles LM (6 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))
