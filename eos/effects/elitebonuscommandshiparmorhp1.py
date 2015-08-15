# eliteBonusCommandShipArmorHP1
#
# Used by:
# Ship: Damnation
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")