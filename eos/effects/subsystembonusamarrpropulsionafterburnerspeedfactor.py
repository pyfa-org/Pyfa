# Used by:
# Subsystem: Legion Propulsion - Fuel Catalyst
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Propulsion Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion") * level)
