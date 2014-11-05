# eliteBonusViolatorsEwTargetPainting1
#
# Used by:
# Ships named like: Golem (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusViolators1") * level)
