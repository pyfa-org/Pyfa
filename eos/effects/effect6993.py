# roleBonus2BoosterPenaltyReduction
#
# Used by:
# Ship: Victor
# Ship: Virtuoso
type = "passive"


def handler(fit, src, context):
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterMissileAOECloudPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterCapacitorCapacityPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterAOEVelocityPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterArmorRepairAmountPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterMissileVelocityPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterTurretTrackingPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterShieldCapacityPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterTurretOptimalRangePenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterShieldBoostAmountPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterTurretFalloffPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterArmorHPPenalty", src.getModifiedItemAttr("shipBonusRole2"))
    fit.boosters.filteredItemBoost(lambda mod: mod.item.group.name == "Booster", "boosterMaxVelocityPenalty", src.getModifiedItemAttr("shipBonusRole2"))
