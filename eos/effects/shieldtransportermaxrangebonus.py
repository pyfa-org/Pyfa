# shieldTransporterMaxRangeBonus
#
# Used by:
# Ship: Osprey
# Ship: Scythe
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "shieldTransferRange", ship.getModifiedItemAttr("maxRangeBonus"))
