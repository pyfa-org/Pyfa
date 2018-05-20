# Not used by any item
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""

# User-friendly name for the ability
displayName = "Stasis Webifier"
prefix = "fighterAbilityStasisWebifier"
type = "active", "projected"
grouped = True


def handler(fit, src, context):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("{}SpeedPenalty".format(prefix)) * src.amountActive,
                           stackingPenalties=True)
