# shipBonusRemoteRepairRangePirateFaction2
#
# Used by:
# Ship: Nestor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusPirateFaction2"))
