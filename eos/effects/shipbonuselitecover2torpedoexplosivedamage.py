# Used by:
# Ship: Hound
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Covert Ops").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCoverOps2") * level)
