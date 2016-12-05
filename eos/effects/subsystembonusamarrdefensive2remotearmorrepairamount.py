# subsystemBonusAmarrDefensive2RemoteArmorRepairAmount
#
# Used by:
# Subsystem: Legion Defensive - Adaptive Augmenter
type = "passive"
runTime = "early"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusAmarrDefensive2"),
                                  skill="Amarr Defensive Systems")
