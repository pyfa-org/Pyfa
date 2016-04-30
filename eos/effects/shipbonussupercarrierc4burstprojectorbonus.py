# shipBonusSupercarrierC4BurstProjectorBonus
#
# Used by:
# Ship: Wyvern
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"), "durationECMJammerBurstProjector", src.getModifiedItemAttr("shipBonusSupercarrierC4"), skill="Caldari Carrier")
