# shipBonusPICommoditiesHoldGI2
#
# Used by:
# Ship: Epithal
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Industrial").level
    fit.ship.boostItemAttr("specialPlanetaryCommoditiesHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2") * level)
