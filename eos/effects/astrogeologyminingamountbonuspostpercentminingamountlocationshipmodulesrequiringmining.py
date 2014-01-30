# Used by:
# Implant: Inherent Implants 'Highwall' Mining MX-1001
# Implant: Inherent Implants 'Highwall' Mining MX-1003
# Implant: Inherent Implants 'Highwall' Mining MX-1005
# Implant: Michi's Excavation Augmentor
# Skill: Astrogeology
# Skill: Mining
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", container.getModifiedItemAttr("miningAmountBonus") * level)
