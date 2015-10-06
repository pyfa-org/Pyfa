# surgicalStrikeDamageMultiplierBonusPostPercentDamageMultiplierLocationShipModulesRequiringGunnery
#
# Used by:
# Implants named like: Cerebral Accelerator (5 of 5)
# Implants named like: Eifyr and Co. 'Gunslinger' Surgical Strike SS (6 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "damageMultiplier", implant.getModifiedItemAttr("damageMultiplierBonus"))
