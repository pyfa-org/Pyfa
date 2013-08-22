# Used by:
# Ship: Hoarder
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Industrial").level
    fit.ship.boostItemAttr("specialAmmoHoldCapacity", ship.getModifiedItemAttr("shipBonusMI2") * level)
