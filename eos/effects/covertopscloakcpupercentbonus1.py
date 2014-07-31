# Used by:
# Ships from group: Covert Ops (5 of 5)
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    level = fit.character.getSkill("Covert Ops").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "cpu", ship.getModifiedItemAttr("eliteBonusCoverOps1") * level)
