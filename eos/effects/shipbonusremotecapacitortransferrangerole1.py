# shipBonusRemoteCapacitorTransferRangeRole1
#
# Used by:
# Ship: Rodiva
# Ship: Zarmazd
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter", "maxRange", src.getModifiedItemAttr("shipBonusRole1"))
