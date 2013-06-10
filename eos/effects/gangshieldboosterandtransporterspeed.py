# Used by:
# Variations of module: Siege Warfare Link - Active Shielding I (2 of 2)
type = "gang", "active"
gangBoost = "shieldRepairDuration"
def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Shield Emission Systems"),
                                  "duration", module.getModifiedItemAttr("commandBonus"),
                                  stackingPenalties = True)
