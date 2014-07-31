# Used by:
# Subsystem: Proteus Defensive - Nanobot Injector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Defensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusGallenteDefensive") * level)
