# Used by:
# Implants named like: Eifyr and Co. 'Alchemist' Nanite Control NC (2 of 2)
# Implants named like: Low grade Edge (5 of 6)
# Skill: Nanite Control
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    attrs = ("boosterShieldBoostAmountPenalty", "boosterShieldCapacityPenalty", "shieldBoostMultiplier")
    for attr in attrs:
        # shieldBoostMultiplier can be positive (Blue Pill) and negative value (other boosters)
        # We're interested in decreasing only side-effects
        fit.boosters.filteredItemBoost(lambda booster: booster.getModifiedItemAttr(attr) < 0,
                                       attr, container.getModifiedItemAttr("boosterAttributeModifier") * level)
