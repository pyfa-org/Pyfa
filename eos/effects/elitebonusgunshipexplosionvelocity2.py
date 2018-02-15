# eliteBonusGunshipExplosionVelocity2
#
# Used by:
# Ship: Jaguar
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "aoeVelocity",
                                    src.getModifiedItemAttr("eliteBonusGunship2"), stackingPenalties=True, skill="Assault Frigates")
