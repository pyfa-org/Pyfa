type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Shield Command",
                                              ),
                                  "buffDuration",
                                  src.getModifiedItemAttr("shipBonusICS3"),
                                  skill="Industrial Command Ships",
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Shield Command",
                                              ),
                                  "warfareBuff1Value",
                                  src.getModifiedItemAttr("shipBonusICS3"),
                                  skill="Industrial Command Ships",
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Shield Command",
                                              ),
                                  "warfareBuff2Value",
                                  src.getModifiedItemAttr("shipBonusICS3"),
                                  skill="Industrial Command Ships",
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Shield Command",
                                              ),
                                  "warfareBuff3Value",
                                  src.getModifiedItemAttr("shipBonusICS3"),
                                  skill="Industrial Command Ships",
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Shield Command"
                                              ),
                                  "warfareBuff4Value",
                                  src.getModifiedItemAttr("shipBonusICS3"),
                                  skill="Industrial Command Ships",
                                  )

#  TODO: test
