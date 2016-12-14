# nosCpuNeedBonusEffect
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "cpu",
                                  src.getModifiedItemAttr("nosferatuCpuNeedBonus"))
