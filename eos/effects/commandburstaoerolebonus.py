# commandBurstAoERoleBonus
#
# Used by:
# Ships from group: Carrier (4 of 4)
# Ships from group: Combat Battlecruiser (13 of 13)
# Ships from group: Command Ship (8 of 8)
# Ships from group: Force Auxiliary (6 of 6)
# Ships from group: Supercarrier (6 of 6)
# Ships from group: Titan (7 of 7)
# Subsystems named like: Offensive Support Processor (4 of 4)
# Ship: Orca
# Ship: Rorqual
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "maxRange",
                                  src.getModifiedItemAttr("roleBonusCommandBurstAoERange"))
