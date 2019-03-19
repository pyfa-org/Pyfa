def effect10():
    type = 'active'
    def handler(fit, module, context):
        module.reloadTime = 1000

    return locals()

def effect1001():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("rechargeRate", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")

    return locals()

def effect1003():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Pulse Laser Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1004():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Beam Laser Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1005():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Blaster Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1006():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Railgun Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1007():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Autocannon Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1008():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Artillery Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1009():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Pulse Laser Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect101():
    type = 'active', "projected"
    def handler(fit, src, context):
        src.reloadTime = 10000
        if "projected" in context:
            if src.item.group.name == 'Missile Launcher Bomb':
                moduleReactivationDelay = src.getModifiedItemAttr("moduleReactivationDelay")
                speed = src.getModifiedItemAttr("speed")
                neutAmount = src.getModifiedChargeAttr("energyNeutralizerAmount")
                if moduleReactivationDelay and neutAmount and speed:
                    fit.addDrain(src, speed + moduleReactivationDelay, neutAmount, 0)
                ecmStrengthBonus = src.getModifiedChargeAttr("scan{0}StrengthBonus".format(fit.scanType))
                if ecmStrengthBonus:
                    strModifier = 1 - ecmStrengthBonus / fit.scanStrength
                    fit.ecmProjectedStr *= strModifier

    return locals()

def effect1010():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Beam Laser Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1011():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Blaster Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1012():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Railgun Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1013():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Autocannon Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1014():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Artillery Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1015():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Pulse Laser Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1016():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Beam Laser Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1017():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Blaster Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1018():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Railgun Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1019():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Autocannon Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1020():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Artillery Specialization"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1021():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship2"),
                                      skill="Assault Frigates")

    return locals()

def effect1024():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect1025():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect1030():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect1033():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics Cruisers")

    return locals()

def effect1034():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics Cruisers")

    return locals()

def effect1035():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics Cruisers")

    return locals()

def effect1036():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics Cruisers")

    return locals()

def effect1046():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "maxRange",
                                      src.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect1047():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "maxRange",
                                      src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect1048():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "maxRange",
                                      src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect1049():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "maxRange",
                                      src.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect1056():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1057():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1058():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1060():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1061():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1062():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1063():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1080():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1081():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosionDelay", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                        skill="Heavy Assault Cruisers")

    return locals()

def effect1082():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "explosionDelay", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                        skill="Heavy Assault Cruisers")

    return locals()

def effect1084():
    type = "passive"
    def handler(fit, ship, context):
        fit.extraAttributes.increase("droneControlRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                     skill="Heavy Assault Cruisers")

    return locals()

def effect1087():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect1099():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect1176():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                      "speedFactor", container.getModifiedItemAttr("speedFBonus") * level)

    return locals()

def effect1179():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship2"),
                                      skill="Assault Frigates")

    return locals()

def effect118():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))

    return locals()

def effect1181():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics1"),
                                      skill="Logistics Cruisers")

    return locals()

def effect1182():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect1183():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics2"),
                                      skill="Logistics Cruisers")

    return locals()

def effect1184():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect1185():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.boostItemAttr("signatureRadius", implant.getModifiedItemAttr("signatureRadiusBonus"))

    return locals()

def effect1190():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                      "duration", container.getModifiedItemAttr("iceHarvestCycleBonus") * level)

    return locals()

def effect1200():
    type = "passive"
    def handler(fit, module, context):
        module.multiplyItemAttr("specialtyMiningAmount",
                                module.getModifiedChargeAttr("specialisationAsteroidYieldMultiplier"))

    return locals()

def effect1212():
    type = "passive"
    runTime = "late"
    def handler(fit, module, context):
        module.preAssignItemAttr("specialtyMiningAmount", module.getModifiedItemAttr("miningAmount"))

    return locals()

def effect1215():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect1218():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1219():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", ship.getModifiedItemAttr("shipBonusAB"),
                                      skill="Amarr Battleship")

    return locals()

def effect1220():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect1221():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect1222():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect1228():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect1230():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1232():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1233():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1234():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1239():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1240():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect1255():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "durationBonus", implant.getModifiedItemAttr("implantSetBloodraider"))

    return locals()

def effect1256():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                      "duration", implant.getModifiedItemAttr("durationBonus"))

    return locals()

def effect1261():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "velocityBonus", implant.getModifiedItemAttr("implantSetSerpentis"))

    return locals()

def effect1264():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusInterceptor2"),
                                      skill="Interceptors")

    return locals()

def effect1268():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusInterceptor2"),
                                      skill="Interceptors")

    return locals()

def effect1281():
    type = "passive"
    def handler(fit, container, context):
        penalized = "implant" not in context
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", container.getModifiedItemAttr("repairBonus"),
                                      stackingPenalties=penalized)

    return locals()

def effect1318():
    type = "passive"
    def handler(fit, container, context):
        groups = ("ECM", "Burst Jammer")
        level = container.level if "skill" in context else 1
        for scanType in ("Gravimetric", "Ladar", "Magnetometric", "Radar"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                          "scan{0}StrengthBonus".format(scanType),
                                          container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level,
                                          stackingPenalties=False if "skill" in context else True)

    return locals()

def effect1360():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect1361():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect1370():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Target Painting"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect1372():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect1395():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", container.getModifiedItemAttr("shieldBoostMultiplier"))

    return locals()

def effect1397():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "shieldBoostMultiplier", implant.getModifiedItemAttr("implantSetGuristas"))

    return locals()

def effect1409():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                      "duration", container.getModifiedItemAttr("durationBonus") * level)

    return locals()

def effect1410():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Propulsion Jamming"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect1412():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect1434():
    type = "passive"
    def handler(fit, ship, context):
        for sensorType in ("Gravimetric", "Ladar", "Magnetometric", "Radar"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Electronic Warfare"),
                                          "scan{0}StrengthBonus".format(sensorType),
                                          ship.getModifiedItemAttr("shipBonusCB"), stackingPenalties=True,
                                          skill="Caldari Battleship")

    return locals()

def effect1441():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")

    return locals()

def effect1442():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect1443():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect1445():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                      "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                      stackingPenalties="skill" not in context)

    return locals()

def effect1446():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                      stackingPenalties="skill" not in context)

    return locals()

def effect1448():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                      "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                      stackingPenalties="skill" not in context)

    return locals()

def effect1449():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                      "falloffEffectiveness", skill.getModifiedItemAttr("falloffBonus") * skill.level)

    return locals()

def effect1450():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "falloffEffectiveness", skill.getModifiedItemAttr("falloffBonus") * skill.level)

    return locals()

def effect1451():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                      "falloffEffectiveness", skill.getModifiedItemAttr("falloffBonus") * skill.level)

    return locals()

def effect1452():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                      stackingPenalties="skill" not in context and "implant" not in context)

    return locals()

def effect1453():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "falloffEffectiveness", skill.getModifiedItemAttr("falloffBonus") * skill.level)

    return locals()

def effect1472():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalize = False if "skill" in context or "implant" in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeCloudSize", container.getModifiedItemAttr("aoeCloudSizeBonus") * level,
                                        stackingPenalties=penalize)

    return locals()

def effect1500():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "capacitorNeed", container.getModifiedItemAttr("shieldBoostCapacitorBonus") * level)

    return locals()

def effect1550():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "signatureRadiusBonus",
                                      skill.getModifiedItemAttr("scanSkillTargetPaintStrengthBonus") * skill.level)

    return locals()

def effect1551():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMF2"),
                                      skill="Minmatar Frigate")

    return locals()

def effect157():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1577():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(
            lambda implant: "signatureRadiusBonus" in implant.itemModifiedAttributes and
                            "implantSetAngel" in implant.itemModifiedAttributes,
            "signatureRadiusBonus",
            implant.getModifiedItemAttr("implantSetAngel"))

    return locals()

def effect1579():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "armorHpBonus", implant.getModifiedItemAttr("implantSetSansha") or 1)

    return locals()

def effect1581():
    type = "passive"
    def handler(fit, skill, context):
        fit.ship.boostItemAttr("jumpDriveRange", skill.getModifiedItemAttr("jumpDriveRangeBonus") * skill.level)

    return locals()

def effect1585():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1586():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1587():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1588():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect159():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1590():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalize = False if "skill" in context or "implant" in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeVelocity", container.getModifiedItemAttr("aoeVelocityBonus") * level,
                                        stackingPenalties=penalize)

    return locals()

def effect1592():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"),
                                        "emDamage", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1593():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1594():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1595():
    type = "passive"
    def handler(fit, src, context):
        mod = src.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "emDamage", src.getModifiedItemAttr("damageMultiplierBonus") * mod)

    return locals()

def effect1596():
    type = "passive"
    def handler(fit, src, context):
        mod = src.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", src.getModifiedItemAttr("damageMultiplierBonus") * mod)

    return locals()

def effect1597():
    type = "passive"
    def handler(fit, src, context):
        mod = src.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", src.getModifiedItemAttr("damageMultiplierBonus") * mod)

    return locals()

def effect160():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect161():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1615():
    type = "passive"
    def handler(fit, ship, context):
        skillName = "Advanced Spaceship Command"
        skill = fit.character.getSkill(skillName)
        fit.ship.boostItemAttr("agility", skill.getModifiedItemAttr("agilityBonus"), skill=skillName)

    return locals()

def effect1616():
    type = "passive"
    def handler(fit, skill, context):
        if fit.ship.item.requiresSkill("Capital Ships"):
            fit.ship.boostItemAttr("agility", skill.getModifiedItemAttr("agilityBonus") * skill.level)

    return locals()

def effect1617():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.multiplyItemAttr("agility", src.getModifiedItemAttr("advancedCapitalAgility"), stackingPenalties=True)

    return locals()

def effect162():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1634():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                      "capacitorNeed", container.getModifiedItemAttr("shieldBoostCapacitorBonus") * level)

    return locals()

def effect1635():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                      "duration", container.getModifiedItemAttr("durationSkillBonus") * level,
                                      stackingPenalties="skill" not in context)

    return locals()

def effect1638():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Gunnery") or mod.item.requiresSkill("Missile Launcher Operation"),
            "power", skill.getModifiedItemAttr("powerNeedBonus") * skill.level)

    return locals()

def effect1643():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                      src.getModifiedItemAttr("mindlinkBonus"))

    return locals()

def effect1644():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration",
                                      src.getModifiedItemAttr("mindlinkBonus"))

    return locals()

def effect1645():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                      src.getModifiedItemAttr("mindlinkBonus"))

    return locals()

def effect1646():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                      src.getModifiedItemAttr("mindlinkBonus"))

    return locals()

def effect1650():
    type = "passive"
    def handler(fit, skill, context):
        amount = -skill.getModifiedItemAttr("consumptionQuantityBonus")
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill(skill),
                                         "consumptionQuantity", amount * skill.level)

    return locals()

def effect1657():
    type = "passive"
    def handler(fit, src, context):
        mod = src.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", src.getModifiedItemAttr("damageMultiplierBonus") * mod)

    return locals()

def effect1668():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusA2"), skill="Amarr Freighter")

    return locals()

def effect1669():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusC2"), skill="Caldari Freighter")

    return locals()

def effect1670():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusG2"), skill="Gallente Freighter")

    return locals()

def effect1671():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusM2"), skill="Minmatar Freighter")

    return locals()

def effect1672():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusA1"), skill="Amarr Freighter")

    return locals()

def effect1673():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusC1"), skill="Caldari Freighter")

    return locals()

def effect1674():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusG1"), skill="Gallente Freighter")

    return locals()

def effect1675():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusM1"), skill="Minmatar Freighter")

    return locals()

def effect17():
    type = "passive"
    grouped = True
    def handler(fit, container, context):
        miningDroneAmountPercent = container.getModifiedItemAttr("miningDroneAmountPercent")
        if (miningDroneAmountPercent is None) or (miningDroneAmountPercent == 0):
            pass
        else:
            container.multiplyItemAttr("miningAmount", miningDroneAmountPercent / 100)

    return locals()

def effect172():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1720():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
            "shieldBonus", module.getModifiedItemAttr("shieldBoostMultiplier"),
            stackingPenalties=True)

    return locals()

def effect1722():
    type = "passive"
    def handler(fit, skill, context):
        fit.ship.boostItemAttr("jumpDriveCapacitorNeed",
                               skill.getModifiedItemAttr("jumpDriveCapacitorNeedBonus") * skill.level)

    return locals()

def effect173():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1730():
    type = "passive"
    def handler(fit, skill, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill(skill),
                                     "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect1738():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect174():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect1763():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", container.getModifiedItemAttr("rofBonus") * level)

    return locals()

def effect1764():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalized = False if "skill" in context or "implant" in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", container.getModifiedItemAttr("speedFactor") * level,
                                        stackingPenalties=penalized)

    return locals()

def effect1773():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect1804():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect1805():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusAF"),
                               skill="Amarr Frigate")

    return locals()

def effect1806():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusAF"),
                               skill="Amarr Frigate")

    return locals()

def effect1807():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusAF"),
                               skill="Amarr Frigate")

    return locals()

def effect1812():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect1813():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonusCC2"),
                               skill="Caldari Cruiser")

    return locals()

def effect1814():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCC2"),
                               skill="Caldari Cruiser")

    return locals()

def effect1815():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusCC2"),
                               skill="Caldari Cruiser")

    return locals()

def effect1816():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect1817():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonusCF"),
                               skill="Caldari Frigate")

    return locals()

def effect1819():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCF"),
                               skill="Caldari Frigate")

    return locals()

def effect1820():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusCF"),
                               skill="Caldari Frigate")

    return locals()

def effect1848():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("mindlinkBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                      src.getModifiedItemAttr("mindlinkBonus"))

    return locals()

def effect1851():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                      "speed", skill.getModifiedItemAttr("rofBonus") * skill.level)

    return locals()

def effect1862():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect1863():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect1864():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusCF2"),
                                        skill="Caldari Frigate")

    return locals()

def effect1882():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "miningAmount", module.getModifiedItemAttr("miningAmountBonus"))

    return locals()

def effect1885():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                      "speed", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect1886():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                      "speed", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect1896():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                      "duration", ship.getModifiedItemAttr("eliteBonusBarge2"), skill="Exhumers")

    return locals()

def effect1910():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                      skill="Recon Ships")

    return locals()

def effect1911():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanGravimetricStrengthBonus", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                      skill="Recon Ships")

    return locals()

def effect1912():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanMagnetometricStrengthBonus", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                      skill="Recon Ships")

    return locals()

def effect1913():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanRadarStrengthBonus", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                      skill="Recon Ships")

    return locals()

def effect1914():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanLadarStrengthBonus", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                      skill="Recon Ships")

    return locals()

def effect1921():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")

    return locals()

def effect1922():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")

    return locals()

def effect1959():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))

    return locals()

def effect1964():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect1969():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect1996():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect2000():
    type = "passive"
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr("droneRangeBonus")
        fit.extraAttributes.increase("droneControlRange", amount)

    return locals()

def effect2008():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cynosural Field Generator",
                                      "duration", ship.getModifiedItemAttr("durationBonus"))

    return locals()

def effect2013():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "maxVelocity", container.getModifiedItemAttr("droneMaxVelocityBonus") * level, stackingPenalties=True)

    return locals()

def effect2014():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        stacking = False if "skill" in context else True
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "maxRange",
                                     container.getModifiedItemAttr("rangeSkillBonus") * level,
                                     stackingPenalties=stacking)

    return locals()

def effect2015():
    type = "passive"
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "shieldCapacity", module.getModifiedItemAttr("hullHpBonus"))

    return locals()

def effect2016():
    type = "passive"
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "armorHP", module.getModifiedItemAttr("hullHpBonus"))

    return locals()

def effect2017():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "hp", container.getModifiedItemAttr("hullHpBonus") * level)

    return locals()

def effect2019():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                     "shieldBonus", container.getModifiedItemAttr("damageHP") * level)

    return locals()

def effect2020():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                     "armorDamageAmount", container.getModifiedItemAttr("damageHP") * level,
                                     stackingPenalties=True)

    return locals()

def effect2029():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusAdd"))

    return locals()

def effect2041():
    type = "passive"
    def handler(fit, module, context):
        for type in ("kinetic", "thermal", "explosive", "em"):
            fit.ship.boostItemAttr("armor%sDamageResonance" % type.capitalize(),
                                   module.getModifiedItemAttr("%sDamageResistanceBonus" % type),
                                   stackingPenalties=True)

    return locals()

def effect2052():
    type = "passive"
    def handler(fit, module, context):
        for type in ("kinetic", "thermal", "explosive", "em"):
            fit.ship.boostItemAttr("shield%sDamageResonance" % type.capitalize(),
                                   module.getModifiedItemAttr("%sDamageResistanceBonus" % type),
                                   stackingPenalties=True)

    return locals()

def effect2053():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Resistance Amplifier",
                                      "emDamageResistanceBonus", skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2054():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Resistance Amplifier",
                                      "explosiveDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2055():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Resistance Amplifier",
                                      "kineticDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2056():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Resistance Amplifier",
                                      "thermalDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect21():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("capacityBonus"))

    return locals()

def effect2105():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Coating",
                                      "emDamageResistanceBonus", skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2106():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Coating",
                                      "explosiveDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2107():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Coating",
                                      "kineticDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2108():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Coating",
                                      "thermalDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2109():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Plating Energized",
                                      "emDamageResistanceBonus", skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2110():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Plating Energized",
                                      "explosiveDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2111():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Plating Energized",
                                      "kineticDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect2112():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Plating Energized",
                                      "thermalDamageResistanceBonus",
                                      skill.getModifiedItemAttr("hardeningBonus") * skill.level)

    return locals()

def effect212():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Electronics Upgrades"),
                                      "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)

    return locals()

def effect2130():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect2131():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect2132():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect2133():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "maxRange", ship.getModifiedItemAttr("maxRangeBonus2"))

    return locals()

def effect2134():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster", "maxRange",
                                      ship.getModifiedItemAttr("maxRangeBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Shield Booster", "maxRange",
                                      ship.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect2135():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer", "maxRange",
                                      src.getModifiedItemAttr("maxRangeBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Armor Repairer", "maxRange",
                                      src.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect214():
    type = "passive", "structure"
    def handler(fit, skill, context):
        amount = skill.getModifiedItemAttr("maxTargetBonus") * skill.level
        fit.extraAttributes.increase("maxTargetsLockedFromSkills", amount)

    return locals()

def effect2143():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMC2"),
                                      skill="Minmatar Cruiser")

    return locals()

def effect2155():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusCommandShips1"),
                                      skill="Command Ships")

    return locals()

def effect2156():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")

    return locals()

def effect2157():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusCommandShips1"),
                                      skill="Command Ships")

    return locals()

def effect2158():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "speed", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")

    return locals()

def effect2160():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")

    return locals()

def effect2161():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusCommandShips1"),
                                      skill="Command Ships")

    return locals()

def effect2179():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         type, ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect2181():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         type, ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect2186():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         type, ship.getModifiedItemAttr("shipBonusGB2"), skill="Gallente Battleship")

    return locals()

def effect2187():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGB2"),
                                     skill="Gallente Battleship")

    return locals()

def effect2188():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect2189():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect2200():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Light Missiles") or mod.charge.requiresSkill("Rockets"),
            "kineticDamage", ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")

    return locals()

def effect2201():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")

    return locals()

def effect2215():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect223():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.boostItemAttr("maxVelocity", implant.getModifiedItemAttr("velocityBonus"))

    return locals()

def effect2232():
    type = "passive"
    def handler(fit, module, context):
        for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            fit.ship.boostItemAttr("scan%sStrength" % type,
                                   module.getModifiedItemAttr("scan%sStrengthPercent" % type),
                                   stackingPenalties=True)

    return locals()

def effect2249():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "miningAmount", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect2250():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                     "miningAmount", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect2251():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                         src.getModifiedItemAttr("maxGangModules"))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupOnline",
                                         src.getModifiedItemAttr("maxGangModules"))

    return locals()

def effect2252():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemForce(lambda mod: mod.item.requiresSkill("Cloaking"),
                                      "moduleReactivationDelay",
                                      container.getModifiedItemAttr("covertOpsAndReconOpsCloakModuleDelay"))

    return locals()

def effect2253():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemForce(lambda mod: mod.item.group.name == "Cloaking Device",
                                      "cloakingTargetingDelay",
                                      ship.getModifiedItemAttr("covertOpsStealthBomberTargettingDelay"))

    return locals()

def effect2255():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect227():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus"))

    return locals()

def effect2298():
    type = "passive"
    def handler(fit, implant, context):
        for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            sensorType = "scan{0}Strength".format(type)
            sensorBoost = "scan{0}StrengthPercent".format(type)
            if sensorBoost in implant.item.attributes:
                fit.ship.boostItemAttr(sensorType, implant.getModifiedItemAttr(sensorBoost))

    return locals()

def effect230():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "duration", container.getModifiedItemAttr("durationBonus") * level)

    return locals()

def effect2302():
    type = "passive"
    def handler(fit, module, context):
        for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
            for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
                bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
                bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
                booster = "%s%sDamageResonance" % (layer, damageType)
                fit.ship.multiplyItemAttr(bonus, module.getModifiedItemAttr(booster),
                                          stackingPenalties=True, penaltyGroup="preMul")

    return locals()

def effect2305():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                      skill="Recon Ships")

    return locals()

def effect235():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.boostItemAttr("warpCapacitorNeed", implant.getModifiedItemAttr("warpCapacitorNeedBonus"))

    return locals()

def effect2354():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect2355():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect2356():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                      "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)

    return locals()

def effect2402():
    type = "passive"
    def handler(fit, skill, context):
        damageTypes = ("em", "explosive", "kinetic", "thermal")
        for dmgType in damageTypes:
            dmgAttr = "{0}Damage".format(dmgType)
            fit.modules.filteredItemBoost(
                lambda mod: mod.item.group.name == "Super Weapon" and dmgAttr in mod.itemModifiedAttributes,
                dmgAttr, skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect242():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                      "speedFactor", implant.getModifiedItemAttr("speedFBonus"))

    return locals()

def effect2422():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.boostItemAttr("maxVelocity", implant.getModifiedItemAttr("implantBonusVelocity"))

    return locals()

def effect2432():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("capacitorCapacity", container.getModifiedItemAttr("capacitorCapacityBonus") * level)

    return locals()

def effect244():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect2444():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "cpu", module.getModifiedItemAttr("cpuPenaltyPercent"))

    return locals()

def effect2445():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                      "cpu", module.getModifiedItemAttr("cpuPenaltyPercent"))

    return locals()

def effect2456():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Upgrades"),
                                      "cpuPenaltyPercent",
                                      container.getModifiedItemAttr("miningUpgradeCPUReductionBonus") * level)

    return locals()

def effect2465():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("Em", "Explosive", "Kinetic", "Thermal"):
            fit.ship.boostItemAttr("armor{0}DamageResonance".format(type), ship.getModifiedItemAttr("shipBonusAB"),
                                   skill="Amarr Battleship")

    return locals()

def effect2479():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                      "duration", module.getModifiedItemAttr("iceHarvestCycleBonus"))

    return locals()

def effect2485():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.boostItemAttr("armorHP", implant.getModifiedItemAttr("armorHpBonus2"))

    return locals()

def effect2488():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.boostItemAttr("maxVelocity", implant.getModifiedItemAttr("velocityBonus2"))

    return locals()

def effect2489():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusMC"),
                                      skill="Minmatar Cruiser")

    return locals()

def effect2490():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusGC2"),
                                      skill="Gallente Cruiser")

    return locals()

def effect2491():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Jammer",
                                      "ecmBurstRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                      stackingPenalties=False if "skill" in context else True)

    return locals()

def effect2492():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Jammer",
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect25():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))

    return locals()

def effect2503():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB2"),
                                      skill="Gallente Battleship")

    return locals()

def effect2504():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect2561():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusGunship1"),
                                        skill="Assault Frigates")

    return locals()

def effect2589():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        for i in range(5):
            attr = "boosterEffectChance{0}".format(i + 1)
            fit.boosters.filteredItemBoost(lambda booster: attr in booster.itemModifiedAttributes,
                                           attr, container.getModifiedItemAttr("boosterChanceBonus") * level)

    return locals()

def effect26():
    type = "active"
    runTime = "late"
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr("structureDamageAmount")
        speed = module.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("hullRepair", amount / speed)

    return locals()

def effect2602():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                               skill="Caldari Battleship")

    return locals()

def effect2603():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                               skill="Caldari Battleship")

    return locals()

def effect2604():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                               skill="Caldari Battleship")

    return locals()

def effect2605():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                               skill="Caldari Battleship")

    return locals()

def effect2611():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship1"),
                                      skill="Assault Frigates")

    return locals()

def effect2644():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"), stackingPenalties=True)

    return locals()

def effect2645():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionMultiplier"),
                                  stackingPenalties=True)

    return locals()

def effect2646():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True)

    return locals()

def effect2647():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                      "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect2648():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                      "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect2649():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Light",
                                      "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect2670():
    type = "active"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True)
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True)
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            fit.ship.boostItemAttr(
                "scan{}Strength".format(scanType),
                module.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                stackingPenalties=True
            )

    return locals()

def effect2688():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "capacitorNeed", module.getModifiedItemAttr("capNeedBonus"))

    return locals()

def effect2689():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "capacitorNeed", module.getModifiedItemAttr("capNeedBonus"))

    return locals()

def effect2690():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "cpu", module.getModifiedItemAttr("cpuNeedBonus"))

    return locals()

def effect2691():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "cpu", module.getModifiedItemAttr("cpuNeedBonus"))

    return locals()

def effect2693():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "falloff", module.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True)

    return locals()

def effect2694():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "falloff", module.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True)

    return locals()

def effect2695():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Projectile Weapon",
                                      "falloff", module.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True)

    return locals()

def effect2696():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True)

    return locals()

def effect2697():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True)

    return locals()

def effect2698():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Projectile Weapon",
                                      "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True)

    return locals()

def effect27():
    runTime = "late"
    type = "active"
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr("armorDamageAmount")
        speed = module.getModifiedItemAttr("duration") / 1000.0
        rps = amount / speed
        fit.extraAttributes.increase("armorRepair", rps)
        fit.extraAttributes.increase("armorRepairPreSpool", rps)
        fit.extraAttributes.increase("armorRepairFullSpool", rps)

    return locals()

def effect2706():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "power", module.getModifiedItemAttr("drawback"))

    return locals()

def effect2707():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "power", module.getModifiedItemAttr("drawback"))

    return locals()

def effect2708():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Projectile Weapon",
                                      "power", module.getModifiedItemAttr("drawback"))

    return locals()

def effect271():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("armorHP", (container.getModifiedItemAttr("armorHpBonus") or 0) * level)

    return locals()

def effect2712():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("armorHP", module.getModifiedItemAttr("drawback"))

    return locals()

def effect2713():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("cpuOutput", module.getModifiedItemAttr("drawback"))

    return locals()

def effect2714():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "cpu", module.getModifiedItemAttr("drawback"))

    return locals()

def effect2716():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("drawback"), stackingPenalties=True)

    return locals()

def effect2717():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("drawback"),
                               stackingPenalties=True)

    return locals()

def effect2718():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("shieldCapacity", module.getModifiedItemAttr("drawback"))

    return locals()

def effect272():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "duration", container.getModifiedItemAttr("durationSkillBonus") * level)

    return locals()

def effect2726():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect2727():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                         "maxGroupActive", skill.level)

    return locals()

def effect273():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Upgrades"),
                                      "power", container.getModifiedItemAttr("powerNeedBonus") * level)

    return locals()

def effect2734():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("Gravimetric", "Ladar", "Radar", "Magnetometric"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                          "scan{0}StrengthBonus".format(type),
                                          ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect2735():
    type = "boosterSideEffect"
    displayName = "Armor Capacity"
    attr = "boosterArmorHPPenalty"
    def handler(fit, booster, context):
        fit.ship.boostItemAttr("armorHP", booster.getModifiedItemAttr(attr))

    return locals()

def effect2736():
    type = "boosterSideEffect"
    displayName = "Armor Repair Amount"
    attr = "boosterArmorRepairAmountPenalty"
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Unit",
                                      "armorDamageAmount", booster.getModifiedItemAttr(attr))

    return locals()

def effect2737():
    type = "boosterSideEffect"
    displayName = "Shield Capacity"
    attr = "boosterShieldCapacityPenalty"
    def handler(fit, booster, context):
        fit.ship.boostItemAttr("shieldCapacity", booster.getModifiedItemAttr(attr))

    return locals()

def effect2739():
    type = "boosterSideEffect"
    displayName = "Turret Optimal Range"
    attr = "boosterTurretOptimalRangePenalty"
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "maxRange", booster.getModifiedItemAttr(attr))

    return locals()

def effect2741():
    type = "boosterSideEffect"
    displayName = "Turret Falloff"
    attr = "boosterTurretFalloffPenalty"
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "falloff", booster.getModifiedItemAttr(attr))

    return locals()

def effect2745():
    type = "boosterSideEffect"
    displayName = "Cap Capacity"
    attr = "boosterCapacitorCapacityPenalty"
    def handler(fit, booster, context):
        fit.ship.boostItemAttr("capacitorCapacity", booster.getModifiedItemAttr(attr))

    return locals()

