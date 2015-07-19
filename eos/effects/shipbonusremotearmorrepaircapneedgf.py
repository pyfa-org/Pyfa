# shipBonusRemoteArmorRepairCapNeedGF
#
# Used by:
# Ship: Navitas
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
