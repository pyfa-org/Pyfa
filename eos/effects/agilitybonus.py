type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("agility", src.getModifiedItemAttr("agilityBonusAdd"))
