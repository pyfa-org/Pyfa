from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import types
from typing import Any


class FitResolutionError(ValueError):
    pass


@dataclass(frozen=True)
class RuntimeConfig:
    repo_root: Path
    game_db: Path
    savedata_db: Path
    build_game_db_if_missing: bool = False

    @classmethod
    def defaults(
        cls,
        repo_root: str | Path | None = None,
        game_db: str | Path | None = None,
        savedata_db: str | Path | None = None,
        build_game_db_if_missing: bool = False,
    ) -> "RuntimeConfig":
        root = Path(repo_root or Path(__file__).resolve().parent.parent).resolve()
        return cls(
            repo_root=root,
            game_db=Path(game_db or (root / "eve.db")).expanduser().resolve(),
            savedata_db=Path(savedata_db or (Path.home() / ".pyfa" / "saveddata.db")).expanduser().resolve(),
            build_game_db_if_missing=build_game_db_if_missing,
        )


_runtime_lock = threading.RLock()
_runtime: "PyfaRuntime | None" = None


class PyfaRuntime:
    def __init__(
        self,
        config: RuntimeConfig,
        eos_db: Any,
        item_cls: Any,
        fit_cls: Any,
        ship_cls: Any,
        citadel_cls: Any,
        character_cls: Any,
        damage_pattern_cls: Any,
        implant_location: Any,
    ):
        self.config = config
        self.db = eos_db
        self.item_cls = item_cls
        self.fit_cls = fit_cls
        self.ship_cls = ship_cls
        self.citadel_cls = citadel_cls
        self.character_cls = character_cls
        self.damage_pattern_cls = damage_pattern_cls
        self.implant_location = implant_location
        self.lock = threading.RLock()

    def list_fits(self, query: str | None = None) -> dict[str, Any]:
        query_normalized = query.lower().strip() if query else None
        with self.lock:
            fits = []
            for fit in self.db.getFitList():
                if query_normalized is not None:
                    haystack = " ".join((fit.name, fit.ship.item.typeName, fit.ship.item.group.name)).lower()
                    if query_normalized not in haystack:
                        continue
                fits.append(self._serialize_fit_reference(fit))
            fits.sort(key=lambda item: (item["ship_name"], item["name"], item["id"]))
            return {"fits": fits, "count": len(fits)}

    def get_fit_details(self, identifier: int | str) -> dict[str, Any]:
        with self.lock:
            fit = self._resolve_fit(identifier)
            return self._serialize_fit(fit)

    def compare_fits(self, fit_a: int | str, fit_b: int | str) -> dict[str, Any]:
        with self.lock:
            resolved_a = self._resolve_fit(fit_a)
            resolved_b = self._resolve_fit(fit_b)
            serialized_a = self._serialize_fit(resolved_a)
            serialized_b = self._serialize_fit(resolved_b)
            metrics_a = self._extract_key_metrics(serialized_a["stats"])
            metrics_b = self._extract_key_metrics(serialized_b["stats"])
            delta = {
                key: None if metrics_a[key] is None or metrics_b[key] is None else round(metrics_b[key] - metrics_a[key], 4)
                for key in metrics_a
            }
            return {
                "fit_a": serialized_a,
                "fit_b": serialized_b,
                "delta_b_minus_a": delta,
            }

    def create_fit(self, ship_name: str, fit_name: str | None = None) -> dict[str, Any]:
        with self.lock:
            item = self._resolve_ship(ship_name)
            try:
                ship = self.ship_cls(item)
            except ValueError:
                ship = self.citadel_cls(item)
            fit = self.fit_cls(ship, fit_name or f"New {item.typeName}")
            fit.character = self.character_cls.getAll5()
            fit.damagePattern = self.damage_pattern_cls.getDefaultBuiltin()
            fit.implantLocation = self.implant_location.CHARACTER
            fit.booster = False
            self.db.save(fit)
            self._recalculate_fit(fit)
            return self._serialize_fit(fit)

    def get_ship_profile(self, ship_name: str) -> dict[str, Any]:
        with self.lock:
            item = self._resolve_ship(ship_name)
            try:
                ship = self.ship_cls(item)
            except ValueError:
                ship = self.citadel_cls(item)
            fit = self.fit_cls(ship, f"Empty {item.typeName}")
            fit.character = self.character_cls.getAll5()
            fit.damagePattern = self.damage_pattern_cls.getDefaultBuiltin()
            fit.implantLocation = self.implant_location.CHARACTER
            self._recalculate_fit(fit)
            return {
                "ship": {
                    "id": item.ID,
                    "name": item.typeName,
                    "group": item.group.name,
                    "category": item.group.category.name,
                    "race": getattr(item, "race", None),
                    "description": getattr(item, "description", None),
                },
                "empty_fit_stats": self._serialize_stats(fit),
            }

    def _resolve_fit(self, identifier: int | str):
        if isinstance(identifier, int):
            fit = self.db.getFit(identifier)
            if fit is None:
                raise FitResolutionError(f"Could not find fit with ID {identifier}.")
            self._recalculate_fit(fit)
            return fit

        value = str(identifier).strip()
        if not value:
            raise FitResolutionError("Fit identifier cannot be empty.")

        if value.isdigit():
            fit = self.db.getFit(int(value))
            if fit is not None:
                self._recalculate_fit(fit)
                return fit

        results = list(self.db.searchFits(value))
        exact = [fit for fit in results if fit.name.lower() == value.lower()]
        matches = exact or results
        if not matches:
            raise FitResolutionError(f"Could not find a fit matching {value!r}.")
        if len(matches) > 1:
            formatted = ", ".join(f"[{fit.ID}] {fit.name}" for fit in matches[:5])
            raise FitResolutionError(f"Fit identifier {value!r} is ambiguous. Matches: {formatted}")
        fit = matches[0]
        self._recalculate_fit(fit)
        return fit

    def _resolve_ship(self, ship_name: str):
        item = self.db.getItem(ship_name)
        if item is None:
            raise ValueError(f"Could not find a ship named {ship_name!r}. Use the exact in-game type name.")
        category_name = item.group.category.name
        if category_name not in {"Ship", "Structure"}:
            raise ValueError(f"{ship_name!r} is not a ship or structure hull.")
        return item

    @staticmethod
    def _round(value: Any) -> float | None:
        if value is None:
            return None
        return round(float(value), 4)

    @staticmethod
    def _serialize_datetime(value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    def _serialize_damage(self, damage: Any) -> dict[str, float | None]:
        return {
            "em": self._round(damage.em),
            "thermal": self._round(damage.thermal),
            "kinetic": self._round(damage.kinetic),
            "explosive": self._round(damage.explosive),
            "pure": self._round(damage.pure),
            "total": self._round(damage.total),
        }

    def _serialize_tank(self, tank: dict[str, Any]) -> dict[str, float | None]:
        return {key: self._round(value) for key, value in tank.items()}

    def _serialize_ehp(self, ehp: dict[str, Any]) -> dict[str, float | None]:
        layers = {key: self._round(value) for key, value in ehp.items()}
        layers["total"] = self._round(sum(value or 0 for value in ehp.values()))
        return layers

    def _serialize_fit_reference(self, fit: Any) -> dict[str, Any]:
        return {
            "id": fit.ID,
            "name": fit.name,
            "ship_id": fit.ship.item.ID,
            "ship_name": fit.ship.item.typeName,
            "ship_group": fit.ship.item.group.name,
            "created": self._serialize_datetime(fit.created),
            "modified": self._serialize_datetime(fit.modified),
        }

    def _serialize_stats(self, fit: Any) -> dict[str, Any]:
        return {
            "damage": {
                "weapon_dps": self._serialize_damage(fit.getWeaponDps()),
                "drone_dps": self._serialize_damage(fit.getDroneDps()),
                "total_dps": self._serialize_damage(fit.getTotalDps()),
                "weapon_volley": self._serialize_damage(fit.getWeaponVolley()),
                "drone_volley": self._serialize_damage(fit.getDroneVolley()),
                "total_volley": self._serialize_damage(fit.getTotalVolley()),
            },
            "defense": {
                "hp": {key: self._round(value) for key, value in fit.hp.items()},
                "ehp": self._serialize_ehp(fit.ehp),
                "tank": self._serialize_tank(fit.tank),
                "effective_tank": self._serialize_tank(fit.effectiveTank),
                "sustainable_tank": self._serialize_tank(fit.sustainableTank),
                "effective_sustainable_tank": self._serialize_tank(fit.effectiveSustainableTank),
            },
            "capacitor": {
                "stable": fit.capStable,
                "state": self._round(fit.capState),
                "used_per_second": self._round(fit.capUsed),
                "recharge_per_second": self._round(fit.capRecharge),
                "delta_per_second": self._round(fit.capDelta),
            },
            "mobility": {
                "max_speed": self._round(fit.maxSpeed),
                "align_time": self._round(fit.alignTime),
                "warp_speed": self._round(fit.warpSpeed),
                "signature_radius": self._round(fit.ship.getModifiedItemAttr("signatureRadius")),
            },
            "targeting": {
                "max_targets": self._round(fit.maxTargets),
                "max_target_range": self._round(fit.maxTargetRange),
                "scan_strength": self._round(fit.scanStrength),
                "lock_time_vs_40m": self._round(fit.calculateLockTime(40)),
            },
            "resources": {
                "calibration": self._round(fit.ship.getModifiedItemAttr("upgradeCapacity")),
                "powergrid_output": self._round(fit.ship.getModifiedItemAttr("powerOutput")),
                "cpu_output": self._round(fit.ship.getModifiedItemAttr("cpuOutput")),
            },
        }

    def _serialize_fit(self, fit: Any) -> dict[str, Any]:
        return {
            "fit": {
                **self._serialize_fit_reference(fit),
                "notes": fit.notes,
                "is_structure": fit.isStructure,
            },
            "stats": self._serialize_stats(fit),
        }

    def _extract_key_metrics(self, stats: dict[str, Any]) -> dict[str, float | None]:
        return {
            "total_dps": stats["damage"]["total_dps"]["total"],
            "total_volley": stats["damage"]["total_volley"]["total"],
            "ehp_total": stats["defense"]["ehp"]["total"],
            "max_speed": stats["mobility"]["max_speed"],
            "align_time": stats["mobility"]["align_time"],
            "warp_speed": stats["mobility"]["warp_speed"],
            "cap_delta_per_second": stats["capacitor"]["delta_per_second"],
            "lock_time_vs_40m": stats["targeting"]["lock_time_vs_40m"],
        }

    @staticmethod
    def _recalculate_fit(fit: Any) -> None:
        fit.clear()
        fit.calculateModifiedAttributes()


def initialize_runtime(config: RuntimeConfig | None = None) -> PyfaRuntime:
    global _runtime

    resolved_config = config or RuntimeConfig.defaults()
    with _runtime_lock:
        if _runtime is not None:
            if _runtime.config != resolved_config:
                raise RuntimeError("Pyfa MCP runtime has already been initialized with a different configuration.")
            return _runtime

        if not resolved_config.game_db.exists():
            if resolved_config.build_game_db_if_missing:
                _build_game_db(resolved_config)
            else:
                raise FileNotFoundError(
                    f"Gamedata DB not found at {resolved_config.game_db}. "
                    "Generate it with `python3 db_update.py` or pass --build-game-db-if-missing."
                )

        resolved_config.savedata_db.parent.mkdir(parents=True, exist_ok=True)

        repo_root = str(resolved_config.repo_root)
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)

        _ensure_wx_available()

        import eos.config as eos_config

        eos_config.gamedataCache = False
        eos_config.gamedata_connectionstring = f"sqlite:///{resolved_config.game_db}?check_same_thread=False"
        eos_config.saveddata_connectionstring = f"sqlite:///{resolved_config.savedata_db}?check_same_thread=False"
        eos_config.set_lang("en")

        import eos.db as eos_db
        from eos.const import ImplantLocation
        from eos.gamedata import Item
        from eos.saveddata.character import Character
        from eos.saveddata.citadel import Citadel
        from eos.saveddata.damagePattern import DamagePattern
        from eos.saveddata.fit import Fit
        from eos.saveddata.ship import Ship

        eos_db.saveddata_meta.create_all()

        _runtime = PyfaRuntime(
            config=resolved_config,
            eos_db=eos_db,
            item_cls=Item,
            fit_cls=Fit,
            ship_cls=Ship,
            citadel_cls=Citadel,
            character_cls=Character,
            damage_pattern_cls=DamagePattern,
            implant_location=ImplantLocation,
        )
        return _runtime


