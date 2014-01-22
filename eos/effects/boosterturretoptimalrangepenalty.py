# Used by:
# Implant: Improved Blue Pill Booster
# Implant: Improved Mindflood Booster
# Implant: Improved Sooth Sayer Booster
# Implant: Standard Blue Pill Booster
# Implant: Standard Mindflood Booster
# Implant: Standard Sooth Sayer Booster
# Implant: Strong Blue Pill Booster
# Implant: Strong Mindflood Booster
# Implant: Strong Sooth Sayer Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "maxRange", booster.getModifiedItemAttr("boosterTurretOptimalRange"))
