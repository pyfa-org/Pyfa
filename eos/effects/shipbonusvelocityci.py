# Used by:
# Variations of ship: Badger (2 of 2)
# Variations of ship: Badger Mark II (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Industrial").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusCI") * level)
