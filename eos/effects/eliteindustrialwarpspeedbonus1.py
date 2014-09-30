# eliteIndustrialWarpSpeedBonus1
#
# Used by:
# Ships from group: Blockade Runner (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    fit.ship.boostItemAttr("warpSpeedMultiplier", ship.getModifiedItemAttr("eliteBonusIndustrial1") * level)
