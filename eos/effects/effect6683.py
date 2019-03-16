# structureModuleEffectTargetPainter
#
# Used by:
# Variations of structure module: Standup Target Painter I (2 of 2)
type = "projected", "active"


def handler(fit, container, context, *args, **kwargs):
    if "projected" in context:
        fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties=True, *args, **kwargs)
