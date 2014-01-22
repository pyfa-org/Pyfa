# Used by:
# Implant: Improved Crash Booster
# Implant: Improved Drop Booster
# Implant: Improved Frentix Booster
# Implant: Improved Sooth Sayer Booster
# Implant: Standard Crash Booster
# Implant: Standard Drop Booster
# Implant: Standard Frentix Booster
# Implant: Standard Sooth Sayer Booster
# Implant: Strong Crash Booster
# Implant: Strong Drop Booster
# Implant: Strong Frentix Booster
# Implant: Strong Sooth Sayer Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.ship.boostItemAttr("maxVelocity", booster.getModifiedItemAttr("boosterMaxVelocityPenalty"))
