# Not used by any item
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "aoeVelocity", src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True, skill="Target Navigation Prediction")
