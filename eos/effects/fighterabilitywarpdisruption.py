# fighterAbilityWarpDisruption
#
# Used by:
# Fighters named like: Siren (4 of 4)
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""

# User-friendly name for the ability
displayName = "Warp Disruption"
prefix = "fighterAbilityWarpDisruption"
type = "active", "projected"
grouped = True


def handler(fit, src, context):
    if "projected" not in context:
        return
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("{}PointStrength".format(prefix)) * src.amountActive)
