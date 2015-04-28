# shipBonusVelocityCI
#
# Used by:
# Variations of ship: Tayra (2 of 2)
# Ship: Crane
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Industrial").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusCI") * level)
