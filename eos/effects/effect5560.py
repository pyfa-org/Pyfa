# roleBonusMarauderMJDRReactivationDelayBonus
#
# Used by:
# Ships from group: Marauder (4 of 4)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Micro Jump Drive",
                                  "moduleReactivationDelay", ship.getModifiedItemAttr("roleBonusMarauder"))
