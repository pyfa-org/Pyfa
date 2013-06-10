# Used by:
# Implant: Siege Warfare Mindlink
# Skill: Siege Warfare
type = "gang"
gangBoost = "shieldCapacity"
gangBonus = "shieldCapacityBonus"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus) * level)
