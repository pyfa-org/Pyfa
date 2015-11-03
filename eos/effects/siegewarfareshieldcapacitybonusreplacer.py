# siegeWarfareShieldCapacityBonusReplacer
#
# Used by:
# Implant: Caldari Navy Warfare Mindlink
# Implant: Republic Fleet Warfare Mindlink
# Implant: Siege Warfare Mindlink
type = "gang"
gangBoost = "shieldCapacity"
gangBonus = "shieldCapacityBonus"
def handler(fit, container, context):
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus) * level)
