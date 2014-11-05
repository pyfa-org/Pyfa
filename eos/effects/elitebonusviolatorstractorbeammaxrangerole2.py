# eliteBonusViolatorsTractorBeamMaxRangeRole2
#
# Used by:
# Ships from group: Marauder (16 of 16)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusViolatorsRole2"))
