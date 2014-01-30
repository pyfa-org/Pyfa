# Used by:
# Implants named like: Eifyr Strike (6 of 6)
# Implant: Advanced Cerebral Accelerator
# Implant: Prototype Cerebral Accelerator
# Implant: Standard Cerebral Accelerator
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "damageMultiplier", implant.getModifiedItemAttr("damageMultiplierBonus"))
