# Used by:
# Implant: Improved Exile Booster
# Implant: Improved Frentix Booster
# Implant: Standard Exile Booster
# Implant: Standard Frentix Booster
# Implant: Strong Exile Booster
# Implant: Strong Frentix Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", booster.getModifiedItemAttr("boosterTurretTrackingPenalty"))
