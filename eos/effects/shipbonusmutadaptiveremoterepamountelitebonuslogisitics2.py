# shipBonusMutadaptiveRemoteRepAmounteliteBonusLogisitics2
#
# Used by:
# Ship: Zarmazd
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "armorDamageAmount", src.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics Cruisers")
