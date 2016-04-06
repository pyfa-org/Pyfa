# shipCapitalAgilityBonus
#
# Used by:
# Ships from group: Supercarrier (5 of 5)
# Items from market group: Ships > Capital Ships (22 of 32)
type = "passive"
def handler(fit, src, context):
    fit.ship.multiplyItemAttr("agility", src.getModifiedItemAttr("advancedCapitalAgility"), stackingPenalties=True)
