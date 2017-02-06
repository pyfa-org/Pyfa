# Not used by any item
type = "gang"
gangBoost = "shieldCapacity"
gangBonus = "shieldCapacityBonus"


def handler(fit, container, context):
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus))
