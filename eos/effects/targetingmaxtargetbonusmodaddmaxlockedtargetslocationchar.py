# targetingMaxTargetBonusModAddMaxLockedTargetsLocationChar
#
# Used by:
# Skills named like: Target Management (2 of 2)
type = "passive"


def handler(fit, skill, context):
    amount = skill.getModifiedItemAttr("maxTargetBonus") * skill.level
    fit.extraAttributes.increase("maxTargetsLockedFromSkills", amount)
