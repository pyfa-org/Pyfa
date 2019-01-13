# shipBonusMutadaptiveRemoteRepairRangeRole3
#
# Used by:
# Ship: Rodiva
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "maxRange", src.getModifiedItemAttr("shipBonusRole3"))
