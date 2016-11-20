# commandshipMultiRelayEffect
#
# Used by:
# Ships from group: Command Ship (8 of 8)
# Ships from group: Industrial Command Ship (2 of 2)
# Ship: Rorqual
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ),
                                     "maxGroupOnline",
                                     ship.getModifiedItemAttr("maxGangModules"),
                                     )
#  TODO: test
