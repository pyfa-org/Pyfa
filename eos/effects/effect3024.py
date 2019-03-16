# eliteBonusCoverOpsBombExplosiveDmg1
#
# Used by:
# Ship: Hound
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"),
                                    skill="Covert Ops")
