# subsystemBonusAmarrPropulsionAfterburnerSpeedFactor
#
# Used by:
# Subsystem: Legion Propulsion - Fuel Catalyst
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"), skill="Amarr Propulsion Systems")
