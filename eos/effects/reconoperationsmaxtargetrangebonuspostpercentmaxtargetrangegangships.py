# Used by:
# Implant: Information Warfare Mindlink
# Skill: Information Warfare
type = "gang"
gangBoost = "maxTargetRange"
gangBonus = "maxTargetRangeBonus"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus) * level)
