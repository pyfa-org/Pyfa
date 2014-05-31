type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    fit.ship.boostItemAttr("warpSpeedMultiplier", ship.getModifiedItemAttr("eliteBonusIndustrial1") * level)
