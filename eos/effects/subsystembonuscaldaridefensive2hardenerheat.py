# subsystemBonusCaldariDefensive2HardenerHeat
#
# Used by:
# Subsystem: Tengu Defensive - Supplemental Screening
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Tactical Shield Manipulation"),
                                  "overloadHardeningBonus", src.getModifiedItemAttr("subsystemBonusCaldariDefensive2"),
                                  skill="Caldari Defensive Systems")
