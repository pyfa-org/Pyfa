from enum import Enum, auto


# Define the various groups of attributes
class AttrGroup(Enum):
    FITTING = auto()
    STRUCTURE = auto()
    SHIELD = auto()
    ARMOR = auto()
    TARGETING = auto()
    EWAR_RESISTS = auto()
    CAPACITOR = auto()
    SHARED_FACILITIES = auto()
    FIGHTER_FACILITIES = auto()
    ON_DEATH = auto()
    JUMP_SYSTEMS = auto()
    PROPULSIONS = auto()
    FIGHTERS = auto()


# todo: instead of defining the attribute grouping as "grouped attributes" vs "normal attributes",
# define the liast of grouped attributes outside. When iterating over attributes, can then find
# the first one and apply them all
RequiredSkillAttrs = sum((["requiredSkill{}".format(x), "requiredSkill{}Level".format(x)] for x in range(1, 7)), [])

#todo: maybe moved some of these basic definitions into eos proper? Can really be useful with effect writing as a lot of these are used over and over
damage_types = ["em", "thermal", "kinetic", "explosive"]
scan_types = ["radar", "magnetometric", "gravimetric", "ladar"]

DamageAttrs = ["{}Damage".format(x) for x in damage_types]
HullResistsAttrs = ["{}DamageResonance".format(x) for x in damage_types]
ArmorResistsAttrs = ["armor{}DamageResonance".format(x.capitalize()) for x in damage_types]
ShieldResistsAttrs = ["shield{}DamageResonance".format(x.capitalize()) for x in damage_types]
ScanStrAttrs = ["scan{}Strength".format(x.capitalize()) for x in scan_types]

# convert to named tuples
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

AttrGroupDict = {
    AttrGroup.FITTING           : {
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
    AttrGroup.STRUCTURE         : {
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
    AttrGroup.ARMOR             : {
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
    AttrGroup.SHIELD            : {
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
    AttrGroup.EWAR_RESISTS      : {
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
    AttrGroup.CAPACITOR         : {
        "label": "Capacitor",
        "attributes": [
            "capacitorCapacity",
            "rechargeRate",
        ]
    },
    AttrGroup.TARGETING         : {
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
    AttrGroup.SHARED_FACILITIES : {
        "label" : "Shared Facilities",
        "attributes": [
            "fleetHangarCapacity",
            "shipMaintenanceBayCapacity",
            "maxJumpClones",
        ]
    },
    AttrGroup.FIGHTER_FACILITIES: {
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
    AttrGroup.ON_DEATH          : {
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
    AttrGroup.JUMP_SYSTEMS      : {
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
    AttrGroup.PROPULSIONS       : {
        "label": "Propulsion",
        "attributes": [
            "maxVelocity"
        ]
    },
    AttrGroup.FIGHTERS          : {
        "label": "Fighters",
        "attributes": [
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
    AttrGroup.FITTING,
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
