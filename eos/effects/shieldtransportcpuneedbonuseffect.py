# shieldTransportCpuNeedBonusEffect
#
# Used by:
# Ships from group: Logistics (3 of 5)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "cpu",
                                  src.getModifiedItemAttr("shieldTransportCpuNeedBonus"))
