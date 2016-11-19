# commandshipMultiRelayEffect
#
# Used by:
# Ships from group: Command Ship (8 of 8)
# Ship: Orca
# Ship: Rorqual
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ),
                                     "maxGroupOnline",
                                     ship.getModifiedItemAttr("shipBonusICS2"),
                                     )
#  TODO: test
