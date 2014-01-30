# Used by:
# Skill: Advanced Target Management
# Skill: Target Management
type = "passive"
def handler(fit, skill, context):
    amount = skill.getModifiedItemAttr("maxTargetBonus") * skill.level
    fit.extraAttributes.increase("maxTargetsLockedFromSkills", amount)
