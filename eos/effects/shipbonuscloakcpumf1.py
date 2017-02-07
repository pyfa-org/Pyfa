# shipBonusCloakCpuMF1
#
# Used by:
# Ship: Caedes
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"), "cpu",
                                  src.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
