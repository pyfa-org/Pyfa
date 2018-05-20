# Not used by any item
type = "projected", "active"


def handler(fit, container, context, *args, **kwargs):
    if "projected" in context:
        fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties=True, *args, **kwargs)
