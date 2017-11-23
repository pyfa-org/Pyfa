type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Shield Boost"

# Attribute that this effect targets
attr = "boosterShieldBoostAmountPenalty"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"), "shieldBonus",
                                  src.getModifiedItemAttr("boosterShieldBoostAmountPenalty"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"), "shieldBonus",
                                  src.getModifiedItemAttr("boosterShieldBoostAmountPenalty"))