def effect2746():
    type = "boosterSideEffect"
    displayName = "Velocity"
    attr = "boosterMaxVelocityPenalty"
    def handler(fit, booster, context):
        fit.ship.boostItemAttr("maxVelocity", booster.getModifiedItemAttr(attr))

    return locals()

def effect2747():
    type = "boosterSideEffect"
    displayName = "Turret Tracking"
    attr = "boosterTurretTrackingPenalty"
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "trackingSpeed", booster.getModifiedItemAttr(attr))

    return locals()

def effect2748():
    type = "boosterSideEffect"
    displayName = "Missile Velocity"
    attr = "boosterMissileVelocityPenalty"
    def handler(fit, booster, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", booster.getModifiedItemAttr(attr))

    return locals()

def effect2749():
    type = "boosterSideEffect"
    displayName = "Missile Explosion Velocity"
    attr = "boosterAOEVelocityPenalty"
    def handler(fit, booster, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeVelocity", booster.getModifiedItemAttr(attr))

    return locals()

def effect2756():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("Gravimetric", "Magnetometric", "Ladar", "Radar"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                          "scan{0}StrengthBonus".format(type), ship.getModifiedItemAttr("shipBonusCC"),
                                          skill="Caldari Cruiser")

    return locals()

def effect2757():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect2760():
    runTime = 'early'
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        attrs = ("boosterArmorHPPenalty", "boosterArmorRepairAmountPenalty")
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr("boosterAttributeModifier") * level)

    return locals()

def effect2763():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        attrs = ("boosterShieldBoostAmountPenalty", "boosterShieldCapacityPenalty", "shieldBoostMultiplier")
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: booster.getModifiedItemAttr(attr) < 0,
                                           attr, container.getModifiedItemAttr("boosterAttributeModifier") * level)

    return locals()

def effect2766():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        attrs = ("boosterCapacitorCapacityPenalty", "boosterMaxVelocityPenalty")
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr("boosterAttributeModifier") * level)

    return locals()

def effect277():
    type = "passive"
    def handler(fit, skill, context):
        fit.ship.increaseItemAttr("shieldUniformity", skill.getModifiedItemAttr("uniformityBonus") * skill.level)

    return locals()

def effect2776():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        attrs = ("boosterAOEVelocityPenalty", "boosterMissileAOECloudPenalty", "boosterMissileVelocityPenalty")
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr("boosterAttributeModifier") * level)

    return locals()

def effect2778():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        attrs = ("boosterTurretFalloffPenalty", "boosterTurretOptimalRangePenalty", "boosterTurretTrackingPenalty")
        for attr in attrs:
            fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                           container.getModifiedItemAttr("boosterAttributeModifier") * level)

    return locals()

def effect279():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect2791():
    type = "boosterSideEffect"
    displayName = "Missile Explosion Radius"
    attr = "boosterMissileAOECloudPenalty"
    def handler(fit, booster, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeCloudSize", booster.getModifiedItemAttr(attr))

    return locals()

def effect2792():
    type = "passive"
    def handler(fit, module, context):
        for type in ("kinetic", "thermal", "explosive", "em"):
            fit.ship.boostItemAttr("armor" + type.capitalize() + "DamageResonance",
                                   module.getModifiedItemAttr(type + "DamageResistanceBonus") or 0,
                                   stackingPenalties=True)

    return locals()

def effect2794():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Salvaging"),
                                         "accessDifficultyBonus", container.getModifiedItemAttr("accessDifficultyBonus"),
                                         position="post")

    return locals()

def effect2795():
    type = "passive"
    def handler(fit, module, context):
        for type in ("kinetic", "thermal", "explosive", "em"):
            fit.ship.boostItemAttr("shield" + type.capitalize() + "DamageResonance",
                                   module.getModifiedItemAttr(type + "DamageResistanceBonus") or 0,
                                   stackingPenalties=True)

    return locals()

def effect2796():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("mass", module.getModifiedItemAttr("massBonusPercentage"), stackingPenalties=True)

    return locals()

def effect2797():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2798():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2799():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2801():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2802():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2803():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2804():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect2805():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusAB2"),
                                      skill="Amarr Battleship")

    return locals()

def effect2809():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect2810():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "explosionDelay", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                        skill="Heavy Assault Cruisers")

    return locals()

def effect2812():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Jammer",
                                      "ecmBurstRange", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")

    return locals()

def effect2837():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("armorHP", module.getModifiedItemAttr("armorHPBonusAdd"))

    return locals()

def effect2847():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "trackingSpeed", container.getModifiedItemAttr("trackingSpeedBonus") * level)

    return locals()

def effect2848():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemIncrease(lambda module: module.item.requiresSkill("Archaeology"),
                                         "accessDifficultyBonus",
                                         container.getModifiedItemAttr("accessDifficultyBonusModifier"), position="post")

    return locals()

def effect2849():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemIncrease(lambda c: c.item.requiresSkill("Hacking"),
                                         "accessDifficultyBonus",
                                         container.getModifiedItemAttr("accessDifficultyBonusModifier"), position="post")

    return locals()

def effect2850():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                      "duration", module.getModifiedItemAttr("durationBonus"))

    return locals()

def effect2851():
    type = "passive"
    def handler(fit, container, context):
        for dmgType in ("em", "kinetic", "explosive", "thermal"):
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                               "%sDamage" % dmgType,
                                               container.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                               stackingPenalties=True)

    return locals()

def effect2853():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda module: module.item.requiresSkill("Cloaking"),
                                      "cloakingTargetingDelay", module.getModifiedItemAttr("cloakingTargetingDelayBonus"))

    return locals()

def effect2857():
    type = "active"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"))

    return locals()

def effect2865():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("implantBonusVelocity"),
                               stackingPenalties=True)

    return locals()

def effect2866():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.boosters.filteredItemBoost(lambda bst: True, "boosterDuration",
                                       container.getModifiedItemAttr("durationBonus") * level)

    return locals()

def effect2867():
    type = "passive"
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "damageMultiplier", module.getModifiedItemAttr("damageMultiplierBonus"),
                                     stackingPenalties=True)

    return locals()

def effect2868():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                      "armorDamageAmount", implant.getModifiedItemAttr("repairBonus"),
                                      stackingPenalties=True)

    return locals()

def effect287():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect2872():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Defender Missiles"),
                                           "maxVelocity", container.getModifiedItemAttr("missileVelocityBonus"))

    return locals()

def effect2881():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2882():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2883():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2884():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2885():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gas Cloud Harvesting"),
                                      "duration", implant.getModifiedItemAttr("durationBonus"))

    return locals()

def effect2887():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2888():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2889():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2890():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2891():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2892():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2893():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2894():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2899():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect290():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level)

    return locals()

def effect2900():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2901():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2902():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2903():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2904():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2905():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2906():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2907():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "emDamage", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2908():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2909():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "kineticDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2910():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect2911():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Data Miners",
                                      "duration", implant.getModifiedItemAttr("durationBonus"))

    return locals()

def effect2967():
    type = "passive"
    def handler(fit, skill, context):
        amount = -skill.getModifiedItemAttr("consumptionQuantityBonus")
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill(skill),
                                         "consumptionQuantity", amount * skill.level)

    return locals()

def effect2977():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Hull Repair Systems"),
                                      "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)

    return locals()

def effect298():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "falloff", container.getModifiedItemAttr("falloffBonus") * level)

    return locals()

def effect2980():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Hull Repair Systems"),
                                      "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)

    return locals()

def effect2982():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                                  mod.item.getAttribute("duration"),
                                      "duration",
                                      skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                                  mod.item.getAttribute("durationECMJammerBurstProjector"),
                                      "durationECMJammerBurstProjector",
                                      skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                                  mod.item.getAttribute("durationTargetIlluminationBurstProjector"),
                                      "durationTargetIlluminationBurstProjector",
                                      skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                                  mod.item.getAttribute("durationSensorDampeningBurstProjector"),
                                      "durationSensorDampeningBurstProjector",
                                      skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                                  mod.item.getAttribute("durationWeaponDisruptionBurstProjector"),
                                      "durationWeaponDisruptionBurstProjector",
                                      skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)

    return locals()

def effect3001():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("speed", module.getModifiedItemAttr("overloadRofBonus"))

    return locals()

def effect3002():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus") or 0)

    return locals()

def effect3024():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                        "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"),
                                        skill="Covert Ops")

    return locals()

def effect3025():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("damageMultiplier", module.getModifiedItemAttr("overloadDamageModifier"))

    return locals()

def effect3026():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                        "kineticDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"),
                                        skill="Covert Ops")

    return locals()

def effect3027():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                        "thermalDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"),
                                        skill="Covert Ops")

    return locals()

def effect3028():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                        "emDamage", ship.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")

    return locals()

def effect3029():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("emDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))

    return locals()

def effect3030():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("thermalDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))

    return locals()

def effect3031():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("explosiveDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))

    return locals()

def effect3032():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("kineticDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))

    return locals()

def effect3035():
    type = "overheat"
    def handler(fit, module, context):
        for type in ("kinetic", "thermal", "explosive", "em"):
            module.boostItemAttr("%sDamageResistanceBonus" % type,
                                 module.getModifiedItemAttr("overloadHardeningBonus"))

    return locals()

def effect3036():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Bomb",
                                      "moduleReactivationDelay", skill.getModifiedItemAttr("reactivationDelayBonus") * skill.level)

    return locals()

def effect3046():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityModifier"), stackingPenalties=True)

    return locals()

def effect3047():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("hp", module.getModifiedItemAttr("structureHPMultiplier"))

    return locals()

def effect3061():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "heatDamage", module.getModifiedItemAttr("heatDamageBonus"))

    return locals()

def effect315():
    type = "passive"
    def handler(fit, skill, context):
        amount = skill.getModifiedItemAttr("maxActiveDroneBonus") * skill.level
        fit.extraAttributes.increase("maxActiveDrones", amount)

    return locals()

def effect3169():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "cpu",
                                      src.getModifiedItemAttr("shieldTransportCpuNeedBonus"))

    return locals()

def effect3172():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                     "armorDamageAmount", ship.getModifiedItemAttr("droneArmorDamageAmountBonus"))

    return locals()

def effect3173():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                     "shieldBonus", ship.getModifiedItemAttr("droneShieldBonusBonus"))

    return locals()

def effect3174():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("maxRange", module.getModifiedItemAttr("overloadRangeBonus"),
                             stackingPenalties=True)

    return locals()

def effect3175():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("speedFactor", module.getModifiedItemAttr("overloadSpeedFactorBonus"),
                             stackingPenalties=True)

    return locals()

def effect3182():
    type = "overheat"
    def handler(fit, module, context):
        if "projected" not in context:
            for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
                module.boostItemAttr("scan{0}StrengthBonus".format(scanType),
                                     module.getModifiedItemAttr("overloadECMStrengthBonus"),
                                     stackingPenalties=True)

    return locals()

def effect3196():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: "heatDamage" in mod.item.attributes, "heatDamage",
                                      skill.getModifiedItemAttr("thermodynamicsHeatDamage") * skill.level)

    return locals()

def effect3200():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
        module.boostItemAttr("armorDamageAmount", module.getModifiedItemAttr("overloadArmorDamageAmount"),
                             stackingPenalties=True)

    return locals()

def effect3201():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
        module.boostItemAttr("shieldBonus", module.getModifiedItemAttr("overloadShieldBonus"), stackingPenalties=True)

    return locals()

def effect3212():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("FoF Missiles"),
                                        "aoeCloudSize", container.getModifiedItemAttr("aoeCloudSizeBonus") * level)

    return locals()

def effect3234():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect3235():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect3236():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect3237():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect3241():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("eliteBonusGunship1"),
                               skill="Assault Frigates")

    return locals()

def effect3242():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("eliteBonusGunship1"),
                               skill="Assault Frigates")

    return locals()

def effect3243():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("eliteBonusGunship1"),
                               skill="Assault Frigates")

    return locals()

def effect3244():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("eliteBonusGunship1"),
                               skill="Assault Frigates")

    return locals()

def effect3249():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("rechargeRate", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect3264():
    type = "passive"
    def handler(fit, skill, context):
        amount = -skill.getModifiedItemAttr("consumptionQuantityBonus")
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill(skill),
                                         "consumptionQuantity", amount * skill.level)

    return locals()

def effect3267():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Industrial Reconfiguration"),
                                      "consumptionQuantity", ship.getModifiedItemAttr("shipBonusORECapital1"),
                                      skill="Capital Industrial Ships")

    return locals()

def effect3297():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", ship.getModifiedItemAttr("shipBonusAB"),
                                      skill="Amarr Battleship")

    return locals()

def effect3298():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", ship.getModifiedItemAttr("shipBonusAC"),
                                      skill="Amarr Cruiser")

    return locals()

def effect3299():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", ship.getModifiedItemAttr("shipBonusAF"),
                                      skill="Amarr Frigate")

    return locals()

def effect3313():
    type = "passive"
    def handler(fit, skill, context):
        fit.ship.boostItemAttr("maxJumpClones", skill.getModifiedItemAttr("maxJumpClonesBonus") * skill.level)

    return locals()

def effect3331():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")

    return locals()

def effect3335():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect3336():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusMC2"),
                               skill="Minmatar Cruiser")

    return locals()

def effect3339():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusMC2"),
                               skill="Minmatar Cruiser")

    return locals()

def effect3340():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusMC2"),
                               skill="Minmatar Cruiser")

    return locals()

def effect3343():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                      skill="Heavy Interdiction Cruisers")

    return locals()

def effect3355():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                        skill="Heavy Interdiction Cruisers")

    return locals()

def effect3356():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                        skill="Heavy Interdiction Cruisers")

    return locals()

def effect3357():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                        skill="Heavy Interdiction Cruisers")

    return locals()

def effect3366():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect3367():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect3369():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect3370():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect3371():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "capacitorNeed", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect3374():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("signatureRadius", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                               skill="Electronic Attack Ships")

    return locals()

def effect3379():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "capacitorNeed", implant.getModifiedItemAttr("capNeedBonus"))

    return locals()

def effect3380():
    from eos.saveddata.module import State
    type = "projected", "active"
    runTime = "early"
    def handler(fit, module, context):
        if "projected" in context:
            fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))
            if module.charge is not None and module.charge.ID == 45010:
                for mod in fit.modules:
                    if not mod.isEmpty and mod.item.requiresSkill("High Speed Maneuvering") and mod.state > State.ONLINE:
                        mod.state = State.ONLINE
                    if not mod.isEmpty and mod.item.requiresSkill("Micro Jump Drive Operation") and mod.state > State.ONLINE:
                        mod.state = State.ONLINE
        else:
            if module.charge is None:
                fit.ship.boostItemAttr("mass", module.getModifiedItemAttr("massBonusPercentage"))
                fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"))
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                              "speedBoostFactor", module.getModifiedItemAttr("speedBoostFactorBonus"))
                fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                          "speedFactor", module.getModifiedItemAttr("speedFactorBonus"))
            fit.ship.forceItemAttr("disallowAssistance", 1)

    return locals()

def effect3392():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")

    return locals()

def effect34():
    type = 'active'
    def handler(fit, module, context):
        rt = module.getModifiedItemAttr("reloadTime")
        if not rt:
            module.reloadTime = 10000
        else:
            module.reloadTime = rt

    return locals()

def effect3403():
    type = "passive"
    def handler(fit, ship, context):
        if fit.extraAttributes["cloaked"]:
            fit.ship.multiplyItemAttr("maxVelocity", ship.getModifiedItemAttr("eliteBonusBlackOps2"), skill="Black Ops")

    return locals()

def effect3406():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")

    return locals()

def effect3415():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect3416():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect3417():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect3424():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusViolators1"), skill="Marauders")

    return locals()

def effect3425():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusViolators1"), skill="Marauders")

    return locals()

def effect3427():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusViolatorsRole2"))

    return locals()

def effect3439():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusViolators1"),
                                      skill="Marauders")

    return locals()

def effect3447():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect3466():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("rechargeRate", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                               skill="Electronic Attack Ships")

    return locals()

def effect3467():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacitorCapacity", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                               skill="Electronic Attack Ships")

    return locals()

def effect3468():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Disrupt Field Generator",
                                      "warpScrambleRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors2"),
                                      skill="Heavy Interdiction Cruisers")

    return locals()

def effect3473():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                      "maxTractorVelocity", ship.getModifiedItemAttr("eliteBonusViolatorsRole3"))

    return locals()

def effect3478():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect3480():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")

    return locals()

def effect3483():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect3484():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect3487():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect3489():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect3493():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cargo Scanner",
                                      "cargoScanRange", ship.getModifiedItemAttr("cargoScannerRangeBonus"))

    return locals()

def effect3494():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Survey Scanner",
                                      "surveyScanRange", ship.getModifiedItemAttr("surveyScannerRangeBonus"))

    return locals()

def effect3495():
    type = "passive"
    def handler(fit, ship, context):
        groups = ("Stasis Web", "Warp Scrambler")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "capacitorNeed", ship.getModifiedItemAttr("eliteBonusInterceptorRole"))

    return locals()

def effect3496():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "agilityBonus", implant.getModifiedItemAttr("implantSetThukker"))

    return locals()

def effect3498():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "scanStrengthBonus", implant.getModifiedItemAttr("implantSetSisters"))

    return locals()

def effect3499():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "boosterAttributeModifier",
                                                 implant.getModifiedItemAttr("implantSetSyndicate"))

    return locals()

def effect3513():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "rangeSkillBonus", implant.getModifiedItemAttr("implantSetMordus"))

    return locals()

def effect3514():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusInterceptor2"), skill="Interceptors")

    return locals()

def effect3519():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"),
                                      "cpu", skill.getModifiedItemAttr("cpuNeedBonus") * skill.level)

    return locals()

def effect3520():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"),
                                      "power", skill.getModifiedItemAttr("powerNeedBonus") * skill.level)

    return locals()

def effect3526():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cynosural Field Generator",
                                      "consumptionQuantity",
                                      container.getModifiedItemAttr("consumptionQuantityBonusPercentage") * level)

    return locals()

def effect3530():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")

    return locals()

def effect3532():
    type = "passive"
    def handler(fit, skill, context):
        fit.ship.boostItemAttr("jumpDriveConsumptionAmount",
                               skill.getModifiedItemAttr("consumptionQuantityBonusPercentage") * skill.level)

    return locals()

def effect3561():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                      "trackingSpeedBonus",
                                      container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)

    return locals()

def effect3568():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "maxRangeBonus", ship.getModifiedItemAttr("eliteBonusLogistics1"),
                                      skill="Logistics Cruisers")

    return locals()

def effect3569():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "maxRangeBonus", ship.getModifiedItemAttr("eliteBonusLogistics2"),
                                      skill="Logistics Cruisers")

    return locals()

def effect3570():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "trackingSpeedBonus", ship.getModifiedItemAttr("eliteBonusLogistics2"),
                                      skill="Logistics Cruisers")

    return locals()

def effect3571():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "trackingSpeedBonus", ship.getModifiedItemAttr("eliteBonusLogistics1"),
                                      skill="Logistics Cruisers")

    return locals()

def effect3586():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalized = False if "skill" in context else True
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "scanResolutionBonus",
                                      container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level,
                                      stackingPenalties=penalized)

    return locals()

def effect3587():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "maxTargetRangeBonus", ship.getModifiedItemAttr("shipBonusGC2"),
                                      skill="Gallente Cruiser")

    return locals()

def effect3588():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "maxTargetRangeBonus", ship.getModifiedItemAttr("shipBonusGF2"),
                                      skill="Gallente Frigate")

    return locals()

def effect3589():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "scanResolutionBonus", ship.getModifiedItemAttr("shipBonusGF2"),
                                      skill="Gallente Frigate")

    return locals()

def effect3590():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "scanResolutionBonus", ship.getModifiedItemAttr("shipBonusGC2"),
                                      skill="Gallente Cruiser")

    return locals()

def effect3591():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "maxTargetRangeBonus",
                                      container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)

    return locals()

def effect3592():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("hp", ship.getModifiedItemAttr("eliteBonusJumpFreighter1"), skill="Jump Freighters")

    return locals()

def effect3593():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("jumpDriveConsumptionAmount", ship.getModifiedItemAttr("eliteBonusJumpFreighter2"),
                               skill="Jump Freighters")

    return locals()

def effect3597():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("scanResolutionBonus", module.getModifiedChargeAttr("scanResolutionBonusBonus"))

    return locals()

def effect3598():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("maxTargetRangeBonus", module.getModifiedChargeAttr("maxTargetRangeBonusBonus"))

    return locals()

def effect3599():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("trackingSpeedBonus", module.getModifiedChargeAttr("trackingSpeedBonusBonus"))

    return locals()

def effect3600():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("maxRangeBonus", module.getModifiedChargeAttr("maxRangeBonusBonus"))

    return locals()

def effect3601():
    type = "passive"
    def handler(fit, module, context):
        module.forceItemAttr("disallowInEmpireSpace", module.getModifiedChargeAttr("disallowInEmpireSpace"))

    return locals()

def effect3602():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("duration", module.getModifiedChargeAttr("durationBonus"))

    return locals()

def effect3617():
    type = "passive"
    runTime = "early"
    def handler(fit, module, context):
        module.boostItemAttr("signatureRadiusBonus", module.getModifiedChargeAttr("signatureRadiusBonusBonus"))

    return locals()

def effect3618():
    type = "passive"
    runTime = "early"
    def handler(fit, module, context):
        module.boostItemAttr("massBonusPercentage", module.getModifiedChargeAttr("massBonusPercentageBonus"))

    return locals()

def effect3619():
    type = "passive"
    runTime = "early"
    def handler(fit, module, context):
        module.boostItemAttr("speedBoostFactorBonus", module.getModifiedChargeAttr("speedBoostFactorBonusBonus"))

    return locals()

def effect3620():
    type = "passive"
    runTime = "early"
    def handler(fit, module, context):
        module.boostItemAttr("speedFactorBonus", module.getModifiedChargeAttr("speedFactorBonusBonus"))

    return locals()

def effect3648():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("warpScrambleRange", module.getModifiedChargeAttr("warpScrambleRangeBonus"))

    return locals()

def effect3649():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusViolators1"),
                                      skill="Marauders")

    return locals()

def effect3650():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))

    return locals()

def effect3651():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))

    return locals()

def effect3652():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                      "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))

    return locals()

def effect3653():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Projectors",
                                      "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))

    return locals()

def effect3655():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True)

    return locals()

def effect3656():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                      stackingPenalties=True)

    return locals()

def effect3657():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True)

    return locals()

def effect3659():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True)

    return locals()

def effect3660():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))

    return locals()

def effect3668():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mining Laser",
                                      "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect3669():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Frequency Mining Laser",
                                      "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect3670():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Strip Miner",
                                      "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect3671():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                      "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect3672():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "maxRangeBonus", implant.getModifiedItemAttr("implantSetORE"))

    return locals()

def effect3677():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")

    return locals()

def effect3678():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("eliteBonusJumpFreighter1"),
                               skill="Jump Freighters")

    return locals()

def effect3679():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("eliteBonusJumpFreighter1"), skill="Jump Freighters")

    return locals()

def effect3680():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusC1"), skill="Caldari Freighter")

    return locals()

def effect3681():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusM1"), skill="Minmatar Freighter")

    return locals()

def effect3682():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusG1"), skill="Gallente Freighter")

    return locals()

def effect3683():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusA1"), skill="Amarr Freighter")

    return locals()

def effect3686():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("falloffBonus", module.getModifiedChargeAttr("falloffBonusBonus"))

    return locals()

def effect3703():
    type = "passive"
    def handler(fit, ship, context):
        groups = ("Missile Launcher Rapid Light", "Missile Launcher Heavy", "Missile Launcher Heavy Assault")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "speed", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect3705():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect3706():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect3726():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("agilityBonus"), stackingPenalties=True)

    return locals()

def effect3727():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("implantBonusVelocity"),
                               stackingPenalties=True)

    return locals()

def effect3739():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxRange",
                                      src.getModifiedItemAttr("roleBonusTractorBeamRange"))

    return locals()

def effect3740():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxTractorVelocity",
                                      ship.getModifiedItemAttr("roleBonusTractorBeamVelocity"))

    return locals()

def effect3742():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("specialOreHoldCapacity",
                               src.getModifiedItemAttr("shipBonusICS1"),
                               skill="Industrial Command Ships")
        fit.ship.boostItemAttr("capacity",
                               src.getModifiedItemAttr("shipBonusICS1"),
                               skill="Industrial Command Ships")

    return locals()

def effect3744():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                      src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")

    return locals()

def effect3745():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Survey Scanner", "surveyScanRange",
                                      src.getModifiedItemAttr("roleBonusSurveyScannerRange"))

    return locals()

def effect3765():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                         "power", ship.getModifiedItemAttr("stealthBomberLauncherPower"))

    return locals()

def effect3766():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusInterceptor"),
                                      skill="Interceptors")

    return locals()

def effect3767():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "aoeVelocity", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                        skill="Command Ships")

    return locals()

def effect3771():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("armorHP", module.getModifiedItemAttr("armorHPBonusAdd") or 0)

    return locals()

def effect3773():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("turretSlotsLeft", module.getModifiedItemAttr("turretHardPointModifier"))
        fit.ship.increaseItemAttr("launcherSlotsLeft", module.getModifiedItemAttr("launcherHardPointModifier"))

    return locals()

def effect3774():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("hiSlots", module.getModifiedItemAttr("hiSlotModifier"))
        fit.ship.increaseItemAttr("medSlots", module.getModifiedItemAttr("medSlotModifier"))
        fit.ship.increaseItemAttr("lowSlots", module.getModifiedItemAttr("lowSlotModifier"))

    return locals()

def effect3782():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("powerOutput", module.getModifiedItemAttr("powerOutput"))

    return locals()

def effect3783():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("cpuOutput", module.getModifiedItemAttr("cpuOutput"))

    return locals()

def effect3797():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("droneBandwidth", module.getModifiedItemAttr("droneBandwidth"))

    return locals()

def effect3799():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("droneCapacity", module.getModifiedItemAttr("droneCapacity"))

    return locals()

def effect38():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect3807():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRange"))

    return locals()

def effect3808():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadius"))

    return locals()

def effect3810():
    type = "passive"
    def handler(fit, subsystem, context):
        fit.ship.increaseItemAttr("capacity", subsystem.getModifiedItemAttr("cargoCapacityAdd") or 0)

    return locals()

def effect3811():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("capacitorCapacity", module.getModifiedItemAttr("capacitorCapacity") or 0)

    return locals()

def effect3831():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacity"))

    return locals()

def effect3857():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"),
                               skill="Amarr Propulsion Systems")

    return locals()

def effect3859():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                               skill="Caldari Propulsion Systems")

    return locals()

def effect3860():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                               skill="Minmatar Propulsion Systems")

    return locals()

def effect3861():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "speedFactor", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                                      skill="Minmatar Propulsion Systems")

    return locals()

def effect3863():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "speedFactor", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                                      skill="Caldari Propulsion Systems")

    return locals()

def effect3864():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "speedFactor", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"),
                                      skill="Amarr Propulsion Systems")

    return locals()

def effect3865():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"),
                               skill="Amarr Propulsion Systems")

    return locals()

def effect3866():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                               skill="Caldari Propulsion Systems")

    return locals()

def effect3867():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                               skill="Gallente Propulsion Systems")

    return locals()

def effect3868():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                               skill="Minmatar Propulsion Systems")

    return locals()

def effect3869():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "signatureRadiusBonus", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                                      skill="Minmatar Propulsion Systems")

    return locals()

def effect3872():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "signatureRadiusBonus", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"),
                                      skill="Amarr Propulsion Systems")

    return locals()

def effect3875():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                      "capacitorNeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                                      skill="Gallente Propulsion Systems")

    return locals()

def effect3893():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanLadarStrength", src.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                               skill="Minmatar Core Systems")

    return locals()

def effect3895():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanMagnetometricStrength", src.getModifiedItemAttr("subsystemBonusGallenteCore"),
                               skill="Gallente Core Systems")

    return locals()

def effect3897():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanGravimetricStrength", src.getModifiedItemAttr("subsystemBonusCaldariCore"), skill="Caldari Core Systems")

    return locals()

def effect39():
    type = "projected", "active"
    def handler(fit, module, context):
        if "projected" in context:
            fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))

    return locals()

def effect3900():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanRadarStrength", src.getModifiedItemAttr("subsystemBonusAmarrCore"),
                               skill="Amarr Core Systems")

    return locals()

def effect391():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "miningAmount", container.getModifiedItemAttr("miningAmountBonus") * level)

    return locals()

def effect392():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("hp", container.getModifiedItemAttr("hullHpBonus") * level)

    return locals()

def effect394():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        amount = container.getModifiedItemAttr("velocityBonus") or 0
        fit.ship.boostItemAttr("maxVelocity", amount * level,
                               stackingPenalties="skill" not in context and "implant" not in context and "booster" not in context)

    return locals()

def effect395():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("agility", container.getModifiedItemAttr("agilityBonus") * level,
                               stackingPenalties="skill" not in context and "implant" not in context)

    return locals()

def effect3959():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                      skill="Amarr Defensive Systems")

    return locals()

def effect396():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Grid Upgrades"),
                                      "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)

    return locals()

