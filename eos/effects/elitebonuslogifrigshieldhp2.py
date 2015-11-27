type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("eliteBonusLogiFrig2"), skill="Logistics Frigates")
