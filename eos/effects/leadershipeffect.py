# Used by:
# Skill: Leadership
type = "gang"
gangBoost = "scanResolution"
gangBonus = "scanResolutionBonus"
def handler(fit, skill, context):
    fit.ship.boostItemAttr(gangBoost, skill.getModifiedItemAttr(gangBonus) * skill.level)
