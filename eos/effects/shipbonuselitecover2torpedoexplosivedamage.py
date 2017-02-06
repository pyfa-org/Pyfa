# shipBonusEliteCover2TorpedoExplosiveDamage
#
# Used by:
# Ship: Hound
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCoverOps2"),
                                    skill="Covert Ops")
