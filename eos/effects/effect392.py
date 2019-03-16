# mechanicHullHpBonusPostPercentHpShip
#
# Used by:
# Implants named like: Inherent Implants 'Noble' Mechanic MC (6 of 6)
# Modules named like: Transverse Bulkhead (8 of 8)
# Skill: Mechanics
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("hp", container.getModifiedItemAttr("hullHpBonus") * level)
