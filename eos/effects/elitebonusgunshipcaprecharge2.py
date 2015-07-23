# eliteBonusGunshipCapRecharge2
#
# Used by:
# Ship: Vengeance
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("rechargeRate", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")