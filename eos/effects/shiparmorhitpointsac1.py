type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorHP", src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
