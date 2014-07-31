# Used by:
# Implants named like: Inherent Implants 'Highwall' Mining MX (3 of 3)
# Implant: Michi's Excavation Augmentor
# Skill: Astrogeology
# Skill: Mining
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", container.getModifiedItemAttr("miningAmountBonus") * level)
