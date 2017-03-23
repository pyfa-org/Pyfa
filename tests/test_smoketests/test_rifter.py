# noinspection PyPackageRequirements

import pytest

from _development.helpers import DBInMemory as DB, Gamedata, Saveddata


# noinspection PyShadowingNames
@pytest.fixture
def Rifter(DB, Gamedata, Saveddata):
    print("Creating Rifter")
    print(DB['db'].gamedata_session.bind)
    print(DB['db'].saveddata_session.bind)
    item = DB['db'].gamedata_session.query(Gamedata['Item']).filter(Gamedata['Item'].name == "Rifter").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "My Rifter Fit")

    return fit


# noinspection PyShadowingNames
def test_rifter_empty_char0(DB, Saveddata, Rifter):
    """
    We test an empty ship because if we use this as a base for testing our V skills,
    and CCP ever fucks we the base states, all our derived stats will be wrong.
    """
    char0 = Saveddata['Character'].getAll0()

    Rifter.character = char0
    Rifter.calculateModifiedAttributes()

    assert Rifter.ship.getModifiedItemAttr("agility") == 3.2
    assert Rifter.ship.getModifiedItemAttr("armorEmDamageResonance") == 0.4
    assert Rifter.ship.getModifiedItemAttr("armorExplosiveDamageResonance") == 0.9
    assert Rifter.ship.getModifiedItemAttr("armorHP") == 450.0
    assert Rifter.ship.getModifiedItemAttr("armorKineticDamageResonance") == 0.75
    assert Rifter.ship.getModifiedItemAttr("armorThermalDamageResonance") == 0.65
    assert Rifter.ship.getModifiedItemAttr("armorUniformity") == 0.75
    assert Rifter.ship.getModifiedItemAttr("baseWarpSpeed") == 1.0
    assert Rifter.ship.getModifiedItemAttr("capacitorCapacity") == 250.0
    assert Rifter.ship.getModifiedItemAttr("capacity") == 140.0
    assert Rifter.ship.getModifiedItemAttr("cpuLoad") == 0.0
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 130.0
    assert Rifter.ship.getModifiedItemAttr("damage") == 0.0
    assert Rifter.ship.getModifiedItemAttr("droneBandwidth") == 0.0
    assert Rifter.ship.getModifiedItemAttr("droneCapacity") == 0.0
    assert Rifter.ship.getModifiedItemAttr("emDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("explosiveDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("fwLpKill") == 25.0
    assert Rifter.ship.getModifiedItemAttr("gfxBoosterID") == 397.0
    assert Rifter.ship.getModifiedItemAttr("heatAttenuationHi") == 0.63
    assert Rifter.ship.getModifiedItemAttr("heatAttenuationLow") == 0.5
    assert Rifter.ship.getModifiedItemAttr("heatAttenuationMed") == 0.5
    assert Rifter.ship.getModifiedItemAttr("heatCapacityHi") == 100.0
    assert Rifter.ship.getModifiedItemAttr("heatCapacityLow") == 100.0
    assert Rifter.ship.getModifiedItemAttr("heatCapacityMed") == 100.0
    assert Rifter.ship.getModifiedItemAttr("heatDissipationRateHi") == 0.01
    assert Rifter.ship.getModifiedItemAttr("heatDissipationRateLow") == 0.01
    assert Rifter.ship.getModifiedItemAttr("heatDissipationRateMed") == 0.01
    assert Rifter.ship.getModifiedItemAttr("heatGenerationMultiplier") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hiSlots") == 4.0
    assert Rifter.ship.getModifiedItemAttr("hp") == 350.0
    assert Rifter.ship.getModifiedItemAttr("hullEmDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hullExplosiveDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hullKineticDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hullThermalDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("kineticDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("launcherSlotsLeft") == 2.0
    assert Rifter.ship.getModifiedItemAttr("lowSlots") == 3.0
    assert Rifter.ship.getModifiedItemAttr("mainColor") == 16777215.0
    assert Rifter.ship.getModifiedItemAttr("mass") == 1067000.0
    assert Rifter.ship.getModifiedItemAttr("maxDirectionalVelocity") == 3000.0
    assert Rifter.ship.getModifiedItemAttr("maxLockedTargets") == 4.0
    assert Rifter.ship.getModifiedItemAttr("maxPassengers") == 2.0
    assert Rifter.ship.getModifiedItemAttr("maxTargetRange") == 22500.0
    assert Rifter.ship.getModifiedItemAttr("maxVelocity") == 365.0
    assert Rifter.ship.getModifiedItemAttr("medSlots") == 3.0
    assert Rifter.ship.getModifiedItemAttr("metaLevel") == 0.0
    assert Rifter.ship.getModifiedItemAttr("minTargetVelDmgMultiplier") == 0.05
    assert Rifter.ship.getModifiedItemAttr("powerLoad") == 0.0
    assert Rifter.ship.getModifiedItemAttr("powerOutput") == 41.0
    assert Rifter.ship.getModifiedItemAttr("powerToSpeed") == 1.0
    assert Rifter.ship.getModifiedItemAttr("propulsionGraphicID") == 397.0
    assert Rifter.ship.getModifiedItemAttr("radius") == 31.0
    assert Rifter.ship.getModifiedItemAttr("rechargeRate") == 125000.0
    assert Rifter.ship.getModifiedItemAttr("requiredSkill1") == 3329.0
    assert Rifter.ship.getModifiedItemAttr("requiredSkill1Level") == 1.0
    assert Rifter.ship.getModifiedItemAttr("rigSize") == 1.0
    assert Rifter.ship.getModifiedItemAttr("rigSlots") == 3.0
    assert Rifter.ship.getModifiedItemAttr("scanGravimetricStrength") == 0.0
    assert Rifter.ship.getModifiedItemAttr("scanLadarStrength") == 8.0
    assert Rifter.ship.getModifiedItemAttr("scanMagnetometricStrength") == 0.0
    assert Rifter.ship.getModifiedItemAttr("scanRadarStrength") == 0.0
    assert Rifter.ship.getModifiedItemAttr("scanResolution") == 660.0
    assert Rifter.ship.getModifiedItemAttr("scanSpeed") == 1500.0
    assert Rifter.ship.getModifiedItemAttr("shieldCapacity") == 450.0
    assert Rifter.ship.getModifiedItemAttr("shieldEmDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("shieldExplosiveDamageResonance") == 0.5
    assert Rifter.ship.getModifiedItemAttr("shieldKineticDamageResonance") == 0.6
    assert Rifter.ship.getModifiedItemAttr("shieldRechargeRate") == 625000.0
    assert Rifter.ship.getModifiedItemAttr("shieldThermalDamageResonance") == 0.8
    assert Rifter.ship.getModifiedItemAttr("shieldUniformity") == 0.75
    assert Rifter.ship.getModifiedItemAttr("shipBonusMF") == 5.0
    assert Rifter.ship.getModifiedItemAttr("shipBonusMF2") == 10.0
    assert Rifter.ship.getModifiedItemAttr("shipScanResistance") == 0.0
    assert Rifter.ship.getModifiedItemAttr("signatureRadius") == 35.0
    assert Rifter.ship.getModifiedItemAttr("structureUniformity") == 1.0
    assert Rifter.ship.getModifiedItemAttr("techLevel") == 1.0
    assert Rifter.ship.getModifiedItemAttr("thermalDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("turretSlotsLeft") == 3.0
    assert Rifter.ship.getModifiedItemAttr("typeColorScheme") == 11342.0
    assert Rifter.ship.getModifiedItemAttr("uniformity") == 1.0
    assert Rifter.ship.getModifiedItemAttr("upgradeCapacity") == 400.0
    assert Rifter.ship.getModifiedItemAttr("upgradeSlotsLeft") == 3.0
    assert Rifter.ship.getModifiedItemAttr("volume") == 27289.0
    assert Rifter.ship.getModifiedItemAttr("warpCapacitorNeed") == 2.24e-06
    assert Rifter.ship.getModifiedItemAttr("warpFactor") == 0.0
    assert Rifter.ship.getModifiedItemAttr("warpSpeedMultiplier") == 5.0


# noinspection PyShadowingNames
def test_rifter_empty_char5(DB, Saveddata, Rifter):
    """
    Test char skills applying to a ship
    """
    char5 = Saveddata['Character'].getAll5()

    Rifter.character = char5
    Rifter.calculateModifiedAttributes()

    assert Rifter.ship.getModifiedItemAttr("agility") == 2.16
    assert Rifter.ship.getModifiedItemAttr("armorEmDamageResonance") == 0.4
    assert Rifter.ship.getModifiedItemAttr("armorExplosiveDamageResonance") == 0.9
    assert Rifter.ship.getModifiedItemAttr("armorHP") == 562.5
    assert Rifter.ship.getModifiedItemAttr("armorKineticDamageResonance") == 0.75
    assert Rifter.ship.getModifiedItemAttr("armorThermalDamageResonance") == 0.65
    assert Rifter.ship.getModifiedItemAttr("armorUniformity") == 0.75
    assert Rifter.ship.getModifiedItemAttr("baseWarpSpeed") == 1.0
    assert Rifter.ship.getModifiedItemAttr("capacitorCapacity") == 312.5
    assert Rifter.ship.getModifiedItemAttr("capacity") == 140.0
    assert Rifter.ship.getModifiedItemAttr("cpuLoad") == 0.0
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 162.5
    assert Rifter.ship.getModifiedItemAttr("damage") == 0.0
    assert Rifter.ship.getModifiedItemAttr("droneBandwidth") == 0.0
    assert Rifter.ship.getModifiedItemAttr("droneCapacity") == 0.0
    assert Rifter.ship.getModifiedItemAttr("emDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("explosiveDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("fwLpKill") == 25.0
    assert Rifter.ship.getModifiedItemAttr("gfxBoosterID") == 397.0
    assert Rifter.ship.getModifiedItemAttr("heatAttenuationHi") == 0.63
    assert Rifter.ship.getModifiedItemAttr("heatAttenuationLow") == 0.5
    assert Rifter.ship.getModifiedItemAttr("heatAttenuationMed") == 0.5
    assert Rifter.ship.getModifiedItemAttr("heatCapacityHi") == 100.0
    assert Rifter.ship.getModifiedItemAttr("heatCapacityLow") == 100.0
    assert Rifter.ship.getModifiedItemAttr("heatCapacityMed") == 100.0
    assert Rifter.ship.getModifiedItemAttr("heatDissipationRateHi") == 0.01
    assert Rifter.ship.getModifiedItemAttr("heatDissipationRateLow") == 0.01
    assert Rifter.ship.getModifiedItemAttr("heatDissipationRateMed") == 0.01
    assert Rifter.ship.getModifiedItemAttr("heatGenerationMultiplier") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hiSlots") == 4.0
    assert Rifter.ship.getModifiedItemAttr("hp") == 437.5
    assert Rifter.ship.getModifiedItemAttr("hullEmDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hullExplosiveDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hullKineticDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("hullThermalDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("kineticDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("launcherSlotsLeft") == 2.0
    assert Rifter.ship.getModifiedItemAttr("lowSlots") == 3.0
    assert Rifter.ship.getModifiedItemAttr("mainColor") == 16777215.0
    assert Rifter.ship.getModifiedItemAttr("mass") == 1067000.0
    assert Rifter.ship.getModifiedItemAttr("maxDirectionalVelocity") == 3000.0
    assert Rifter.ship.getModifiedItemAttr("maxLockedTargets") == 4.0
    assert Rifter.ship.getModifiedItemAttr("maxPassengers") == 2.0
    assert Rifter.ship.getModifiedItemAttr("maxTargetRange") == 28125.0
    assert Rifter.ship.getModifiedItemAttr("maxVelocity") == 456.25
    assert Rifter.ship.getModifiedItemAttr("medSlots") == 3.0
    assert Rifter.ship.getModifiedItemAttr("metaLevel") == 0.0
    assert Rifter.ship.getModifiedItemAttr("minTargetVelDmgMultiplier") == 0.05
    assert Rifter.ship.getModifiedItemAttr("powerLoad") == 0.0
    assert Rifter.ship.getModifiedItemAttr("powerOutput") == 51.25
    assert Rifter.ship.getModifiedItemAttr("powerToSpeed") == 1.0
    assert Rifter.ship.getModifiedItemAttr("propulsionGraphicID") == 397.0
    assert Rifter.ship.getModifiedItemAttr("radius") == 31.0
    assert Rifter.ship.getModifiedItemAttr("rechargeRate") == 93750.0
    assert Rifter.ship.getModifiedItemAttr("requiredSkill1") == 3329.0
    assert Rifter.ship.getModifiedItemAttr("requiredSkill1Level") == 1.0
    assert Rifter.ship.getModifiedItemAttr("rigSize") == 1.0
    assert Rifter.ship.getModifiedItemAttr("rigSlots") == 3.0
    assert Rifter.ship.getModifiedItemAttr("scanGravimetricStrength") == 0.0
    assert Rifter.ship.getModifiedItemAttr("scanLadarStrength") == 9.6
    assert Rifter.ship.getModifiedItemAttr("scanMagnetometricStrength") == 0.0
    assert Rifter.ship.getModifiedItemAttr("scanRadarStrength") == 0.0
    assert Rifter.ship.getModifiedItemAttr("scanResolution") == 825.0
    assert Rifter.ship.getModifiedItemAttr("scanSpeed") == 1500.0
    assert Rifter.ship.getModifiedItemAttr("shieldCapacity") == 562.5
    assert Rifter.ship.getModifiedItemAttr("shieldEmDamageResonance") == 1.0
    assert Rifter.ship.getModifiedItemAttr("shieldExplosiveDamageResonance") == 0.5
    assert Rifter.ship.getModifiedItemAttr("shieldKineticDamageResonance") == 0.6
    assert Rifter.ship.getModifiedItemAttr("shieldRechargeRate") == 468750.0
    assert Rifter.ship.getModifiedItemAttr("shieldThermalDamageResonance") == 0.8
    assert Rifter.ship.getModifiedItemAttr("shieldUniformity") == 1
    assert Rifter.ship.getModifiedItemAttr("shipBonusMF") == 5.0
    assert Rifter.ship.getModifiedItemAttr("shipBonusMF2") == 10.0
    assert Rifter.ship.getModifiedItemAttr("shipScanResistance") == 0.0
    assert Rifter.ship.getModifiedItemAttr("signatureRadius") == 35.0
    assert Rifter.ship.getModifiedItemAttr("structureUniformity") == 1.0
    assert Rifter.ship.getModifiedItemAttr("techLevel") == 1.0
    assert Rifter.ship.getModifiedItemAttr("thermalDamageResonance") == 0.67
    assert Rifter.ship.getModifiedItemAttr("turretSlotsLeft") == 3.0
    assert Rifter.ship.getModifiedItemAttr("typeColorScheme") == 11342.0
    assert Rifter.ship.getModifiedItemAttr("uniformity") == 1.0
    assert Rifter.ship.getModifiedItemAttr("upgradeCapacity") == 400.0
    assert Rifter.ship.getModifiedItemAttr("upgradeSlotsLeft") == 3.0
    assert Rifter.ship.getModifiedItemAttr("volume") == 27289.0
    assert Rifter.ship.getModifiedItemAttr("warpCapacitorNeed") == 1.12e-06
    assert Rifter.ship.getModifiedItemAttr("warpFactor") == 0.0
    assert Rifter.ship.getModifiedItemAttr("warpSpeedMultiplier") == 5.0


# noinspection PyShadowingNames
def test_rifter_coprocessor(DB, Saveddata, Rifter):
    char5 = Saveddata['Character'].getAll5()
    char0 = Saveddata['Character'].getAll0()

    Rifter.character = char0
    mod = Saveddata['Module'](DB['db'].getItem("Co-Processor II"))
    mod.state = Saveddata['State'].OFFLINE
    Rifter.modules.append(mod)

    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 130

    Rifter.calculateModifiedAttributes()
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 130

    mod.state = Saveddata['State'].ONLINE
    Rifter.clear()
    Rifter.calculateModifiedAttributes()
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 143

    Rifter.character = char5
    Rifter.clear()
    Rifter.calculateModifiedAttributes()
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 178.75
