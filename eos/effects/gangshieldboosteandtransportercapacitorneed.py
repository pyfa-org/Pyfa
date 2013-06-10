# Used by:
# Variations of module: Siege Warfare Link - Shield Efficiency I (2 of 2)
type = "gang", "active"
gangBoost = "shieldRepairCapacitorNeed"
def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", module.getModifiedItemAttr("commandBonus"),
                                  stackingPenalties = True)
