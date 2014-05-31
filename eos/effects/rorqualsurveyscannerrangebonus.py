# Used by:
# Ships from group: Capital Industrial Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Survey Scanner",
                                  "surveyScanRange", ship.getModifiedItemAttr("surveyScannerRangeBonus"))
