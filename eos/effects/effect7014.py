# eliteBonusGunshipThermalMissileDamage1
#
# Used by:
# Ship: Jaguar
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "thermalDamage",
                                    src.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")
