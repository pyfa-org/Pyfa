# shipBonusEliteCover2TorpedoEMDamage
#
# Used by:
# Ship: Purifier
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "emDamage", ship.getModifiedItemAttr("eliteBonusCoverOps2"), skill="Covert Ops")
