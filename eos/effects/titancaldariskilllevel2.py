# Used by:
# Skill: Caldari Titan
type = "passive"
def handler(fit, skill, context):
    fit.ship.multiplyItemAttr("shipBonusCT2", skill.level)
