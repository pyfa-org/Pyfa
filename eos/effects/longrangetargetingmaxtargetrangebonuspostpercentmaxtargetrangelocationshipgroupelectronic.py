# Used by:
# Implants named like: Zainou 'Gypsy' Long Range Targeting LT (6 of 6)
# Skill: Long Range Targeting
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("maxTargetRange", container.getModifiedItemAttr("maxTargetRangeBonus") * level)
