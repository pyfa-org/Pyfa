# shipBonusOreCapacityGI2
#
# Used by:
# Ship: Miasmos
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("specialOreHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2"), skill="Gallente Industrial")
