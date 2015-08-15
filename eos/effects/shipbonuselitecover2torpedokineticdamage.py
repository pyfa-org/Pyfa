# shipBonusEliteCover2TorpedoKineticDamage
#
# Used by:
# Ship: Manticore
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "kineticDamage", ship.getModifiedItemAttr("eliteBonusCoverOps2"), skill="Covert Ops")
