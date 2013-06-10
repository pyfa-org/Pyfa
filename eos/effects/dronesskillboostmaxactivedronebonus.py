# Used by:
# Skill: Drones
type = "passive"
def handler(fit, skill, context):
    amount = skill.getModifiedItemAttr("maxActiveDroneBonus") * skill.level
    fit.extraAttributes.increase("maxActiveDrones", amount)
