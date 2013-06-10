# Used by:
# Subsystem: Proteus Propulsion - Localized Injectors
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Propulsion Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "capacitorNeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion") * level)
