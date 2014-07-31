# Used by:
# Ships from group: Black Ops (4 of 4)
type = "passive"
def handler(fit, ship, context):
    if fit.extraAttributes["cloaked"]:
        level = fit.character.getSkill("Black Ops").level
        fit.ship.multiplyItemAttr("maxVelocity", ship.getModifiedItemAttr("eliteBonusBlackOps2") * level)
