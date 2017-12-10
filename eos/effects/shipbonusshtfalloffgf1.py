# shipBonusSHTFalloffGF1
#
# Used by:
# Ship: Virtuoso
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"), "falloff",
                                  src.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
