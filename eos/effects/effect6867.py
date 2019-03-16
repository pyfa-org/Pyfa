# shipBonusSPTRoFMF
#
# Used by:
# Ship: Pacifier
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "speed", src.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
