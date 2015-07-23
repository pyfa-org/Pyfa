# subsystemBonusGallenteDefensive2RemoteArmorRepairAmount
#
# Used by:
# Subsystem: Proteus Defensive - Adaptive Augmenter
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusGallenteDefensive2"), skill="Gallente Defensive Systems")
