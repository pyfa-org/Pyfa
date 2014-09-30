# eliteBonusJumpFreighterShieldHP1
#
# Used by:
# Ship: Nomad
# Ship: Rhea
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Jump Freighters").level
    fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("eliteBonusJumpFreighter1") * level)
