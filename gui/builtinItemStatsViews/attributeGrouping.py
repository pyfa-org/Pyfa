from service.const import GuiAttrGroup

RequiredSkillAttrs = sum((["requiredSkill{}".format(x), "requiredSkill{}Level".format(x)] for x in range(1, 7)), [])

#todo: maybe moved some of these basic definitions into eos proper? Can really be useful with effect writing as a lot of these are used over and over
damage_types = ["em", "thermal", "kinetic", "explosive"]
scan_types = ["radar", "magnetometric", "gravimetric", "ladar"]

DamageAttrs = ["{}Damage".format(x) for x in damage_types]
HullResistsAttrs = ["{}DamageResonance".format(x) for x in damage_types]
ArmorResistsAttrs = ["armor{}DamageResonance".format(x.capitalize()) for x in damage_types]
ShieldResistsAttrs = ["shield{}DamageResonance".format(x.capitalize()) for x in damage_types]
ScanStrAttrs = ["scan{}Strength".format(x.capitalize()) for x in scan_types]

# todo: convert to named tuples?
AttrGroups = [
    (DamageAttrs, "Damage"),
    (HullResistsAttrs, "Resistances"),
    (ArmorResistsAttrs, "Resistances"),
    (ShieldResistsAttrs, "Resistances"),
    (ScanStrAttrs, "Sensor Strengths")
]

GroupedAttributes = []
for x in AttrGroups:
    GroupedAttributes += x[0]

