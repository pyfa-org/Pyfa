# Used by:
# Implant: Eifyr and Co. 'Alchemist' Nanite Control NC-903
# Implant: Eifyr and Co. 'Alchemist' Nanite Control NC-905
# Implant: Low-grade Edge Alpha
# Implant: Low-grade Edge Beta
# Implant: Low-grade Edge Delta
# Implant: Low-grade Edge Epsilon
# Implant: Low-grade Edge Gamma
# Skill: Neurotoxin Control
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    attrs = ("boosterShieldBoostAmountPenalty", "boosterShieldCapacityPenalty", "shieldBoostMultiplier")
    for attr in attrs:
        # shieldBoostMultiplier can be positive (Blue Pill) and negative value (other boosters)
        # We're interested in decreasing only side-effects
        fit.boosters.filteredItemBoost(lambda booster: booster.getModifiedItemAttr(attr) < 0,
                                       attr, container.getModifiedItemAttr("boosterAttributeModifier") * level)
