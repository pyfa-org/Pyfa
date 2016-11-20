# oreCapitalShipSkillMultiplier5
#
# Used by:
# Skill: Capital Industrial Ships
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.ship.multiplyItemAttr("shipBonusORECapital5", src.getModifiedItemAttr("skillLevel") * lvl)
