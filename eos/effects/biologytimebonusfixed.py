# Used by:
# Implant: Eifyr and Co. 'Alchemist' Biology BY-805
# Implant: Eifyr and Co. 'Alchemist' Biology BY-810
# Skill: Biology
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.boosters.filteredItemBoost(lambda bst: True, "boosterDuration", container.getModifiedItemAttr("durationBonus") * level)
