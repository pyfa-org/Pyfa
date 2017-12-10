# eliteBonusCoverOpsBombKineticDmg1
#
# Used by:
# Ship: Manticore
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "kineticDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"),
                                    skill="Covert Ops")
