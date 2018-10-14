from enum import Enum


class AttrGroupingType(Enum):
    # These are self-explanatory
    LABEL = 0
    NORMAL = 1
    RESIST = 2
    SENSOR = 3


# Define the various groups of attributes
class AttrGroup(Enum):
    FITTING = 0
    STRUCTURE = 1
    SHIELD = 2
    ARMOR = 3
    TARGETING = 4
    EWAR_RESISTS = 5
    CAPACITOR = 6
    SHARED_FACILITIES = 7
    FIGHTER_FACILITIES = 8
    ON_DEATH = 9
    JUMP_SYSTEMS = 10
    PROPULSIONS = 11
    FIGHTERS = 12


RequiredSkillAttrs = sum((["requiredSkill{}".format(x), "requiredSkill{}Level".format(x)] for x in range(1, 7)), [])


AttrGroupDict = {
    AttrGroup.FITTING           : {
        AttrGroupingType.LABEL: "Fitting",
        AttrGroupingType.NORMAL: [
            "cpu",
            "power",
            "rigSize",
            "upgradeCost",
            "attributeMass", ]
    },
    AttrGroup.STRUCTURE         : {
        AttrGroupingType.LABEL: "Structure",
        AttrGroupingType.NORMAL: [
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
        ],
        AttrGroupingType.RESIST: [
            ("em", "emDamageResonance"),
            ("thermal", "thermalDamageResonance"),
            ("kinetic", "kineticDamageResonance"),
            ("explosive", "explosiveDamageResonance")
        ]
    },
    AttrGroup.ARMOR             : {
        AttrGroupingType.LABEL: "Armor",
        AttrGroupingType.NORMAL: [
            "armorHP",
            "armorDamageLimit"
        ],
        AttrGroupingType.RESIST: [
            ("em", "armorEmDamageResonance"),
            ("thermal", "armorThermalDamageResonance"),
            ("kinetic", "armorKineticDamageResonance"),
            ("explosive", "armorExplosiveDamageResonance")
        ]

    },
    AttrGroup.SHIELD            : {
        AttrGroupingType.LABEL: "Shield",
        AttrGroupingType.NORMAL: [
            "shieldCapacity",
            "shieldRechargeRate",
            "shieldDamageLimit"
        ],
        AttrGroupingType.RESIST: [
            ("em", "shieldEmDamageResonance"),
            ("thermal", "shieldExplosiveDamageResonance"),
            ("kinetic", "shieldKineticDamageResonance"),
            ("explosive", "shieldThermalDamageResonance")
        ]

    },
    AttrGroup.EWAR_RESISTS      : {
        AttrGroupingType.LABEL: "Electronic Warfare",
        AttrGroupingType.NORMAL: [
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
    AttrGroup.CAPACITOR         : {
        AttrGroupingType.LABEL: "Capacitor",
        AttrGroupingType.NORMAL: [
            "capacitorCapacity",
            "rechargeRate",
        ]
    },
    AttrGroup.TARGETING         : {
        AttrGroupingType.LABEL: "Targeting",
        AttrGroupingType.NORMAL: [
            "maxTargetRange",
            "maxRange",
            "maxLockedTargets",
            "signatureRadius",
            "optimalSigRadius",
            "scanResolution",
            "proximityRange",
            "falloff",
            "trackingSpeed",
        ],
        AttrGroupingType.SENSOR: [
            "scanLadarStrength",
            "scanMagnetometricStrength",
            "scanGravimetricStrength",
            "scanRadarStrength",
        ]
    },
    AttrGroup.SHARED_FACILITIES : {
        AttrGroupingType.LABEL: "Shared Facilities",
        AttrGroupingType.NORMAL: [
            "shipMaintenanceBayCapacity",
            "fleetHangarCapacity",
            "maxJumpClones",
        ]
    },
    AttrGroup.FIGHTER_FACILITIES: {
        AttrGroupingType.LABEL: "Fighter Squadron Facilities",
        AttrGroupingType.NORMAL: [
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
    AttrGroup.ON_DEATH          : {
        AttrGroupingType.LABEL: "On Death",
        AttrGroupingType.NORMAL: [
            "onDeathDamageEM",
            "onDeathDamageTherm",
            "onDeathDamageKin",
            "onDeathDamageExp",
            "onDeathAOERadius",
            "onDeathSignatureRadius",
        ]
    },
    AttrGroup.JUMP_SYSTEMS      : {
        AttrGroupingType.LABEL: "Jump Drive Systems",
        AttrGroupingType.NORMAL: [
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
    AttrGroup.PROPULSIONS       : {
        AttrGroupingType.LABEL: "Propulsion",
        AttrGroupingType.NORMAL: [
            "maxVelocity"
        ]
    },
    AttrGroup.FIGHTERS          : {
        AttrGroupingType.LABEL: "Fighters",
        AttrGroupingType.NORMAL: [
            "mass",
            "maxVelocity",
            "agility",
            "volume",
            "signatureRadius",
            "fighterSquadronMaxSize",
            "fighterSquadronOrbitRange",
            "fighterRefuelingTime",
        ]
    },
}

Group1 = [
    AttrGroup.STRUCTURE,
    AttrGroup.ARMOR,
    AttrGroup.SHIELD,
    AttrGroup.EWAR_RESISTS,
    AttrGroup.CAPACITOR,
    AttrGroup.TARGETING,
    AttrGroup.SHARED_FACILITIES,
    AttrGroup.FIGHTER_FACILITIES,
    AttrGroup.ON_DEATH,
    AttrGroup.JUMP_SYSTEMS,
    AttrGroup.PROPULSIONS,
]

CategoryGroups = {
    "Fighter"  : [
        AttrGroup.FIGHTERS,
        AttrGroup.SHIELD,
        AttrGroup.TARGETING,
    ],
    "Ship"     : Group1,
    "Drone"    : Group1,
    "Structure": Group1
}
