# eliteBonusCoverOpsBombEmDmg1
#
# Used by:
# Ship: Purifier
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "emDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")
