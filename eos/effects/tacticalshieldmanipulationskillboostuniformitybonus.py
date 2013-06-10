# Used by:
# Skill: Tactical Shield Manipulation
type = "passive"
def handler(fit, skill, context):
    fit.ship.increaseItemAttr("shieldUniformity", skill.getModifiedItemAttr("uniformityBonus") * skill.level)