def effect3961():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                      skill="Gallente Defensive Systems")

    return locals()

def effect3962():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                      skill="Minmatar Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                      skill="Minmatar Defensive Systems")

    return locals()

def effect3964():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", module.getModifiedItemAttr("subsystemBonusCaldariDefensive"),
                                      skill="Caldari Defensive Systems")

    return locals()

def effect397():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("cpuOutput", container.getModifiedItemAttr("cpuOutputBonus2") * level)

    return locals()

def effect3976():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("shieldCapacity", module.getModifiedItemAttr("subsystemBonusCaldariDefensive"),
                               skill="Caldari Defensive Systems")

    return locals()

def effect3979():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                               skill="Minmatar Defensive Systems")
        fit.ship.boostItemAttr("armorHP", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                               skill="Minmatar Defensive Systems")

    return locals()

def effect3980():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("armorHP", module.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                               skill="Gallente Defensive Systems")

    return locals()

def effect3982():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("armorHP", module.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                               skill="Amarr Defensive Systems")

    return locals()

def effect3992():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("shieldCapacity", beacon.getModifiedItemAttr("shieldCapacityMultiplier"))

    return locals()

def effect3993():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("maxTargetRange", beacon.getModifiedItemAttr("maxTargetRangeMultiplier"),
                                  stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect3995():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("signatureRadius", beacon.getModifiedItemAttr("signatureRadiusMultiplier"),
                                  stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect3996():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", beacon.getModifiedItemAttr("armorEmDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect3997():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance",
                               beacon.getModifiedItemAttr("armorExplosiveDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect3998():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance",
                               beacon.getModifiedItemAttr("armorKineticDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect3999():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance",
                               beacon.getModifiedItemAttr("armorThermalDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect4():
    runTime = "late"
    type = "active"
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr("shieldBonus")
        speed = module.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("shieldRepair", amount / speed)

    return locals()

def effect4002():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "maxVelocity", beacon.getModifiedItemAttr("missileVelocityMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4003():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("maxVelocity", beacon.getModifiedItemAttr("maxVelocityMultiplier"),
                                  stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4016():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                         "damageMultiplier", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect4017():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "thermalDamage", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4018():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "emDamage", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4019():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "explosiveDamage", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4020():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "kineticDamage", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4021():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill("Drones"),
                                        "damageMultiplier", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                        stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4022():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                         "trackingSpeed", module.getModifiedItemAttr("trackingSpeedMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4023():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "aoeVelocity", beacon.getModifiedItemAttr("aoeVelocityMultiplier"))

    return locals()

def effect4033():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "heatDamage" in mod.itemModifiedAttributes,
                                         "heatDamage", module.getModifiedItemAttr("heatDamageMultiplier"))

    return locals()

def effect4034():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadArmorDamageAmount" in mod.itemModifiedAttributes,
                                         "overloadArmorDamageAmount", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4035():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadDamageModifier" in mod.itemModifiedAttributes,
                                         "overloadDamageModifier", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4036():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadDurationBonus" in mod.itemModifiedAttributes,
                                         "overloadDurationBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4037():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadECCMStrenghtBonus" in mod.itemModifiedAttributes,
                                         "overloadECCMStrenghtBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4038():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadECMStrenghtBonus" in mod.itemModifiedAttributes,
                                         "overloadECMStrenghtBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4039():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadHardeningBonus" in mod.itemModifiedAttributes,
                                         "overloadHardeningBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4040():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadRangeBonus" in mod.itemModifiedAttributes,
                                         "overloadRangeBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4041():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadRofBonus" in mod.itemModifiedAttributes,
                                         "overloadRofBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4042():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadSelfDurationBonus" in mod.itemModifiedAttributes,
                                         "overloadSelfDurationBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4043():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadShieldBonus" in mod.itemModifiedAttributes,
                                         "overloadShieldBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4044():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: "overloadSpeedFactorBonus" in mod.itemModifiedAttributes,
                                         "overloadSpeedFactorBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))

    return locals()

def effect4045():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                         "empFieldRange", module.getModifiedItemAttr("empFieldRangeMultiplier"))

    return locals()

def effect4046():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                         "emDamage", module.getModifiedItemAttr("smartbombDamageMultiplier"))

    return locals()

def effect4047():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                         "thermalDamage", module.getModifiedItemAttr("smartbombDamageMultiplier"))

    return locals()

def effect4048():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                         "kineticDamage", module.getModifiedItemAttr("smartbombDamageMultiplier"))

    return locals()

def effect4049():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                         "explosiveDamage", module.getModifiedItemAttr("smartbombDamageMultiplier"))

    return locals()

def effect4054():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                         "damageMultiplier", module.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect4055():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                         "damageMultiplier", module.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect4056():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                         "damageMultiplier", module.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect4057():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Rockets"),
                                           "emDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4058():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Rockets"),
                                           "explosiveDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4059():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Rockets"),
                                           "kineticDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4060():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Rockets"),
                                           "thermalDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4061():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                           "thermalDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4062():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                           "emDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4063():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                           "explosiveDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect408():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect4086():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Repair Systems") or
                                                     mod.item.requiresSkill("Capital Repair Systems"),
                                         "armorDamageAmount", module.getModifiedItemAttr("armorDamageAmountMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4088():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                         "armorDamageAmount",
                                         module.getModifiedItemAttr("armorDamageAmountMultiplierRemote"),
                                         stackingPenalties=True)

    return locals()

def effect4089():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                         "shieldBonus", module.getModifiedItemAttr("shieldBonusMultiplierRemote"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4090():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("capacitorCapacity", beacon.getModifiedItemAttr("capacitorCapacityMultiplierSystem"))

    return locals()

def effect4091():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("rechargeRate", beacon.getModifiedItemAttr("rechargeRateMultiplier"))

    return locals()

def effect4093():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", module.getModifiedItemAttr("subsystemBonusAmarrOffensive"),
                                      skill="Amarr Offensive Systems")

    return locals()

def effect4104():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", module.getModifiedItemAttr("subsystemBonusCaldariOffensive"),
                                      skill="Caldari Offensive Systems")

    return locals()

def effect4106():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "falloff", module.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                      skill="Gallente Offensive Systems")

    return locals()

def effect4114():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect4115():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "maxRange", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect4122():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "speed", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")

    return locals()

def effect4135():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", beacon.getModifiedItemAttr("shieldEmDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect4136():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance",
                               beacon.getModifiedItemAttr("shieldExplosiveDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect4137():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance",
                               beacon.getModifiedItemAttr("shieldKineticDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect4138():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance",
                               beacon.getModifiedItemAttr("shieldThermalDamageResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect414():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "speed", container.getModifiedItemAttr("turretSpeeBonus") * level)

    return locals()

def effect4152():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      module.getModifiedItemAttr("subsystemBonusAmarrCore"),
                                      skill="Amarr Core Systems")

    return locals()

def effect4153():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      module.getModifiedItemAttr("subsystemBonusCaldariCore"),
                                      skill="Caldari Core Systems")

    return locals()

def effect4154():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      module.getModifiedItemAttr("subsystemBonusGallenteCore"),
                                      skill="Gallente Core Systems")

    return locals()

def effect4155():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      module.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                                      skill="Minmatar Core Systems")

    return locals()

def effect4158():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("capacitorCapacity", src.getModifiedItemAttr("subsystemBonusCaldariCore"),
                               skill="Caldari Core Systems")

    return locals()

def effect4159():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("capacitorCapacity", src.getModifiedItemAttr("subsystemBonusAmarrCore"), skill="Amarr Core Systems")

    return locals()

def effect4161():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseMaxScanDeviation",
                                        container.getModifiedItemAttr("maxScanDeviationModifier") * level)

    return locals()

def effect4162():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalized = False if "skill" in context or "implant" in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseSensorStrength", container.getModifiedItemAttr("scanStrengthBonus") * level,
                                        stackingPenalties=penalized)

    return locals()

def effect4165():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                        "baseSensorStrength", ship.getModifiedItemAttr("shipBonusCF2"),
                                        skill="Caldari Frigate")

    return locals()

def effect4166():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                        "baseSensorStrength", ship.getModifiedItemAttr("shipBonusMF2"),
                                        skill="Minmatar Frigate")

    return locals()

def effect4167():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                        "baseSensorStrength", ship.getModifiedItemAttr("shipBonusGF2"),
                                        skill="Gallente Frigate")

    return locals()

def effect4168():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                        "baseSensorStrength", ship.getModifiedItemAttr("eliteBonusCovertOps2"),
                                        skill="Covert Ops")

    return locals()

def effect4187():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserAmarr1"),
                                      skill="Amarr Strategic Cruiser")

    return locals()

def effect4188():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserCaldari1"),
                                      skill="Caldari Strategic Cruiser")

    return locals()

def effect4189():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserGallente1"),
                                      skill="Gallente Strategic Cruiser")

    return locals()

def effect4190():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserMinmatar1"),
                                      skill="Minmatar Strategic Cruiser")

    return locals()

def effect4215():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "capacitorNeed", module.getModifiedItemAttr("subsystemBonusAmarrOffensive2"),
                                      skill="Amarr Offensive Systems")

    return locals()

def effect4216():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "powerTransferAmount",
                                      src.getModifiedItemAttr("subsystemBonusAmarrCore2"), skill="Amarr Core Systems")

    return locals()

def effect4217():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "energyNeutralizerAmount",
                                      src.getModifiedItemAttr("subsystemBonusAmarrCore2"), skill="Amarr Core Systems")

    return locals()

def effect4248():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "kineticDamage", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                        skill="Caldari Offensive Systems")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                        skill="Caldari Offensive Systems")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "kineticDamage", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                        skill="Caldari Offensive Systems")

    return locals()

def effect4250():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "armorHP", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                     skill="Gallente Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "hp", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                     skill="Gallente Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "damageMultiplier", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                     skill="Gallente Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "shieldCapacity", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                     skill="Gallente Offensive Systems")

    return locals()

def effect4251():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive2"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect4256():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "speed", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive2"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect4264():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("rechargeRate", src.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                               skill="Minmatar Core Systems")

    return locals()

def effect4265():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("rechargeRate", src.getModifiedItemAttr("subsystemBonusGallenteCore"),
                               skill="Gallente Core Systems")

    return locals()

def effect4269():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("subsystemBonusAmarrCore3"),
                               skill="Amarr Core Systems")

    return locals()

def effect4270():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("subsystemBonusMinmatarCore3"),
                               skill="Minmatar Core Systems")

    return locals()

def effect4271():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")

    return locals()

def effect4272():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusGallenteCore2"),
                               skill="Gallente Core Systems")

    return locals()

def effect4273():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "maxRange",
                                      src.getModifiedItemAttr("subsystemBonusGallenteCore2"), skill="Gallente Core Systems")

    return locals()

def effect4274():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", src.getModifiedItemAttr("subsystemBonusMinmatarCore2"), skill="Minmatar Core Systems")

    return locals()

def effect4275():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                               skill="Caldari Propulsion Systems")

    return locals()

def effect4277():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                               skill="Gallente Propulsion Systems")

    return locals()

def effect4278():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                               skill="Gallente Propulsion Systems")

    return locals()

def effect4280():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("agility", beacon.getModifiedItemAttr("agilityMultiplier"), stackingPenalties=True)

    return locals()

def effect4282():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", module.getModifiedItemAttr("subsystemBonusGallenteOffensive2"),
                                      skill="Gallente Offensive Systems")

    return locals()

def effect4283():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", module.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                      skill="Caldari Offensive Systems")

    return locals()

def effect4286():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")

    return locals()

def effect4288():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("subsystemBonusGallenteOffensive2"), skill="Gallente Offensive Systems")

    return locals()

def effect4290():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "capacitorNeed", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive2"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect4292():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "capacitorNeed", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                      skill="Caldari Offensive Systems")

    return locals()

def effect4321():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanLadarStrengthBonus",
                                      src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanRadarStrengthBonus",
                                      src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "maxRange",
                                      src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanGravimetricStrengthBonus",
                                      src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanMagnetometricStrengthBonus",
                                      src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")

    return locals()

def effect4327():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "hp", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "armorHP", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "shieldCapacity", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "damageMultiplier", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")

    return locals()

def effect4330():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "maxRange", module.getModifiedItemAttr("subsystemBonusAmarrOffensive3"),
                                      skill="Amarr Offensive Systems")

    return locals()

def effect4331():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles") or mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "maxVelocity", src.getModifiedItemAttr("subsystemBonusCaldariOffensive3"),
                                        skill="Caldari Offensive Systems")

    return locals()

def effect4342():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusMinmatarCore2"),
                               skill="Minmatar Core Systems")

    return locals()

def effect4343():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusAmarrCore2"),
                               skill="Amarr Core Systems")

    return locals()

def effect4347():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "trackingSpeed", module.getModifiedItemAttr("subsystemBonusGallenteOffensive3"),
                                      skill="Gallente Offensive Systems")

    return locals()

def effect4351():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "trackingSpeed", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect4358():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "maxRange", module.getModifiedItemAttr("ecmRangeBonus"),
                                      stackingPenalties=True)

    return locals()

def effect4360():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "speed", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")

    return locals()

def effect4362():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                        "emDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")

    return locals()

def effect4366():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect4369():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.forceItemAttr("warpBubbleImmune", module.getModifiedItemAttr("warpBubbleImmuneModifier"))

    return locals()

def effect4370():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusCC2"),
                                      skill="Caldari Cruiser")

    return locals()

def effect4372():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusCB3"),
                                      skill="Caldari Battleship")

    return locals()

def effect4373():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")

    return locals()

def effect4377():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect4378():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect4379():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect4380():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect4384():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusReconShip1"),
                                        skill="Recon Ships")

    return locals()

def effect4385():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusReconShip1"),
                                        skill="Recon Ships")

    return locals()

def effect4393():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "thermalDamage", ship.getModifiedItemAttr("eliteBonusCovertOps2"),
                                        skill="Covert Ops")

    return locals()

def effect4394():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "emDamage", ship.getModifiedItemAttr("eliteBonusCovertOps2"), skill="Covert Ops")

    return locals()

def effect4395():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosiveDamage", ship.getModifiedItemAttr("eliteBonusCovertOps2"),
                                        skill="Covert Ops")

    return locals()

def effect4396():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "kineticDamage", ship.getModifiedItemAttr("eliteBonusCovertOps2"),
                                        skill="Covert Ops")

    return locals()

def effect4397():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect4398():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect4399():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect4400():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect4413():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosionDelay", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect4415():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosionDelay", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect4416():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosionDelay", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect4417():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosionDelay", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect4451():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr("scanRadarStrength", implant.getModifiedItemAttr("scanRadarStrengthModifier"))

    return locals()

def effect4452():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr("scanLadarStrength", implant.getModifiedItemAttr("scanLadarStrengthModifier"))

    return locals()

def effect4453():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr("scanGravimetricStrength", implant.getModifiedItemAttr("scanGravimetricStrengthModifier"))

    return locals()

def effect4454():
    type = "passive"
    def handler(fit, implant, context):
        fit.ship.increaseItemAttr("scanMagnetometricStrength",
                                  implant.getModifiedItemAttr("scanMagnetometricStrengthModifier"))

    return locals()

def effect4456():
    type = "passive"
    runTime = "early"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanMagnetometricStrengthPercent",
                                                 implant.getModifiedItemAttr("implantSetFederationNavy"))

    return locals()

def effect4457():
    type = "passive"
    runTime = "early"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanRadarStrengthPercent",
                                                 implant.getModifiedItemAttr("implantSetImperialNavy"))

    return locals()

def effect4458():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanLadarStrengthPercent",
                                                 implant.getModifiedItemAttr("implantSetRepublicFleet"))

    return locals()

def effect4459():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanGravimetricStrengthPercent",
                                                 implant.getModifiedItemAttr("implantSetCaldariNavy"))

    return locals()

def effect446():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("shieldCapacity", container.getModifiedItemAttr("shieldCapacityBonus") * level)

    return locals()

def effect4460():
    type = "passive"
    runTime = "early"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanRadarStrengthModifier",
                                                 implant.getModifiedItemAttr("implantSetLGImperialNavy"))

    return locals()

def effect4461():
    type = "passive"
    runTime = "early"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanMagnetometricStrengthModifier",
                                                 implant.getModifiedItemAttr("implantSetLGFederationNavy"))

    return locals()

def effect4462():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanGravimetricStrengthModifier",
                                                 implant.getModifiedItemAttr("implantSetLGCaldariNavy"))

    return locals()

def effect4463():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                                 "scanLadarStrengthModifier",
                                                 implant.getModifiedItemAttr("implantSetLGRepublicFleet"))

    return locals()

def effect4464():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"), "speed",
                                      src.getModifiedItemAttr("shipBonusMF"), stackingPenalties=True, skill="Minmatar Frigate")

    return locals()

def effect4471():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect4472():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")

    return locals()

def effect4473():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusATC1"))

    return locals()

def effect4474():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusATC2"))

    return locals()

def effect4475():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusATC2"))

    return locals()

def effect4476():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusATF2"))

    return locals()

def effect4477():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusATF2"))

    return locals()

def effect4478():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusATF1"))

    return locals()

def effect4479():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Survey Probe",
                                        "explosionDelay", ship.getModifiedItemAttr("eliteBonusCovertOps3"),
                                        skill="Covert Ops")

    return locals()

def effect4482():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect4484():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")

    return locals()

def effect4485():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "speedFactor", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect4489():
    type = 'active'
    def handler(fit, module, context):
        pass

    return locals()

def effect4490():
    type = 'active'
    def handler(fit, module, context):
        pass

    return locals()

def effect4491():
    type = 'active'
    def handler(fit, module, context):
        pass

    return locals()

def effect4492():
    type = 'active'
    def handler(fit, module, context):
        pass

    return locals()

def effect4510():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "speedFactor", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect4512():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect4513():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "speedFactor", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect4515():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect4516():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect4527():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "falloff", module.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True)

    return locals()

def effect4555():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"),
                                        "emDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect4556():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"),
                                        "explosiveDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect4557():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"),
                                        "kineticDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect4558():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"),
                                        "thermalDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect4559():
    type = "active"
    def handler(fit, module, context):
        for attr in ("maxRange", "falloff", "trackingSpeed"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          attr, module.getModifiedItemAttr("%sBonus" % attr),
                                          stackingPenalties=True)

    return locals()

def effect4575():
    type = "active"
    runTime = "early"
    def handler(fit, src, context):
        fit.extraAttributes["siege"] = True
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
        fit.ship.multiplyItemAttr("mass", src.getModifiedItemAttr("siegeMassMultiplier"))
        fit.ship.multiplyItemAttr("scanResolution",
                                  src.getModifiedItemAttr("scanResolutionMultiplier"),
                                  stackingPenalties=True)
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
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                      "duration",
                                      src.getModifiedItemAttr("industrialCoreLocalLogisticsDurationBonus"),
                                      )
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                      "shieldBonus",
                                      src.getModifiedItemAttr("industrialCoreLocalLogisticsAmountBonus"),
                                      stackingPenalties=True
                                      )
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
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"),
                                      "maxRange",
                                      src.getModifiedItemAttr("industrialCoreBonusCommandBurstRange"),
                                      stackingPenalties=True
                                      )
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
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
        fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
        fit.ship.increaseItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))
        fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
        fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
        fit.ship.increaseItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))

    return locals()

def effect4576():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "falloffBonus", ship.getModifiedItemAttr("eliteBonusLogistics1"),
                                      skill="Logistics Cruisers")

    return locals()

def effect4577():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                      "falloffBonus", ship.getModifiedItemAttr("eliteBonusLogistics2"),
                                      skill="Logistics Cruisers")

    return locals()

def effect4579():
    type = "passive"
    def handler(fit, module, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Stasis Webifying Drone",
                                     "speedFactor", module.getModifiedItemAttr("webSpeedFactorBonus"))

    return locals()

def effect4619():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect4620():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect4621():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusATF1"))

    return locals()

def effect4622():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusATF2"))

    return locals()

def effect4623():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusATF2"))

    return locals()

def effect4624():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusATC2"))

    return locals()

def effect4625():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusATC2"))

    return locals()

def effect4626():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect4635():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("em", "explosive", "kinetic", "thermal")
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(
                lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
                "{0}Damage".format(damageType), ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect4636():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
            "aoeVelocity", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect4637():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Cruise Missiles") or mod.charge.requiresSkill("Torpedoes"),
            "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")

    return locals()

def effect4640():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
        for damageType in damageTypes:
            fit.ship.boostItemAttr("armor{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("shipBonusAC2"),
                                   skill="Amarr Cruiser")

    return locals()

def effect4643():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("em", "explosive", "kinetic", "thermal")
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                            "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusAC"),
                                            skill="Amarr Cruiser")

    return locals()

def effect4645():
    type = "passive"
    def handler(fit, ship, context):
        groups = ("Missile Launcher Rapid Light", "Missile Launcher Heavy Assault", "Missile Launcher Heavy")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                      skill="Heavy Assault Cruisers")

    return locals()

def effect4648():
    type = "passive"
    def handler(fit, ship, context):
        sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
        for type in sensorTypes:
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scan{0}StrengthBonus".format(type),
                                          ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")

    return locals()

def effect4649():
    type = "passive"
    def handler(fit, ship, context):
        affectedGroups = ("Missile Launcher Cruise", "Missile Launcher Torpedo")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in affectedGroups,
                                      "speed", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect4667():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                      "duration", ship.getModifiedItemAttr("shipBonusOreIndustrial1"),
                                      skill="ORE Industrial")

    return locals()

def effect4668():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                      "duration", ship.getModifiedItemAttr("shipBonusOreIndustrial1"),
                                      skill="ORE Industrial")

    return locals()

def effect4669():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                      "maxTractorVelocity", ship.getModifiedItemAttr("shipBonusOreIndustrial2"),
                                      skill="ORE Industrial")

    return locals()

def effect4670():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusOreIndustrial2"),
                                      skill="ORE Industrial")

    return locals()

def effect4728():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        damages = ("em", "thermal", "kinetic", "explosive")
        for damage in damages:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                            "{0}Damage".format(damage),
                                            beacon.getModifiedItemAttr("systemEffectDamageReduction"))
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Smart Bomb",
                                          "{0}Damage".format(damage),
                                          beacon.getModifiedItemAttr("systemEffectDamageReduction"))
            fit.ship.boostItemAttr("armor{0}DamageResonance".format(damage.capitalize()),
                                   beacon.getModifiedItemAttr("armor{0}DamageResistanceBonus".format(damage.capitalize())))
            fit.ship.boostItemAttr("shield{0}DamageResonance".format(damage.capitalize()),
                                   beacon.getModifiedItemAttr("shield{0}DamageResistanceBonus".format(damage.capitalize())))
        fit.drones.filteredItemBoost(lambda drone: True,
                                     "damageMultiplier", beacon.getModifiedItemAttr("systemEffectDamageReduction"))
        fit.modules.filteredItemBoost(lambda module: module.item.requiresSkill("Gunnery"),
                                      "damageMultiplier", beacon.getModifiedItemAttr("systemEffectDamageReduction"))

    return locals()

def effect4760():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                               skill="Caldari Propulsion Systems")

    return locals()

def effect4775():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", ship.getModifiedItemAttr("shipBonus2AF"),
                                      skill="Amarr Frigate")

    return locals()

def effect4782():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusATF2"))

    return locals()

def effect4789():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusATF1"))

    return locals()

def effect4793():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                      "speed", ship.getModifiedItemAttr("shipBonusATC1"))

    return locals()

def effect4794():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Light",
                                      "speed", ship.getModifiedItemAttr("shipBonusATC1"))

    return locals()

def effect4795():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                      "speed", ship.getModifiedItemAttr("shipBonusATC1"))

    return locals()

def effect4799():
    type = "passive"
    def handler(fit, ship, context):
        sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
        for type in sensorTypes:
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Jammer",
                                          "scan{0}StrengthBonus".format(type),
                                          ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")

    return locals()

def effect48():
    type = "active"
    def handler(fit, module, context):
        module.reloadTime = 10000
        module.forceReload = True
        if module.charge is None:
            return
        capAmount = module.getModifiedChargeAttr("capacitorBonus") or 0
        module.itemModifiedAttributes["capacitorNeed"] = -capAmount

    return locals()

def effect4804():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill(skill), "accessDifficultyBonus",
                                         skill.getModifiedItemAttr("accessDifficultyBonusAbsolutePercent") * skill.level)

    return locals()

def effect4809():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanGravimetricStrengthBonus", module.getModifiedItemAttr("ecmStrengthBonusPercent"),
                                      stackingPenalties=True)

    return locals()

def effect4810():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanLadarStrengthBonus", module.getModifiedItemAttr("ecmStrengthBonusPercent"),
                                      stackingPenalties=True)

    return locals()

def effect4811():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanMagnetometricStrengthBonus",
                                      module.getModifiedItemAttr("ecmStrengthBonusPercent"),
                                      stackingPenalties=True)

    return locals()

def effect4812():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scanRadarStrengthBonus", module.getModifiedItemAttr("ecmStrengthBonusPercent"),
                                      stackingPenalties=True)

    return locals()

def effect4814():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "consumptionQuantity",
                                      skill.getModifiedItemAttr("consumptionQuantityBonusPercent") * skill.level)

    return locals()

def effect4817():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Salvager",
                                      "duration", implant.getModifiedItemAttr("durationBonus"))

    return locals()

def effect4820():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                         "power", ship.getModifiedItemAttr("bcLargeTurretPower"))

    return locals()

def effect4821():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                         "power", ship.getModifiedItemAttr("bcLargeTurretPower"))

    return locals()

def effect4822():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                         "power", ship.getModifiedItemAttr("bcLargeTurretPower"))

    return locals()

def effect4823():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                         "cpu", ship.getModifiedItemAttr("bcLargeTurretCPU"))

    return locals()

def effect4824():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                         "cpu", ship.getModifiedItemAttr("bcLargeTurretCPU"))

    return locals()

def effect4825():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                         "cpu", ship.getModifiedItemAttr("bcLargeTurretCPU"))

    return locals()

def effect4826():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                         "capacitorNeed", ship.getModifiedItemAttr("bcLargeTurretCap"))

    return locals()

def effect4827():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                         "capacitorNeed", ship.getModifiedItemAttr("bcLargeTurretCap"))

    return locals()

def effect485():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("rechargeRate", container.getModifiedItemAttr("capRechargeBonus") * level)

    return locals()

def effect486():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("shieldRechargeRate", container.getModifiedItemAttr("rechargeratebonus") * level)

    return locals()

def effect4867():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "powerEngineeringOutputBonus",
                                                 implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect4868():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "capacitorCapacityBonus",
                                                 implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect4869():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "cpuOutputBonus2", implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect4871():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "capRechargeBonus", implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect4896():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "hp", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect4897():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect4898():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect490():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("powerOutput", container.getModifiedItemAttr("powerEngineeringOutputBonus") * level)

    return locals()

def effect4901():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect4902():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("MWDSignatureRadiusBonus"))

    return locals()

def effect4906():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill("Fighters"),
                                        "damageMultiplier", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                        stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4911():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRateMultiplier"))

    return locals()

def effect4921():
    type = "active"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonusPercent"))

    return locals()

def effect4923():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Micro Jump Drive Operation"),
                                      "duration", skill.getModifiedItemAttr("durationBonus") * skill.level)

    return locals()

