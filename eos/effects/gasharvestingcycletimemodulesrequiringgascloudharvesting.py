# Used by:
# Implants named like: Eifyr and Co. 'Alchemist' Gas Harvesting GH (3 of 3)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gas Cloud Harvesting"),
                                  "duration", implant.getModifiedItemAttr("durationBonus"))