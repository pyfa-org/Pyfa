type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"), "speed", src.getModifiedItemAttr("shipBonusMF") * lvl, skill="Minmatar Frigate")