def effect4928():
    from logbook import Logger
    import eos.config
    pyfalog = Logger(__name__)
    runTime = "late"
    type = "active"
    def handler(fit, module, context):
        damagePattern = fit.damagePattern
        static_adaptive_behavior = eos.config.settings['useStaticAdaptiveArmorHardener']
        if (damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount) and static_adaptive_behavior:
            for attr in ("armorEmDamageResonance", "armorThermalDamageResonance", "armorKineticDamageResonance", "armorExplosiveDamageResonance"):
                fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr), stackingPenalties=True, penaltyGroup="preMul")
            return
        if damagePattern:
            baseDamageTaken = (
                damagePattern.emAmount * fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
                damagePattern.thermalAmount * fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
                damagePattern.kineticAmount * fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
                damagePattern.explosiveAmount * fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
            )
            resistanceShiftAmount = module.getModifiedItemAttr(
                'resistanceShiftAmount') / 100  # The attribute is in percent and we want a fraction
            RAHResistance = [
                module.getModifiedItemAttr('armorEmDamageResonance'),
                module.getModifiedItemAttr('armorThermalDamageResonance'),
                module.getModifiedItemAttr('armorKineticDamageResonance'),
                module.getModifiedItemAttr('armorExplosiveDamageResonance'),
            ]
            cycleList = []
            loopStart = -20
            for num in range(50):
                damagePattern_tuples = [
                    (0, baseDamageTaken[0] * RAHResistance[0], RAHResistance[0]),
                    (3, baseDamageTaken[3] * RAHResistance[3], RAHResistance[3]),
                    (2, baseDamageTaken[2] * RAHResistance[2], RAHResistance[2]),
                    (1, baseDamageTaken[1] * RAHResistance[1], RAHResistance[1]),
                ]
                sortedDamagePattern_tuples = sorted(damagePattern_tuples, key=lambda damagePattern: damagePattern[1])
                if sortedDamagePattern_tuples[2][1] == 0:
                    change0 = 1 - sortedDamagePattern_tuples[0][2]
                    change1 = 1 - sortedDamagePattern_tuples[1][2]
                    change2 = 1 - sortedDamagePattern_tuples[2][2]
                    change3 = -(change0 + change1 + change2)
                elif sortedDamagePattern_tuples[1][1] == 0:
                    change0 = 1 - sortedDamagePattern_tuples[0][2]
                    change1 = 1 - sortedDamagePattern_tuples[1][2]
                    change2 = -(change0 + change1) / 2
                    change3 = -(change0 + change1) / 2
                else:
                    change0 = min(resistanceShiftAmount, 1 - sortedDamagePattern_tuples[0][2])
                    change1 = min(resistanceShiftAmount, 1 - sortedDamagePattern_tuples[1][2])
                    change2 = -(change0 + change1) / 2
                    change3 = -(change0 + change1) / 2
                RAHResistance[sortedDamagePattern_tuples[0][0]] = sortedDamagePattern_tuples[0][2] + change0
                RAHResistance[sortedDamagePattern_tuples[1][0]] = sortedDamagePattern_tuples[1][2] + change1
                RAHResistance[sortedDamagePattern_tuples[2][0]] = sortedDamagePattern_tuples[2][2] + change2
                RAHResistance[sortedDamagePattern_tuples[3][0]] = sortedDamagePattern_tuples[3][2] + change3
                for i, val in enumerate(cycleList):
                    tolerance = 1e-06
                    if abs(RAHResistance[0] - val[0]) <= tolerance and \
                                abs(RAHResistance[1] - val[1]) <= tolerance and \
                                abs(RAHResistance[2] - val[2]) <= tolerance and \
                                abs(RAHResistance[3] - val[3]) <= tolerance:
                        loopStart = i
                        break
                if loopStart >= 0:
                    break
                cycleList.append(list(RAHResistance))
            loopCycles = cycleList[loopStart:]
            numCycles = len(loopCycles)
            average = [0, 0, 0, 0]
            for cycle in loopCycles:
                for i in range(4):
                    average[i] += cycle[i]
            for i in range(4):
                average[i] = round(average[i] / numCycles, 3)
            for i, attr in enumerate((
                    'armorEmDamageResonance', 'armorThermalDamageResonance', 'armorKineticDamageResonance',
                    'armorExplosiveDamageResonance')):
                module.increaseItemAttr(attr, average[i] - module.getModifiedItemAttr(attr))
                fit.ship.multiplyItemAttr(attr, average[i], stackingPenalties=True, penaltyGroup="preMul")

    return locals()

def effect4934():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGF2"),
                                      skill="Gallente Frigate")

    return locals()

def effect4936():
    runTime = "late"
    type = "active"
    def handler(fit, module, context):
        amount = module.getModifiedItemAttr("shieldBonus")
        speed = module.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("shieldRepair", amount / speed)

    return locals()

def effect494():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("warpCapacitorNeed", container.getModifiedItemAttr("warpCapacitorNeedBonus") * level,
                               stackingPenalties="skill" not in context)

    return locals()

def effect4941():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect4942():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect4945():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Breaker",
                                      "duration", skill.getModifiedItemAttr("durationBonus") * skill.level)

    return locals()

def effect4946():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Breaker",
                                      "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)

    return locals()

def effect4950():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect4951():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
            "shieldBonus", container.getModifiedItemAttr("shieldBoostMultiplier"))

    return locals()

def effect4961():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Shield Operation") or
                                                     mod.item.requiresSkill("Capital Shield Operation"),
                                         "shieldBonus", module.getModifiedItemAttr("shieldBonusMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect4967():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
            "duration", module.getModifiedItemAttr("durationSkillBonus"))

    return locals()

def effect4970():
    type = "boosterSideEffect"
    displayName = "Shield Boost"
    attr = "boosterShieldBoostAmountPenalty"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"), "shieldBonus",
                                      src.getModifiedItemAttr("boosterShieldBoostAmountPenalty"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"), "shieldBonus",
                                      src.getModifiedItemAttr("boosterShieldBoostAmountPenalty"))

    return locals()

def effect4972():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Light",
                                      "speed", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect4973():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rocket",
                                      "speed", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect4974():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("eliteBonusViolators2"), skill="Marauders")

    return locals()

def effect4975():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusATF2"))

    return locals()

def effect4976():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Resistance Shift Hardener", "duration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Resistance Phasing"), "duration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect4989():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeCloudSize", implant.getModifiedItemAttr("aoeCloudSizeBonus"))

    return locals()

def effect4990():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("rookieSETCapBonus"))

    return locals()

def effect4991():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("rookieSETDamageBonus"))

    return locals()

def effect4994():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))

    return locals()

def effect4995():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))

    return locals()

def effect4996():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))

    return locals()

def effect4997():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))

    return locals()

def effect4999():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("rookieSHTOptimalBonus"))

    return locals()

def effect50():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRateMultiplier") or 1)

    return locals()

def effect5000():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("rookieMissileKinDamageBonus"))

    return locals()

def effect5008():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))

    return locals()

def effect5009():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))

    return locals()

def effect5011():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))

    return locals()

def effect5012():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))

    return locals()

def effect5013():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("rookieSHTDamageBonus"))

    return locals()

def effect5014():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("rookieDroneBonus"))

    return locals()

def effect5015():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "maxTargetRangeBonus", ship.getModifiedItemAttr("rookieDampStrengthBonus"))

    return locals()

def effect5016():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "scanResolutionBonus", ship.getModifiedItemAttr("rookieDampStrengthBonus"))

    return locals()

def effect5017():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("rookieArmorRepBonus"))

    return locals()

def effect5018():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("rookieShipVelocityBonus"))

    return locals()

def effect5019():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("rookieTargetPainterStrengthBonus"))

    return locals()

def effect5020():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("rookieSPTDamageBonus"))

    return locals()

def effect5021():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("rookieShieldBoostBonus"))

    return locals()

def effect5028():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("Gravimetric", "Ladar", "Radar", "Magnetometric"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                          "scan{0}StrengthBonus".format(type),
                                          ship.getModifiedItemAttr("rookieECMStrengthBonus"))

    return locals()

def effect5029():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                     "miningAmount",
                                     src.getModifiedItemAttr("roleBonusDroneMiningYield"),
                                     )

    return locals()

def effect5030():
    type = "passive"
    def handler(fit, container, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                     "miningAmount", container.getModifiedItemAttr("rookieDroneBonus"))

    return locals()

def effect5035():
    type = "passive"
    def handler(fit, ship, context):
        for type in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         type, ship.getModifiedItemAttr("rookieDroneBonus"))

    return locals()

def effect5036():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                      "duration", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect504():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        amount = container.getModifiedItemAttr("droneRangeBonus") * level
        fit.extraAttributes.increase("droneControlRange", amount)

    return locals()

def effect5045():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                      "duration", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect5048():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                      "duration", ship.getModifiedItemAttr("shipBonusGF"), skill="Amarr Frigate")

    return locals()

def effect5051():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                      "duration", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect5055():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                         "duration", ship.getModifiedItemAttr("iceHarvestCycleBonus"))

    return locals()

def effect5058():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Mining"),
                                         "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))

    return locals()

def effect5059():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                      "duration", container.getModifiedItemAttr("shipBonusORE3"), skill="Mining Barge")

    return locals()

def effect506():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)

    return locals()

def effect5066():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Target Painting"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect5067():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("specialOreHoldCapacity", ship.getModifiedItemAttr("shipBonusORE2"), skill="Mining Barge")

    return locals()

def effect5068():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("shipBonusORE2"), skill="Mining Barge")

    return locals()

def effect5069():
    type = "passive"
    runTime = "early"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Mercoxit Processing"),
                                        "specialisationAsteroidYieldMultiplier",
                                        module.getModifiedItemAttr("miningAmountBonus"))

    return locals()

def effect507():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.ship.boostItemAttr("maxTargetRange", container.getModifiedItemAttr("maxTargetRangeBonus") * level)

    return locals()

def effect5079():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect508():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect5080():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect5081():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True)

    return locals()

def effect5087():
    type = "passive"
    def handler(fit, ship, context):
        for layer in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         layer, ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5090():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect51():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("rechargeRate", module.getModifiedItemAttr("capacitorRechargeRateMultiplier"))

    return locals()

def effect5103():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect5104():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5105():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect5106():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect5107():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5108():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonusGF2"),
                                      skill="Gallente Frigate")

    return locals()

def effect5109():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect511():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect5110():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect5111():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5119():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                        "baseSensorStrength", ship.getModifiedItemAttr("shipBonus2AF"),
                                        skill="Amarr Frigate")

    return locals()

def effect512():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5121():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "powerTransferAmount", ship.getModifiedItemAttr("energyTransferAmountBonus"))

    return locals()

def effect5122():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")

    return locals()

def effect5123():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5124():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect5125():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonusGC2"),
                                      skill="Gallente Cruiser")

    return locals()

def effect5126():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect5127():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect5128():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5129():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMC"),
                                      skill="Minmatar Cruiser")

    return locals()

def effect5131():
    type = "passive"
    def handler(fit, ship, context):
        groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "speed", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect5132():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect5133():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect5136():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5139():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "miningAmount", module.getModifiedItemAttr("shipBonusOREfrig1"),
                                      skill="Mining Frigate")

    return locals()

def effect514():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect5142():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                         "miningAmount", module.getModifiedItemAttr("miningAmountMultiplier"))

    return locals()

def effect5153():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5156():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                      "duration", module.getModifiedItemAttr("shipBonusOREfrig2"), skill="Mining Frigate")

    return locals()

def effect516():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5162():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Resistance Shift Hardener", "capacitorNeed",
                                      src.getModifiedItemAttr("capNeedBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Resistance Phasing"), "capacitorNeed",
                                      src.getModifiedItemAttr("capNeedBonus") * lvl)

    return locals()

def effect5165():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "maxVelocity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5168():
    type = "passive"
    def handler(fit, container, context):
        fit.drones.filteredItemIncrease(lambda drone: drone.item.requiresSkill("Salvage Drone Operation"),
                                        "accessDifficultyBonus",
                                        container.getModifiedItemAttr("accessDifficultyBonus") * container.level)

    return locals()

def effect5180():
    type = "passive"
    def handler(fit, container, context):
        fit.ship.boostItemAttr("scanGravimetricStrength",
                               container.getModifiedItemAttr("sensorStrengthBonus") * container.level)

    return locals()

def effect5181():
    type = "passive"
    def handler(fit, container, context):
        fit.ship.boostItemAttr("scanLadarStrength", container.getModifiedItemAttr("sensorStrengthBonus") * container.level)

    return locals()

def effect5182():
    type = "passive"
    def handler(fit, container, context):
        fit.ship.boostItemAttr("scanMagnetometricStrength",
                               container.getModifiedItemAttr("sensorStrengthBonus") * container.level)

    return locals()

def effect5183():
    type = "passive"
    def handler(fit, container, context):
        fit.ship.boostItemAttr("scanRadarStrength", container.getModifiedItemAttr("sensorStrengthBonus") * container.level)

    return locals()

def effect5185():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", ship.getModifiedItemAttr("shipBonus2AF"),
                                      skill="Amarr Frigate")

    return locals()

def effect5187():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                      "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusGC"),
                                      skill="Gallente Cruiser")

    return locals()

def effect5188():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                      stackingPenalties=True)

    return locals()

def effect5189():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                      stackingPenalties=True)

    return locals()

def effect5190():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Projectile Weapon",
                                      "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                      stackingPenalties=True)

    return locals()

def effect5201():
    type = "passive"
    def handler(fit, container, context):
        level = container.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Reinforcer",
                                      "massAddition", container.getModifiedItemAttr("massPenaltyReduction") * level)

    return locals()

def effect5205():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("rookieSETTracking"))

    return locals()

def effect5206():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("rookieSETOptimal"))

    return locals()

def effect5207():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", ship.getModifiedItemAttr("rookieNosDrain"))

    return locals()

def effect5208():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", ship.getModifiedItemAttr("rookieNeutDrain"))

    return locals()

def effect5209():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "speedFactor", ship.getModifiedItemAttr("rookieWebAmount"))

    return locals()

def effect521():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect5212():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda mod: True,
                                     "maxVelocity", ship.getModifiedItemAttr("rookieDroneMWDspeed"))

    return locals()

def effect5213():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "maxVelocity", ship.getModifiedItemAttr("rookieRocketVelocity"))

    return locals()

def effect5214():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("rookieLightMissileVelocity"))

    return locals()

def effect5215():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("rookieSHTTracking"))

    return locals()

def effect5216():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("rookieSHTFalloff"))

    return locals()

def effect5217():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("rookieSPTTracking"))

    return locals()

def effect5218():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("rookieSPTFalloff"))

    return locals()

def effect5219():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("rookieSPTOptimal"))

    return locals()

def effect5220():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5221():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5222():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5223():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5224():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5225():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5226():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5227():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5228():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5229():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseSensorStrength", container.getModifiedItemAttr("shipBonusRole8"))

    return locals()

def effect5230():
    type = "active"
    def handler(fit, module, context):
        for damageType in ("kinetic", "thermal", "explosive", "em"):
            fit.ship.boostItemAttr("shield" + damageType.capitalize() + "DamageResonance",
                                   module.getModifiedItemAttr(damageType + "DamageResistanceBonus"),
                                   stackingPenalties=True)

    return locals()

def effect5231():
    type = "active"
    def handler(fit, module, context):
        for damageType in ("kinetic", "thermal", "explosive", "em"):
            fit.ship.boostItemAttr("armor%sDamageResonance" % damageType.capitalize(),
                                   module.getModifiedItemAttr("%sDamageResistanceBonus" % damageType),
                                   stackingPenalties=True)

    return locals()

def effect5234():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "explosiveDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5237():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "kineticDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5240():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "thermalDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5243():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "emDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5259():
    type = "passive"
    runTime = "early"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                      "cpu", ship.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")

    return locals()

def effect5260():
    type = "passive"
    runTime = "early"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                      "cpu", ship.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")

    return locals()

def effect5261():
    type = "passive"
    def handler(fit, module, context):
        module.increaseItemAttr("cpu", module.getModifiedItemAttr("covertCloakCPUAdd") or 0)

    return locals()

def effect5262():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Cloaking"),
                                         "covertCloakCPUAdd", module.getModifiedItemAttr("covertCloakCPUPenalty"))

    return locals()

def effect5263():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Cynosural Field Theory"),
                                         "covertCloakCPUAdd", module.getModifiedItemAttr("covertCloakCPUPenalty"))

    return locals()

def effect5264():
    type = "passive"
    def handler(fit, module, context):
        module.increaseItemAttr("cpu", module.getModifiedItemAttr("warfareLinkCPUAdd") or 0)

    return locals()

def effect5265():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"),
                                         "warfareLinkCPUAdd", module.getModifiedItemAttr("warfareLinkCPUPenalty"))

    return locals()

def effect5266():
    type = "passive"
    runTime = "early"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                      "cpu", ship.getModifiedItemAttr("eliteIndustrialCovertCloakBonus"),
                                      skill="Transport Ships")

    return locals()

def effect5267():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "power", module.getModifiedItemAttr("drawback"))

    return locals()

def effect5268():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                      "power", module.getModifiedItemAttr("drawback"))

    return locals()

def effect527():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusMI"), skill="Minmatar Industrial")

    return locals()

def effect5275():
    runTime = "late"
    type = "active"
    def handler(fit, module, context):
        if module.charge and module.charge.name == "Nanite Repair Paste":
            multiplier = 3
        else:
            multiplier = 1
        amount = module.getModifiedItemAttr("armorDamageAmount") * multiplier
        speed = module.getModifiedItemAttr("duration") / 1000.0
        rps = amount / speed
        fit.extraAttributes.increase("armorRepair", rps)
        fit.extraAttributes.increase("armorRepairPreSpool", rps)
        fit.extraAttributes.increase("armorRepairFullSpool", rps)

    return locals()

def effect529():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusAI"), skill="Amarr Industrial")

    return locals()

def effect5293():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")

    return locals()

def effect5294():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")

    return locals()

def effect5295():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                     src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")

    return locals()

def effect5300():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                     src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                     src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                     src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")

    return locals()

def effect5303():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")

    return locals()

def effect5304():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")

    return locals()

def effect5305():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCD1"),
                                        skill="Caldari Destroyer")

    return locals()

def effect5306():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCD1"),
                                        skill="Caldari Destroyer")

    return locals()

def effect5307():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")

    return locals()

def effect5308():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")

    return locals()

def effect5309():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")

    return locals()

def effect5310():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGD2"), skill="Gallente Destroyer")

    return locals()

def effect5311():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                     src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")

    return locals()

def effect5316():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                     src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                     src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                     src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")

    return locals()

def effect5317():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMD1"),
                                      skill="Minmatar Destroyer")

    return locals()

def effect5318():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusMD2"), skill="Minmatar Destroyer")

    return locals()

def effect5319():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusMD1"),
                                        skill="Minmatar Destroyer")

    return locals()

def effect5320():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusMD1"),
                                        skill="Minmatar Destroyer")

    return locals()

def effect5321():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMD2"),
                                      skill="Minmatar Destroyer")

    return locals()

def effect5322():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusABC1"),
                               skill="Amarr Battlecruiser")

    return locals()

def effect5323():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusABC1"),
                               skill="Amarr Battlecruiser")

    return locals()

def effect5324():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusABC1"),
                               skill="Amarr Battlecruiser")

    return locals()

def effect5325():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusABC1"),
                               skill="Amarr Battlecruiser")

    return locals()

def effect5326():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusABC2"),
                                     skill="Amarr Battlecruiser")

    return locals()

def effect5331():
    type = "passive"
    def handler(fit, ship, context):
        for layer in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         layer, ship.getModifiedItemAttr("shipBonusABC2"), skill="Amarr Battlecruiser")

    return locals()

def effect5332():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC1"),
                                      skill="Amarr Battlecruiser")

    return locals()

def effect5333():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusABC2"),
                                      skill="Amarr Battlecruiser")

    return locals()

def effect5334():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCBC1"), skill="Caldari Battlecruiser")

    return locals()

def effect5335():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                               skill="Caldari Battlecruiser")

    return locals()

def effect5336():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                               skill="Caldari Battlecruiser")

    return locals()

def effect5337():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                               skill="Caldari Battlecruiser")

    return locals()

def effect5338():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                               skill="Caldari Battlecruiser")

    return locals()

def effect5339():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCBC1"),
                                        skill="Caldari Battlecruiser")

    return locals()

def effect5340():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCBC1"),
                                        skill="Caldari Battlecruiser")

    return locals()

def effect5341():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC1"),
                                      skill="Gallente Battlecruiser")

    return locals()

def effect5342():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGBC2"),
                                      skill="Gallente Battlecruiser")

    return locals()

def effect5343():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC1"),
                                     skill="Gallente Battlecruiser")

    return locals()

def effect5348():
    type = "passive"
    def handler(fit, ship, context):
        for layer in ("shieldCapacity", "armorHP", "hp"):
            fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                         layer, ship.getModifiedItemAttr("shipBonusGBC1"), skill="Gallente Battlecruiser")

    return locals()

def effect5349():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                      "speed", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")

    return locals()

def effect5350():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                      "speed", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")

    return locals()

def effect5351():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMBC1"),
                                      skill="Minmatar Battlecruiser")

    return locals()

def effect5352():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMBC1"),
                                      skill="Minmatar Battlecruiser")

    return locals()

def effect5353():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")

    return locals()

def effect5354():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC1"),
                                      skill="Amarr Battlecruiser")

    return locals()

def effect5355():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusABC2"),
                                      skill="Amarr Battlecruiser")

    return locals()

def effect5356():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCBC1"), skill="Caldari Battlecruiser")

    return locals()

def effect5357():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusCBC2"),
                                      skill="Caldari Battlecruiser")

    return locals()

def effect5358():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGBC1"),
                                      skill="Gallente Battlecruiser")

    return locals()

def effect5359():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC2"),
                                      skill="Gallente Battlecruiser")

    return locals()

def effect536():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("cpuOutput", module.getModifiedItemAttr("cpuMultiplier"))

    return locals()

def effect5360():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusMBC1"), skill="Minmatar Battlecruiser")

    return locals()

def effect5361():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")

    return locals()

def effect5364():
    type = "passive"
    def handler(fit, booster, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Capital Repair Systems"),
            "armorDamageAmount", booster.getModifiedItemAttr("armorDamageAmountBonus") or 0)

    return locals()

def effect5365():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("eliteBonusViolators2"),
                                      skill="Marauders")

    return locals()

def effect5366():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusATC2"))

    return locals()

def effect5367():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGB2"),
                                      skill="Gallente Battleship")

    return locals()

def effect5378():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCBC1"),
                                        skill="Caldari Battlecruiser")

    return locals()

def effect5379():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCBC1"),
                                        skill="Caldari Battlecruiser")

    return locals()

def effect5380():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGBC2"),
                                      skill="Gallente Battlecruiser")

    return locals()

def effect5381():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusABC1"),
                                      skill="Amarr Battlecruiser")

    return locals()

def effect5382():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect5383():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect5384():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect5385():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect5386():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect5387():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect5388():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect5389():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5390():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "maxVelocity", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5397():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseMaxScanDeviation",
                                        module.getModifiedItemAttr("maxScanDeviationModifierModule"),
                                        stackingPenalties=True)

    return locals()

def effect5398():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                      "duration", module.getModifiedItemAttr("scanDurationBonus"))

    return locals()

def effect5399():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseSensorStrength", module.getModifiedItemAttr("scanStrengthBonusModule"),
                                        stackingPenalties=True)

    return locals()

def effect5402():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusABC2"),
                                        skill="Amarr Battlecruiser")

    return locals()

def effect5403():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusABC2"),
                                        skill="Amarr Battlecruiser")

    return locals()

def effect5410():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC2"),
                                      skill="Amarr Battlecruiser")

    return locals()

def effect5411():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")

    return locals()

def effect5417():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect5418():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect5419():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect542():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect5420():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "hp", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect5424():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")

    return locals()

def effect5427():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")

    return locals()

def effect5428():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "maxRange", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")

    return locals()

def effect5429():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusMB2"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5430():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "aoeVelocity", ship.getModifiedItemAttr("shipBonusMB2"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5431():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect5433():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"),
                                         "virusCoherence", container.getModifiedItemAttr("virusCoherenceBonus") * level)

    return locals()

def effect5437():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Archaeology"),
                                         "virusCoherence", container.getModifiedItemAttr("virusCoherenceBonus") * level)

    return locals()

def effect5440():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                           "kineticDamage", beacon.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5444():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect5445():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect5456():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                      "speed", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect5457():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                      "speed", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect5459():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"), "virusStrength", src.getModifiedItemAttr("virusStrengthBonus"))

    return locals()

def effect5460():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemIncrease(
            lambda mod: (mod.item.requiresSkill("Hacking") or mod.item.requiresSkill("Archaeology")),
            "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)

    return locals()

def effect5461():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("shieldRechargeRate", module.getModifiedItemAttr("rechargeratebonus") or 0)

    return locals()

def effect5468():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusCI2"), skill="Caldari Industrial")

    return locals()

def effect5469():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusMI2"), skill="Minmatar Industrial")

    return locals()

def effect5470():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusGI2"), skill="Gallente Industrial")

    return locals()

def effect5471():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusAI2"), skill="Amarr Industrial")

    return locals()

def effect5476():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("specialOreHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2"),
                               skill="Gallente Industrial")

    return locals()

def effect5477():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("specialAmmoHoldCapacity", ship.getModifiedItemAttr("shipBonusMI2"),
                               skill="Minmatar Industrial")

    return locals()

def effect5478():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("specialPlanetaryCommoditiesHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2"),
                               skill="Gallente Industrial")

    return locals()

def effect5479():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("specialMineralHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2"),
                               skill="Gallente Industrial")

    return locals()

def effect5480():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "implantBonusVelocity", implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect5482():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "agilityBonus", implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect5483():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "shieldCapacityBonus", implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect5484():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                                 "armorHpBonus2", implant.getModifiedItemAttr("implantSetChristmas"))

    return locals()

def effect5485():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect5486():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMBC2"),
                                      skill="Minmatar Battlecruiser")

    return locals()

def effect549():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMB"),
                                      skill="Minmatar Battleship")

    return locals()

def effect5496():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                      "speed", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")

    return locals()

def effect5497():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                      "speed", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")

    return locals()

def effect5498():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "aoeVelocity", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                        skill="Command Ships")

    return locals()

def effect5499():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                        skill="Command Ships")

    return locals()

def effect55():
    type = "active"
    def handler(fit, module, context):
        pass

    return locals()

def effect550():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusGB"),
                                      skill="Gallente Battleship")

    return locals()

def effect5500():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "aoeCloudSize", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                        skill="Command Ships")

    return locals()

def effect5501():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                      skill="Command Ships")

    return locals()

def effect5502():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusCommandShips1"),
                                      skill="Command Ships")

    return locals()

def effect5503():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "trackingSpeed", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                     skill="Command Ships")

    return locals()

def effect5504():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "maxVelocity", ship.getModifiedItemAttr("eliteBonusCommandShips2"),
                                     skill="Command Ships")

    return locals()

def effect5505():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "speed", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")

    return locals()

def effect5514():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("em", "explosive", "kinetic", "thermal")
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                            "{0}Damage".format(damageType),
                                            ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")

    return locals()

def effect5521():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("em", "explosive", "kinetic", "thermal")
        for damageType in damageTypes:
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                            "{0}Damage".format(damageType),
                                            ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")

    return locals()

def effect553():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")

    return locals()

def effect5539():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5540():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5541():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5542():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect5552():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                        skill="Heavy Assault Cruisers")

    return locals()

def effect5553():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                        skill="Heavy Assault Cruisers")

    return locals()

def effect5554():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGC2"),
                                      skill="Gallente Cruiser")

    return locals()

def effect5555():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "maxVelocity", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5556():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5557():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                     skill="Heavy Assault Cruisers")

    return locals()

def effect5558():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "trackingSpeed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                     skill="Heavy Assault Cruisers")

    return locals()

def effect5559():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect5560():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Micro Jump Drive",
                                      "moduleReactivationDelay", ship.getModifiedItemAttr("roleBonusMarauder"))

    return locals()

def effect5564():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")

    return locals()

def effect5568():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")

    return locals()

def effect5570():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                      "war"
                                      "fareBuff1Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "buffDuration", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")

    return locals()

def effect5572():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")

    return locals()

def effect5573():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")

    return locals()

def effect5574():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")

    return locals()

def effect5575():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")

    return locals()

def effect56():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("powerOutput", module.getModifiedItemAttr("powerOutputMultiplier", None))

    return locals()

def effect5607():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                      "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)

    return locals()

def effect5610():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect5611():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusGB2"), skill="Gallente Battleship")

    return locals()

def effect5618():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy",
                                      "speed", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect5619():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy",
                                      "speed", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect562():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5620():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy",
                                      "speed", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect5621():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                      "speed", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect5622():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                      "speed", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect5628():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect5629():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5630():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5631():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5632():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5633():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect5634():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5635():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5636():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")

    return locals()

def effect5637():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5638():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5639():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusMB"),
                                        skill="Minmatar Battleship")

    return locals()

def effect5644():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect5647():
    type = "passive"
    runTime = "early"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                      "cpu", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5650():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
        for damageType in damageTypes:
            fit.ship.boostItemAttr("armor{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("shipBonusAF"),
                                   skill="Amarr Frigate")

    return locals()

def effect5657():
    type = "passive"
    def handler(fit, ship, context):
        damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
        for damageType in damageTypes:
            fit.ship.boostItemAttr("shield{0}DamageResonance".format(damageType),
                                   ship.getModifiedItemAttr("eliteBonusInterceptor2"), skill="Interceptors")

    return locals()

def effect5673():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusInterceptor2"),
                                      skill="Interceptors")

    return locals()

def effect5676():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")

    return locals()

def effect5688():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")

    return locals()

def effect5695():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("Em", "Thermal", "Explosive", "Kinetic"):
            fit.ship.boostItemAttr("armor%sDamageResonance" % damageType,
                                   ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")

    return locals()

def effect57():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacityMultiplier", None))

    return locals()

def effect5717():
    runTime = "early"
    type = "passive"
    def handler(fit, implant, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                                 "WarpSBonus", implant.getModifiedItemAttr("implantSetWarpSpeed"))

    return locals()

def effect5721():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5722():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")

    return locals()

def effect5723():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusInterdictors2"),
                                      skill="Interdictors")

    return locals()

def effect5724():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5725():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5726():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5733():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosiveDamage", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect5734():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "kineticDamage", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect5735():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "emDamage", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect5736():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "thermalDamage", ship.getModifiedItemAttr("eliteBonusViolatorsRole1"))

    return locals()

def effect5737():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseSensorStrength", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5738():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusRole8"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusRole8"))

    return locals()

