# shipBonusMutadaptiveRemoteRepCapNeedeliteBonusLogisitics1
#
# Used by:
# Ship: Zarmazd
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "capacitorNeed", src.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics Cruisers")
