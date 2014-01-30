# Used by:
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Targeting Implants > Implant Slot 08 (6 of 6)
# Skill: Long Range Targeting
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("maxTargetRange", container.getModifiedItemAttr("maxTargetRangeBonus") * level)
