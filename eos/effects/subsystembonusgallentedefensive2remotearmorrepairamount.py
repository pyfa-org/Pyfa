# subsystemBonusGallenteDefensive2RemoteArmorRepairAmount
#
# Used by:
# Subsystem: Proteus Defensive - Adaptive Augmenter
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Defensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusGallenteDefensive2") * level)
