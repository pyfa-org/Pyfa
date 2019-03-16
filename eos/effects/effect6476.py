# doomsdayAOEWeb
#
# Used by:
# Module: Stasis Webification Burst Projector
# Structure Module: Standup Stasis Webification Burst Projector
type = "active", "projected"


def handler(fit, module, context, *args, **kwargs):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                           stackingPenalties=True, *args, **kwargs)
