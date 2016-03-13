# shipBonusRemoteArmorRepairCapNeedGF
#
# Used by:
# Variations of ship: Navitas (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
