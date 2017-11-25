# eliteCovertOpsBonusArmorRepAmount4
#
# Used by:
# Ship: Virtuoso
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "armorDamageAmount",
                                  src.getModifiedItemAttr("eliteBonusCovertOps4"), skill="Covert Ops")
