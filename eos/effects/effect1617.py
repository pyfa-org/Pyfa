# shipCapitalAgilityBonus
#
# Used by:
# Items from market group: Ships > Capital Ships (31 of 40)
type = "passive"


def handler(fit, src, context):
    fit.ship.multiplyItemAttr("agility", src.getModifiedItemAttr("advancedCapitalAgility"), stackingPenalties=True)
