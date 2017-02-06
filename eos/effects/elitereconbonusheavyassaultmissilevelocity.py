# eliteReconBonusHeavyAssaultMissileVelocity
#
# Used by:
# Ship: Rook
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusReconShip1"),
                                    skill="Recon Ships")
