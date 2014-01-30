# Used by:
# Implant: Eifyr and Co. 'Alchemist' Neurotoxin Recovery NR-1003
# Implant: Eifyr and Co. 'Alchemist' Neurotoxin Recovery NR-1005
# Skill: Neurotoxin Recovery
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    for i in xrange(5):
        attr = "boosterEffectChance{0}".format(i+1)
        fit.boosters.filteredItemBoost(lambda booster: attr in booster.itemModifiedAttributes,
                                       attr, container.getModifiedItemAttr("boosterChanceBonus") * level)
