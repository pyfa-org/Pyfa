type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                           skill="Caldari Propulsion Systems")
