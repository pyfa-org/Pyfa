# Used by:
# Skill: Minmatar Titan
type = "passive"
def handler(fit, skill, context):
    fit.ship.multiplyItemAttr("titanMinmatarBonus2", skill.level)
