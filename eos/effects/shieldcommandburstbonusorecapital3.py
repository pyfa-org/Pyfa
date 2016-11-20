type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Shield Command",
                                                 ),
                                     "buffDuration",
                                     src.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Shield Command",
                                                 ),
                                     "warfareBuff1Value",
                                     src.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Shield Command",
                                                 ),
                                     "warfareBuff2Value",
                                     src.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Shield Command",
                                                 ),
                                     "warfareBuff3Value",
                                     src.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )

    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Shield Command",
                                                 ),
                                     "warfareBuff4Value",
                                     src.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )

#  TODO: test
