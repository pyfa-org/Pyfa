# Used by:
# Skill: Multitasking
# Skill: Targeting
type = "passive"
def handler(fit, skill, context):
    amount = skill.getModifiedItemAttr("maxTargetBonus") * skill.level
    fit.extraAttributes.increase("maxTargetsLockedFromSkills", amount)
