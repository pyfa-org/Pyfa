# shipBonusMutadaptiveRepAmountPC1
#
# Used by:
# Ship: Rodiva
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "armorDamageAmount", src.getModifiedItemAttr("shipBonusPC1"), skill="Precursor Cruiser")
