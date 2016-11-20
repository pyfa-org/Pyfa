# shieldBoostAmplifier
#
# Used by:
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Shield Boost Amplifier (25 of 25)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
        "shieldBonus", module.getModifiedItemAttr("shieldBoostMultiplier"),
        stackingPenalties=True)
