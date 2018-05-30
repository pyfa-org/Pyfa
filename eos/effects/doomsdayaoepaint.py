# doomsdayAOEPaint
#
# Used by:
# Module: Target Illumination Burst Projector
# Structure Module: Standup Target Illumination Burst Projector
type = "projected", "active"


def handler(fit, container, context, *args, **kwargs):
    if "projected" in context:
        fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties=True, *args, **kwargs)
