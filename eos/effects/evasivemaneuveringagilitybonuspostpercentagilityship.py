# evasiveManeuveringAgilityBonusPostPercentAgilityShip
#
# Used by:
# Modules from group: Rig Anchor (4 of 4)
# Implants named like: Eifyr and Co. 'Rogue' Evasive Maneuvering EM (6 of 6)
# Implants named like: grade Nomad (10 of 12)
# Modules named like: Low Friction Nozzle Joints (8 of 8)
# Implant: Genolution Core Augmentation CA-4
# Skill: Evasive Maneuvering
# Skill: Spaceship Command
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("agility", container.getModifiedItemAttr("agilityBonus") * level,
                           stackingPenalties="skill" not in context and "implant" not in context)
