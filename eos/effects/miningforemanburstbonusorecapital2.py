# Mining Command Boost
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Mining Foreman",
                                              ),
                                  "buffDuration",
                                  src.getModifiedItemAttr("shipBonusORECapital2"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Mining Foreman",
                                              ),
                                  "warfareBuff1Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Mining Foreman",
                                              ),
                                  "warfareBuff2Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Mining Foreman",
                                              ),
                                  "warfareBuff3Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ) and
                                              mod.item.requiresSkill in
                                              (
                                                  "Mining Foreman",
                                              ),
                                  "warfareBuff4Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"),
                                  skill="Capital Industrial Ships",
                                  )

#  TODO: test
