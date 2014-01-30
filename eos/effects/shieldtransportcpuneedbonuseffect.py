# Used by:
# Ship: Basilisk
# Ship: Etana
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "cpu", ship.getModifiedItemAttr("shieldTransportCpuNeedBonus"))
