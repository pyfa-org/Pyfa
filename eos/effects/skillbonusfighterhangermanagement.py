type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.ship.boostItemAttr("fighterCapacity", src.getModifiedItemAttr("skillBonusFighterHangerSize") * lvl)
