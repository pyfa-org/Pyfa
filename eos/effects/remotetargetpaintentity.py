# remoteTargetPaintEntity
#
# Used by:
# Drones named like: TP (3 of 3)
type = "projected", "active"


def handler(fit, container, context, *args, **kwargs):
    if "projected" in context:
        fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties=True, *args, **kwargs)
