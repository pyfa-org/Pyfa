# Used by:
# Implants named like: Low grade Talisman (10 of 12)
# Implants named like: Talisman (15 of 18)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                  "duration", implant.getModifiedItemAttr("durationBonus"))
