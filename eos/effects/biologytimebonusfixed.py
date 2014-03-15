# Used by:
# Implants named like: Eifyr and Co. 'Alchemist' Biology BY (2 of 2)
# Skill: Biology
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.boosters.filteredItemBoost(lambda bst: True, "boosterDuration", container.getModifiedItemAttr("durationBonus") * level)
