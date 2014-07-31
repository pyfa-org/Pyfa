# Used by:
# Ship: Augoror
# Ship: Exequror
# Ship: Inquisitor
# Ship: Navitas
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))
