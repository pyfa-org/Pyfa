type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Mining Drone Specialization"), "miningAmount", src.getModifiedItemAttr("miningAmountBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Mining Drone Specialization"), "maxVelocity", src.getModifiedItemAttr("maxVelocityBonus") * lvl)
