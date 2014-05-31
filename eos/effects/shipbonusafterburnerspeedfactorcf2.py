# Used by:
# Ship: Succubus
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("shipBonusCF2") * level)
