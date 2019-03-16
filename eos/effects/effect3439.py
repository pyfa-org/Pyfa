# eliteBonusViolatorsEwTargetPainting1
#
# Used by:
# Ship: Golem
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusViolators1"),
                                  skill="Marauders")
