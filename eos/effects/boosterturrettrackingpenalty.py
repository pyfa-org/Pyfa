# Used by:
# Implants named like: Exile Booster (3 of 4)
# Implants named like: Frentix Booster (3 of 4)
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", booster.getModifiedItemAttr("boosterTurretTrackingPenalty"))
