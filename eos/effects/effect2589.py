# modifyBoosterEffectChanceWithBoosterChanceBonusPostPercent
#
# Used by:
# Implants named like: Eifyr and Co. 'Alchemist' Neurotoxin Recovery NR (2 of 2)
# Skill: Neurotoxin Recovery
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    for i in range(5):
        attr = "boosterEffectChance{0}".format(i + 1)
        fit.boosters.filteredItemBoost(lambda booster: attr in booster.itemModifiedAttributes,
                                       attr, container.getModifiedItemAttr("boosterChanceBonus") * level)
