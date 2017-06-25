type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion"), skill="Caldari Propulsion Systems")
