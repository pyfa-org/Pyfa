# Used by:
# Implants named like: Talisman (10 of 12)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Emission Systems"),
                                  "duration", implant.getModifiedItemAttr("durationBonus"))