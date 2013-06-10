# Used by:
# Ship: Redeemer
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Black Ops").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusBlackOps1") * level)
