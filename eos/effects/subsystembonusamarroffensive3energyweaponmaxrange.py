# Used by:
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusAmarrOffensive3") * level)
