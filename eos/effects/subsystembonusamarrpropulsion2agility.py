type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"), skill="Amarr Propulsion Systems")
