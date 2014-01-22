# Used by:
# Implant: Eifyr and Co. 'Alchemist' Gas Harvesting GH-801
# Implant: Eifyr and Co. 'Alchemist' Gas Harvesting GH-803
# Implant: Eifyr and Co. 'Alchemist' Gas Harvesting GH-805
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gas Cloud Harvesting"),
                                  "duration", implant.getModifiedItemAttr("durationBonus"))