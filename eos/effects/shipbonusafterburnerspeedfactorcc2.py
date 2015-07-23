# shipBonusAfterburnerSpeedFactorCC2
#
# Used by:
# Ship: Phantasm
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
