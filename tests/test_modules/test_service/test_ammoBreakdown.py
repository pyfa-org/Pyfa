# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))
sys._called_from_test = True  # need db open for tests (see eos/config.py)

# This import is here to hack around circular import issues
import pytest
import gui.mainFrame
# noinspection PyPackageRequirements
from eos.saveddata.cargo import Cargo
from service.ammoBreakdown import get_ammo_in_cargo_usable_by_weapons, get_ammo_breakdown


# noinspection PyShadowingNames
@pytest.fixture
def RifterWithProjectileAmmo():
    """Rifter fit with 200mm Autocannon IIs and projectile ammo (EMP S, Fusion S) in cargo."""
    from service.port import Port
    eft_lines = """[Rifter, Rifter - AC Test]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S

EMP S x500
Fusion S x500
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    return fit


# ---- get_ammo_in_cargo_usable_by_weapons ----

def test_get_ammo_in_cargo_usable_by_weapons_NoneFit():
    assert get_ammo_in_cargo_usable_by_weapons(None) == set()


def test_get_ammo_in_cargo_usable_by_weapons_EmptyCargo():
    from service.port import Port
    eft_lines = """[Rifter, Empty Rifter]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    fit.cargo.clear()  # Remove any cargo from imported fit
    assert get_ammo_in_cargo_usable_by_weapons(fit) == set()


def test_get_ammo_in_cargo_usable_by_weapons_NoWeapons():
    from service.port import Port
    eft_lines = """[Rifter, Rifter No Guns]

EMP S x500
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    fit.modules.clear()  # Remove any modules
    assert get_ammo_in_cargo_usable_by_weapons(fit) == set()


def test_get_ammo_in_cargo_usable_by_weapons_AmmoNotUsable():
    from service.port import Port
    import eos.db
    eft_lines = """[Rifter, Rifter Wrong Ammo]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S

Multifrequency S x100
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    # Replace cargo with only laser crystal (not usable by projectile guns)
    fit.cargo.clear()
    crystal = Cargo(eos.db.getItem("Multifrequency S"))
    crystal.amount = 100
    fit.cargo.append(crystal)
    assert get_ammo_in_cargo_usable_by_weapons(fit) == set()


def test_imported_fit_has_modules_and_cargo():
    """Sanity check: EFT import produces fit with both modules and cargo."""
    from service.port import Port
    eft_lines = """[Rifter, Rifter Single Ammo]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S

EMP S x500
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    assert len(fit.modules) >= 1
    assert len(fit.cargo) >= 1


def test_get_ammo_in_cargo_usable_by_weapons_SingleAmmoUsable():
    from service.port import Port
    eft_lines = """[Rifter, Rifter Single Ammo]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S

EMP S x500
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    usable = get_ammo_in_cargo_usable_by_weapons(fit)
    assert len(usable) >= 1
    names = {c.name for c in usable}
    assert "EMP S" in names


def test_get_ammo_in_cargo_usable_by_weapons_MultipleAmmoUsable(RifterWithProjectileAmmo):
    fit = RifterWithProjectileAmmo
    usable = get_ammo_in_cargo_usable_by_weapons(fit)
    names = {c.name for c in usable}
    assert "EMP S" in names
    assert "Fusion S" in names
    assert len(usable) >= 2


# ---- get_ammo_breakdown ----

def test_get_ammo_breakdown_NoneFit():
    assert get_ammo_breakdown(None) == []


def test_get_ammo_breakdown_NoUsableAmmo():
    from service.port import Port
    eft_lines = """[Rifter, Rifter No Cargo]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    fit.cargo.clear()
    assert get_ammo_breakdown(fit) == []


def test_get_ammo_breakdown_SingleAmmo():
    from service.port import Port
    eft_lines = """[Rifter, Rifter Single Ammo]
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S
200mm Autocannon II, EMP S

EMP S x500
"""
    fit = Port.importEft(eft_lines.splitlines())
    assert fit is not None
    result = get_ammo_breakdown(fit)
    assert len(result) == 1
    row = result[0]
    assert row['ammoName'] == "EMP S"
    assert 'damageType' in row
    assert 'optimal' in row
    assert 'falloff' in row
    assert isinstance(row['alpha'], (int, float))
    assert isinstance(row['dps'], (int, float))


def test_get_ammo_breakdown_ResultSortedByName(RifterWithProjectileAmmo):
    result = get_ammo_breakdown(RifterWithProjectileAmmo)
    assert len(result) >= 2
    names = [r['ammoName'] for r in result]
    assert names == sorted(names)


def test_get_ammo_breakdown_ResultStructure(RifterWithProjectileAmmo):
    result = get_ammo_breakdown(RifterWithProjectileAmmo)
    assert len(result) >= 1
    required_keys = {'ammoName', 'damageType', 'optimal', 'falloff', 'alpha', 'dps'}
    for row in result:
        assert required_keys.issubset(row.keys())
        assert isinstance(row['ammoName'], str)
        assert isinstance(row['damageType'], str)
        assert isinstance(row['optimal'], str)
        assert isinstance(row['falloff'], str)
        assert isinstance(row['alpha'], (int, float))
        assert isinstance(row['dps'], (int, float))


def test_get_ammo_breakdown_DamageTypeFormat(RifterWithProjectileAmmo):
    result = get_ammo_breakdown(RifterWithProjectileAmmo)
    for row in result:
        dt = row['damageType']
        assert dt in ("EM", "Thermal", "Kinetic", "Explosive", "—") or " / " in dt


def test_get_ammo_breakdown_OptimalFalloffFormat(RifterWithProjectileAmmo):
    result = get_ammo_breakdown(RifterWithProjectileAmmo)
    for row in result:
        assert "km" in row['optimal'] or row['optimal'] == "—"
        assert "km" in row['falloff'] or row['falloff'] == "—"
