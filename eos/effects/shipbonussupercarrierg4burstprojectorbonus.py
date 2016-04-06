# shipBonusSupercarrierG4BurstProjectorBonus
#
# Used by:
# Ship: Nyx
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"), "durationSensorDampeningBurstProjector", src.getModifiedItemAttr("shipBonusSupercarrierG4"), skill="Gallente Carrier")
