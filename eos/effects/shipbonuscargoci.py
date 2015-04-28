# shipBonusCargoCI
#
# Used by:
# Variations of ship: Badger (2 of 2)
# Ship: Tayra
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Industrial").level
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusCI") * level)
