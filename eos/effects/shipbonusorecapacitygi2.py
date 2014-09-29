# shipBonusOreCapacityGI2
#
# Used by:
# Ship: Miasmos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Industrial").level
    fit.ship.boostItemAttr("specialOreHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2") * level)
