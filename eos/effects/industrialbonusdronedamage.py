# industrialBonusDroneDamage
#
# Used by:
# Ships from group: Blockade Runner (4 of 4)
# Ships from group: Deep Space Transport (4 of 4)
# Ships from group: Exhumer (3 of 3)
# Ships from group: Industrial (17 of 17)
# Ships from group: Industrial Command Ship (2 of 2)
# Ships from group: Mining Barge (3 of 3)
# Variations of ship: Venture (3 of 3)
# Ship: Rorqual
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier",
                                 src.getModifiedItemAttr("industrialBonusDroneDamage"))