# Start defining all the known attribute groups
AttrGroupDict = {
    GuiAttrGroup.FITTING           : {
        "label" : "Fitting",
        "attributes": [
            # parent-level attributes
            "cpuOutput",
            "powerOutput",
            "upgradeCapacity",
            "hiSlots",
            "medSlots",
            "lowSlots",
            "serviceSlots",
            "turretSlotsLeft",
            "launcherSlotsLeft",
            "upgradeSlotsLeft",
            # child-level attributes
            "cpu",
            "power",
            "rigSize",
            "upgradeCost",
            # "mass",
        ]
    },
    GuiAttrGroup.STRUCTURE         : {
        "label" : "Structure",
        "attributes": [
            "hp",
            "capacity",
            "mass",
            "volume",
            "agility",
            "droneCapacity",
            "droneBandwidth",
            "generalMiningHoldCapacity",
            "specialIceHoldCapacity",
            "specialGasHoldCapacity",
            "specialMineralHoldCapacity",
            "specialSalvageHoldCapacity",
            "specialShipHoldCapacity",
            "specialSmallShipHoldCapacity",
            "specialMediumShipHoldCapacity",
            "specialLargeShipHoldCapacity",
            "specialIndustrialShipHoldCapacity",
            "specialAmmoHoldCapacity",
            "specialCommandCenterHoldCapacity",
            "specialPlanetaryCommoditiesHoldCapacity",
            "structureDamageLimit",
            "specialSubsystemHoldCapacity",
            "emDamageResonance",
            "thermalDamageResonance",
            "kineticDamageResonance",
            "explosiveDamageResonance"
        ]
    },
    GuiAttrGroup.ARMOR             : {
       "label": "Armor",
        "attributes":[
            "armorHP",
            "armorDamageLimit",
            "armorEmDamageResonance",
            "armorThermalDamageResonance",
            "armorKineticDamageResonance",
            "armorExplosiveDamageResonance",
        ]

    },
    GuiAttrGroup.SHIELD            : {
        "label": "Shield",
        "attributes": [
            "shieldCapacity",
            "shieldRechargeRate",
            "shieldDamageLimit",
            "shieldEmDamageResonance",
            "shieldExplosiveDamageResonance",
            "shieldKineticDamageResonance",
            "shieldThermalDamageResonance",
        ]

    },
    GuiAttrGroup.EWAR_RESISTS      : {
        "label": "Electronic Warfare",
        "attributes": [
            "ECMResistance",
            "remoteAssistanceImpedance",
            "remoteRepairImpedance",
            "energyWarfareResistance",
            "sensorDampenerResistance",
            "stasisWebifierResistance",
            "targetPainterResistance",
            "weaponDisruptionResistance",
        ]
    },
    GuiAttrGroup.CAPACITOR         : {
        "label": "Capacitor",
        "attributes": [
            "capacitorCapacity",
            "rechargeRate",
        ]
    },
    GuiAttrGroup.TARGETING         : {
        "label": "Targeting",
        "attributes": [
            "maxTargetRange",
            "maxRange",
            "maxLockedTargets",
            "signatureRadius",
            "optimalSigRadius",
            "scanResolution",
            "proximityRange",
            "falloff",
            "trackingSpeed",
            "scanRadarStrength",
            "scanMagnetometricStrength",
            "scanGravimetricStrength",
            "scanLadarStrength",
        ]
    },
    GuiAttrGroup.SHARED_FACILITIES : {
        "label" : "Shared Facilities",
        "attributes": [
            "fleetHangarCapacity",
            "shipMaintenanceBayCapacity",
            "maxJumpClones",
        ]
    },
    GuiAttrGroup.FIGHTER_FACILITIES: {
        "label": "Fighter Squadron Facilities",
        "attributes": [
            "fighterCapacity",
            "fighterTubes",
            "fighterLightSlots",
            "fighterSupportSlots",
            "fighterHeavySlots",
            "fighterStandupLightSlots",
            "fighterStandupSupportSlots",
            "fighterStandupHeavySlots",
        ]
    },
    GuiAttrGroup.ON_DEATH          : {
        "label": "On Death",
        "attributes": [
            "onDeathDamageEM",
            "onDeathDamageTherm",
            "onDeathDamageKin",
            "onDeathDamageExp",
            "onDeathAOERadius",
            "onDeathSignatureRadius",
        ]
    },
    GuiAttrGroup.JUMP_SYSTEMS      : {
        "label": "Jump Drive Systems",
        "attributes": [
            "jumpDriveCapacitorNeed",
            "jumpDriveRange",
            "jumpDriveConsumptionType",
            "jumpDriveConsumptionAmount",
            "jumpPortalCapacitorNeed",
            "jumpDriveDuration",
            "specialFuelBayCapacity",
            "jumpPortalConsumptionMassFactor",
            "jumpPortalDuration",
        ]
    },
    GuiAttrGroup.PROPULSIONS       : {
        "label": "Propulsion",
        "attributes": [
            "maxVelocity"
        ]
    },
    GuiAttrGroup.FIGHTERS          : {
        "label": "Fighter",
        "attributes": [
            "mass",
            "maxVelocity",
            "agility",
            "volume",
            "signatureRadius",
            "fighterSquadronMaxSize",
            "fighterRefuelingTime",
            "fighterSquadronOrbitRange",
        ]
    },
    GuiAttrGroup.SHIP_GROUP           : {
        "label" : "Can Fit To",
        "attributes": []
    },
}

AttrGroupDict[GuiAttrGroup.SHIP_GROUP]["attributes"].extend([("canFitShipGroup{:02d}".format(i+1), "Group") for i in range(20)])
AttrGroupDict[GuiAttrGroup.SHIP_GROUP]["attributes"].extend([("canFitShipType{:01d}".format(i+1), "Ship") for i in range(20)])

Group1 = [
    GuiAttrGroup.FITTING,
    GuiAttrGroup.STRUCTURE,
    GuiAttrGroup.ARMOR,
    GuiAttrGroup.SHIELD,
    GuiAttrGroup.EWAR_RESISTS,
    GuiAttrGroup.CAPACITOR,
    GuiAttrGroup.TARGETING,
    GuiAttrGroup.SHARED_FACILITIES,
    GuiAttrGroup.FIGHTER_FACILITIES,
    GuiAttrGroup.ON_DEATH,
    GuiAttrGroup.JUMP_SYSTEMS,
    GuiAttrGroup.PROPULSIONS,
    GuiAttrGroup.SHIP_GROUP
]

CategoryGroups = {
    "Fighter"  : [
        GuiAttrGroup.FIGHTERS,
        GuiAttrGroup.SHIELD,
        GuiAttrGroup.TARGETING,
    ],
    "Ship"     : Group1,
    "Drone"    : Group1,
    "Structure": Group1
}
