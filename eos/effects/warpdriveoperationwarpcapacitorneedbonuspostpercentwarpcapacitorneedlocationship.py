# Used by:
# Implants named like: Eifyr and Co. 'Rogue' Warp Drive Operation WD (6 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", implant.getModifiedItemAttr("warpCapacitorNeedBonus"))
