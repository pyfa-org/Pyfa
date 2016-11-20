# shipBonusDreadnoughtA3CapNeed
#
# Used by:
# Ship: Revelation
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "capacitorNeed",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtA3"), skill="Amarr Dreadnought")
