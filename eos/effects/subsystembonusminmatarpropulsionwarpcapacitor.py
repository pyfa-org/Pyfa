type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                           skill="Minmatar Propulsion Systems")
