# chargeBonusWarfareCharge
#
# Used by:
# Items from market group: Ammunition & Charges > Command Burst Charges (15 of 15)


'''
Some documentation:
When the fit is calculated, we gather up all the gang effects and stick them onto the fit. We don't run the actual
effect yet, only give the fit details so that it can run the effect at a later time. We need to do this so that we can
only run the strongest effect. When we are done, one of the last things that we do with the fit is to loop through those
bonuses and actually run the effect. To do this, we have a special argument passed into the effect handler that tells it
which warfareBuffID to run (shouldn't need this right now, but better safe than sorry)
'''

type = "active", "gang"
def handler(fit, module, context, **kwargs):
    print "In chargeBonusWarfareEffect, context: ", context

    def runEffect(id, value):
        print "RUN EFFECT: ", fit,

        if id == 10:  # Shield Burst: Shield Harmonizing: Shield Resistance
            for damageType in ("Em", "Explosive", "Thermal", "Kinetic"):
                fit.ship.boostItemAttr("shield%sDamageResonance" % damageType, value, stackingPenalties=True)

        if id == 11:  # Shield Burst: Active Shielding: Repair Duration/Capacitor
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed", value)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Shield Emission Systems"), "duration", value)

        if id == 12:  # Shield Burst: Shield Extension: Shield HP
            fit.ship.boostItemAttr("shieldCapacity", value, stackingPenalties=True)

        if id == 13:  # Armor Burst: Armor Energizing: Armor Resistance
            for damageType in ("Em", "Thermal", "Explosive", "Kinetic"):
                fit.ship.boostItemAttr("armor%sDamageResonance" % damageType, value, stackingPenalties=True)

        if id == 14:  # Armor Burst: Rapid Repair: Repair Duration/Capacitor
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or mod.item.requiresSkill("Repair Systems"), "capacitorNeed", value)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or mod.item.requiresSkill("Repair Systems"), "duration", value)

        if id == 15:  # Armor Burst: Armor Reinforcement: Armor HP
            fit.ship.boostItemAttr("armorHP", value, stackingPenalties=True)

        if id == 16:  # Information Burst: Sensor Optimization: Scan Resolution
            fit.ship.boostItemAttr("scanResolution", value, stackingPenalties=True)

        if id == 17:  # Information Burst: Electronic Superiority: EWAR Range and Strength
            groups = ("ECM", "Sensor Dampener", "Weapon Disruptor", "Target Painter")
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "maxRange", value, stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "falloffEffectiveness", value, stackingPenalties=True)

            for scanType in ("Magnetometric", "Radar", "Ladar", "Gravimetric"):
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.nam == "ECM", "scan%sStrengthBonus" % scanType, value, stackingPenalties=True)

            for attr in ("missileVelocityBonus", "explosionDelayBonus", "aoeVelocityBonus", "falloffBonus",
                         "maxRangeBonus", "aoeCloudSizeBonus", "trackingSpeedBonus"):
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor", attr, value)

            for attr in ("maxTargetRangeBonus", "scanResolutionBonus"):
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener", attr, value)

            fit.modules.filteredItemBoost(lambda mod: mod.item.gorup.name == "Target Painter", "signatureRadiusBonus", value, stackingPenalties=True)

        if id == 18:  # Information Burst: Electronic Hardening: Scan Strength
            for scanType in ("Gravimetric", "Radar", "Ladar", "Magnetometric"):
                fit.ship.boostItemAttr("scan%sStrength" % scanType, value, stackingPenalties=True)

        if id == 19:  # Information Burst: Electronic Hardening: RSD/RWD Resistance
            fit.ship.boostItemAttr("sensorDampenerResistance", value)
            fit.ship.boostItemAttr("weaponDisruptionResistance", value)

        if id == 26:  # Information Burst: Sensor Optimization: Targeting Range
            fit.ship.boostItemAttr("maxTargetRange", value)

        if id == 20:  # Skirmish Burst: Evasive Maneuvers: Signature Radius
            fit.ship.boostItemAttr("signatureRadius", value, stackingPenalties=True)

        if id == 21:  # Skirmish Burst: Interdiction Maneuvers: Tackle Range
            groups = ("Stasis Web", "Warp Scrambler")
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "maxRange", value, stackingPenalties=True)

        if id == 22:  # Skirmish Burst: Rapid Deployment: AB/MWD Speed Increase
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner") or mod.item.requiresSkill("High Speed Maneuvering"), "speedFactor", value, stackingPenalties=True)

        if id == 23:  # Mining Burst: Mining Laser Field Enhancement: Mining/Survey Range
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or mod.item.requiresSkill("Ice Harvesting") or mod.item.requiresSkill("Gas Cloud Harvesting"), "maxRange", value, stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("CPU Management"), "surveyScanRange", value, stackingPenalties=True)

        if id == 24:  # Mining Burst: Mining Laser Optimization: Mining Capacitor/Duration
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or mod.item.requiresSkill("Ice Harvesting") or mod.item.requiresSkill("Gas Cloud Harvesting"), "capacitorNeed", value, stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or mod.item.requiresSkill("Ice Harvesting") or mod.item.requiresSkill("Gas Cloud Harvesting"), "duration", value, stackingPenalties = True)

        if id == 25:  # Mining Burst: Mining Equipment Preservation: Crystal Volatility
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"), "crystalVolatilityChance", value, stackingPenalties=True)

    for x in xrange(1, 4):
        if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedChargeAttr("warfareBuff{}Multiplier".format(x))
            id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
            print "Buff ID: ",id," value: ",value
            if id:
                if 'commandRun' not in context:
                    print "Add buffID", id, " to ", fit
                    fit.addCommandBonus(id, value, module, kwargs['effect'])
                elif kwargs['warfareBuffID'] is not None and kwargs['warfareBuffID'] == id:
                    print "Running buffID ", kwargs['warfareBuffID'], " on ", fit
                    runEffect(kwargs['warfareBuffID'], value)

