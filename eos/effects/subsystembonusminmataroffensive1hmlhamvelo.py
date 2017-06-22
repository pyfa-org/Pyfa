type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Missiles"), "maxVelocity", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Assault Missiles"), "maxVelocity", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
