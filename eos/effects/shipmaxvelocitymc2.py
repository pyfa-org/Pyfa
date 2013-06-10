# Used by:
# Ship: Vagabond
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusMC2") * level)
