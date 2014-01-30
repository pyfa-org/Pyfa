# Used by:
# Implant: Low-grade Talisman Alpha
# Implant: Low-grade Talisman Beta
# Implant: Low-grade Talisman Delta
# Implant: Low-grade Talisman Epsilon
# Implant: Low-grade Talisman Gamma
# Implant: Talisman Alpha
# Implant: Talisman Beta
# Implant: Talisman Delta
# Implant: Talisman Epsilon
# Implant: Talisman Gamma
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                  "duration", implant.getModifiedItemAttr("durationBonus"))
