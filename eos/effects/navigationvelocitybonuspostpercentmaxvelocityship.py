# Used by:
# Modules named like: Auxiliary Thrusters (8 of 8)
# Implant: Low-grade Snake Beta
# Implant: Low-grade Snake Delta
# Implant: Low-grade Snake Epsilon
# Implant: Low-grade Snake Gamma
# Implant: Low-grade Snake Omega
# Implant: Quafe Zero
# Implant: Snake Alpha
# Implant: Snake Beta
# Implant: Snake Delta
# Implant: Snake Epsilon
# Implant: Snake Gamma
# Implant: Snake Omega
# Skill: Navigation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    amount = container.getModifiedItemAttr("velocityBonus") or 0
    fit.ship.boostItemAttr("maxVelocity", amount * level,
                           stackingPenalties = "skill" not in context and "implant" not in context and "booster" not in context)
