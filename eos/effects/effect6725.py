# shipBonusSETFalloffAF2
#
# Used by:
# Ship: Caedes
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"), "falloff",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
