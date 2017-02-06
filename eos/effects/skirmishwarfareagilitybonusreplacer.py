# Not used by any item
type = "gang"
gangBoost = "agility"
gangBonus = "agilityBonus"


def handler(fit, container, context):
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus))
