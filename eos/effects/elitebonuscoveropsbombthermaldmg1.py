# eliteBonusCoverOpsBombThermalDmg1
#
# Used by:
# Ship: Nemesis
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "thermalDamage", ship.getModifiedItemAttr("eliteBonusCoverOps1"), skill="Covert Ops")
