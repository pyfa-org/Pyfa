type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "explosionDelay", src.getModifiedItemAttr("shipBonusCC2") * lvl, skill="Caldari Cruiser")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"), "explosionDelay", src.getModifiedItemAttr("shipBonusCC2") * lvl, skill="Caldari Cruiser")