def effect5754():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("maxRangeBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
        module.boostItemAttr("falloffBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
        module.boostItemAttr("trackingSpeedBonus", module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))

    return locals()

def effect5757():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("maxTargetRangeBonus", module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"))
        module.boostItemAttr("scanResolutionBonus", module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"),
                             stackingPenalties=True)
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            module.boostItemAttr(
                "scan{}StrengthPercent".format(scanType),
                module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"),
                stackingPenalties=True
            )

    return locals()

def effect5758():
    type = "overheat"
    def handler(fit, module, context):
        module.boostItemAttr("signatureRadiusBonus", module.getModifiedItemAttr("overloadPainterStrengthBonus") or 0)

    return locals()

def effect5769():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                     "structureDamageAmount", container.getModifiedItemAttr("damageHP") * level)

    return locals()

def effect5778():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect5779():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect5793():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        for attr in ("maxRangeBonus", "falloffBonus"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                          attr, container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)

    return locals()

def effect58():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("capacitorCapacity", module.getModifiedItemAttr("capacitorCapacityMultiplier", None))

    return locals()

def effect5802():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "speedFactor", module.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect5803():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5804():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5805():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "hp", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5806():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5807():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5808():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5809():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect581():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)

    return locals()

def effect5810():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "hp", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5811():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusGB2"),
                                        skill="Gallente Battleship")

    return locals()

def effect5812():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusGB2"),
                                        skill="Gallente Battleship")

    return locals()

def effect5813():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "speedFactor", module.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5814():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5815():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect5816():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5817():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "hp", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5818():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5819():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect582():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "speed", skill.getModifiedItemAttr("rofBonus") * skill.level)

    return locals()

def effect5820():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "speedFactor", module.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect5821():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5822():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "hp", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5823():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5824():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect5825():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect5826():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect5827():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect5829():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "duration", ship.getModifiedItemAttr("shipBonusORE3"), skill="Mining Barge")

    return locals()

def effect5832():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Mining") or mod.item.requiresSkill("Ice Harvesting"),
            "maxRange", ship.getModifiedItemAttr("shipBonusORE2"), skill="Mining Barge")

    return locals()

def effect5839():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "thermal", "explosive", "kinetic"):
            fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                                   ship.getModifiedItemAttr("eliteBonusBarge1"), skill="Exhumers")

    return locals()

def effect584():
    type = "passive"
    def handler(fit, implant, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "damageMultiplier", implant.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect5840():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "duration", ship.getModifiedItemAttr("eliteBonusBarge2"), skill="Exhumers")

    return locals()

def effect5852():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                      "miningAmount", module.getModifiedItemAttr("eliteBonusExpedition1"),
                                      skill="Expedition Frigates")

    return locals()

def effect5853():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("signatureRadius", ship.getModifiedItemAttr("eliteBonusExpedition2"),
                               skill="Expedition Frigates")

    return locals()

def effect5862():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "emDamage", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect5863():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCB"),
                                        skill="Caldari Battleship")

    return locals()

def effect5864():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "thermalDamage", ship.getModifiedItemAttr("shipBonusCB"),
                                        skill="Caldari Battleship")

    return locals()

def effect5865():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", ship.getModifiedItemAttr("shipBonusCB"),
                                        skill="Caldari Battleship")

    return locals()

def effect5866():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                      "maxRange", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")

    return locals()

def effect5867():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosionDelay", ship.getModifiedItemAttr("shipBonusRole8"))

    return locals()

def effect5868():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("capacity", module.getModifiedItemAttr("drawback"))

    return locals()

def effect5869():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", ship.getModifiedItemAttr("eliteBonusIndustrial1"),
                               skill="Transport Ships")

    return locals()

def effect587():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect5870():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusCI2"), skill="Caldari Industrial")

    return locals()

def effect5871():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("shipBonusMI2"), skill="Minmatar Industrial")

    return locals()

def effect5872():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusAI2"),
                                      skill="Amarr Industrial")

    return locals()

def effect5873():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGI2"),
                                      skill="Gallente Industrial")

    return locals()

def effect5874():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("fleetHangarCapacity", ship.getModifiedItemAttr("eliteBonusIndustrial1"),
                               skill="Transport Ships")

    return locals()

def effect588():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Projectile Weapon",
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect5881():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "thermal", "explosive", "kinetic"):
            fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                                   ship.getModifiedItemAttr("eliteBonusIndustrial2"), skill="Transport Ships")

    return locals()

def effect5888():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "thermal", "explosive", "kinetic"):
            fit.ship.boostItemAttr("armor{}DamageResonance".format(damageType.capitalize()),
                                   ship.getModifiedItemAttr("eliteBonusIndustrial2"), skill="Transport Ships")

    return locals()

def effect5889():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                      "overloadSpeedFactorBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect589():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect5890():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                      "overloadSpeedFactorBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect5891():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"),
                                      "overloadHardeningBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect5892():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"),
                                      "overloadSelfDurationBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect5893():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Tactical Shield Manipulation"),
                                      "overloadHardeningBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect5896():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "overloadShieldBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "overloadSelfDurationBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect5899():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "overloadArmorDamageAmount", ship.getModifiedItemAttr("roleBonusOverheatDST"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "overloadSelfDurationBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))

    return locals()

def effect59():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("capacity", module.getModifiedItemAttr("cargoCapacityMultiplier"))

    return locals()

def effect590():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Pulse Weapons"),
                                      "duration", container.getModifiedItemAttr("durationBonus") * level)

    return locals()

def effect5900():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("warpSpeedMultiplier", module.getModifiedItemAttr("warpSpeedAdd"))

    return locals()

def effect5901():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Reinforced Bulkhead",
                                      "cpu", ship.getModifiedItemAttr("cpuNeedBonus"))

    return locals()

def effect5911():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.ship.boostItemAttr("jumpDriveConsumptionAmount",
                               module.getModifiedItemAttr("consumptionQuantityBonusPercentage"), stackingPenalties=True)

    return locals()

def effect5912():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                         "powerTransferAmount", beacon.getModifiedItemAttr("energyTransferAmountBonus"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5913():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.multiplyItemAttr("armorHP", beacon.getModifiedItemAttr("armorHPMultiplier"))

    return locals()

def effect5914():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                         "energyNeutralizerAmount",
                                         beacon.getModifiedItemAttr("energyWarfareStrengthMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5915():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                         "powerTransferAmount",
                                         beacon.getModifiedItemAttr("energyWarfareStrengthMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5916():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "explosiveDamage", beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5917():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "kineticDamage", beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5918():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "thermalDamage", beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5919():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "emDamage", beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5920():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "aoeCloudSize", beacon.getModifiedItemAttr("aoeCloudSizeMultiplier"))

    return locals()

def effect5921():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Target Painting"),
                                         "signatureRadiusBonus",
                                         beacon.getModifiedItemAttr("targetPainterStrengthMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5922():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Stasis Web",
                                         "speedFactor", beacon.getModifiedItemAttr("stasisWebStrengthMultiplier"),
                                         stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5923():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "energyNeutralizerAmount",
                                           beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5924():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "scanGravimetricStrengthBonus",
                                           beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5925():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "scanLadarStrengthBonus",
                                           beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5926():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "scanMagnetometricStrengthBonus",
                                           beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5927():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                           "scanRadarStrengthBonus",
                                           beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                           stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5929():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.drones.filteredItemMultiply(lambda drone: True,
                                        "trackingSpeed", beacon.getModifiedItemAttr("trackingSpeedMultiplier"),
                                        stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect5934():
    from eos.saveddata.module import State
    runTime = "early"
    type = "projected", "active"
    def handler(fit, module, context):
        if "projected" not in context:
            return
        fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))
        for mod in fit.modules:
            if not mod.isEmpty and mod.state > State.ONLINE and (
                    mod.item.requiresSkill("Micro Jump Drive Operation") or
                    mod.item.requiresSkill("High Speed Maneuvering")
            ):
                mod.state = State.ONLINE
            if not mod.isEmpty and mod.item.requiresSkill("Micro Jump Drive Operation") and mod.state > State.ONLINE:
                mod.state = State.ONLINE

    return locals()

def effect5938():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect5939():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rocket",
                                      "speed", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect5940():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "speed", ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")

    return locals()

def effect5944():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", ship.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")

    return locals()

def effect5945():
    type = "active"
    runTime = "early"
    def handler(fit, module, context):
        fit.extraAttributes["cloaked"] = True
        fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityModifier"))

    return locals()

def effect5951():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", module.getModifiedItemAttr("drawback"), stackingPenalties=True)

    return locals()

def effect5956():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect5957():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                      skill="Heavy Interdiction Cruisers")

    return locals()

def effect5958():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect5959():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                      skill="Heavy Interdiction Cruisers")

    return locals()

def effect596():
    type = "passive"
    def handler(fit, module, context):
        module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))

    return locals()

def effect598():
    type = "passive"
    def handler(fit, module, context):
        module.multiplyItemAttr("speed", module.getModifiedChargeAttr("speedMultiplier") or 1)

    return locals()

def effect599():
    type = "passive"
    def handler(fit, module, context):
        module.multiplyItemAttr("falloff", module.getModifiedChargeAttr("fallofMultiplier") or 1)

    return locals()

def effect5994():
    type = "passive"
    def handler(fit, module, context):
        for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
            tgtAttr = '{}DamageResonance'.format(dmgType)
            fit.ship.forceItemAttr(tgtAttr, module.getModifiedItemAttr("resistanceKillerHull"))

    return locals()

def effect5995():
    type = "passive"
    def handler(fit, module, context):
        for layer in ('armor', 'shield'):
            for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
                tgtAttr = '{}{}DamageResonance'.format(layer, dmgType.capitalize())
                fit.ship.forceItemAttr(tgtAttr, module.getModifiedItemAttr("resistanceKiller"))

    return locals()

def effect5998():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusO2"), skill="ORE Freighter",
                               stackingPenalties=True)

    return locals()

def effect60():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("hp", module.getModifiedItemAttr("structureHPMultiplier"))

    return locals()

def effect600():
    type = "passive"
    def handler(fit, module, context):
        module.multiplyItemAttr("trackingSpeed", module.getModifiedChargeAttr("trackingSpeedMultiplier"))

    return locals()

def effect6001():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("shipMaintenanceBayCapacity", ship.getModifiedItemAttr("freighterBonusO1"),
                               skill="ORE Freighter")

    return locals()

def effect6006():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr1"),
                                      skill="Amarr Tactical Destroyer")

    return locals()

def effect6007():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr2"),
                                      skill="Amarr Tactical Destroyer")

    return locals()

def effect6008():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr3"),
                                      skill="Amarr Tactical Destroyer")

    return locals()

def effect6009():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"), "cpu", src.getModifiedItemAttr("roleBonusT3ProbeCPU"))

    return locals()

def effect6010():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr(
            "maxTargetRange",
            1 / module.getModifiedItemAttr("modeMaxTargetRangePostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6011():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Energy Turret"),
            "maxRange",
            1 / module.getModifiedItemAttr("modeMaxRangePostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6012():
    type = "passive"
    def handler(fit, module, context):
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            fit.ship.multiplyItemAttr(
                "scan{}Strength".format(scanType),
                1 / (module.getModifiedItemAttr("mode{}StrengthPostDiv".format(scanType)) or 1),
                stackingPenalties=True,
                penaltyGroup="postDiv"
            )

    return locals()

def effect6014():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("signatureRadius", 1 / module.getModifiedItemAttr("modeSignatureRadiusPostDiv"),
                                  stackingPenalties=True, penaltyGroup="postDiv")

    return locals()

def effect6015():
    type = "passive"
    def handler(fit, module, context):
        for srcResType, tgtResType in (
                ("Em", "Em"),
                ("Explosive", "Explosive"),
                ("Kinetic", "Kinetic"),
                ("Thermic", "Thermal")
        ):
            fit.ship.multiplyItemAttr(
                "armor{0}DamageResonance".format(tgtResType),
                1 / module.getModifiedItemAttr("mode{0}ResistancePostDiv".format(srcResType)),
                stackingPenalties=True,
                penaltyGroup="postDiv"
            )

    return locals()

def effect6016():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr(
            "agility",
            1 / module.getModifiedItemAttr("modeAgilityPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6017():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr(
            "maxVelocity",
            1 / module.getModifiedItemAttr("modeVelocityPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect602():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")

    return locals()

def effect6020():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect6021():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect6025():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")

    return locals()

def effect6027():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("eliteBonusReconShip1"),
                                      skill="Recon Ships")

    return locals()

def effect6032():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                      "power", ship.getModifiedItemAttr("powerTransferPowerNeedBonus"))

    return locals()

def effect6036():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar3"),
                                      skill="Minmatar Tactical Destroyer")

    return locals()

def effect6037():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar1"),
                                      skill="Minmatar Tactical Destroyer")

    return locals()

def effect6038():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar2"),
                                      skill="Minmatar Tactical Destroyer")

    return locals()

def effect6039():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
            "trackingSpeed",
            1 / module.getModifiedItemAttr("modeTrackingPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect604():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusMB2"), skill="Minmatar Battleship")

    return locals()

def effect6040():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
            "signatureRadiusBonus",
            1 / module.getModifiedItemAttr("modeMWDSigPenaltyPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6041():
    type = "passive"
    def handler(fit, module, context):
        for srcResType, tgtResType in (
                ("Em", "Em"),
                ("Explosive", "Explosive"),
                ("Kinetic", "Kinetic"),
                ("Thermic", "Thermal")
        ):
            fit.ship.multiplyItemAttr(
                "shield{0}DamageResonance".format(tgtResType),
                1 / module.getModifiedItemAttr("mode{0}ResistancePostDiv".format(srcResType)),
                stackingPenalties=True,
                penaltyGroup="postDiv"
            )

    return locals()

def effect6045():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC3"), skill="Gallente Cruiser")

    return locals()

def effect6046():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "hp", ship.getModifiedItemAttr("shipBonusGC3"), skill="Gallente Cruiser")

    return locals()

def effect6047():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusGC3"), skill="Gallente Cruiser")

    return locals()

def effect6048():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusGC3"), skill="Gallente Cruiser")

    return locals()

def effect6051():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6052():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6053():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6054():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "hp", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6055():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6056():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6057():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6058():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6059():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                     "hp", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6060():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "hp", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6061():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "armorHP", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6062():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                     "shieldCapacity", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect6063():
    type = "active"
    def handler(fit, module, context):
        fit.ship.forceItemAttr("disallowAssistance", module.getModifiedItemAttr("disallowAssistance"))
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            fit.ship.boostItemAttr(
                "scan{}Strength".format(scanType),
                module.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                stackingPenalties=True
            )

    return locals()

def effect607():
    type = "active"
    runTime = "early"
    def handler(fit, module, context):
        fit.extraAttributes["cloaked"] = True
        fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityModifier"))

    return locals()

def effect6076():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeMultiply(
            lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
            "maxVelocity",
            1 / module.getModifiedItemAttr("modeMaxRangePostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6077():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari3"),
                                      skill="Caldari Tactical Destroyer")

    return locals()

def effect6083():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "explosive", "kinetic", "thermal"):
            fit.modules.filteredChargeBoost(
                lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect6085():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari1"),
                                      skill="Caldari Tactical Destroyer")

    return locals()

def effect6088():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "explosive", "kinetic", "thermal"):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                            "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusMC2"),
                                            skill="Minmatar Cruiser")

    return locals()

def effect6093():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "explosive", "kinetic", "thermal"):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                            "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusMC2"),
                                            skill="Minmatar Cruiser")

    return locals()

def effect6096():
    type = "passive"
    def handler(fit, ship, context):
        for damageType in ("em", "explosive", "kinetic", "thermal"):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                            "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusMC2"),
                                            skill="Minmatar Cruiser")

    return locals()

def effect6098():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "reloadTime", ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari2"),
                                      skill="Caldari Tactical Destroyer")

    return locals()

def effect61():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("agility", src.getModifiedItemAttr("agilityBonusAdd"))

    return locals()

def effect6104():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                         "duration", ship.getModifiedItemAttr("entosisDurationMultiplier") or 1)

    return locals()

def effect6110():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", module.getModifiedItemAttr("missileVelocityBonus"),
                                        stackingPenalties=True)

    return locals()

def effect6111():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosionDelay", module.getModifiedItemAttr("explosionDelayBonus"),
                                        stackingPenalties=True)

    return locals()

def effect6112():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeCloudSize", module.getModifiedItemAttr("aoeCloudSizeBonus"),
                                        stackingPenalties=True)

    return locals()

def effect6113():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "aoeVelocity", module.getModifiedItemAttr("aoeVelocityBonus"),
                                        stackingPenalties=True)

    return locals()

def effect6128():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("aoeCloudSizeBonus", module.getModifiedChargeAttr("aoeCloudSizeBonusBonus"))

    return locals()

def effect6129():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("aoeVelocityBonus", module.getModifiedChargeAttr("aoeVelocityBonusBonus"))

    return locals()

def effect6130():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("missileVelocityBonus", module.getModifiedChargeAttr("missileVelocityBonusBonus"))

    return locals()

def effect6131():
    type = "passive"
    def handler(fit, module, context):
        module.boostItemAttr("explosionDelayBonus", module.getModifiedChargeAttr("explosionDelayBonusBonus"))

    return locals()

def effect6135():
    type = "active"
    def handler(fit, container, context):
        for srcAttr, tgtAttr in (
                ("aoeCloudSizeBonus", "aoeCloudSize"),
                ("aoeVelocityBonus", "aoeVelocity"),
                ("missileVelocityBonus", "maxVelocity"),
                ("explosionDelayBonus", "explosionDelay"),
        ):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                            tgtAttr, container.getModifiedItemAttr(srcAttr),
                                            stackingPenalties=True)

    return locals()

def effect6144():
    type = "overheat"
    def handler(fit, module, context):
        for tgtAttr in (
                "aoeCloudSizeBonus",
                "explosionDelayBonus",
                "missileVelocityBonus",
                "maxVelocityModifier",
                "aoeVelocityBonus"
        ):
            module.boostItemAttr(tgtAttr, module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))

    return locals()

def effect6148():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                      ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente3"),
                                      skill="Gallente Tactical Destroyer")

    return locals()

def effect6149():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente1"),
                                      skill="Gallente Tactical Destroyer")

    return locals()

def effect6150():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente2"),
                                      skill="Gallente Tactical Destroyer")

    return locals()

def effect6151():
    type = "passive"
    def handler(fit, module, context):
        for srcResType, tgtResType in (
                ("Em", "em"),
                ("Explosive", "explosive"),
                ("Kinetic", "kinetic"),
                ("Thermic", "thermal")
        ):
            fit.ship.multiplyItemAttr(
                "{0}DamageResonance".format(tgtResType),
                1 / module.getModifiedItemAttr("mode{0}ResistancePostDiv".format(srcResType))
            )

    return locals()

def effect6152():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
            "maxRange",
            1 / module.getModifiedItemAttr("modeMaxRangePostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6153():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
            "capacitorNeed",
            1 / module.getModifiedItemAttr("modeMWDCapPostDiv")
        )

    return locals()

def effect6154():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
            "speedFactor",
            1 / module.getModifiedItemAttr("modeMWDVelocityPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6155():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Repair Systems"),
            "duration",
            1 / module.getModifiedItemAttr("modeArmorRepDurationPostDiv")
        )

    return locals()

def effect6163():
    runtime = "late"
    type = "passive"
    def handler(fit, src, context):
        fit.extraAttributes['speedLimit'] = src.getModifiedItemAttr("speedLimit")

    return locals()

def effect6164():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        fit.ship.boostItemAttr("maxVelocity", beacon.getModifiedItemAttr("maxVelocityMultiplier"), stackingPenalties=True)

    return locals()

def effect6166():
    runTime = "early"
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Propulsion Jamming"),
                                      "speedFactorBonus", ship.getModifiedItemAttr("shipBonusAT"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Propulsion Jamming"),
                                      "speedBoostFactorBonus", ship.getModifiedItemAttr("shipBonusAT"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Propulsion Jamming"),
                                      "massBonusPercentage", ship.getModifiedItemAttr("shipBonusAT"))

    return locals()

def effect6170():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                         "entosisCPUAdd", ship.getModifiedItemAttr("entosisCPUPenalty"))

    return locals()

def effect6171():
    type = "passive"
    def handler(fit, module, context):
        module.increaseItemAttr("cpu", module.getModifiedItemAttr("entosisCPUAdd"))

    return locals()

def effect6172():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "falloff", ship.getModifiedItemAttr("roleBonusCBC"))

    return locals()

def effect6173():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "falloff", ship.getModifiedItemAttr("roleBonusCBC"))

    return locals()

def effect6174():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("roleBonusCBC"))

    return locals()

def effect6175():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "maxVelocity", skill.getModifiedItemAttr("roleBonusCBC"))

    return locals()

def effect6176():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "maxVelocity", ship.getModifiedItemAttr("roleBonusCBC"))

    return locals()

def effect6177():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusCBC2"),
                                      skill="Caldari Battlecruiser")

    return locals()

def effect6178():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusMBC2"),
                                      skill="Minmatar Battlecruiser")

    return locals()

def effect6184():
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "projected", "active"
    runTime = "late"
    def handler(fit, src, context, **kwargs):
        if "projected" in context:
            amount = src.getModifiedItemAttr("powerTransferAmount")
            duration = src.getModifiedItemAttr("duration")
            if 'effect' in kwargs:
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.addDrain(src, duration, -amount, 0)

    return locals()

def effect6185():
    type = "projected", "active"
    runTime = "late"
    def handler(fit, module, context):
        if "projected" not in context:
            return
        bonus = module.getModifiedItemAttr("structureDamageAmount")
        duration = module.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("hullRepair", bonus / duration)

    return locals()

def effect6186():
    type = "projected", "active"
    def handler(fit, container, context, **kwargs):
        if "projected" in context:
            bonus = container.getModifiedItemAttr("shieldBonus")
            duration = container.getModifiedItemAttr("duration") / 1000.0
            fit.extraAttributes.increase("shieldRepair", bonus / duration, **kwargs)

    return locals()

def effect6187():
    from eos.saveddata.module import State
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "active", "projected"
    def handler(fit, src, context, **kwargs):
        if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or
                                        hasattr(src, "amountActive")):
            amount = src.getModifiedItemAttr("energyNeutralizerAmount")
            if 'effect' in kwargs:
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            time = src.getModifiedItemAttr("duration")
            fit.addDrain(src, time, amount, 0)

    return locals()

def effect6188():
    type = "projected", "active"
    runTime = "late"
    def handler(fit, container, context, **kwargs):
        if "projected" in context:
            bonus = container.getModifiedItemAttr("armorDamageAmount")
            duration = container.getModifiedItemAttr("duration") / 1000.0
            rps = bonus / duration
            fit.extraAttributes.increase("armorRepair", rps)
            fit.extraAttributes.increase("armorRepairPreSpool", rps)
            fit.extraAttributes.increase("armorRepairFullSpool", rps)

    return locals()

def effect6195():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                               skill="Expedition Frigates")
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                               skill="Expedition Frigates")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                               skill="Expedition Frigates")
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                               skill="Expedition Frigates")

    return locals()

def effect6196():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "duration",
                                      src.getModifiedItemAttr("eliteBonusExpedition2"), skill="Expedition Frigates")

    return locals()

def effect6197():
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "active", "projected"
    runTime = "late"
    def handler(fit, src, context, **kwargs):
        amount = src.getModifiedItemAttr("powerTransferAmount")
        time = src.getModifiedItemAttr("duration")
        if 'effect' in kwargs and "projected" in context:
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
        if "projected" in context:
            fit.addDrain(src, time, amount, 0)
        elif "module" in context:
            src.itemModifiedAttributes.force("capacitorNeed", -amount)

    return locals()

def effect6201():
    type = "active"
    def handler(fit, src, context):
        pass

    return locals()

def effect6208():
    type = "active"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonusPercent"),
                               stackingPenalties=True)

    return locals()

def effect6214():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "power",
                                      src.getModifiedItemAttr("roleBonusCD"))

    return locals()

def effect6216():
    from eos.saveddata.module import State
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "active", "projected"
    def handler(fit, src, context, **kwargs):
        amount = 0
        if "projected" in context:
            if (hasattr(src, "state") and src.state >= State.ACTIVE) or hasattr(src, "amountActive"):
                amount = src.getModifiedItemAttr("energyNeutralizerAmount")
                if 'effect' in kwargs:
                    amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
                time = src.getModifiedItemAttr("duration")
                fit.addDrain(src, time, amount, 0)
    return locals()

def effect6222():
    from eos.saveddata.module import State
    runTime = "early"
    type = "projected", "active"
    def handler(fit, module, context):
        if "projected" in context:
            fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))
            if module.charge is not None and module.charge.ID == 47336:
                for mod in fit.modules:
                    if not mod.isEmpty and mod.item.requiresSkill("High Speed Maneuvering") and mod.state > State.ONLINE:
                        mod.state = State.ONLINE
                    if not mod.isEmpty and mod.item.requiresSkill("Micro Jump Drive Operation") and mod.state > State.ONLINE:
                        mod.state = State.ONLINE

    return locals()

def effect623():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                     "miningAmount",
                                     container.getModifiedItemAttr("miningAmountBonus") * level)

    return locals()

def effect6230():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")

    return locals()

def effect6232():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")

    return locals()

def effect6233():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect6234():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")

    return locals()

def effect6237():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")

    return locals()

def effect6238():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect6239():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "duration",
                                      src.getModifiedItemAttr("shipBonusOREfrig2"), skill="Mining Frigate")

    return locals()

def effect6241():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")

    return locals()

def effect6242():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")

    return locals()

def effect6245():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")

    return locals()

def effect6246():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")

    return locals()

def effect6253():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect6256():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")

    return locals()

def effect6257():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")

    return locals()

def effect6260():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")

    return locals()

def effect6267():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect627():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("powerOutput", module.getModifiedItemAttr("powerIncrease"))

    return locals()

def effect6272():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusElectronicAttackShip3"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect6273():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect6278():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusElectronicAttackShip3"),
                                      skill="Electronic Attack Ships")

    return locals()

def effect6281():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect6285():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonus3AF"), skill="Amarr Frigate")

    return locals()

def effect6287():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect6291():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonus3AF"), skill="Amarr Frigate")

    return locals()

def effect6294():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect6299():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAC3"), skill="Amarr Cruiser")

    return locals()

def effect63():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("armorHP", module.getModifiedItemAttr("armorHPMultiplier"))

    return locals()

def effect6300():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect6301():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                      src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect6305():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusAC3"), skill="Amarr Cruiser")

    return locals()

def effect6307():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusMD1"), skill="Minmatar Destroyer")

    return locals()

def effect6308():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusMD1"), skill="Minmatar Destroyer")

    return locals()

def effect6309():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusMD1"), skill="Minmatar Destroyer")

    return locals()

def effect6310():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", src.getModifiedItemAttr("shipBonusMD1"),
                                        skill="Minmatar Destroyer")

    return locals()

def effect6315():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")

    return locals()

def effect6316():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")

    return locals()

def effect6317():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Micro Jump Drive Operation"), "duration",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer2"), skill="Command Destroyers")

    return locals()

def effect6318():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusMD2"),
                               skill="Minmatar Destroyer")

    return locals()

def effect6319():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusMD2"),
                               skill="Minmatar Destroyer")

    return locals()

def effect6320():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusMD2"),
                               skill="Minmatar Destroyer")

    return locals()

def effect6321():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusMD2"),
                               skill="Minmatar Destroyer")

    return locals()

def effect6322():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr("scanGravimetricStrengthBonus", src.getModifiedChargeAttr("scanGravimetricStrengthBonusBonus"))

    return locals()

def effect6323():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr("scanLadarStrengthBonus", src.getModifiedChargeAttr("scanLadarStrengthBonusBonus"))

    return locals()

def effect6324():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr("scanMagnetometricStrengthBonus", src.getModifiedChargeAttr("scanMagnetometricStrengthBonusBonus"))

    return locals()

def effect6325():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr("scanRadarStrengthBonus", src.getModifiedChargeAttr("scanRadarStrengthBonusBonus"))

    return locals()

def effect6326():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")

    return locals()

def effect6327():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")

    return locals()

def effect6328():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")

    return locals()

def effect6329():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosiveDamage", src.getModifiedItemAttr("shipBonusCD1"),
                                        skill="Caldari Destroyer")

    return locals()

def effect6330():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusCD2"),
                               skill="Caldari Destroyer")

    return locals()

def effect6331():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusCD2"),
                               skill="Caldari Destroyer")

    return locals()

def effect6332():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusCD2"),
                               skill="Caldari Destroyer")

    return locals()

def effect6333():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusCD2"),
                               skill="Caldari Destroyer")

    return locals()

def effect6334():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")

    return locals()

def effect6335():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusAD2"),
                               skill="Amarr Destroyer")

    return locals()

def effect6336():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusAD2"),
                               skill="Amarr Destroyer")

    return locals()

def effect6337():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")

    return locals()

def effect6338():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusAD2"),
                               skill="Amarr Destroyer")

    return locals()

def effect6339():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("eliteBonusCommandDestroyer1"), skill="Command Destroyers")

    return locals()

def effect6340():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusGD2"),
                               skill="Gallente Destroyer")

    return locals()

def effect6341():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusGD2"),
                               skill="Gallente Destroyer")

    return locals()

def effect6342():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusGD2"),
                               skill="Gallente Destroyer")

    return locals()

def effect6343():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusGD2"),
                               skill="Gallente Destroyer")

    return locals()

