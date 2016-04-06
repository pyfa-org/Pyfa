type = "passive"
def handler(fit, src, context):
    fit.ship.multiplyItemAttr("agility", src.getModifiedItemAttr("advancedCapitalAgility"), stackingPenalties=True)
