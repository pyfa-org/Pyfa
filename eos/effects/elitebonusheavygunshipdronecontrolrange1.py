# eliteBonusHeavyGunshipDroneControlRange1
#
# Used by:
# Ship: Ishtar
# Ship: 伊什塔级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    amount = ship.getModifiedItemAttr("eliteBonusHeavyGunship1") * level
    fit.extraAttributes.increase("droneControlRange", amount)
