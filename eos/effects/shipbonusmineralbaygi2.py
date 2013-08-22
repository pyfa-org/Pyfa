# Used by:
# Ship: Kryos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Industrial").level
    fit.ship.boostItemAttr("specialMineralHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2") * level)
