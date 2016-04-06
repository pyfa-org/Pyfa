type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"), "durationTargetIlluminationBurstProjector", src.getModifiedItemAttr("shipBonusSupercarrierM4"), skill="Minmatar Carrier")
