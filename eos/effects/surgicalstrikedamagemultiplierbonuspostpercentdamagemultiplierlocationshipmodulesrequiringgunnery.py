# Used by:
# Implants named like: Cerebral Accelerator (3 of 3)
# Implants named like: Eifyr and Co. 'Gunslinger' Surgical Strike SS (6 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "damageMultiplier", implant.getModifiedItemAttr("damageMultiplierBonus"))
