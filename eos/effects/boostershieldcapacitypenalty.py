# Used by:
# Implant: Improved Blue Pill Booster
# Implant: Improved Drop Booster
# Implant: Improved Sooth Sayer Booster
# Implant: Improved X-Instinct Booster
# Implant: Standard Blue Pill Booster
# Implant: Standard Drop Booster
# Implant: Standard Sooth Sayer Booster
# Implant: Standard X-Instinct Booster
# Implant: Strong Blue Pill Booster
# Implant: Strong Drop Booster
# Implant: Strong Sooth Sayer Booster
# Implant: Strong X-Instinct Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.ship.boostItemAttr("shieldCapacity", booster.getModifiedItemAttr("boosterShieldCapacityPenalty"))
