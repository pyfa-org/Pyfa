# Used by:
# Skill: Gallente Titan
type = "passive"
def handler(fit, skill, context):
    fit.ship.multiplyItemAttr("titanGallenteBonus2", skill.level)
