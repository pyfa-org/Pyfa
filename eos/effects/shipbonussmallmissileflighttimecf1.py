type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "explosionDelay", src.getModifiedItemAttr("shipBonusCF") * lvl, skill="Caldari Frigate")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"), "explosionDelay", src.getModifiedItemAttr("shipBonusCF") * lvl, skill="Caldari Frigate")
