# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("structureRigScanResBonus"),
                           stackingPenalties=True)
