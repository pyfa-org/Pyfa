# Used by:
# Implant: Improved Crash Booster
# Implant: Improved Exile Booster
# Implant: Improved Frentix Booster
# Implant: Improved X-Instinct Booster
# Implant: Standard Crash Booster
# Implant: Standard Exile Booster
# Implant: Standard Frentix Booster
# Implant: Standard X-Instinct Booster
# Implant: Strong Crash Booster
# Implant: Strong Exile Booster
# Implant: Strong Frentix Booster
# Implant: Strong X-Instinct Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.ship.boostItemAttr("armorHP", booster.getModifiedItemAttr("boosterArmorHPPenalty"))
