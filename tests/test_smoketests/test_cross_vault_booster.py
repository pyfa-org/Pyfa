"""
Smoketest: combat ship in one vault receives boost from a booster ship in another vault.

Verifies that boost calculation is vault-agnostic: when the booster fit lives in vault A
and the combat fit in vault B, linking them and recalculating the combat fit should
apply command bonuses correctly (commandBonuses populated).
"""
import pytest

# No GUI imports - use eos.db and fixtures only so test runs without gui.mainFrame/Market


def _make_booster_fit(DB, Gamedata, Saveddata):
    """Build a minimal booster fit: command destroyer + Shield Command Burst I."""
    ship_item = DB["gamedata_session"].query(Gamedata["Item"]).filter(
        Gamedata["Item"].name == "Stork"
    ).first()
    if ship_item is None:
        return None
    burst_item = DB["db"].getItem("Shield Command Burst I")
    if burst_item is None:
        return None
    # Command burst must have a charge loaded to apply any bonus (warfareBuffID comes from charge)
    charge_item = DB["db"].getItem("Shield Harmonizing Charge I")
    if charge_item is None:
        return None
    ship = Saveddata["Ship"](ship_item)
    fit = Saveddata["Fit"](ship, "Booster Stork")
    fit.booster = True
    fit.implantLocation = 0  # FIT; required for fits table NOT NULL
    mod = Saveddata["Module"](burst_item)
    mod.state = Saveddata["State"].ONLINE
    mod.charge = charge_item
    fit.modules.append(mod)
    return fit


def test_cross_vault_booster_combat_ship_gets_boost_calculated(DB, Gamedata, Saveddata, RifterFit):
    """
    Booster in vault A, combat ship in vault B: link them and assert combat fit
    receives command bonuses after recalc (boost calculated correctly).
    """
    eos_db = DB["db"]

    # Create booster fit (may be None if gamedata lacks Stork / Shield Command Burst I)
    booster_fit = _make_booster_fit(DB, Gamedata, Saveddata)
    if booster_fit is None:
        pytest.skip("Gamedata missing Stork, Shield Command Burst I, or Shield Harmonizing Charge I")

    combat_fit = RifterFit
    combat_fit.implantLocation = 0  # FIT; required for fits table NOT NULL

    # Save both fits so they get IDs
    eos_db.save(booster_fit)
    eos_db.save(combat_fit)
    booster_id = booster_fit.ID
    combat_id = combat_fit.ID

    existing_vaults = eos_db.getVaultList()
    default_vault_id = existing_vaults[0].ID if existing_vaults else None

    vault_a_id = eos_db.createVault("VaultA")
    vault_b_id = eos_db.createVault("VaultB")

    try:
        # Assign booster to vault A, combat to vault B
        eos_db.moveFitToVault(booster_fit.ID, vault_a_id)
        eos_db.moveFitToVault(combat_fit.ID, vault_b_id)

        # Reload so vaultID is set on the instances
        combat_fit = eos_db.getFit(combat_fit.ID)
        booster_fit = eos_db.getFit(booster_fit.ID)

        # Link booster to combat (same as GUI add command fit)
        combat_fit.commandFitDict[booster_fit.ID] = booster_fit
        eos_db.saveddata_session.flush()
        eos_db.saveddata_session.refresh(booster_fit)

        # Booster must be calculated so its modules (and charge attributes) are ready
        booster_fit.calculateModifiedAttributes()
        # Recalc combat fit so command effects are applied from booster to combat
        combat_fit.clear()
        combat_fit.calculateModifiedAttributes()

        # Boost calculated correctly: combat ship should have command bonuses from the booster
        assert len(combat_fit.commandBonuses) > 0, (
            "Combat ship in vault B should receive boost from booster in vault A; commandBonuses was empty"
        )
    finally:
        # Cleanup: remove fits, then delete our vaults (need an existing vault as default)
        for fit_id in (combat_id, booster_id):
            fit = eos_db.getFit(fit_id)
            if fit is not None:
                eos_db.remove(fit)
        if default_vault_id is not None:
            eos_db.deleteVault(vault_a_id, default_vault_id)
            eos_db.deleteVault(vault_b_id, default_vault_id)
