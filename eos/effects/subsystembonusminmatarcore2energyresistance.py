type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusMinmatarCore2"), skill="Minmatar Core Systems")
