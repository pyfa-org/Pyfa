type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "capacitorNeed", src.getModifiedItemAttr("shipBonusTitanA2"), skill="Amarr Titan")
