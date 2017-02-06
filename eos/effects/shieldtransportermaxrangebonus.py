# shieldTransporterMaxRangeBonus
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
# Ship: Osprey
# Ship: Rorqual
# Ship: Scythe
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster", "maxRange",
                                  ship.getModifiedItemAttr("maxRangeBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Shield Booster", "maxRange",
                                  ship.getModifiedItemAttr("maxRangeBonus"))
