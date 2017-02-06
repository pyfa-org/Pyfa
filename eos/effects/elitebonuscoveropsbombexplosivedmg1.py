# eliteBonusCoverOpsBombExplosiveDmg1
#
# Used by:
# Ship: Hound
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCoverOps1"),
                                    skill="Covert Ops")
