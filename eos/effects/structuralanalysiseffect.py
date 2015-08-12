# structuralAnalysisEffect
#
# Used by:
# Implants named like: Inherent Implants 'Noble' Repair Proficiency RP (6 of 6)
# Modules named like: Auxiliary Nano Pump (8 of 8)
# Modules named like: QA Multiship Module Players (4 of 4)
# Implant: Imperial Navy Modified 'Noble' Implant
type = "passive"
def handler(fit, container, context):
    penalized = "implant" not in context
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", container.getModifiedItemAttr("repairBonus"),
                                  stackingPenalties=penalized)
