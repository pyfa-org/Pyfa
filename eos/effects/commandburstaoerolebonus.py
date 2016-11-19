# Command Burst AOE Bonus
#
# Used by:
# Orca
type = "passive"


#  TODO: this isn't applying correctly :(
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in
                                              (
                                                  "Command Burst",
                                              ),
                                  "maxRange",
                                  src.getModifiedItemAttr("roleBonusCommandBurstAoERange"),
                                  )
#  TODO: test
