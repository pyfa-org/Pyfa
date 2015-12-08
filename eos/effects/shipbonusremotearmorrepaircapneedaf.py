# shipBonusRemoteArmorRepairCapNeedAF
#
# Used by:
# Ship: Deacon
# Ship: Inquisitor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
