# shipProjectileRofMF
#
# Used by:
# Ship: Claw
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"), "speed",
                                  src.getModifiedItemAttr("shipBonusMF"), stackingPenalties=True, skill="Minmatar Frigate")
