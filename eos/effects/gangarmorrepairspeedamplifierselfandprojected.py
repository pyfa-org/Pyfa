# gangArmorRepairSpeedAmplifierSelfAndProjected
#
# Used by:
# Variations of module: Armored Warfare Link - Rapid Repair I (2 of 2)
type = "gang", "active"
gangBoost = "armorRepairDuration"
runTime = "late"

def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "duration", module.getModifiedItemAttr("commandBonus"))
