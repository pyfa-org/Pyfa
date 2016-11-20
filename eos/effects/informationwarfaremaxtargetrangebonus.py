# informationWarfareMaxTargetRangeBonus
#
# Used by:
# Implant: Caldari Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
# Implant: Information Warfare Mindlink
type = "gang"
gangBoost = "maxTargetRange"
gangBonus = "maxTargetRangeBonus"


def handler(fit, container, context):
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus))
