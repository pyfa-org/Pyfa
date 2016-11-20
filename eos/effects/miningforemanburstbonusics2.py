# miningForemanBurstBonusICS2
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Mining Foreman",
                                                 ),
                                     "buffDuration",
                                     src.getModifiedItemAttr("shipBonusICS2"),
                                     skill="Industrial Command Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Mining Foreman",
                                                 ),
                                     "warfareBuff1Value",
                                     src.getModifiedItemAttr("shipBonusICS2"),
                                     skill="Industrial Command Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Mining Foreman",
                                                 ),
                                     "warfareBuff2Value",
                                     src.getModifiedItemAttr("shipBonusICS2"),
                                     skill="Industrial Command Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Mining Foreman",
                                                 ),
                                     "warfareBuff3Value",
                                     src.getModifiedItemAttr("shipBonusICS2"),
                                     skill="Industrial Command Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Mining Foreman",
                                                 ),
                                     "warfareBuff4Value",
                                     src.getModifiedItemAttr("shipBonusICS2"),
                                     skill="Industrial Command Ships",
                                     )

#  TODO: test
