type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1") * lvl, skill="Minmatar Carrier")
