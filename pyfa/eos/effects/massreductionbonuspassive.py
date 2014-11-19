# massReductionBonusPassive
#
# Used by:
# Modules named like: Higgs Anchor I (4 of 4)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("mass", module.getModifiedItemAttr("massBonusPercentage"), stackingPenalties=True)
