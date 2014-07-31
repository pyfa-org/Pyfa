# Used by:
# Implants named like: Zainou 'Snapshot' Torpedoes TD (6 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))
