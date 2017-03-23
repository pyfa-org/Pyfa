# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
from _development.helpers_fits import RifterFit


# noinspection PyShadowingNames
def test_rifter_empty_char0(DB, Saveddata, RifterFit):
    """
    We test an empty ship because if we use this as a base for testing our V skills,
    and CCP ever fucks with the base states, all our derived stats will be wrong.
    """
    char0 = Saveddata['Character'].getAll0()

    RifterFit.character = char0
    RifterFit.calculateModifiedAttributes()

    assert RifterFit.ship.getModifiedItemAttr("agility") == 3.2
    assert RifterFit.ship.getModifiedItemAttr("armorEmDamageResonance") == 0.4
    assert RifterFit.ship.getModifiedItemAttr("armorExplosiveDamageResonance") == 0.9
    assert RifterFit.ship.getModifiedItemAttr("armorHP") == 450.0
    assert RifterFit.ship.getModifiedItemAttr("armorKineticDamageResonance") == 0.75
    assert RifterFit.ship.getModifiedItemAttr("armorThermalDamageResonance") == 0.65
    assert RifterFit.ship.getModifiedItemAttr("armorUniformity") == 0.75
    assert RifterFit.ship.getModifiedItemAttr("baseWarpSpeed") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("capacitorCapacity") == 250.0
    assert RifterFit.ship.getModifiedItemAttr("capacity") == 140.0
    assert RifterFit.ship.getModifiedItemAttr("cpuLoad") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("cpuOutput") == 130.0
    assert RifterFit.ship.getModifiedItemAttr("damage") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("droneBandwidth") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("droneCapacity") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("emDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("explosiveDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("fwLpKill") == 25.0
    assert RifterFit.ship.getModifiedItemAttr("gfxBoosterID") == 397.0
    assert RifterFit.ship.getModifiedItemAttr("heatAttenuationHi") == 0.63
    assert RifterFit.ship.getModifiedItemAttr("heatAttenuationLow") == 0.5
    assert RifterFit.ship.getModifiedItemAttr("heatAttenuationMed") == 0.5
    assert RifterFit.ship.getModifiedItemAttr("heatCapacityHi") == 100.0
    assert RifterFit.ship.getModifiedItemAttr("heatCapacityLow") == 100.0
    assert RifterFit.ship.getModifiedItemAttr("heatCapacityMed") == 100.0
    assert RifterFit.ship.getModifiedItemAttr("heatDissipationRateHi") == 0.01
    assert RifterFit.ship.getModifiedItemAttr("heatDissipationRateLow") == 0.01
    assert RifterFit.ship.getModifiedItemAttr("heatDissipationRateMed") == 0.01
    assert RifterFit.ship.getModifiedItemAttr("heatGenerationMultiplier") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hiSlots") == 4.0
    assert RifterFit.ship.getModifiedItemAttr("hp") == 350.0
    assert RifterFit.ship.getModifiedItemAttr("hullEmDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hullExplosiveDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hullKineticDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hullThermalDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("kineticDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("launcherSlotsLeft") == 2.0
    assert RifterFit.ship.getModifiedItemAttr("lowSlots") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("mainColor") == 16777215.0
    assert RifterFit.ship.getModifiedItemAttr("mass") == 1067000.0
    assert RifterFit.ship.getModifiedItemAttr("maxDirectionalVelocity") == 3000.0
    assert RifterFit.ship.getModifiedItemAttr("maxLockedTargets") == 4.0
    assert RifterFit.ship.getModifiedItemAttr("maxPassengers") == 2.0
    assert RifterFit.ship.getModifiedItemAttr("maxTargetRange") == 22500.0
    assert RifterFit.ship.getModifiedItemAttr("maxVelocity") == 365.0
    assert RifterFit.ship.getModifiedItemAttr("medSlots") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("metaLevel") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("minTargetVelDmgMultiplier") == 0.05
    assert RifterFit.ship.getModifiedItemAttr("powerLoad") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("powerOutput") == 41.0
    assert RifterFit.ship.getModifiedItemAttr("powerToSpeed") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("propulsionGraphicID") == 397.0
    assert RifterFit.ship.getModifiedItemAttr("radius") == 31.0
    assert RifterFit.ship.getModifiedItemAttr("rechargeRate") == 125000.0
    assert RifterFit.ship.getModifiedItemAttr("requiredSkill1") == 3329.0
    assert RifterFit.ship.getModifiedItemAttr("requiredSkill1Level") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("rigSize") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("rigSlots") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("scanGravimetricStrength") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("scanLadarStrength") == 8.0
    assert RifterFit.ship.getModifiedItemAttr("scanMagnetometricStrength") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("scanRadarStrength") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("scanResolution") == 660.0
    assert RifterFit.ship.getModifiedItemAttr("scanSpeed") == 1500.0
    assert RifterFit.ship.getModifiedItemAttr("shieldCapacity") == 450.0
    assert RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("shieldExplosiveDamageResonance") == 0.5
    assert RifterFit.ship.getModifiedItemAttr("shieldKineticDamageResonance") == 0.6
    assert RifterFit.ship.getModifiedItemAttr("shieldRechargeRate") == 625000.0
    assert RifterFit.ship.getModifiedItemAttr("shieldThermalDamageResonance") == 0.8
    assert RifterFit.ship.getModifiedItemAttr("shieldUniformity") == 0.75
    assert RifterFit.ship.getModifiedItemAttr("shipBonusMF") == 5.0
    assert RifterFit.ship.getModifiedItemAttr("shipBonusMF2") == 10.0
    assert RifterFit.ship.getModifiedItemAttr("shipScanResistance") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("signatureRadius") == 35.0
    assert RifterFit.ship.getModifiedItemAttr("structureUniformity") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("techLevel") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("thermalDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("turretSlotsLeft") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("typeColorScheme") == 11342.0
    assert RifterFit.ship.getModifiedItemAttr("uniformity") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("upgradeCapacity") == 400.0
    assert RifterFit.ship.getModifiedItemAttr("upgradeSlotsLeft") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("volume") == 27289.0
    assert RifterFit.ship.getModifiedItemAttr("warpCapacitorNeed") == 2.24e-06
    assert RifterFit.ship.getModifiedItemAttr("warpFactor") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("warpSpeedMultiplier") == 5.0


# noinspection PyShadowingNames
def test_rifter_empty_char5(DB, Saveddata, RifterFit):
    """
    Test char skills applying to a ship
    """
    char5 = Saveddata['Character'].getAll5()

    RifterFit.character = char5
    RifterFit.calculateModifiedAttributes()

    assert RifterFit.ship.getModifiedItemAttr("agility") == 2.16
    assert RifterFit.ship.getModifiedItemAttr("armorEmDamageResonance") == 0.4
    assert RifterFit.ship.getModifiedItemAttr("armorExplosiveDamageResonance") == 0.9
    assert RifterFit.ship.getModifiedItemAttr("armorHP") == 562.5
    assert RifterFit.ship.getModifiedItemAttr("armorKineticDamageResonance") == 0.75
    assert RifterFit.ship.getModifiedItemAttr("armorThermalDamageResonance") == 0.65
    assert RifterFit.ship.getModifiedItemAttr("armorUniformity") == 0.75
    assert RifterFit.ship.getModifiedItemAttr("baseWarpSpeed") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("capacitorCapacity") == 312.5
    assert RifterFit.ship.getModifiedItemAttr("capacity") == 140.0
    assert RifterFit.ship.getModifiedItemAttr("cpuLoad") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("cpuOutput") == 162.5
    assert RifterFit.ship.getModifiedItemAttr("damage") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("droneBandwidth") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("droneCapacity") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("emDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("explosiveDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("fwLpKill") == 25.0
    assert RifterFit.ship.getModifiedItemAttr("gfxBoosterID") == 397.0
    assert RifterFit.ship.getModifiedItemAttr("heatAttenuationHi") == 0.63
    assert RifterFit.ship.getModifiedItemAttr("heatAttenuationLow") == 0.5
    assert RifterFit.ship.getModifiedItemAttr("heatAttenuationMed") == 0.5
    assert RifterFit.ship.getModifiedItemAttr("heatCapacityHi") == 100.0
    assert RifterFit.ship.getModifiedItemAttr("heatCapacityLow") == 100.0
    assert RifterFit.ship.getModifiedItemAttr("heatCapacityMed") == 100.0
    assert RifterFit.ship.getModifiedItemAttr("heatDissipationRateHi") == 0.01
    assert RifterFit.ship.getModifiedItemAttr("heatDissipationRateLow") == 0.01
    assert RifterFit.ship.getModifiedItemAttr("heatDissipationRateMed") == 0.01
    assert RifterFit.ship.getModifiedItemAttr("heatGenerationMultiplier") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hiSlots") == 4.0
    assert RifterFit.ship.getModifiedItemAttr("hp") == 437.5
    assert RifterFit.ship.getModifiedItemAttr("hullEmDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hullExplosiveDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hullKineticDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("hullThermalDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("kineticDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("launcherSlotsLeft") == 2.0
    assert RifterFit.ship.getModifiedItemAttr("lowSlots") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("mainColor") == 16777215.0
    assert RifterFit.ship.getModifiedItemAttr("mass") == 1067000.0
    assert RifterFit.ship.getModifiedItemAttr("maxDirectionalVelocity") == 3000.0
    assert RifterFit.ship.getModifiedItemAttr("maxLockedTargets") == 4.0
    assert RifterFit.ship.getModifiedItemAttr("maxPassengers") == 2.0
    assert RifterFit.ship.getModifiedItemAttr("maxTargetRange") == 28125.0
    assert RifterFit.ship.getModifiedItemAttr("maxVelocity") == 456.25
    assert RifterFit.ship.getModifiedItemAttr("medSlots") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("metaLevel") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("minTargetVelDmgMultiplier") == 0.05
    assert RifterFit.ship.getModifiedItemAttr("powerLoad") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("powerOutput") == 51.25
    assert RifterFit.ship.getModifiedItemAttr("powerToSpeed") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("propulsionGraphicID") == 397.0
    assert RifterFit.ship.getModifiedItemAttr("radius") == 31.0
    assert RifterFit.ship.getModifiedItemAttr("rechargeRate") == 93750.0
    assert RifterFit.ship.getModifiedItemAttr("requiredSkill1") == 3329.0
    assert RifterFit.ship.getModifiedItemAttr("requiredSkill1Level") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("rigSize") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("rigSlots") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("scanGravimetricStrength") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("scanLadarStrength") == 9.6
    assert RifterFit.ship.getModifiedItemAttr("scanMagnetometricStrength") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("scanRadarStrength") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("scanResolution") == 825.0
    assert RifterFit.ship.getModifiedItemAttr("scanSpeed") == 1500.0
    assert RifterFit.ship.getModifiedItemAttr("shieldCapacity") == 562.5
    assert RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("shieldExplosiveDamageResonance") == 0.5
    assert RifterFit.ship.getModifiedItemAttr("shieldKineticDamageResonance") == 0.6
    assert RifterFit.ship.getModifiedItemAttr("shieldRechargeRate") == 468750.0
    assert RifterFit.ship.getModifiedItemAttr("shieldThermalDamageResonance") == 0.8
    assert RifterFit.ship.getModifiedItemAttr("shieldUniformity") == 1
    assert RifterFit.ship.getModifiedItemAttr("shipBonusMF") == 5.0
    assert RifterFit.ship.getModifiedItemAttr("shipBonusMF2") == 10.0
    assert RifterFit.ship.getModifiedItemAttr("shipScanResistance") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("signatureRadius") == 35.0
    assert RifterFit.ship.getModifiedItemAttr("structureUniformity") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("techLevel") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("thermalDamageResonance") == 0.67
    assert RifterFit.ship.getModifiedItemAttr("turretSlotsLeft") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("typeColorScheme") == 11342.0
    assert RifterFit.ship.getModifiedItemAttr("uniformity") == 1.0
    assert RifterFit.ship.getModifiedItemAttr("upgradeCapacity") == 400.0
    assert RifterFit.ship.getModifiedItemAttr("upgradeSlotsLeft") == 3.0
    assert RifterFit.ship.getModifiedItemAttr("volume") == 27289.0
    assert RifterFit.ship.getModifiedItemAttr("warpCapacitorNeed") == 1.12e-06
    assert RifterFit.ship.getModifiedItemAttr("warpFactor") == 0.0
    assert RifterFit.ship.getModifiedItemAttr("warpSpeedMultiplier") == 5.0


# noinspection PyShadowingNames
def test_rifter_coprocessor(DB, Saveddata, RifterFit):
    char5 = Saveddata['Character'].getAll5()
    char0 = Saveddata['Character'].getAll0()

    RifterFit.character = char0
    mod = Saveddata['Module'](DB['db'].getItem("Co-Processor II"))
    mod.state = Saveddata['State'].OFFLINE
    RifterFit.modules.append(mod)

    assert RifterFit.ship.getModifiedItemAttr("cpuOutput") == 130

    RifterFit.calculateModifiedAttributes()
    assert RifterFit.ship.getModifiedItemAttr("cpuOutput") == 130

    mod.state = Saveddata['State'].ONLINE
    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()
    assert RifterFit.ship.getModifiedItemAttr("cpuOutput") == 143

    RifterFit.character = char5
    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()
    assert RifterFit.ship.getModifiedItemAttr("cpuOutput") == 178.75
