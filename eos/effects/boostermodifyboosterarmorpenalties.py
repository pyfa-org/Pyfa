# Used by:
# Implants named like: Eifyr and Co. 'Alchemist' Nanite Control NC (2 of 2)
# Implants named like: Low grade Edge (5 of 6)
# Skill: Nanite Control
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    attrs = ("boosterArmorHPPenalty", "boosterArmorRepairAmountPenalty")
    for attr in attrs:
        fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                       container.getModifiedItemAttr("boosterAttributeModifier") * level)
