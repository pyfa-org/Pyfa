# navigationVelocityBonusPostPercentMaxVelocityShip
#
# Used by:
# Modules from group: Rig Anchor (4 of 4)
# Implants named like: Agency 'Overclocker' SB Dose (3 of 4)
# Implants named like: grade Snake (16 of 18)
# Modules named like: Auxiliary Thrusters (8 of 8)
# Implant: Quafe Zero
# Skill: Navigation
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    amount = container.getModifiedItemAttr("velocityBonus") or 0
    fit.ship.boostItemAttr("maxVelocity", amount * level,
                           stackingPenalties="skill" not in context and "implant" not in context and "booster" not in context)
