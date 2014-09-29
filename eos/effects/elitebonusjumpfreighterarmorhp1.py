# eliteBonusJumpFreighterArmorHP1
#
# Used by:
# Ship: Anshar
# Ship: Ark
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Jump Freighters").level
    fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("eliteBonusJumpFreighter1") * level)
