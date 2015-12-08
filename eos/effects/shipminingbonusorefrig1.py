# shipMiningBonusOREfrig1
#
# Used by:
# Ships from group: Expedition Frigate (2 of 2)
# Ship: Venture
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", module.getModifiedItemAttr("shipBonusOREfrig1"), skill="Mining Frigate")
