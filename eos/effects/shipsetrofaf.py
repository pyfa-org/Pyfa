# shipSETROFAF
#
# Used by:
# Ship: Retribution
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"), "speed",
                                  src.getModifiedItemAttr("shipBonusAF"), stackingPenalties=False, skill="Amarr Frigate")