def effect6350():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Light Missiles") or mod.charge.requiresSkill("Rockets"), "kineticDamage",
            src.getModifiedItemAttr("shipBonus3CF"), skill="Caldari Frigate")

    return locals()

def effect6351():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusCC3"), skill="Caldari Cruiser")

    return locals()

def effect6352():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "falloffEffectiveness",
                                      src.getModifiedItemAttr("roleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "maxRange",
                                      src.getModifiedItemAttr("roleBonus"))

    return locals()

def effect6353():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "cpu",
                                      src.getModifiedItemAttr("roleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "capacitorNeed",
                                      src.getModifiedItemAttr("roleBonus"))

    return locals()

def effect6354():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "trackingSpeedBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "explosionDelayBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "maxRangeBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "falloffBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "missileVelocityBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeVelocityBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeCloudSizeBonus",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect6355():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "capacitorNeed",
                                      src.getModifiedItemAttr("roleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "cpu", src.getModifiedItemAttr("roleBonus"))

    return locals()

def effect6356():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "falloffEffectiveness",
                                      src.getModifiedItemAttr("roleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "maxRange",
                                      src.getModifiedItemAttr("roleBonus"))

    return locals()

def effect6357():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Navigation"), "maxRange",
                                      src.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect6358():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Navigation"),
                                         "warpScrambleStrength", ship.getModifiedItemAttr("roleBonus"))

    return locals()

def effect6359():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "aoeVelocity",
                                        src.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect6360():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect6361():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonus3MF"), skill="Minmatar Frigate")

    return locals()

def effect6362():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange",
                                      src.getModifiedItemAttr("roleBonus"))

    return locals()

def effect6368():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster", "falloffEffectiveness",
                                      src.getModifiedItemAttr("falloffBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Shield Booster",
                                      "falloffEffectiveness", src.getModifiedItemAttr("falloffBonus"))

    return locals()

def effect6369():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect6370():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "falloffEffectiveness",
                                      src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect6371():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "falloffEffectiveness", src.getModifiedItemAttr("shipBonusGC"),
                                      skill="Gallente Cruiser")

    return locals()

def effect6372():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "falloffEffectiveness", src.getModifiedItemAttr("shipBonusAC2"),
                                      skill="Amarr Cruiser")

    return locals()

def effect6373():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer", "falloffEffectiveness",
                                      src.getModifiedItemAttr("falloffBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Armor Repairer",
                                      "falloffEffectiveness", src.getModifiedItemAttr("falloffBonus"))

    return locals()

def effect6374():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone", "structureDamageAmount",
                                     src.getModifiedItemAttr("droneArmorDamageAmountBonus"))

    return locals()

def effect6377():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "duration",
                                      src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")

    return locals()

def effect6378():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "duration",
                                      src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed",
                                      src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")

    return locals()

def effect6379():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorHP", src.getModifiedItemAttr("eliteBonusLogiFrig2"), skill="Logistics Frigates")

    return locals()

def effect6380():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("eliteBonusLogiFrig2"), skill="Logistics Frigates")

    return locals()

def effect6381():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("signatureRadius", src.getModifiedItemAttr("eliteBonusLogiFrig2"),
                               skill="Logistics Frigates")

    return locals()

def effect6384():
    type = "overheat"
    def handler(fit, module, context):
        for tgtAttr in (
                "aoeCloudSizeBonus",
                "explosionDelayBonus",
                "missileVelocityBonus",
                "aoeVelocityBonus"
        ):
            module.boostItemAttr(tgtAttr, module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))

    return locals()

def effect6385():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context):
        fit.modules.filteredItemForce(lambda mod: mod.item.group.name == "Cloaking Device",
                                      "maxVelocityModifier", src.getModifiedItemAttr("velocityPenaltyReduction"))

    return locals()

def effect6386():
    type = "passive"
    def handler(fit, src, context):
        level = src.level if "skill" in context else 1
        for attr in (
                "explosionDelayBonus",
                "aoeVelocityBonus",
                "aoeCloudSizeBonus",
                "missileVelocityBonus"
        ):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                          attr, src.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)

    return locals()

def effect6395():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "missileVelocityBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeVelocityBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "maxRangeBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "explosionDelayBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeCloudSizeBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "trackingSpeedBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "falloffBonus",
                                      src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect6396():
    type = "passive", "structure"
    def handler(fit, src, context):
        groups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile", "Structure Guided Bomb")
        for damageType in ("em", "thermal", "explosive", "kinetic"):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                            "%sDamage" % damageType, src.getModifiedItemAttr("damageMultiplierBonus"),
                                            skill="Structure Missile Systems")

    return locals()

def effect6400():
    type = "passive", "structure"
    def handler(fit, src, context):
        groups = ("Structure Warp Scrambler", "Structure Disruption Battery", "Structure Stasis Webifier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "capacitorNeed", src.getModifiedItemAttr("capNeedBonus"),
                                      skill="Structure Electronic Systems")

    return locals()

def effect6401():
    type = "passive", "structure"
    def handler(fit, src, context):
        groups = ("Structure Energy Neutralizer", "Structure Area Denial Module")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "capacitorNeed", src.getModifiedItemAttr("capNeedBonus"),
                                      skill="Structure Engineering Systems")

    return locals()

def effect6402():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Structure Anti-Subcapital Missile", "Structure Anti-Capital Missile")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                      "aoeVelocity", src.getModifiedItemAttr("structureRigMissileExploVeloBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6403():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Structure Anti-Subcapital Missile", "Structure Anti-Capital Missile")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                      "maxVelocity", src.getModifiedItemAttr("structureRigMissileVelocityBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6404():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                      "maxRange", src.getModifiedItemAttr("structureRigEwarOptimalBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                      "falloffEffectiveness", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6405():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                      "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6406():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Structure ECM Battery", "Structure Disruption Battery")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "falloff", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "maxRange", src.getModifiedItemAttr("structureRigEwarOptimalBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "falloffEffectiveness", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6407():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Structure ECM Battery", "Structure Disruption Battery")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6408():
    type = "passive"
    def handler(fit, src, context):
        fit.extraAttributes.increase("maxTargetsLockedFromSkills", src.getModifiedItemAttr("structureRigMaxTargetBonus"))

    return locals()

def effect6409():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("structureRigScanResBonus"),
                               stackingPenalties=True)

    return locals()

def effect6410():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Structure Guided Bomb",
                                        "aoeCloudSize", src.getModifiedItemAttr("structureRigMissileExplosionRadiusBonus"),
                                        stackingPenalties=True)

    return locals()

def effect6411():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Structure Guided Bomb",
                                        "maxVelocity", src.getModifiedItemAttr("structureRigMissileVelocityBonus"),
                                        stackingPenalties=True)

    return locals()

def effect6412():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Area Denial Module",
                                      "empFieldRange", src.getModifiedItemAttr("structureRigPDRangeBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6413():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Area Denial Module",
                                      "capacitorNeed", src.getModifiedItemAttr("structureRigPDCapUseBonus"),
                                      stackingPenalties=True)

    return locals()

def effect6417():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Structure Doomsday Weapon",
                                         "lightningWeaponDamageLossTarget",
                                         src.getModifiedItemAttr("structureRigDoomsdayDamageLossTargetBonus"))

    return locals()

def effect6422():
    type = "projected", "active"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True, *args, **kwargs)
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6423():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" in context:
            for srcAttr, tgtAttr in (
                    ("aoeCloudSizeBonus", "aoeCloudSize"),
                    ("aoeVelocityBonus", "aoeVelocity"),
                    ("missileVelocityBonus", "maxVelocity"),
                    ("explosionDelayBonus", "explosionDelay"),
            ):
                fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                                tgtAttr, module.getModifiedItemAttr(srcAttr),
                                                stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6424():
    type = "projected", "active"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" in context:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "falloff", module.getModifiedItemAttr("falloffBonus"),
                                          stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6425():
    type = "projected", "active"
    def handler(fit, container, context, *args, **kwargs):
        if "projected" in context:
            fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                                   stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6426():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6427():
    type = "projected", "active"
    def handler(fit, module, context):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True)
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True)
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            fit.ship.boostItemAttr(
                "scan{}Strength".format(scanType),
                module.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                stackingPenalties=True
            )

    return locals()

def effect6428():
    type = "projected", "active"
    def handler(fit, module, context, **kwargs):
        if "projected" in context:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                          stackingPenalties=True, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                          stackingPenalties=True, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "falloff", module.getModifiedItemAttr("falloffBonus"),
                                          stackingPenalties=True, **kwargs)

    return locals()

def effect6431():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Missile Attack"
    prefix = "fighterAbilityMissiles"
    type = "active"
    hasCharges = True
    def handler(fit, src, context):
        pass

    return locals()

def effect6434():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    displayName = "Energy Neutralizer"
    prefix = "fighterAbilityEnergyNeutralizer"
    type = "active", "projected"
    grouped = True
    def handler(fit, src, context, **kwargs):
        if "projected" in context:
            amount = src.getModifiedItemAttr("{}Amount".format(prefix)) * src.amountActive
            time = src.getModifiedItemAttr("{}Duration".format(prefix))
            if 'effect' in kwargs:
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.addDrain(src, time, amount, 0)

    return locals()

def effect6435():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Stasis Webifier"
    prefix = "fighterAbilityStasisWebifier"
    type = "active", "projected"
    grouped = True
    def handler(fit, src, context):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("{}SpeedPenalty".format(prefix)) * src.amountActive,
                               stackingPenalties=True)

    return locals()

def effect6436():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Warp Disruption"
    prefix = "fighterAbilityWarpDisruption"
    type = "active", "projected"
    grouped = True
    def handler(fit, src, context):
        if "projected" not in context:
            return
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("{}PointStrength".format(prefix)) * src.amountActive)

    return locals()

def effect6437():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    displayName = "ECM"
    prefix = "fighterAbilityECM"
    type = "projected", "active"
    grouped = True
    def handler(fit, module, context, **kwargs):
        if "projected" not in context:
            return
        strModifier = 1 - (module.getModifiedItemAttr("{}Strength{}".format(prefix, fit.scanType)) * module.amountActive) / fit.scanStrength
        if 'effect' in kwargs:
            strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
        fit.ecmProjectedStr *= strModifier

    return locals()

def effect6439():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Evasive Maneuvers"
    prefix = "fighterAbilityEvasiveManeuvers"
    grouped = True
    type = "active"
    runTime = "late"
    def handler(fit, container, context):
        container.boostItemAttr("maxVelocity",
                                container.getModifiedItemAttr("fighterAbilityEvasiveManeuversSpeedBonus"))
        container.boostItemAttr("signatureRadius",
                                container.getModifiedItemAttr("fighterAbilityEvasiveManeuversSignatureRadiusBonus"),
                                stackingPenalties=True)
        container.multiplyItemAttr("shieldEmDamageResonance",
                                   container.getModifiedItemAttr("fighterAbilityEvasiveManeuversEmResonance"),
                                   stackingPenalties=True)
        container.multiplyItemAttr("shieldThermalDamageResonance",
                                   container.getModifiedItemAttr("fighterAbilityEvasiveManeuversThermResonance"),
                                   stackingPenalties=True)
        container.multiplyItemAttr("shieldKineticDamageResonance",
                                   container.getModifiedItemAttr("fighterAbilityEvasiveManeuversKinResonance"),
                                   stackingPenalties=True)
        container.multiplyItemAttr("shieldExplosiveDamageResonance",
                                   container.getModifiedItemAttr("fighterAbilityEvasiveManeuversExpResonance"),
                                   stackingPenalties=True)

    return locals()

def effect6441():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Microwarpdrive"
    grouped = True
    type = "active"
    runTime = "late"
    def handler(fit, module, context):
        module.boostItemAttr("maxVelocity", module.getModifiedItemAttr("fighterAbilityMicroWarpDriveSpeedBonus"),
                             stackingPenalties=True)
        module.boostItemAttr("signatureRadius",
                             module.getModifiedItemAttr("fighterAbilityMicroWarpDriveSignatureRadiusBonus"),
                             stackingPenalties=True)

    return locals()

def effect6443():
    type = 'active'
    def handler(fit, module, context):
        pass

    return locals()

def effect6447():
    type = 'active'
    def handler(fit, module, context):
        pass

    return locals()

def effect6448():
    type = "passive"
    def handler(fit, container, context):
        missileGroups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile")
        for srcAttr, tgtAttr in (
                ("aoeCloudSizeBonus", "aoeCloudSize"),
                ("aoeVelocityBonus", "aoeVelocity"),
                ("missileVelocityBonus", "maxVelocity"),
                ("explosionDelayBonus", "explosionDelay"),
        ):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in missileGroups,
                                            tgtAttr, container.getModifiedItemAttr(srcAttr),
                                            stackingPenalties=True)

    return locals()

def effect6449():
    type = "passive"
    def handler(fit, module, context):
        missileGroups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile")
        for dmgType in ("em", "kinetic", "explosive", "thermal"):
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.group.name in missileGroups,
                                               "%sDamage" % dmgType,
                                               module.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                               stackingPenalties=True)
        launcherGroups = ("Structure XL Missile Launcher", "Structure Multirole Missile Launcher")
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name in launcherGroups,
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect6465():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Turret Attack"
    prefix = "fighterAbilityAttackMissile"
    type = "active"
    def handler(fit, src, context):
        pass

    return locals()

def effect6470():
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "projected", "active"
    def handler(fit, module, context, **kwargs):
        if "projected" in context:
            strModifier = 1 - module.getModifiedItemAttr("scan{0}StrengthBonus".format(fit.scanType)) / fit.scanStrength
            if 'effect' in kwargs:
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.ecmProjectedStr *= strModifier

    return locals()

def effect6472():
    type = "active"
    def handler(fit, src, context):
        pass

    return locals()

def effect6473():
    type = "active"
    def handler(fit, src, context):
        pass

    return locals()

def effect6474():
    type = "active"
    def handler(fit, src, context):
        pass

    return locals()

def effect6475():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Structure Doomsday Weapon",
                                         "lightningWeaponTargetAmount",
                                         src.getModifiedItemAttr("structureRigDoomsdayTargetAmountBonus"))

    return locals()

def effect6476():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6477():
    from eos.saveddata.module import State
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "active", "projected"
    def handler(fit, src, context, **kwargs):
        if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or
                                        hasattr(src, "amountActive")):
            amount = src.getModifiedItemAttr("energyNeutralizerAmount")
            if 'effect' in kwargs:
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            time = src.getModifiedItemAttr("duration")
            fit.addDrain(src, time, amount, 0)

    return locals()

def effect6478():
    type = "projected", "active"
    def handler(fit, container, context, *args, **kwargs):
        if "projected" in context:
            fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                                   stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6479():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" in context:
            for srcAttr, tgtAttr in (
                    ("aoeCloudSizeBonus", "aoeCloudSize"),
                    ("aoeVelocityBonus", "aoeVelocity"),
                    ("missileVelocityBonus", "maxVelocity"),
                    ("explosionDelayBonus", "explosionDelay"),
            ):
                fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                                tgtAttr, module.getModifiedItemAttr(srcAttr),
                                                stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "falloff", module.getModifiedItemAttr("falloffBonus"),
                                          stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6481():
    type = "projected", "active"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True, *args, **kwargs)
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6482():
    type = "projected", "active"
    def handler(fit, module, context):
        return

    return locals()

def effect6484():
    type = "active"
    runtime = "late"
    def handler(fit, src, context):
        for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
            fit.ship.multiplyItemAttr('{}DamageResonance'.format(dmgType),
                                      src.getModifiedItemAttr("hull{}DamageResonance".format(dmgType.title())),
                                      stackingPenalties=True, penaltyGroup="postMul")

    return locals()

def effect6485():
    """
    Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
    effects, and thus this effect file contains some custom information useful only to fighters.
    """
    displayName = "Bomb"
    prefix = "fighterAbilityLaunchBomb"
    type = "active"
    hasCharges = True
    def handler(fit, src, context):
        pass

    return locals()

def effect6487():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("energyWarfareResistance",
                               module.getModifiedItemAttr("energyWarfareResistanceBonus"),
                               stackingPenalties=True)

    return locals()

def effect6488():
    type = "active"
    def handler(fit, module, context):
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            module.boostItemAttr("scan{}StrengthPercent".format(scanType),
                                 module.getModifiedChargeAttr("sensorStrengthBonusBonus"))

    return locals()

def effect6501():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")

    return locals()

def effect6502():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"),
                               skill="Amarr Dreadnought")
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"),
                               skill="Amarr Dreadnought")
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"),
                               skill="Amarr Dreadnought")
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtA2"),
                               skill="Amarr Dreadnought")

    return locals()

def effect6503():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtA3"), skill="Amarr Dreadnought")

    return locals()

def effect6504():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")

    return locals()

def effect6505():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                               skill="Caldari Dreadnought")
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                               skill="Caldari Dreadnought")
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                               skill="Caldari Dreadnought")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusDreadnoughtC2"),
                               skill="Caldari Dreadnought")

    return locals()

def effect6506():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")

    return locals()

def effect6507():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "speed",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG2"), skill="Gallente Dreadnought")

    return locals()

def effect6508():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"), "duration",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG3"), skill="Gallente Dreadnought")

    return locals()

def effect6509():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtM1"), skill="Minmatar Dreadnought")

    return locals()

def effect6510():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "speed",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtM2"), skill="Minmatar Dreadnought")

    return locals()

def effect6511():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"), "duration",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtM2"), skill="Minmatar Dreadnought")

    return locals()

def effect6513():
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "projected", "active"
    def handler(fit, module, context, **kwargs):
        if "projected" in context:
            strModifier = 1 - module.getModifiedItemAttr("scan{0}StrengthBonus".format(fit.scanType)) / fit.scanStrength
            if 'effect' in kwargs:
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.ecmProjectedStr *= strModifier

    return locals()

def effect6526():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems") or
                                                  mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                      "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"),
                                      skill="Amarr Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or
                                                  mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"),
                                      skill="Amarr Carrier")

    return locals()

def effect6527():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryA2"),
                               skill="Amarr Carrier")

    return locals()

def effect6533():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                                  mod.item.requiresSkill("Information Command"),
                                      "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                                  mod.item.requiresSkill("Information Command"),
                                      "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                                  mod.item.requiresSkill("Information Command"),
                                      "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                                  mod.item.requiresSkill("Information Command"),
                                      "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                                  mod.item.requiresSkill("Information Command"),
                                      "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")

    return locals()

def effect6534():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")

    return locals()

def effect6535():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")

    return locals()

def effect6536():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")

    return locals()

def effect6537():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "cpu",
                                      src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect6545():
    type = "passive"
    def handler(fit, src, context):
        if src.getModifiedItemAttr("shipBonusForceAuxiliaryC1") is None:
            return  # See GH Issue 1321
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems") or
                                                  mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                      "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryC1"),
                                      skill="Caldari Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or
                                                  mod.item.requiresSkill("Capital Shield Emission Systems"),
                                      "shieldBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryC1"),
                                      skill="Caldari Carrier")

    return locals()

def effect6546():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                               skill="Caldari Carrier")

    return locals()

def effect6548():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or
                                                  mod.item.requiresSkill("Capital Shield Emission Systems"),
                                      "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryG1"),
                                      skill="Gallente Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or
                                                  mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                      "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryG1"),
                                      skill="Gallente Carrier")

    return locals()

def effect6549():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "armorDamageAmount",
                                      src.getModifiedItemAttr("shipBonusForceAuxiliaryG2"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"), "armorDamageAmount",
                                      src.getModifiedItemAttr("shipBonusForceAuxiliaryG2"), skill="Gallente Carrier")

    return locals()

def effect6551():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or
                                                  mod.item.requiresSkill("Capital Shield Emission Systems"),
                                      "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1"),
                                      skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or
                                                  mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                      "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1"),
                                      skill="Minmatar Carrier")

    return locals()

def effect6552():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"), "shieldBonus",
                                      src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"), "shieldBonus",
                                      src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")

    return locals()

def effect6555():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity",
                                     src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)

    return locals()

def effect6556():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                     src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)

    return locals()

def effect6557():
    type = "active"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretRangeFalloff", src.getModifiedItemAttr("falloffBonus"),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesExplosionVelocity",
                                       src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "trackingSpeed",
                                     src.getModifiedItemAttr("trackingSpeedBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileExplosionRadius",
                                       src.getModifiedItemAttr("aoeCloudSizeBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretTrackingSpeed",
                                       src.getModifiedItemAttr("trackingSpeedBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesExplosionRadius",
                                       src.getModifiedItemAttr("aoeCloudSizeBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange",
                                       src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileRangeOptimal", src.getModifiedItemAttr("maxRangeBonus"),
                                       stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "falloff",
                                     src.getModifiedItemAttr("falloffBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileExplosionVelocity",
                                       src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileRangeFalloff", src.getModifiedItemAttr("falloffBonus"),
                                       stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange",
                                     src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretRangeOptimal", src.getModifiedItemAttr("maxRangeBonus"),
                                       stackingPenalties=True)

    return locals()

def effect6558():
    type = "overheat"
    def handler(fit, module, context):
        overloadBonus = module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus")
        module.boostItemAttr("maxRangeBonus", overloadBonus)
        module.boostItemAttr("falloffBonus", overloadBonus)
        module.boostItemAttr("trackingSpeedBonus", overloadBonus)
        module.boostItemAttr("aoeCloudSizeBonus", overloadBonus)
        module.boostItemAttr("aoeVelocityBonus", overloadBonus)

    return locals()

def effect6559():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileExplosionRadius",
                                       src.getModifiedItemAttr("aoeCloudSizeBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileRangeOptimal", src.getModifiedItemAttr("maxRangeBonus"),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretRangeFalloff", src.getModifiedItemAttr("falloffBonus"),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesExplosionRadius",
                                       src.getModifiedItemAttr("aoeCloudSizeBonus"), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "falloff",
                                     src.getModifiedItemAttr("falloffBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileRangeFalloff", src.getModifiedItemAttr("falloffBonus"),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretTrackingSpeed",
                                       src.getModifiedItemAttr("trackingSpeedBonus"), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange",
                                     src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "trackingSpeed",
                                     src.getModifiedItemAttr("trackingSpeedBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretRangeOptimal", src.getModifiedItemAttr("maxRangeBonus"),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesExplosionVelocity",
                                       src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileExplosionVelocity",
                                       src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange",
                                       src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)

    return locals()

def effect6560():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6561():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Light Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("maxVelocityBonus") * lvl)

    return locals()

def effect6562():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("shieldBonus") * lvl)

    return locals()

def effect6563():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6565():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context):
        for attr in [
            "structureRigDoomsdayDamageLossTargetBonus",
            "structureRigScanResBonus",
            "structureRigPDRangeBonus",
            "structureRigPDCapUseBonus",
            "structureRigMissileExploVeloBonus",
            "structureRigMissileVelocityBonus",
            "structureRigEwarOptimalBonus",
            "structureRigEwarFalloffBonus",
            "structureRigEwarCapUseBonus",
            "structureRigMissileExplosionRadiusBonus"
        ]:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Jury Rigging"),
                                      attr, src.getModifiedItemAttr("structureRoleBonus"))

    return locals()

def effect6566():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("fighterBonusShieldCapacityPercent"))
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("fighterBonusVelocityPercent"), stackingPenalties=True, penaltyGroup="postMul")
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDuration",
                                       src.getModifiedItemAttr("fighterBonusROFPercent"), stackingPenalties=True, penaltyGroup="postMul")
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretDuration",
                                       src.getModifiedItemAttr("fighterBonusROFPercent"), stackingPenalties=True, penaltyGroup="postMul")
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesDuration",
                                       src.getModifiedItemAttr("fighterBonusROFPercent"), stackingPenalties=True, penaltyGroup="postMul")
        fit.fighters.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Fighters"), "shieldRechargeRate",
                                       src.getModifiedItemAttr("fighterBonusShieldRechargePercent"))

    return locals()

def effect6567():
    type = "active"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("scanResolutionBonus"), stackingPenalties=True)
        for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
            attr = "scan{}Strength".format(scanType)
            bonus = src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType))
            fit.ship.boostItemAttr(attr, bonus, stackingPenalties=True)
            fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), attr, bonus,
                                           stackingPenalties=True)
        groups = [
            'Burst Jammer',
            'Weapon Disruptor',
            'ECM',
            'Stasis Grappler',
            'Sensor Dampener',
            'Target Painter']
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                                  mod.item.requiresSkill("Propulsion Jamming"),
                                      "capacitorNeed", src.getModifiedItemAttr("ewCapacitorNeedBonus"))

    return locals()

def effect657():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("agility",
                               module.getModifiedItemAttr("agilityMultiplier"),
                               stackingPenalties=True)

    return locals()

def effect6570():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.ship.boostItemAttr("fighterCapacity", src.getModifiedItemAttr("skillBonusFighterHangarSize") * lvl)

    return locals()

def effect6571():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Autocannon Specialization"),
                                      "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6572():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Artillery Specialization"),
                                      "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6573():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Blaster Specialization"),
                                      "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6574():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Railgun Specialization"),
                                      "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6575():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Pulse Laser Specialization"),
                                      "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6576():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Beam Laser Specialization"),
                                      "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)

    return locals()

def effect6577():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missile Specialization"), "speed",
                                      src.getModifiedItemAttr("rofBonus") * lvl)

    return locals()

def effect6578():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Torpedo Specialization"), "speed",
                                      src.getModifiedItemAttr("rofBonus") * lvl)

    return locals()

def effect6580():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"), "structureDamageAmount",
                                     src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"), "armorDamageAmount",
                                     src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"), "shieldBonus",
                                     src.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect6581():
    type = "active"
    runTime = "early"
    def handler(fit, src, context):
        for skill, amtAttr, stack in (
                ("Capital Remote Armor Repair Systems", "armorDamageAmount", True),
                ("Capital Shield Emission Systems", "shieldBonus", True),
                ("Capital Capacitor Emission Systems", "powerTransferAmount", False),
                ("Capital Remote Hull Repair Systems", "structureDamageAmount", False)):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "duration",
                                          src.getModifiedItemAttr("siegeRemoteLogisticsDurationBonus"))
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), amtAttr,
                                          src.getModifiedItemAttr("siegeRemoteLogisticsAmountBonus"),
                                          stackingPenalties=stack)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "maxRange",
                                          src.getModifiedItemAttr("siegeRemoteLogisticsRangeBonus"), stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "falloffEffectiveness",
                                          src.getModifiedItemAttr("siegeRemoteLogisticsRangeBonus"), stackingPenalties=True)
        for skill, amtAttr in (
                ("Capital Shield Operation", "shieldBonus"),
                ("Capital Repair Systems", "armorDamageAmount")):
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), "duration",
                                          src.getModifiedItemAttr("siegeLocalLogisticsDurationBonus"))
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill), amtAttr,
                                          src.getModifiedItemAttr("siegeLocalLogisticsAmountBonus"))
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
        fit.ship.multiplyItemAttr("scanResolution", src.getModifiedItemAttr("scanResolutionMultiplier"),
                                  stackingPenalties=True)
        fit.ship.multiplyItemAttr("mass", src.getModifiedItemAttr("siegeMassMultiplier"), stackingPenalties=True)
        fit.ship.increaseItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargetsBonus"))
        groups = [
            'Burst Jammer',
            'Weapon Disruptor',
            'ECM',
            'Stasis Grappler',
            'Sensor Dampener',
            'Target Painter']
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                                  mod.item.requiresSkill("Propulsion Jamming"),
                                      "capacitorNeed", src.getModifiedItemAttr("ewCapacitorNeedBonus"))
        fit.ship.forceItemAttr("disallowOffensiveModifiers", src.getModifiedItemAttr("disallowOffensiveModifiers"))
        fit.ship.forceItemAttr("disallowAssistance", src.getModifiedItemAttr("disallowAssistance"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                     src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
        fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
        fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
        fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
        fit.ship.forceItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))
        fit.ship.forceItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))

    return locals()

def effect6582():
    type = "active"
    runTime = "early"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret") or
                                                  mod.item.requiresSkill("Capital Hybrid Turret") or
                                                  mod.item.requiresSkill("Capital Projectile Turret"),
                                      "damageMultiplier", src.getModifiedItemAttr("siegeTurretDamageBonus"))
        for type in ("kinetic", "thermal", "explosive", "em"):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes") or
                                                        mod.charge.requiresSkill("XL Cruise Missiles") or
                                                        mod.charge.requiresSkill("Torpedoes"),
                                            "%sDamage" % type, src.getModifiedItemAttr("siegeMissileDamageBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation") or
                                                  mod.item.requiresSkill("Capital Repair Systems"),
                                      "duration", src.getModifiedItemAttr("siegeLocalLogisticsDurationBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                      "shieldBonus", src.getModifiedItemAttr("siegeLocalLogisticsAmountBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("siegeLocalLogisticsAmountBonus"),
                                      stackingPenalties=True)
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"))
        fit.ship.multiplyItemAttr("mass", src.getModifiedItemAttr("siegeMassMultiplier"),
                                  stackingPenalties=True, penaltyGroup="postMul")
        fit.ship.forceItemAttr("disallowOffensiveModifiers", src.getModifiedItemAttr("disallowOffensiveModifiers"))
        fit.ship.forceItemAttr("disallowAssistance", src.getModifiedItemAttr("disallowAssistance"))
        for group in ("Missile Launcher XL Torpedo", "Missile Launcher Rapid Torpedo", "Missile Launcher XL Cruise"):
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == group, "speed",
                                          src.getModifiedItemAttr("siegeLauncherROFBonus"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "maxVelocity",
                                        src.getModifiedItemAttr("siegeTorpedoVelocityBonus"), stackingPenalties=True)
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
        fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
        fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
        fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
        fit.ship.boostItemAttr("weaponDisruptionResistance", src.getModifiedItemAttr("weaponDisruptionResistanceBonus"))
        fit.ship.forceItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))
        fit.ship.forceItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))

    return locals()

