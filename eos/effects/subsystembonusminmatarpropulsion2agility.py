type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                           skill="Minmatar Propulsion Systems")
