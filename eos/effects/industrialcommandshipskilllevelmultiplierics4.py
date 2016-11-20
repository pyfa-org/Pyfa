# industrialCommandShipSkillLevelMultiplierICS4
#
# Used by:
# Skill: Industrial Command Ships
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.ship.multiplyItemAttr("shipBonusICS4", src.getModifiedItemAttr("skillLevel") * lvl)
