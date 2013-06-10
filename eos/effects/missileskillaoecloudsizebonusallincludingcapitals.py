# Used by:
# Implants named like: Crash Booster (4 of 4)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Citadel Cruise Missiles") or mod.charge.requiresSkill("Citadel Torpedoes"),
                                    "aoeCloudSize", implant.getModifiedItemAttr("aoeCloudSizeBonus"))