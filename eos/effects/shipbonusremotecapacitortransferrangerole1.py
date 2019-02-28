# shipBonusRemoteCapacitorTransferRangeRole1
#
# Used by:
# Variations of ship: Rodiva (2 of 2)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter", "maxRange", src.getModifiedItemAttr("shipBonusRole1"))
