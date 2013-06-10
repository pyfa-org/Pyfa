# Used by:
# Modules named like: Drone Control Range Augmentor (8 of 8)
# Skill: Electronic Warfare Drone Interfacing
# Skill: Scout Drone Operation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    amount = container.getModifiedItemAttr("droneRangeBonus") * level
    fit.extraAttributes.increase("droneControlRange", amount)
