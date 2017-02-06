# eliteBonusInterdictorsMissileKineticDamage1
#
# Used by:
# Ship: Flycatcher
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(
        lambda mod: mod.charge.requiresSkill("Light Missiles") or mod.charge.requiresSkill("Rockets"),
        "kineticDamage", ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")
