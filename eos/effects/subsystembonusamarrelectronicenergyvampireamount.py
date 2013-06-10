# Used by:
# Subsystem: Legion Electronics - Energy Parasitic Complex
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Electronic Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferAmount", module.getModifiedItemAttr("subsystemBonusAmarrElectronic") * level)
