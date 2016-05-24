type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed", src.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics Cruisers")
