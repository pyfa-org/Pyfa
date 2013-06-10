# Used by:
# Ships from group: Jump Freighter (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Jump Freighters").level
    fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("eliteBonusJumpFreighter1") * level)
