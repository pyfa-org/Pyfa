# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Survey Scanner",
                                  "surveyScanRange", ship.getModifiedItemAttr("surveyScannerRangeBonus"))