def effect6591():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierA3"),
                                  skill="Amarr Carrier")

    return locals()

def effect6592():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierC3"),
                                  skill="Caldari Carrier")

    return locals()

def effect6593():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierG3"),
                                  skill="Gallente Carrier")

    return locals()

def effect6594():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusSupercarrierM3"),
                                  skill="Minmatar Carrier")

    return locals()

def effect6595():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")

    return locals()

def effect6596():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")

    return locals()

def effect6597():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusCarrierG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusCarrierG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusCarrierG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusCarrierG4"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusCarrierG4"), skill="Gallente Carrier")

    return locals()

def effect6598():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")

    return locals()

def effect6599():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusCarrierA1"),
                               skill="Amarr Carrier")

    return locals()

def effect660():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        "emDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect6600():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusCarrierC1"),
                               skill="Caldari Carrier")

    return locals()

def effect6601():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusCarrierG1"), skill="Gallente Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusCarrierG1"), skill="Gallente Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusCarrierG1"), skill="Gallente Carrier")

    return locals()

def effect6602():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusCarrierM1"), skill="Minmatar Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusCarrierM1"), skill="Minmatar Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusCarrierM1"), skill="Minmatar Carrier")

    return locals()

def effect6603():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA1"), skill="Amarr Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA1"), skill="Amarr Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA1"), skill="Amarr Carrier")

    return locals()

def effect6604():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierC1"), skill="Caldari Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierC1"), skill="Caldari Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierC1"), skill="Caldari Carrier")

    return locals()

def effect6605():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierG1"), skill="Gallente Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierG1"), skill="Gallente Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierG1"), skill="Gallente Carrier")

    return locals()

def effect6606():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierM1"), skill="Minmatar Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierM1"), skill="Minmatar Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusSupercarrierM1"), skill="Minmatar Carrier")

    return locals()

def effect6607():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")

    return locals()

def effect6608():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")

    return locals()

def effect6609():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")

    return locals()

def effect661():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        "explosiveDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect6610():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusSupercarrierM5"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusSupercarrierM5"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusSupercarrierM5"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusSupercarrierM5"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusSupercarrierM5"), skill="Minmatar Carrier")

    return locals()

def effect6611():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"), "speedFactor",
                                      src.getModifiedItemAttr("shipBonusSupercarrierC2"), skill="Caldari Carrier")

    return locals()

def effect6612():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesExplosionVelocity",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileExplosionVelocity",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA2"), skill="Amarr Carrier")

    return locals()

def effect6613():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                         src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect6614():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "armorHPBonusAdd",
                                      src.getModifiedItemAttr("shipBonusRole2"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Upgrades"), "capacityBonus",
                                      src.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect6615():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"),
                                      "durationWeaponDisruptionBurstProjector",
                                      src.getModifiedItemAttr("shipBonusSupercarrierA4"), skill="Amarr Carrier")

    return locals()

def effect6616():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"),
                                      "durationECMJammerBurstProjector", src.getModifiedItemAttr("shipBonusSupercarrierC4"),
                                      skill="Caldari Carrier")

    return locals()

def effect6617():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"),
                                      "durationSensorDampeningBurstProjector",
                                      src.getModifiedItemAttr("shipBonusSupercarrierG4"), skill="Gallente Carrier")

    return locals()

def effect6618():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"),
                                      "durationTargetIlluminationBurstProjector",
                                      src.getModifiedItemAttr("shipBonusSupercarrierM4"), skill="Minmatar Carrier")

    return locals()

def effect6619():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                         src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect662():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        "thermalDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect6620():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "reloadTime",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtC3"), skill="Caldari Dreadnought")

    return locals()

def effect6621():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"),
                               skill="Amarr Carrier")
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierA2"),
                               skill="Amarr Carrier")

    return locals()

def effect6622():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"),
                               skill="Caldari Carrier")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusSupercarrierC2"),
                               skill="Caldari Carrier")

    return locals()

def effect6623():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("shipBonusSupercarrierG2"), skill="Gallente Carrier")

    return locals()

def effect6624():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("shipBonusSupercarrierM2"), skill="Minmatar Carrier")

    return locals()

def effect6625():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange",
                                       src.getModifiedItemAttr("shipBonusCarrierA2"), skill="Amarr Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"),
                                       "fighterAbilityEnergyNeutralizerOptimalRange",
                                       src.getModifiedItemAttr("shipBonusCarrierA2"), skill="Amarr Carrier")

    return locals()

def effect6626():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange",
                                       src.getModifiedItemAttr("shipBonusCarrierC2"), skill="Caldari Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"),
                                       "fighterAbilityECMRangeOptimal", src.getModifiedItemAttr("shipBonusCarrierC2"),
                                       skill="Caldari Carrier")

    return locals()

def effect6627():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange",
                                       src.getModifiedItemAttr("shipBonusCarrierG2"), skill="Gallente Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"),
                                       "fighterAbilityWarpDisruptionRange", src.getModifiedItemAttr("shipBonusCarrierG2"),
                                       skill="Gallente Carrier")

    return locals()

def effect6628():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange",
                                       src.getModifiedItemAttr("shipBonusCarrierM2"), skill="Minmatar Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"),
                                       "fighterAbilityStasisWebifierOptimalRange",
                                       src.getModifiedItemAttr("shipBonusCarrierM2"), skill="Minmatar Carrier")

    return locals()

def effect6629():
    type = "passive"
    def handler(fit, src, context):
        src.boostItemAttr("emDamageResistanceBonus", src.getModifiedChargeAttr("emDamageResistanceBonusBonus"))
        src.boostItemAttr("explosiveDamageResistanceBonus",
                          src.getModifiedChargeAttr("explosiveDamageResistanceBonusBonus"))
        src.boostItemAttr("kineticDamageResistanceBonus", src.getModifiedChargeAttr("kineticDamageResistanceBonusBonus"))
        src.boostItemAttr("thermalDamageResistanceBonus", src.getModifiedChargeAttr("thermalDamageResistanceBonusBonus"))

    return locals()

def effect6634():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusTitanA1"), skill="Amarr Titan")

    return locals()

def effect6635():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")

    return locals()

def effect6636():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")

    return locals()

def effect6637():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusTitanM1"), skill="Minmatar Titan")

    return locals()

def effect6638():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher XL Cruise", "speed",
                                      src.getModifiedItemAttr("shipBonusTitanC2"), skill="Caldari Titan")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Torpedo", "speed",
                                      src.getModifiedItemAttr("shipBonusTitanC2"), skill="Caldari Titan")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher XL Torpedo", "speed",
                                      src.getModifiedItemAttr("shipBonusTitanC2"), skill="Caldari Titan")

    return locals()

def effect6639():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesExplosionRadius",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA4"), skill="Amarr Carrier")
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileExplosionRadius",
                                       src.getModifiedItemAttr("shipBonusSupercarrierA4"), skill="Amarr Carrier")

    return locals()

def effect6640():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                         src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect6641():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "armorHPBonusAdd",
                                      src.getModifiedItemAttr("shipBonusRole2"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Upgrades"), "capacityBonus",
                                      src.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect6642():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Doomsday Operation"), "duration",
                                      src.getModifiedItemAttr("rofBonus") * lvl)

    return locals()

def effect6647():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanA3"), skill="Amarr Titan")

    return locals()

def effect6648():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanC3"), skill="Caldari Titan")

    return locals()

def effect6649():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanG3"), skill="Gallente Titan")

    return locals()

def effect6650():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanM3"), skill="Minmatar Titan")

    return locals()

def effect6651():
    type = "projected", "active"
    runTime = "late"
    def handler(fit, module, context, **kwargs):
        if "projected" not in context:
            return
        if module.charge and module.charge.name == "Nanite Repair Paste":
            multiplier = 3
        else:
            multiplier = 1
        amount = module.getModifiedItemAttr("armorDamageAmount") * multiplier
        speed = module.getModifiedItemAttr("duration") / 1000.0
        rps = amount / speed
        fit.extraAttributes.increase("armorRepair", rps)
        fit.extraAttributes.increase("armorRepairPreSpool", rps)
        fit.extraAttributes.increase("armorRepairFullSpool", rps)

    return locals()

def effect6652():
    type = "projected", "active"
    runTime = "late"
    def handler(fit, module, context, **kwargs):
        if "projected" not in context:
            return
        amount = module.getModifiedItemAttr("shieldBonus")
        speed = module.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("shieldRepair", amount / speed, **kwargs)

    return locals()

def effect6653():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusTitanA2"), skill="Amarr Titan")

    return locals()

def effect6654():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "speed",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")

    return locals()

def effect6655():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "speed",
                                      src.getModifiedItemAttr("shipBonusTitanM2"), skill="Minmatar Titan")

    return locals()

def effect6656():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "maxVelocity",
                                        src.getModifiedItemAttr("shipBonusRole3"))

    return locals()

def effect6657():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusTitanC5"), skill="Caldari Titan")

    return locals()

def effect6658():
    type = "active"
    runTime = "early"
    def handler(fit, src, context):
        for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
            for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
                bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
                bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
                booster = "%s%sDamageResonance" % (layer, damageType)
                penalize = False if layer == 'hull' else True
                fit.ship.multiplyItemAttr(bonus, src.getModifiedItemAttr(booster),
                                          stackingPenalties=penalize, penaltyGroup="preMul")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret") or
                                                  mod.item.requiresSkill("Large Hybrid Turret") or
                                                  mod.item.requiresSkill("Large Projectile Turret"),
                                      "maxRange", src.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret") or
                                                  mod.item.requiresSkill("Large Hybrid Turret") or
                                                  mod.item.requiresSkill("Large Projectile Turret"),
                                      "falloff", src.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes") or
                                                    mod.charge.requiresSkill("Cruise Missiles") or
                                                    mod.charge.requiresSkill("Heavy Missiles"),
                                        "maxVelocity", src.getModifiedItemAttr("missileVelocityBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("armorDamageAmountBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", src.getModifiedItemAttr("shieldBoostMultiplier"),
                                      stackingPenalties=True)
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("speedFactor"))
        fit.ship.forceItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargets"))
        fit.ship.forceItemAttr("disallowOffensiveModifiers", src.getModifiedItemAttr("disallowOffensiveModifiers"))
        for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
            fit.ship.boostItemAttr("scan{}Strength".format(scanType),
                                   src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                                   stackingPenalties=True)
        fit.ship.boostItemAttr("remoteRepairImpedance", src.getModifiedItemAttr("remoteRepairImpedanceBonus"))
        fit.ship.boostItemAttr("remoteAssistanceImpedance", src.getModifiedItemAttr("remoteAssistanceImpedanceBonus"))
        fit.ship.boostItemAttr("sensorDampenerResistance", src.getModifiedItemAttr("sensorDampenerResistanceBonus"))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Micro Jump Drive Operation"),
                                         "activationBlocked", src.getModifiedItemAttr("activationBlockedStrenght"))
        fit.ship.boostItemAttr("targetPainterResistance", src.getModifiedItemAttr("targetPainterResistanceBonus"))
        fit.ship.boostItemAttr("weaponDisruptionResistance", src.getModifiedItemAttr("weaponDisruptionResistanceBonus"))
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("siegeModeWarpStatus"))
        fit.ship.forceItemAttr("disallowDocking", src.getModifiedItemAttr("disallowDocking"))
        fit.ship.forceItemAttr("disallowTethering", src.getModifiedItemAttr("disallowTethering"))

    return locals()

def effect6661():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("shipBonusCarrierM3"), skill="Minmatar Carrier")

    return locals()

def effect6662():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("shipBonusCarrierG3"), skill="Gallente Carrier")

    return locals()

def effect6663():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                     src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"), "miningDroneAmountPercent",
                                     src.getModifiedItemAttr("miningAmountBonus") * lvl)

    return locals()

def effect6664():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange",
                                     src.getModifiedItemAttr("rangeSkillBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange",
                                       src.getModifiedItemAttr("rangeSkillBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretRangeOptimal",
                                       src.getModifiedItemAttr("rangeSkillBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileRangeOptimal",
                                       src.getModifiedItemAttr("rangeSkillBonus") * lvl)

    return locals()

def effect6665():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                     src.getModifiedItemAttr("hullHpBonus") * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                     src.getModifiedItemAttr("armorHpBonus") * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                     src.getModifiedItemAttr("shieldCapacityBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("shieldCapacityBonus") * lvl)

    return locals()

def effect6667():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity",
                                     src.getModifiedItemAttr("maxVelocityBonus") * lvl)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("maxVelocityBonus") * lvl)

    return locals()

def effect6669():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                     src.getModifiedItemAttr("hullHpBonus"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                     src.getModifiedItemAttr("hullHpBonus"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                     src.getModifiedItemAttr("hullHpBonus"))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("hullHpBonus"))
        fit.ship.boostItemAttr("cpuOutput", src.getModifiedItemAttr("drawback"))

    return locals()

def effect6670():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange",
                                     src.getModifiedItemAttr("rangeSkillBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange",
                                       src.getModifiedItemAttr("rangeSkillBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackTurretRangeOptimal", src.getModifiedItemAttr("rangeSkillBonus"),
                                       stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                       "fighterAbilityAttackMissileRangeOptimal",
                                       src.getModifiedItemAttr("rangeSkillBonus"), stackingPenalties=True)
        fit.ship.boostItemAttr("cpuOutput", src.getModifiedItemAttr("drawback"))

    return locals()

def effect6671():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity",
                                     src.getModifiedItemAttr("droneMaxVelocityBonus"), stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                       src.getModifiedItemAttr("droneMaxVelocityBonus"), stackingPenalties=True)
        fit.ship.boostItemAttr("cpuOutput", src.getModifiedItemAttr("drawback"))

    return locals()

def effect6679():
    type = "passive", "structure"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Doomsday Weapon",
                                      "duration", src.getModifiedItemAttr("durationBonus"),
                                      skill="Structure Doomsday Operation")

    return locals()

def effect668():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                        "kineticDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect6681():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                         src.getModifiedItemAttr("shipBonusRole3"))

    return locals()

def effect6682():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6683():
    type = "projected", "active"
    def handler(fit, container, context, *args, **kwargs):
        if "projected" in context:
            fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                                   stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6684():
    type = "projected", "active"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True, *args, **kwargs)
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6685():
    type = "projected", "active"
    def handler(fit, module, context):
        if "projected" in context:
            strModifier = 1 - module.getModifiedItemAttr("scan{0}StrengthBonus".format(fit.scanType)) / fit.scanStrength
            fit.ecmProjectedStr *= strModifier

    return locals()

def effect6686():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" in context:
            for srcAttr, tgtAttr in (
                    ("aoeCloudSizeBonus", "aoeCloudSize"),
                    ("aoeVelocityBonus", "aoeVelocity"),
                    ("missileVelocityBonus", "maxVelocity"),
                    ("explosionDelayBonus", "explosionDelay"),
            ):
                fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                                tgtAttr, module.getModifiedItemAttr(srcAttr),
                                                stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "falloff", module.getModifiedItemAttr("falloffBonus"),
                                          stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6687():
    type = "projected", "active"
    def handler(fit, container, context):
        if "projected" in context:
            bonus = container.getModifiedItemAttr("armorDamageAmount")
            duration = container.getModifiedItemAttr("duration") / 1000.0
            rps = bonus / duration
            fit.extraAttributes.increase("armorRepair", rps)
            fit.extraAttributes.increase("armorRepairPreSpool", rps)
            fit.extraAttributes.increase("armorRepairFullSpool", rps)

    return locals()

def effect6688():
    type = "projected", "active"
    def handler(fit, container, context):
        if "projected" in context:
            bonus = container.getModifiedItemAttr("shieldBonus")
            duration = container.getModifiedItemAttr("duration") / 1000.0
            fit.extraAttributes.increase("shieldRepair", bonus / duration)

    return locals()

def effect6689():
    type = "projected", "active"
    runTime = "late"
    def handler(fit, module, context):
        if "projected" not in context:
            return
        bonus = module.getModifiedItemAttr("structureDamageAmount")
        duration = module.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("hullRepair", bonus / duration)

    return locals()

def effect6690():
    type = "active", "projected"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6691():
    from eos.saveddata.module import State
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "active", "projected"
    def handler(fit, src, context, **kwargs):
        if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or
                                        hasattr(src, "amountActive")):
            amount = src.getModifiedItemAttr("energyNeutralizerAmount")
            time = src.getModifiedItemAttr("energyNeutralizerDuration")
            if 'effect' in kwargs:
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.addDrain(src, time, amount, 0)

    return locals()

def effect6692():
    type = "projected", "active"
    def handler(fit, container, context, *args, **kwargs):
        if "projected" in context:
            fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                                   stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6693():
    type = "projected", "active"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" not in context:
            return
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                               stackingPenalties=True, *args, **kwargs)
        fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                               stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6694():
    type = "projected", "active"
    def handler(fit, module, context, *args, **kwargs):
        if "projected" in context:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                          stackingPenalties=True, *args, **kwargs)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                          "falloff", module.getModifiedItemAttr("falloffBonus"),
                                          stackingPenalties=True, *args, **kwargs)

    return locals()

def effect6695():
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "projected", "active"
    def handler(fit, module, context, **kwargs):
        if "projected" in context:
            strModifier = 1 - module.getModifiedItemAttr("scan{0}StrengthBonus".format(fit.scanType)) / fit.scanStrength
            if 'effect' in kwargs:
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.ecmProjectedStr *= strModifier

    return locals()

def effect6697():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Armor", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Resource Processing", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6698():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Navigation", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Anchor", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6699():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Drones", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect67():
    type = 'active'
    def handler(fit, module, context):
        module.reloadTime = 1000

    return locals()

def effect670():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))

    return locals()

def effect6700():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Electronic Systems", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Scanning", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Targeting", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6701():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Projectile Weapon", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6702():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Energy Weapon", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6703():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Hybrid Weapon", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6704():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Launcher", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6705():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Shield", "drawback",
                                      src.getModifiedItemAttr("rigDrawbackBonus") * lvl)

    return locals()

def effect6706():
    runTime = "early"
    type = "passive"
    def handler(fit, src, context):
        fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Cybernetics"),
                                                 "armorRepairBonus", src.getModifiedItemAttr("implantSetSerpentis2"))

    return locals()

def effect6708():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("armorRepairBonus"))

    return locals()

def effect6709():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect6710():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "speedFactor",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtM1"), skill="Minmatar Dreadnought")

    return locals()

def effect6711():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusRole3"))

    return locals()

def effect6712():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "speedFactor",
                                      src.getModifiedItemAttr("shipBonusTitanM1"), skill="Minmatar Titan")

    return locals()

def effect6713():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"), "speedFactor",
                                      src.getModifiedItemAttr("shipBonusSupercarrierM1"), skill="Minmatar Carrier")

    return locals()

def effect6714():
    from eos.modifiedAttributeDict import ModifiedAttributeDict
    type = "projected", "active"
    def handler(fit, module, context, **kwargs):
        if "projected" in context:
            strModifier = 1 - module.getModifiedItemAttr("scan{0}StrengthBonus".format(fit.scanType)) / fit.scanStrength
            if 'effect' in kwargs:
                strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])
            fit.ecmProjectedStr *= strModifier

    return locals()

def effect6717():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"), "capacitorNeed",
                                      src.getModifiedItemAttr("miningDurationRoleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"), "duration",
                                      src.getModifiedItemAttr("miningDurationRoleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "duration",
                                      src.getModifiedItemAttr("miningDurationRoleBonus"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "capacitorNeed",
                                      src.getModifiedItemAttr("miningDurationRoleBonus"))

    return locals()

def effect6720():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldBonus",
                                     src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "structureDamageAmount",
                                     src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorDamageAmount",
                                     src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")

    return locals()

def effect6721():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "falloffEffectiveness",
                                      src.getModifiedItemAttr("eliteBonusLogistics1"),
                                      skill="Logistics Cruisers")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "maxRange",
                                      src.getModifiedItemAttr("eliteBonusLogistics1"),
                                      skill="Logistics Cruisers")

    return locals()

def effect6722():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "falloffEffectiveness",
                                      src.getModifiedItemAttr("roleBonusRepairRange"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "maxRange",
                                      src.getModifiedItemAttr("roleBonusRepairRange"))

    return locals()

def effect6723():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"), "cpu",
                                      src.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")

    return locals()

def effect6724():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "duration",
                                      src.getModifiedItemAttr("eliteBonusLogistics3"), skill="Logistics Cruisers")

    return locals()

def effect6725():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"), "falloff",
                                      src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")

    return locals()

def effect6726():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"), "cpu",
                                      src.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect6727():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"),
                                      "falloffEffectiveness", src.getModifiedItemAttr("eliteBonusCovertOps1"),
                                      stackingPenalties=True, skill="Covert Ops")

    return locals()

def effect6730():
    type = "active"
    runTime = "late"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
        speedBoost = module.getModifiedItemAttr("speedFactor")
        mass = fit.ship.getModifiedItemAttr("mass")
        thrust = module.getModifiedItemAttr("speedBoostFactor")
        fit.ship.boostItemAttr("maxVelocity", speedBoost * thrust / mass)
        fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties=True)

    return locals()

def effect6731():
    type = "active"
    runTime = "late"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
        speedBoost = module.getModifiedItemAttr("speedFactor")
        mass = fit.ship.getModifiedItemAttr("mass")
        thrust = module.getModifiedItemAttr("speedBoostFactor")
        fit.ship.boostItemAttr("maxVelocity", speedBoost * thrust / mass)

    return locals()

def effect6732():
    """
    Some documentation:
    When the fit is calculated, we gather up all the gang effects and stick them onto the fit. We don't run the actual
    effect yet, only give the fit details so that it can run the effect at a later time. We need to do this so that we can
    only run the strongest effect. When we are done, one of the last things that we do with the fit is to loop through those
    bonuses and actually run the effect. To do this, we have a special argument passed into the effect handler that tells it
    which warfareBuffID to run (shouldn't need this right now, but better safe than sorry)
    """
    type = "active", "gang"
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
                value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])

    return locals()

def effect6733():
    type = "active", "gang"
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
                value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])

    return locals()

def effect6734():
    type = "active", "gang"
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
                value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])

    return locals()

def effect6735():
    type = "active", "gang"
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
                value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])

    return locals()

def effect6736():
    type = "active", "gang"
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
                value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])

    return locals()

def effect6737():
    type = "active"
    def handler(fit, module, context):
        for x in range(1, 4):
            value = module.getModifiedChargeAttr("warfareBuff{}Multiplier".format(x))
            module.multiplyItemAttr("warfareBuff{}Value".format(x), value)

    return locals()

def effect675():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Pulse Weapons"),
                                      "cpu", skill.getModifiedItemAttr("cpuNeedBonus") * skill.level)

    return locals()

def effect6753():
    type = "active", "gang"
    def handler(fit, module, context, **kwargs):
        for x in range(1, 5):
            if module.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = module.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])

    return locals()

def effect6762():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Drone Specialization"), "miningAmount",
                                     src.getModifiedItemAttr("miningAmountBonus") * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Drone Specialization"), "maxVelocity",
                                     src.getModifiedItemAttr("maxVelocityBonus") * lvl)

    return locals()

def effect6763():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level if "skill" in context else 1
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Operation"), "duration", src.getModifiedItemAttr("rofBonus") * lvl)

    return locals()

def effect6764():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Specialization"), "duration",
                                     src.getModifiedItemAttr("rofBonus") * lvl)
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Specialization"),
                                     "maxVelocity", src.getModifiedItemAttr("maxVelocityBonus") * lvl)

    return locals()

def effect6765():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Spatial Phenomena Generation"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6766():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                         src.getModifiedItemAttr("maxGangModules"))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupOnline",
                                         src.getModifiedItemAttr("maxGangModules"))

    return locals()

def effect6769():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "maxRange",
                                      src.getModifiedItemAttr("areaOfEffectBonus") * src.level)

    return locals()

def effect677():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)

    return locals()

def effect6770():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6771():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6772():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6773():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6774():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6776():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)

    return locals()

def effect6777():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)

    return locals()

def effect6778():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)

    return locals()

def effect6779():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Multiplier",
                                        src.getModifiedItemAttr("commandStrengthBonus") * lvl)

    return locals()

def effect6780():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)

    return locals()

def effect6782():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"),
                                      "reloadTime",
                                      src.getModifiedItemAttr("reloadTimeBonus") * lvl)

    return locals()

def effect6783():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "maxRange",
                                      src.getModifiedItemAttr("roleBonusCommandBurstAoERange"))

    return locals()

def effect6786():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                      src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                      src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                      src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                      src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                      src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")

    return locals()

def effect6787():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier",
                                     src.getModifiedItemAttr("shipBonusICS4"),
                                     skill="Industrial Command Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "shieldCapacity",
                                     src.getModifiedItemAttr("shipBonusICS4"),
                                     skill="Industrial Command Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "armorHP",
                                     src.getModifiedItemAttr("shipBonusICS4"),
                                     skill="Industrial Command Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "hp",
                                     src.getModifiedItemAttr("shipBonusICS4"),
                                     skill="Industrial Command Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                     "miningAmount",
                                     src.getModifiedItemAttr("shipBonusICS4"),
                                     skill="Industrial Command Ships"
                                     )

    return locals()

def effect6788():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                     "duration",
                                     src.getModifiedItemAttr("shipBonusICS5"),
                                     skill="Industrial Command Ships"
                                     )

    return locals()

def effect6789():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier",
                                     src.getModifiedItemAttr("industrialBonusDroneDamage"))

    return locals()

def effect6790():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Operation"), "duration",
                                     src.getModifiedItemAttr("roleBonusDroneIceHarvestingSpeed"))

    return locals()

def effect6792():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "damageMultiplier",
                                     src.getModifiedItemAttr("shipBonusORECapital4"),
                                     skill="Capital Industrial Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "shieldCapacity",
                                     src.getModifiedItemAttr("shipBonusORECapital4"),
                                     skill="Capital Industrial Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "armorHP",
                                     src.getModifiedItemAttr("shipBonusORECapital4"),
                                     skill="Capital Industrial Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     "hp",
                                     src.getModifiedItemAttr("shipBonusORECapital4"),
                                     skill="Capital Industrial Ships"
                                     )
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                     "miningAmount",
                                     src.getModifiedItemAttr("shipBonusORECapital4"),
                                     skill="Capital Industrial Ships"
                                     )

    return locals()

def effect6793():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                      src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")

    return locals()

def effect6794():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Value",
                                      src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                      src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Value",
                                      src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Value",
                                      src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Value",
                                      src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")

    return locals()

def effect6795():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                     "duration",
                                     src.getModifiedItemAttr("shipBonusORECapital5"),
                                     skill="Capital Industrial Ships"
                                     )

    return locals()

def effect6796():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
            "damageMultiplier",
            1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6797():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
            "damageMultiplier",
            1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6798():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Energy Turret"),
            "damageMultiplier",
            1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6799():
    type = "passive"
    def handler(fit, module, context):
        types = ("thermal", "em", "explosive", "kinetic")
        for type in types:
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                               "{}Damage".format(type),
                                               1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"),
                                               stackingPenalties=True,
                                               penaltyGroup="postDiv")

    return locals()

def effect6800():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("weaponDisruptionResistance", 1 / module.getModifiedItemAttr("modeEwarResistancePostDiv"))
        fit.ship.multiplyItemAttr("sensorDampenerResistance", 1 / module.getModifiedItemAttr("modeEwarResistancePostDiv"))

    return locals()

def effect6801():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("High Speed Maneuvering") or mod.item.requiresSkill("Afterburner"),
            "speedFactor",
            1 / module.getModifiedItemAttr("modeVelocityPostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )

    return locals()

def effect6807():
    type = "passive"
    def handler(fit, src, context):
        lvl = src.level
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Invulnerability Core Operation"), "buffDuration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Invulnerability Core Operation"), "duration",
                                      src.getModifiedItemAttr("durationBonus") * lvl)

    return locals()

def effect6844():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Defender Missiles"),
                                        "maxVelocity", skill.getModifiedItemAttr("missileVelocityBonus") * skill.level)

    return locals()

def effect6845():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Defender Missiles"),
                                      "moduleReactivationDelay", ship.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect6851():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusRole3"))

    return locals()

def effect6852():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", src.getModifiedItemAttr("shipBonusTitanM1"), skill="Minmatar Titan")

    return locals()

def effect6853():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", src.getModifiedItemAttr("shipBonusTitanA1"), skill="Amarr Titan")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", src.getModifiedItemAttr("shipBonusTitanA1"), skill="Amarr Titan")

    return locals()

def effect6855():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                      "energyNeutralizerAmount", src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")

    return locals()

def effect6856():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "maxRange", src.getModifiedItemAttr("shipBonusDreadnoughtM1"), skill="Minmatar Dreadnought")

    return locals()

