# shipBonusCloakCpuMC2
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"), "cpu",
                                  src.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
