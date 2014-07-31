# Used by:
# Ship: Hound
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Covert Ops").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCoverOps1") * level)
