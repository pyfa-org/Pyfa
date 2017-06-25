type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                           skill="Gallente Propulsion Systems")
