# Used by:
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Armor Implants > Implant Slot 08 (6 of 6)
# Skill: Mechanics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("hp", container.getModifiedItemAttr("hullHpBonus") * level)
