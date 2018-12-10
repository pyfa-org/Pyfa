# shipBonusMutadaptiveRemoteRepRangePC1
#
# Used by:
# Ship: Zarmazd
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "maxRange", src.getModifiedItemAttr("shipBonusPC1"), skill="Precursor Cruiser")
