# Used by:
# Ship: Sin
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Black Ops").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("eliteBonusBlackOps1") * level)