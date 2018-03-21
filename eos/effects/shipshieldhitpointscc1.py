type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
