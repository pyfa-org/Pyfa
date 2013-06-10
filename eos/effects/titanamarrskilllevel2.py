# Used by:
# Skill: Amarr Titan
type = "passive"
def handler(fit, skill, context):
    fit.ship.multiplyItemAttr("titanAmarrBonus2", skill.level)
