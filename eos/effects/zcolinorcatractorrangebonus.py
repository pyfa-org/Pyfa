# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", ship.getModifiedItemAttr("shipOrcaTractorBeamRangeBonus1"))
