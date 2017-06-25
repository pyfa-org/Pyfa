# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.forceItemAttr("warpBubbleImmune", module.getModifiedItemAttr("warpBubbleImmuneModifier"))
