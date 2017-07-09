type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                           skill="Caldari Propulsion Systems")
