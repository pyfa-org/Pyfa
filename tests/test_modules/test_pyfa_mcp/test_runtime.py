from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(REPO_ROOT))

from pyfa_mcp.runtime import RuntimeConfig, initialize_runtime, reset_runtime_for_tests  # noqa: E402


@pytest.fixture()
def runtime(tmp_path):
    game_db = REPO_ROOT / "eve.db"
    if not game_db.exists():
        pytest.skip("eve.db is required for Pyfa MCP tests. Generate it with `python3 db_update.py` first.")

    reset_runtime_for_tests()
    runtime = initialize_runtime(
        RuntimeConfig.defaults(
            repo_root=REPO_ROOT,
            game_db=game_db,
            savedata_db=tmp_path / "saveddata.db",
        )
    )
    yield runtime
    reset_runtime_for_tests()


def test_initialize_runtime_requires_gamedata_db(tmp_path):
    reset_runtime_for_tests()
    with pytest.raises(FileNotFoundError):
        initialize_runtime(
            RuntimeConfig.defaults(
                repo_root=REPO_ROOT,
                game_db=tmp_path / "missing.db",
                savedata_db=tmp_path / "saveddata.db",
            )
        )
    reset_runtime_for_tests()


def test_create_fit_and_list_fits(runtime):
    created = runtime.create_fit("Rifter", "MCP Rifter")

    assert created["fit"]["name"] == "MCP Rifter"
    assert created["fit"]["ship_name"] == "Rifter"
    assert created["stats"]["mobility"]["align_time"] is not None

    listing = runtime.list_fits(query="MCP Rifter")
    assert listing["count"] == 1
    assert listing["fits"][0]["id"] == created["fit"]["id"]


def test_get_fit_details_and_compare_fits(runtime):
    rifter = runtime.create_fit("Rifter", "MCP Rifter Compare")
    heron = runtime.create_fit("Heron", "MCP Heron Compare")

    rifter_details = runtime.get_fit_details(str(rifter["fit"]["id"]))
    comparison = runtime.compare_fits(rifter["fit"]["id"], heron["fit"]["id"])

    assert rifter_details["fit"]["ship_name"] == "Rifter"
    assert rifter_details["stats"]["damage"]["total_dps"]["total"] is not None
    assert comparison["fit_a"]["fit"]["id"] == rifter["fit"]["id"]
    assert comparison["fit_b"]["fit"]["id"] == heron["fit"]["id"]
    assert comparison["delta_b_minus_a"]["align_time"] is not None
