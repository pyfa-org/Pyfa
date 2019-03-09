from eos.const import FittingAttrGroup

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
    FittingAttrGroup.FITTING           : {
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
    FittingAttrGroup.STRUCTURE         : {
        "label" : "Structure",
        "attributes": [
            "hp",
            "capacity",
            "mass",
            "volume",
            "agility",
            "droneCapacity",
            "droneBandwidth",
            "specialOreHoldCapacity",
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
    FittingAttrGroup.ARMOR             : {
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
    FittingAttrGroup.SHIELD            : {
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
    FittingAttrGroup.EWAR_RESISTS      : {
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
    FittingAttrGroup.CAPACITOR         : {
        "label": "Capacitor",
        "attributes": [
            "capacitorCapacity",
            "rechargeRate",
        ]
    },
    FittingAttrGroup.TARGETING         : {
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
    FittingAttrGroup.SHARED_FACILITIES : {
        "label" : "Shared Facilities",
        "attributes": [
            "fleetHangarCapacity",
            "shipMaintenanceBayCapacity",
            "maxJumpClones",
        ]
    },
    FittingAttrGroup.FIGHTER_FACILITIES: {
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
    FittingAttrGroup.ON_DEATH          : {
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
    FittingAttrGroup.JUMP_SYSTEMS      : {
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
    FittingAttrGroup.PROPULSIONS       : {
        "label": "Propulsion",
        "attributes": [
            "maxVelocity"
        ]
    },
    FittingAttrGroup.FIGHTERS          : {
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
}

Group1 = [
    FittingAttrGroup.FITTING,
    FittingAttrGroup.STRUCTURE,
    FittingAttrGroup.ARMOR,
    FittingAttrGroup.SHIELD,
    FittingAttrGroup.EWAR_RESISTS,
    FittingAttrGroup.CAPACITOR,
    FittingAttrGroup.TARGETING,
    FittingAttrGroup.SHARED_FACILITIES,
    FittingAttrGroup.FIGHTER_FACILITIES,
    FittingAttrGroup.ON_DEATH,
    FittingAttrGroup.JUMP_SYSTEMS,
    FittingAttrGroup.PROPULSIONS,
]

CategoryGroups = {
    "Fighter"  : [
        FittingAttrGroup.FIGHTERS,
        FittingAttrGroup.SHIELD,
        FittingAttrGroup.TARGETING,
    ],
    "Ship"     : Group1,
    "Drone"    : Group1,
    "Structure": Group1
}
