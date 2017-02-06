# boosterTurretOptimalRangePenalty
#
# Used by:
# Implants named like: Blue Pill Booster (3 of 5)
# Implants named like: Mindflood Booster (3 of 4)
# Implants named like: Sooth Sayer Booster (3 of 4)
type = "boosterSideEffect"
activeByDefault = False


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "maxRange", booster.getModifiedItemAttr("boosterTurretOptimalRange"))
