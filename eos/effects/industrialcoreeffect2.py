# industrialCoreEffect2
#
# Used by:
# Variations of module: Industrial Core I (2 of 2)
type = "active"
runTime = "early"


def handler(fit, src, context):
    fit.extraAttributes["siege"] = True
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
    fit.ship.multiplyItemAttr("mass", src.getModifiedItemAttr("siegeMassMultiplier"))
    fit.ship.multiplyItemAttr("scanResolution",
                              src.getModifiedItemAttr("scanResolutionMultiplier"),
                              stackingPenalties=True)

    #  Remote Shield Repper Bonuses
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "duration",
                                  src.getModifiedItemAttr("industrialCoreRemoteLogisticsDurationBonus"),
                                  )
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "maxRange",
                                  src.getModifiedItemAttr("industrialCoreRemoteLogisticsRangeBonus"),
                                  stackingPenalties=True
                                  )
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "capacitorNeed",
                                  src.getModifiedItemAttr("industrialCoreRemoteLogisticsDurationBonus")
                                  )
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "falloffEffectiveness",
                                  src.getModifiedItemAttr("industrialCoreRemoteLogisticsRangeBonus"),
                                  stackingPenalties=True
                                  )

    #  Local Shield Repper Bonuses
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "duration",
                                  src.getModifiedItemAttr("industrialCoreLocalLogisticsDurationBonus"),
                                  )
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "shieldBonus",
                                  src.getModifiedItemAttr("industrialCoreLocalLogisticsAmountBonus"),
                                  stackingPenalties=True
                                  )

    # Mining Burst Bonuses
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"),
                                  "warfareBuff1Value",
                                  src.getModifiedItemAttr("industrialCoreBonusMiningBurstStrength"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"),
                                  "warfareBuff2Value",
                                  src.getModifiedItemAttr("industrialCoreBonusMiningBurstStrength"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"),
                                  "warfareBuff3Value",
                                  src.getModifiedItemAttr("industrialCoreBonusMiningBurstStrength"),
                                  )

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"),
                                  "warfareBuff4Value",
                                  src.getModifiedItemAttr("industrialCoreBonusMiningBurstStrength"),
                                  )

    #  Command Burst Range Bonus
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"),
                                  "maxRange",
                                  src.getModifiedItemAttr("industrialCoreBonusCommandBurstRange"),
                                  stackingPenalties=True
                                  )

    # Drone Bonuses
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                 "duration",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneIceHarvesting"),
                                 )
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneMining"),
                                 )
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxVelocity",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneVelocity"),
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneDamageHP"),
                                 stackingPenalties=True
                                 )
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "shieldCapacity",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneDamageHP"),
                                 )
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "armorHP",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneDamageHP"),
                                 )
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "hp",
                                 src.getModifiedItemAttr("industrialCoreBonusDroneDamageHP"),
                                 )

    #  Todo: remote impedance (no reps, etc)
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
    fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
    fit.ship.increaseItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))
    fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
    fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
    fit.ship.increaseItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))