def effect6857():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "maxRange", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "falloffEffectiveness", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")

    return locals()

def effect6858():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                      "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")

    return locals()

def effect6859():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "cpu", src.getModifiedItemAttr("shipBonusRole4"))

    return locals()

def effect6860():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "power",
                                      src.getModifiedItemAttr("shipBonusRole5"))

    return locals()

def effect6861():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"), "power", src.getModifiedItemAttr("shipBonusRole5"))

    return locals()

def effect6862():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1"), skill="Minmatar Carrier")

    return locals()

def effect6865():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")

    return locals()

def effect6866():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "explosionDelay", src.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "explosionDelay", src.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect6867():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "speed", src.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")

    return locals()

def effect6871():
    type = "passive"
    def handler(fit, src, context):
        try:
            bonus = max(0, min(50.0, (src.parent.character.secStatus * 10)))
        except:
            bonus = None
        if bonus is not None:
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", bonus, stackingPenalties=True)
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", bonus, stackingPenalties=True)

    return locals()

def effect6872():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange", src.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")

    return locals()

def effect6873():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect6874():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "explosionDelay", src.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "explosionDelay", src.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect6877():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("eliteBonusBlackOps1"), stackingPenalties=True, skill="Black Ops")

    return locals()

def effect6878():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusBlackOps4"), stackingPenalties=True, skill="Black Ops")

    return locals()

def effect6879():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange",
                                      src.getModifiedItemAttr("eliteBonusBlackOps3"), stackingPenalties=True, skill="Black Ops")

    return locals()

def effect6880():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise", "speed",
                                      src.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo", "speed",
                                      src.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy", "speed",
                                      src.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")

    return locals()

def effect6881():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosionDelay",
                                        src.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "explosionDelay",
                                        src.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")

    return locals()

def effect6883():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                      "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")

    return locals()

def effect6894():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"),
        "cpu", src.getModifiedItemAttr("subsystemEnergyNeutFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"),
                                      "power", src.getModifiedItemAttr("subsystemEnergyNeutFittingReduction"))

    return locals()

def effect6895():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "cpu", src.getModifiedItemAttr("subsystemMETFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "power", src.getModifiedItemAttr("subsystemMETFittingReduction"))

    return locals()

def effect6896():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "cpu", src.getModifiedItemAttr("subsystemMHTFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "power", src.getModifiedItemAttr("subsystemMHTFittingReduction"))

    return locals()

def effect6897():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "power", src.getModifiedItemAttr("subsystemMPTFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "cpu", src.getModifiedItemAttr("subsystemMPTFittingReduction"))

    return locals()

def effect6898():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      "cpu", src.getModifiedItemAttr("subsystemMRARFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      "power", src.getModifiedItemAttr("subsystemMRARFittingReduction"))

    return locals()

def effect6899():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      "cpu", src.getModifiedItemAttr("subsystemMRSBFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") and
                                                  mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                      "power", src.getModifiedItemAttr("subsystemMRSBFittingReduction"))

    return locals()

def effect6900():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "cpu", src.getModifiedItemAttr("subsystemMMissileFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "power", src.getModifiedItemAttr("subsystemMMissileFittingReduction"))

    return locals()

def effect6908():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserCaldari2"),
                                      skill="Caldari Strategic Cruiser")

    return locals()

def effect6909():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserAmarr2"),
                                      skill="Amarr Strategic Cruiser")

    return locals()

def effect6910():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserGallente2"),
                                      skill="Gallente Strategic Cruiser")

    return locals()

def effect6911():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                      ship.getModifiedItemAttr("shipBonusStrategicCruiserMinmatar2"),
                                      skill="Minmatar Strategic Cruiser")

    return locals()

def effect6920():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.increaseItemAttr("hp", module.getModifiedItemAttr("structureHPBonusAdd") or 0)

    return locals()

def effect6921():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseSensorStrength", src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"),
                                        skill="Amarr Defensive Systems")

    return locals()

def effect6923():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles") or mod.charge.requiresSkill("Heavy Assault Missiles"),
                                      "maxVelocity", container.getModifiedItemAttr("subsystemBonusMinmatarOffensive"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect6924():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                      "aoeVelocity", container.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect6925():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "maxVelocity", src.getModifiedItemAttr("subsystemBonusGallenteOffensive2"),
                                     skill="Gallente Offensive Systems")
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                     "trackingSpeed", src.getModifiedItemAttr("subsystemBonusGallenteOffensive2"),
                                     skill="Gallente Offensive Systems")

    return locals()

def effect6926():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion"), skill="Amarr Propulsion Systems")

    return locals()

def effect6927():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                               skill="Minmatar Propulsion Systems")

    return locals()

def effect6928():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner") or mod.item.requiresSkill("High Speed Maneuvering"),
                                      "overloadSpeedFactorBonus", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                                      skill="Caldari Propulsion Systems")

    return locals()

def effect6929():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner") or mod.item.requiresSkill("High Speed Maneuvering"),
                                      "overloadSpeedFactorBonus", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                                      skill="Gallente Propulsion Systems")

    return locals()

def effect6930():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusAmarrCore2"), skill="Amarr Core Systems")

    return locals()

def effect6931():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusMinmatarCore2"),
                               skill="Minmatar Core Systems")

    return locals()

def effect6932():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusGallenteCore2"),
                               skill="Gallente Core Systems")

    return locals()

def effect6933():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusCaldariCore2"),
                               skill="Caldari Core Systems")

    return locals()

def effect6934():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargetsBonus"))

    return locals()

def effect6935():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"), "overloadSelfDurationBonus",
                                      src.getModifiedItemAttr("subsystemBonusAmarrCore3"), skill="Amarr Core Systems")

    return locals()

def effect6936():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                      "overloadRangeBonus", src.getModifiedItemAttr("subsystemBonusMinmatarCore3"),
                                      skill="Minmatar Core Systems")

    return locals()

def effect6937():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "overloadRangeBonus",
                                      src.getModifiedItemAttr("subsystemBonusGallenteCore3"), skill="Gallente Core Systems")

    return locals()

def effect6938():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "overloadECMStrengthBonus",
                                      src.getModifiedItemAttr("subsystemBonusCaldariCore3"), skill="Caldari Core Systems")

    return locals()

def effect6939():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadSelfDurationBonus",
                                      src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"), skill="Amarr Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadHardeningBonus",
                                      src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"), skill="Amarr Defensive Systems")

    return locals()

def effect6940():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadHardeningBonus",
                                      src.getModifiedItemAttr("subsystemBonusGallenteDefensive2"), skill="Gallente Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadSelfDurationBonus",
                                      src.getModifiedItemAttr("subsystemBonusGallenteDefensive2"), skill="Gallente Defensive Systems")

    return locals()

def effect6941():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Tactical Shield Manipulation"),
                                      "overloadHardeningBonus", src.getModifiedItemAttr("subsystemBonusCaldariDefensive2"),
                                      skill="Caldari Defensive Systems")

    return locals()

def effect6942():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadSelfDurationBonus",
                                      src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadHardeningBonus",
                                      src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Tactical Shield Manipulation"), "overloadHardeningBonus",
                                      src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")

    return locals()

def effect6943():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusAmarrDefensive3"),
                                      skill="Amarr Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusAmarrDefensive3"),
                                      skill="Amarr Defensive Systems")

    return locals()

def effect6944():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusGallenteDefensive3"),
                                      skill="Gallente Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                      "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusGallenteDefensive3"),
                                      skill="Gallente Defensive Systems")

    return locals()

def effect6945():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "overloadShieldBonus", src.getModifiedItemAttr("subsystemBonusCaldariDefensive3"),
                                      skill="Caldari Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusCaldariDefensive3"),
                                      skill="Caldari Defensive Systems")

    return locals()

def effect6946():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Shield Operation"),
                                      "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive3"),
                                      skill="Minmatar Defensive Systems")
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Shield Operation"),
                                      "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive3"),
                                      skill="Minmatar Defensive Systems")

    return locals()

def effect6947():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                        "baseSensorStrength", src.getModifiedItemAttr("subsystemBonusCaldariDefensive2"),
                                        skill="Caldari Defensive Systems")

    return locals()

def effect6949():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"), "baseSensorStrength",
                                        src.getModifiedItemAttr("subsystemBonusGallenteDefensive2"), skill="Gallente Defensive Systems")

    return locals()

def effect6951():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"), "baseSensorStrength",
                                        src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")

    return locals()

def effect6953():
    type = "passive"
    def handler(fit, module, context):
        module.multiplyItemAttr("power", module.getModifiedItemAttr("mediumRemoteRepFittingMultiplier"))
        module.multiplyItemAttr("cpu", module.getModifiedItemAttr("mediumRemoteRepFittingMultiplier"))

    return locals()

def effect6954():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "power",
                                      src.getModifiedItemAttr("subsystemCommandBurstFittingReduction"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "cpu",
                                      src.getModifiedItemAttr("subsystemCommandBurstFittingReduction"))

    return locals()

def effect6955():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Remote Shield Booster", "Ancillary Remote Shield Booster"),
                                      "falloffEffectiveness", src.getModifiedItemAttr("remoteShieldBoosterFalloffBonus"))

    return locals()

def effect6956():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Remote Armor Repairer", "Ancillary Remote Armor Repairer"),
                                      "maxRange", src.getModifiedItemAttr("remoteArmorRepairerOptimalBonus"))

    return locals()

def effect6957():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Remote Armor Repairer", "Ancillary Remote Armor Repairer"),
                                      "falloffEffectiveness", src.getModifiedItemAttr("remoteArmorRepairerFalloffBonus"))

    return locals()

def effect6958():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "overloadSelfDurationBonus",
                                      src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")

    return locals()

def effect6959():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "overloadSelfDurationBonus",
                                      src.getModifiedItemAttr("subsystemBonusGallenteOffensive3"), skill="Gallente Offensive Systems")

    return locals()

def effect6960():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                      "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusCaldariOffensive3"),
                                      skill="Caldari Offensive Systems")

    return locals()

def effect6961():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"),
                                      skill="Minmatar Offensive Systems")

    return locals()

def effect6962():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"),
                               skill="Amarr Propulsion Systems")

    return locals()

def effect6963():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                               skill="Minmatar Propulsion Systems")

    return locals()

def effect6964():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("baseWarpSpeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                               skill="Gallente Propulsion Systems")

    return locals()

def effect6981():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "thermalDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "kineticDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "thermalDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "kineticDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")

    return locals()

def effect6982():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "explosiveDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "emDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "emDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "explosiveDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "emDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "explosiveDamage",
                                      src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")

    return locals()

def effect6983():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusTitanC1"), skill="Caldari Titan")

    return locals()

def effect6984():
    type = "passive"
    def handler(fit, src, context):
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                       src.getModifiedItemAttr("shipBonusRole4"))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusRole4"))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusRole4"))
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesDamageMultiplier",
                                       src.getModifiedItemAttr("shipBonusRole4"))

    return locals()

def effect6985():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "kineticDamage",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Torpedoes"), "thermalDamage",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "kineticDamage",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Torpedoes"), "thermalDamage",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
        fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                      src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")

    return locals()

def effect6986():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"), "shieldBonus",
                                      src.getModifiedItemAttr("shipBonusForceAuxiliaryG1"), skill="Gallente Carrier")

    return locals()

def effect6987():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                        "structureDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                        "shieldBonus", src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                        "armorDamageAmount", src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                        "armorHP", src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                        "shieldCapacity", src.getModifiedItemAttr("shipBonusRole2"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Drone Operation"),
                                        "hp", src.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect699():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalized = False if "skill" in context or "implant" in context or "booster" in context else True
        fit.ship.boostItemAttr("scanResolution", container.getModifiedItemAttr("scanResolutionBonus") * level,
                               stackingPenalties=penalized)

    return locals()

def effect6992():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect6993():
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

    return locals()

def effect6994():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")

    return locals()

def effect6995():
    type = 'active'
    def handler(fit, module, context):
        module.reloadTime = 1000

    return locals()

def effect6996():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "armorDamageAmount",
                                      src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect6997():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "armorDamageAmount",
                                      src.getModifiedItemAttr("eliteBonusCovertOps4"), skill="Covert Ops")

    return locals()

def effect6999():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                         "cpu", ship.getModifiedItemAttr("stealthBomberLauncherCPU"))

    return locals()

def effect7000():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"), "falloff",
                                      src.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")

    return locals()

def effect7001():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo", "speed", src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect7002():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"), "power", src.getModifiedItemAttr("shipBonusRole3"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"), "cpu", src.getModifiedItemAttr("shipBonusRole3"))

    return locals()

def effect7003():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("eliteBonusCovertOps3"), skill="Covert Ops")

    return locals()

def effect7008():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.multiplyItemAttr("shieldCapacity", src.getModifiedItemAttr("structureFullPowerStateHitpointMultiplier") or 0)
        fit.ship.multiplyItemAttr("armorHP", src.getModifiedItemAttr("structureFullPowerStateHitpointMultiplier") or 0)

    return locals()

def effect7009():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context):
        fit.ship.forceItemAttr("structureFullPowerStateHitpointMultiplier", src.getModifiedItemAttr("serviceModuleFullPowerStateHitpointMultiplier"))

    return locals()

def effect7012():
    type = "active"
    runTime = "early"
    def handler(fit, src, context):
        for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
            for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
                bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
                bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
                booster = "%s%sDamageResonance" % (layer, damageType)
                src.forceItemAttr(booster, src.getModifiedItemAttr("resistanceMultiplier"))

    return locals()

def effect7013():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage",
                                        src.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect7014():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "thermalDamage",
                                        src.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect7015():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "emDamage",
                                        src.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect7016():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "explosiveDamage",
                                        src.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect7017():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "aoeVelocity",
                                        src.getModifiedItemAttr("eliteBonusGunship2"), stackingPenalties=True, skill="Assault Frigates")

    return locals()

def effect7018():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"), "speed",
                                      src.getModifiedItemAttr("shipBonusAF"), stackingPenalties=False, skill="Amarr Frigate")

    return locals()

def effect7020():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange",
                                      src.getModifiedItemAttr("stasisWebRangeBonus"), stackingPenalties=False)

    return locals()

def effect7021():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("structureRigMaxTargetRangeBonus"))

    return locals()

def effect7024():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "trackingSpeed",
                                     src.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")

    return locals()

def effect7026():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context, *args, **kwargs):
        src.boostItemAttr("maxRange", src.getModifiedChargeAttr("warpScrambleRangeBonus"))

    return locals()

def effect7027():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))

    return locals()

def effect7028():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("rechargeRate", module.getModifiedItemAttr("capacitorRechargeRateMultiplier"))

    return locals()

def effect7029():
    type = "passive"
    runTime = "early"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("hiddenArmorHPMultiplier", src.getModifiedItemAttr("armorHpBonus"), stackingPenalties=True)

    return locals()

def effect7030():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Guided Bomb Launcher",
                                      "speed", ship.getModifiedItemAttr("structureAoERoFRoleBonus"))
        for attr in ["duration", "durationTargetIlluminationBurstProjector", "durationWeaponDisruptionBurstProjector",
                     "durationECMJammerBurstProjector", "durationSensorDampeningBurstProjector", "capacitorNeed"]:
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Burst Projector",
                                          attr, ship.getModifiedItemAttr("structureAoERoFRoleBonus"))

    return locals()

def effect7031():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7032():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7033():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                        "emDamage", src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7034():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7035():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7036():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7037():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "thermalDamage", src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7038():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "kineticDamage", src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")

    return locals()

def effect7039():
    type = "passive"
    def handler(fit, src, context):
        groups = ("Structure Anti-Subcapital Missile", "Structure Anti-Capital Missile")
        for dmgType in ("em", "kinetic", "explosive", "thermal"):
            fit.modules.filteredChargeMultiply(lambda mod: mod.item.group.name in groups,
                                               "%sDamage" % dmgType,
                                               src.getModifiedItemAttr("hiddenMissileDamageMultiplier"))

    return locals()

def effect7040():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.multiplyItemAttr("armorHP", src.getModifiedItemAttr("hiddenArmorHPMultiplier") or 0)

    return locals()

def effect7042():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("armorHP", src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")

    return locals()

def effect7043():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect7044():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")

    return locals()

def effect7045():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("signatureRadius", src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")

    return locals()

def effect7046():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("explosiveDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("thermalDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("kineticDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
        fit.ship.boostItemAttr("emDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")

    return locals()

def effect7047():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Propulsion Module", "Micro Jump Drive"),
                                      "power", src.getModifiedItemAttr("flagCruiserFittingBonusPropMods"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Propulsion Module", "Micro Jump Drive"),
                                      "cpu", src.getModifiedItemAttr("flagCruiserFittingBonusPropMods"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Target Painter", "Scan Probe Launcher"),
                                      "cpu", src.getModifiedItemAttr("flagCruiserFittingBonusPainterProbes"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Target Painter", "Scan Probe Launcher"),
                                      "power", src.getModifiedItemAttr("flagCruiserFittingBonusPainterProbes"))

    return locals()

def effect7050():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7051():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7052():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter", "signatureRadiusBonus",
                                      src.getModifiedItemAttr("targetPainterStrengthModifierFlagCruisers"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter", "maxRange",
                                      src.getModifiedItemAttr("targetPainterRangeModifierFlagCruisers"))

    return locals()

def effect7055():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "thermalDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "explosiveDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "kineticDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"), "emDamage",
                                        src.getModifiedItemAttr("shipBonusRole7"))

    return locals()

def effect7058():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7059():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect706():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpFactor", src.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")

    return locals()

def effect7060():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 5):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7061():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7062():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7063():
    runTime = "early"
    type = ("projected", "passive", "gang")
    def handler(fit, beacon, context, **kwargs):
        for x in range(1, 3):
            if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
                value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
                id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))
                if id:
                    fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')

    return locals()

def effect7064():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, beacon, context):
        pass

    return locals()

def effect7071():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect7072():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect7073():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Precursor Weapon"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect7074():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Disintegrator Specialization"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect7075():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Disintegrator Specialization"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect7076():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Disintegrator Specialization"),
                                      "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)

    return locals()

def effect7077():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Precursor Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect7078():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Precursor Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect7079():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Precursor Weapon"),
                                      "speed", ship.getModifiedItemAttr("shipBonusPBS1"), skill="Precursor Battleship")

    return locals()

def effect7080():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Precursor Weapon"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusPBS2"), skill="Precursor Battleship")

    return locals()

def effect7085():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusPC1"), skill="Precursor Cruiser")

    return locals()

def effect7086():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusPC2"), skill="Precursor Cruiser")

    return locals()

def effect7087():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusPF2"), skill="Precursor Frigate")

    return locals()

def effect7088():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusPF1"), skill="Precursor Frigate")

    return locals()

def effect7091():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"), "capacitorNeed", src.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect7092():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect7093():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Pulse Weapons"),
                                      "capacitorNeed", ship.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect7094():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect7097():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Precursor Weapon",
                                      "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)

    return locals()

def effect7111():
    runTime = "early"
    type = ("projected", "passive")
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                         "damageMultiplier", module.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect7112():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "capacitorNeed",
                                      src.getModifiedItemAttr("shipBonusRole2"))

    return locals()

def effect7116():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"), "baseSensorStrength",
                                        src.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")

    return locals()

def effect7117():
    type = "passive"
    def handler(fit, src, context):
        fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("shipRoleBonusWarpSpeed"))

    return locals()

def effect7118():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"), "damageMultiplierBonusPerCycle",
                                         src.getModifiedItemAttr("eliteBonusCovertOps3"), skill="Covert Ops")

    return locals()

def effect7119():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"), "damageMultiplierBonusPerCycle",
                                         src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")

    return locals()

def effect7142():
    type = "active"
    def handler(fit, src, context):
        fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("warpScrambleStrength"))
        fit.ship.boostItemAttr("mass", src.getModifiedItemAttr("massBonusPercentage"), stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"), "speedFactor",
                                      src.getModifiedItemAttr("speedFactorBonus"), stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"), "speedBoostFactor",
                                      src.getModifiedItemAttr("speedBoostFactorBonus"))
        fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"), "activationBlocked",
                                         src.getModifiedItemAttr("activationBlockedStrenght"))
        fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("maxVelocityBonus"), stackingPenalties=True)

    return locals()

def effect7154():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusPD1"),
                                      skill="Precursor Destroyer")

    return locals()

def effect7155():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusPBC1"),
                                      skill="Precursor Battlecruiser")

    return locals()

def effect7156():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                      "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))

    return locals()

def effect7157():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusPD2"),
                                      skill="Precursor Destroyer")

    return locals()

def effect7158():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusPBC2"),
                               skill="Precursor Battlecruiser")

    return locals()

def effect7159():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusPBC2"),
                               skill="Precursor Battlecruiser")

    return locals()

def effect7160():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusPBC2"),
                               skill="Precursor Battlecruiser")

    return locals()

def effect7161():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusPBC2"),
                               skill="Precursor Battlecruiser")

    return locals()

def effect7162():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                      "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))

    return locals()

def effect7166():
    from eos.utils.spoolSupport import SpoolType, SpoolOptions, calculateSpoolup, resolveSpoolOptions
    type = "projected", "active"
    runTime = "late"
    def handler(fit, container, context, **kwargs):
        if "projected" in context:
            repAmountBase = container.getModifiedItemAttr("armorDamageAmount")
            cycleTime = container.getModifiedItemAttr("duration") / 1000.0
            repSpoolMax = container.getModifiedItemAttr("repairMultiplierBonusMax")
            repSpoolPerCycle = container.getModifiedItemAttr("repairMultiplierBonusPerCycle")
            defaultSpoolValue = 1
            spoolType, spoolAmount = resolveSpoolOptions(SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False), container)
            rps = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, spoolType, spoolAmount)[0]) / cycleTime
            rpsPreSpool = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, SpoolType.SCALE, 0)[0]) / cycleTime
            rpsFullSpool = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, SpoolType.SCALE, 1)[0]) / cycleTime
            fit.extraAttributes.increase("armorRepair", rps, **kwargs)
            fit.extraAttributes.increase("armorRepairPreSpool", rpsPreSpool, **kwargs)
            fit.extraAttributes.increase("armorRepairFullSpool", rpsFullSpool, **kwargs)

    return locals()

def effect7167():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter", "maxRange", src.getModifiedItemAttr("shipBonusRole1"))

    return locals()

def effect7168():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "maxRange", src.getModifiedItemAttr("shipBonusRole3"))

    return locals()

def effect7169():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "armorDamageAmount", src.getModifiedItemAttr("shipBonusPC1"), skill="Precursor Cruiser")

    return locals()

def effect7170():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "capacitorNeed", src.getModifiedItemAttr("shipBonusPC2"), skill="Precursor Cruiser")

    return locals()

def effect7171():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "maxRange", src.getModifiedItemAttr("shipBonusPC1"), skill="Precursor Cruiser")

    return locals()

def effect7172():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "capacitorNeed", src.getModifiedItemAttr("eliteBonusLogistics1"), skill="Logistics Cruisers")

    return locals()

def effect7173():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mutadaptive Remote Armor Repairer", "armorDamageAmount", src.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics Cruisers")

    return locals()

def effect7176():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                     src.getModifiedItemAttr("damageMultiplierBonus"))

    return locals()

def effect7177():
    type = "passive"
    def handler(fit, src, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                     src.getModifiedItemAttr("hullHpBonus"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                     src.getModifiedItemAttr("armorHpBonus"))
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                     src.getModifiedItemAttr("shieldCapacityBonus"))

    return locals()

def effect7179():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Strip Miner",
                                      "duration", module.getModifiedItemAttr("miningDurationMultiplier"))

    return locals()

def effect7180():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mining Laser",
                                      "duration", module.getModifiedItemAttr("miningDurationMultiplier"))

    return locals()

def effect7183():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "maxRange",
                                      src.getModifiedItemAttr("warpScrambleRangeBonus"), stackingPenalties=False)

    return locals()

def effect726():
    type = "passive"
    def handler(fit, ship, context):
        if "shipBonusGI" in fit.ship.item.attributes:
            bonusAttr = "shipBonusGI"
        else:
            bonusAttr = "shipBonusGI2"
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr(bonusAttr), skill="Gallente Industrial")

    return locals()

def effect727():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusCI"), skill="Caldari Industrial")

    return locals()

def effect728():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusMI"), skill="Minmatar Industrial")

    return locals()

def effect729():
    type = "passive"
    def handler(fit, ship, context):
        if "shipBonusGI" in fit.ship.item.attributes:
            bonusAttr = "shipBonusGI"
        else:
            bonusAttr = "shipBonusGI2"
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr(bonusAttr), skill="Gallente Industrial")

    return locals()

def effect730():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusCI"), skill="Caldari Industrial")

    return locals()

def effect732():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusAI"), skill="Amarr Industrial")

    return locals()

def effect736():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("capacitorCapacity", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")

    return locals()

def effect744():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("CPU Management"),
                                      "duration", container.getModifiedItemAttr("scanspeedBonus") * level)

    return locals()

def effect754():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect757():
    type = "passive"
    def handler(fit, src, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"), "damageMultiplier",
                                      src.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")

    return locals()

def effect760():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect763():
    type = "passive"
    def handler(fit, container, context):
        for dmgType in ("em", "kinetic", "explosive", "thermal"):
            fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                               "%sDamage" % dmgType,
                                               container.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                               stackingPenalties=True)

    return locals()

def effect784():
    type = "passive"
    def handler(fit, container, context):
        level = container.level if "skill" in context else 1
        penalized = False if "skill" in context or "implant" in context or "booster" in context else True
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "explosionDelay", container.getModifiedItemAttr("maxFlightTimeBonus") * level,
                                        stackingPenalties=penalized)

    return locals()

def effect804():
    type = "passive"
    def handler(fit, module, context):
        rawAttr = module.item.getAttribute("capacitorNeed")
        if rawAttr is not None and rawAttr >= 0:
            module.boostItemAttr("capacitorNeed", module.getModifiedChargeAttr("capNeedBonus") or 0)

    return locals()

def effect836():
    type = "passive"
    def handler(fit, module, context):
        fit.ship.boostItemAttr("capacity", module.getModifiedItemAttr("cargoCapacityBonus"))

    return locals()

def effect848():
    type = "passive"
    def handler(fit, skill, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                      "cloakingTargetingDelay",
                                      skill.getModifiedItemAttr("cloakingTargetingDelayBonus") * skill.level)

    return locals()

def effect854():
    type = "offline"
    def handler(fit, module, context):
        fit.ship.multiplyItemAttr("scanResolution",
                                  module.getModifiedItemAttr("scanResolutionMultiplier"),
                                  stackingPenalties=True, penaltyGroup="cloakingScanResolutionMultiplier")

    return locals()

def effect856():
    type = "passive"
    def handler(fit, container, context):
        penalized = False if "skill" in context or "implant" in context else True
        fit.ship.boostItemAttr("baseWarpSpeed", container.getModifiedItemAttr("WarpSBonus"),
                               stackingPenalties=penalized)

    return locals()

def effect874():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")

    return locals()

def effect882():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")

    return locals()

def effect887():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")

    return locals()

def effect889():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect89():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect891():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")

    return locals()

def effect892():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                        "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")

    return locals()

def effect896():
    type = "passive"
    def handler(fit, container, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Cloaking Device",
                                         "cpu", container.getModifiedItemAttr("cloakingCpuNeedBonus"))

    return locals()

def effect898():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")

    return locals()

def effect899():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "kineticDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")

    return locals()

def effect900():
    type = "passive"
    def handler(fit, ship, context):
        fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Light Drone Operation"),
                                     "thermalDamage", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")

    return locals()

def effect907():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                      "speed", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect909():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect91():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect912():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                      "speed", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")

    return locals()

def effect918():
    type = "passive"
    def handler(fit, ship, context):
        fit.extraAttributes.increase("maxActiveDrones", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect919():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")

    return locals()

def effect92():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect93():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                         "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect95():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect958():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")

    return locals()

def effect959():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusAC2"),
                               skill="Amarr Cruiser")

    return locals()

def effect96():
    type = "passive"
    def handler(fit, module, context):
        fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                         "speed", module.getModifiedItemAttr("speedMultiplier"),
                                         stackingPenalties=True)

    return locals()

def effect960():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusAC2"),
                               skill="Amarr Cruiser")

    return locals()

def effect961():
    type = "passive"
    def handler(fit, ship, context):
        fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusAC2"),
                               skill="Amarr Cruiser")

    return locals()

def effect968():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                      "damageMultiplier", ship.getModifiedItemAttr("shipBonusMC2"),
                                      skill="Minmatar Cruiser")

    return locals()

def effect980():
    type = "active"
    runTime = "early"
    def handler(fit, ship, context):
        fit.extraAttributes["cloaked"] = True

    return locals()

def effect989():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect991():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                      "maxRange", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")

    return locals()

def effect996():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                      "trackingSpeed", ship.getModifiedItemAttr("eliteBonusGunship2"),
                                      skill="Assault Frigates")

    return locals()

def effect998():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                      "falloff", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")

    return locals()

def effect999():
    type = "passive"
    def handler(fit, ship, context):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                      "shieldBonus", ship.getModifiedItemAttr("eliteBonusGunship2"),
                                      skill="Assault Frigates")

    return locals()