def reset_runtime_for_tests() -> None:
    global _runtime

    with _runtime_lock:
        _runtime = None
        for module_name in list(sys.modules):
            if module_name == "eos" or module_name.startswith("eos."):
                del sys.modules[module_name]


def _build_game_db(config: RuntimeConfig) -> None:
    staticdata_dir = config.repo_root / "staticdata"
    if not staticdata_dir.exists():
        raise FileNotFoundError(
            f"Gamedata DB is missing at {config.game_db} and no staticdata directory was found at {staticdata_dir}."
        )
    if config.game_db != (config.repo_root / "eve.db"):
        raise FileNotFoundError(
            f"Gamedata DB is missing at {config.game_db}. Auto-build only supports the default location {config.repo_root / 'eve.db'}."
        )
    with tempfile.TemporaryDirectory() as tmpdir:
        stub_path = Path(tmpdir) / "wx.py"
        stub_path.write_text(_WX_STUB_SOURCE, encoding="utf-8")
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{tmpdir}{os.pathsep}{env['PYTHONPATH']}" if env.get("PYTHONPATH") else tmpdir
        subprocess.run([sys.executable, str(config.repo_root / "db_update.py")], cwd=config.repo_root, env=env, check=True)


def _ensure_wx_available() -> None:
    try:
        __import__("wx")
    except ModuleNotFoundError:
        wx = types.ModuleType("wx")

        class Colour:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        wx.Colour = Colour
        wx.GetTranslation = lambda text: text
        sys.modules["wx"] = wx


_WX_STUB_SOURCE = """\
class Colour:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def GetTranslation(text):
    return text
"""
