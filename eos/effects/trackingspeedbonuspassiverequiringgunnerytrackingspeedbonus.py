# Used by:
# Implants named like: Eifyr and Co. Prediction MR (6 of 6)
# Implant: Improved Drop Booster
# Implant: Ogdin's Eye Coordination Enhancer
# Implant: Standard Drop Booster
# Implant: Strong Drop Booster
# Implant: Synth Drop Booster
# Skill: Motion Prediction
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", container.getModifiedItemAttr("trackingSpeedBonus") * level)
