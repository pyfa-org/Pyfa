# Used by:
# Ship: Panther
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Black Ops").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("eliteBonusBlackOps1") * level)