type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("capacitorCapacity", src.getModifiedItemAttr("subsystemBonusCaldariCore"),
                           skill="Caldari Core Systems")
