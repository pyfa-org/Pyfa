type = "passive"
def handler(fit, src, context):
    fit.ship.filteredItemBoost("scanResolution", src.getModifiedItemAttr("structureRigScanResBonus"),
                            stackingPenalties=True)
