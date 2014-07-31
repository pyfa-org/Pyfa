# Used by:
# Ships from group: Marauder (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", ship.getModifiedItemAttr("eliteBonusViolatorsRole3"))
