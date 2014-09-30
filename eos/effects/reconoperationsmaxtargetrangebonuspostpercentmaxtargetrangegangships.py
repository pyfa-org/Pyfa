# reconOperationsMaxTargetRangeBonusPostPercentMaxTargetRangeGangShips
#
# Used by:
# Implant: Caldari Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
# Implant: Information Warfare Mindlink
# Skill: Information Warfare
type = "gang"
gangBoost = "maxTargetRange"
gangBonus = "maxTargetRangeBonus"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus) * level)
