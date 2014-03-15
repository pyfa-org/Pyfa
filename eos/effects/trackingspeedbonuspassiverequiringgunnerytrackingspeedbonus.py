# Used by:
# Implants named like: Drop Booster (4 of 4)
# Implants named like: Eifyr and Co. 'Gunslinger' Motion Prediction MR (6 of 6)
# Implant: Ogdin's Eye Coordination Enhancer
# Skill: Motion Prediction
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", container.getModifiedItemAttr("trackingSpeedBonus") * level)
