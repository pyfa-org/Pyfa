type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"), "capacitorNeed", src.getModifiedItemAttr("shipBonusRole2"))
