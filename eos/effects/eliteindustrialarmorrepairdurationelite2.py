# Used by:
# Ship: Viator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "duration", ship.getModifiedItemAttr("eliteBonusIndustrial2") * level)
