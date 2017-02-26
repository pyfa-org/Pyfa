# Not used by any item
type = "active", "projected"


def handler(fit, module, context):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                           stackingPenalties=True, remoteResists=True)
