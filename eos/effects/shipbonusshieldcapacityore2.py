# Used by:
# Variations of ship: Procurer (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Mining Barge").level
    fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("shipBonusORE2") * level)
