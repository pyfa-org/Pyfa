# shipBonusEliteCover2TorpedoExplosiveDamage
#
# Used by:
# Ship: Hound
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCovertOps2"),
                                    skill="Covert Ops")
