# shipETDamageAF
#
# Used by:
# Ship: Crucifier Navy Issue
# Ship: Crusader
# Ship: Imperial Navy Slicer
# Ship: Pacifier
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
