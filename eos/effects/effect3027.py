# eliteBonusCoverOpsBombThermalDmg1
#
# Used by:
# Ship: Nemesis
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "thermalDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"),
                                    skill="Covert Ops")
