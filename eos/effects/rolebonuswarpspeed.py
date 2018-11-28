# roleBonusWarpSpeed
#
# Used by:
# Ship: Cynabal
# Ship: Dramiel
# Ship: Leopard
# Ship: Machariel
# Ship: Victorieux Luxury Yacht
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("shipRoleBonusWarpSpeed"))
