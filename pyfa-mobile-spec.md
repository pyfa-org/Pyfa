# PYFA Mobile — Port Specification
**For use with Claude Code / agentic coding workflows**
**Source repo:** https://github.com/pyfa-org/Pyfa (GPL-3.0)
**Target:** Cross-platform mobile app (Android + iOS) preserving PYFA feature parity

---

## 1. Project Goal

Port PYFA (Python Fitting Assistant for EVE Online) to a mobile-native application. The goal is **feature and UX familiarity** — users who know PYFA should feel at home — while building on a proper mobile foundation. This is not a straight fork; the GUI layer is being replaced entirely and parts of the service layer are being refactored. The fitting engine (EOS) is being kept as-is.

---

## 2. Architecture Decision

### Chosen Stack

```
┌─────────────────────────────────────────────┐
│          React Native (Expo) Frontend        │
│   TypeScript · React Navigation · Zustand    │
└────────────────┬────────────────────────────┘
                 │ HTTP (localhost)
┌────────────────▼────────────────────────────┐
│       FastAPI Backend (local, bundled)       │
│   Python 3.11 · EOS engine · SQLAlchemy     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         SQLite Databases (bundled)           │
│   eve.db (trimmed SDE) · saveddata.db        │
└─────────────────────────────────────────────┘
```

### Rationale

- **EOS stays in Python** — The fitting engine is deeply correct, well-tested, and complex. Porting it to TypeScript would be a multi-month effort with high regression risk. Running it as a bundled local process is the only reliable path.
- **React Native (Expo)** — Best mobile UX ceiling for cross-platform development. Expo's managed workflow simplifies iOS/Android builds. Familiar to web developers. Recharts/Victory Native handles graphs.
- **Local FastAPI server** — EOS is accessed via a lightweight REST API running on localhost inside the app process. On Android this is a background service; on iOS it runs as a co-process via a Python runtime bundled with BeeWare/Briefcase or Chaquopy (Android) + Kivy for iOS subprocess approach. See Section 9 for platform-specific bundling notes.
- **SQLite** — Both EOS databases are already SQLite. The SDE (eve.db) is trimmed to only fitting-relevant data to reduce bundle size.

---

## 3. Source Code Audit — What to Keep vs. Discard

### 3.1 `eos/` — **KEEP (unmodified)**

The EOS fitting engine is cleanly separated from wxPython. It has zero GUI imports. Keep it entirely.

| Subpath | Description | Decision |
|---|---|---|
| `eos/saveddata/fit.py` | Core Fit model, slot management, stat calculation dispatch | ✅ Keep |
| `eos/saveddata/ship.py` | Ship wrapper around gamedata Item | ✅ Keep |
| `eos/saveddata/module.py` | Module model with State enum (offline/online/active/overload) | ✅ Keep |
| `eos/saveddata/character.py` | Character model, skill levels | ✅ Keep |
| `eos/saveddata/drone.py` | Drone model | ✅ Keep |
| `eos/saveddata/implant.py` | Implant model | ✅ Keep |
| `eos/saveddata/booster.py` | Booster model | ✅ Keep |
| `eos/saveddata/damagePattern.py` | DamagePattern model | ✅ Keep |
| `eos/saveddata/targetProfile.py` | TargetProfile model | ✅ Keep |
| `eos/saveddata/citadel.py` | Citadel/structure model | ✅ Keep |
| `eos/gamedata.py` | EVE data models: Item, Attribute, Effect, Group, Category | ✅ Keep |
| `eos/db/` | SQLAlchemy ORM, gamedata + saveddata sessions | ✅ Keep |
| `eos/capSim.py` | Capacitor stability simulation (heap-based) | ✅ Keep |
| `eos/const.py` | Game constants (slot types, states, etc.) | ✅ Keep |
| `eos/config.py` | DB path configuration | ✅ Keep — update paths for mobile |
| `eos/effectHandlerHelpers.py` | HandledModuleList, HandledDroneList, etc. | ✅ Keep |
| `eos/utils/` | Float utilities, stats containers | ✅ Keep |

### 3.2 `service/` — **PARTIAL KEEP (refactor)**

The service layer is business logic that sits between EOS and the GUI. Much of it is clean Python, but some files have hard wx dependencies.

| File | wx Coupled? | Decision | Notes |
|---|---|---|---|
| `service/fit.py` | No | ✅ Keep | Core fitting service, wrap with FastAPI routes |
| `service/character.py` | No | ✅ Keep | Character management |
| `service/market.py` | No | ✅ Keep | Market data queries |
| `service/port/port.py` | No | ✅ Keep | EFT/ESI import-export logic |
| `service/port/esi.py` | No | ✅ Keep | ESI fitting format handler |
| `service/price.py` | No | ✅ Keep | Price fetching (Fuzzwork/ESI markets) |
| `service/settings.py` | Partial | ⚠️ Refactor | Remove HTMLExportSettings wx refs; keep SettingsProvider |
| `service/esiAccess.py` | No | ✅ Keep | ESI HTTP client, token management |
| `service/esi.py` | **Yes** | ⚠️ Refactor | SSO login flow opens wx dialog — replace with mobile OAuth |
| `service/server.py` | No | ⚠️ Refactor | Local HTTP server for OAuth callback — replace with mobile deep link |
| `service/update.py` | Partial | ⚠️ Refactor | Remove wx notification; keep version check logic |
| `service/attribute.py` | No | ✅ Keep | Attribute editing |

**Key refactor:** `service/esi.py` contains `gui.ssoLogin.SsoLogin(...)` — the SSO login dialog. This must be replaced with a mobile OAuth flow using the system browser + a deep link callback URI (see Section 7).

### 3.3 `graphs/` — **KEEP logic, replace rendering**

| File | Decision | Notes |
|---|---|---|
| `graphs/data/` | ✅ Keep | Graph calculation logic (DPS vs range, etc.) |
| `graphs/wrapper/` | ✅ Keep | Data wrappers |
| `graphs/graph.py` | ✅ Keep | Graph data computation |
| Any matplotlib rendering | ❌ Discard | Replace with Victory Native / Recharts on the RN side |

The `graphs/` module computes graph data points. The FastAPI backend will expose these as JSON arrays; the React Native frontend will render them using Victory Native.

### 3.4 `gui/` — **DISCARD entirely**

Every file in `gui/` is wxPython and has no reusable code for mobile.

| Module | Mobile Equivalent |
|---|---|
| `gui/mainFrame.py` | App shell + React Navigation layout |
| `gui/shipBrowser.py` | FittingBrowserScreen (ship list + fit list) |
| `gui/marketBrowser.py` | MarketBrowserScreen (searchable item tree) |
| `gui/statsPane.py` | StatsPanelComponent (inline stats cards) |
| `gui/fittingView/` | FittingEditorScreen (slot grid) |
| `gui/additionsPane/` | AdditionsTabsComponent (drones, implants, boosters) |
| `gui/graphFrame/` | GraphScreen (Victory Native charts) |
| `gui/characterEditor.py` | CharacterScreen |
| `gui/esiFittings.py` | ESIFittingsScreen |
| `gui/preferenceDialog.py` | SettingsScreen |
| `gui/patternEditor.py` | DamagePatternScreen |
| `gui/targetProfileEditor.py` | TargetProfileScreen |

### 3.5 `staticdata/` — **KEEP, trim**

The bundled `eve.db` is the EVE Static Data Export. Keep the file but run a schema trim script (see Section 8) to remove non-fitting-relevant tables and reduce bundle size.

### 3.6 `utils/` — **KEEP**

Pure Python utilities. No wx dependencies.

### 3.7 Root-level files

| File | Decision |
|---|---|
| `config.py` | ⚠️ Refactor — update paths for mobile data dirs |
| `pyfa.py` | ❌ Discard — wx app entry point |
| `db_update.py` | ✅ Keep — useful for SDE update script |
| `requirements.txt` | ⚠️ Refactor — remove wx, add FastAPI, uvicorn |

---

## 4. New Project Structure

```
pyfa-mobile/
├── backend/                    # Python backend (EOS + FastAPI)
│   ├── eos/                    # Copied from PYFA repo (unmodified)
│   ├── graphs/                 # Copied from PYFA repo (unmodified)
│   ├── service/                # Copied + refactored from PYFA repo
│   │   ├── fit.py
│   │   ├── character.py
│   │   ├── market.py
│   │   ├── esiAccess.py
│   │   ├── esi.py              # Refactored: remove wx, add token storage API
│   │   ├── port/
│   │   ├── price.py
│   │   └── settings.py         # Refactored: remove wx deps
│   ├── utils/                  # Copied from PYFA repo (unmodified)
│   ├── api/                    # NEW: FastAPI route modules
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app + startup
│   │   ├── routes/
│   │   │   ├── fits.py         # CRUD for fits
│   │   │   ├── ships.py        # Ship browsing/search
│   │   │   ├── market.py       # Module/item browsing
│   │   │   ├── characters.py   # Character management
│   │   │   ├── stats.py        # Fit stats computation
│   │   │   ├── graphs.py       # Graph data endpoints
│   │   │   ├── esi.py          # ESI OAuth + fitting sync
│   │   │   ├── price.py        # Price data
│   │   │   └── settings.py     # App settings
│   │   └── models/             # Pydantic request/response models
│   │       ├── fit.py
│   │       ├── ship.py
│   │       ├── module.py
│   │       └── stats.py
│   ├── config.py               # Refactored config
│   ├── requirements.txt        # FastAPI, uvicorn, SQLAlchemy, requests, etc.
│   └── data/
│       ├── eve.db              # Trimmed SDE SQLite
│       └── saveddata.db        # User data (created on first run)
│
├── mobile/                     # React Native (Expo) frontend
│   ├── app/                    # Expo Router file-based routing
│   │   ├── (tabs)/
│   │   │   ├── fittings.tsx    # Fitting browser tab
│   │   │   ├── market.tsx      # Market browser tab
│   │   │   └── settings.tsx    # Settings tab
│   │   ├── fitting/
│   │   │   └── [id].tsx        # Fitting editor screen
│   │   ├── ship/
│   │   │   └── [id].tsx        # Ship selection screen
│   │   ├── graphs/
│   │   │   └── [fitId].tsx     # Graph screen
│   │   └── character/
│   │       └── index.tsx       # Character management screen
│   ├── components/
│   │   ├── fitting/
│   │   │   ├── SlotGrid.tsx    # High/mid/low/rig/subsystem slot layout
│   │   │   ├── ModuleSlot.tsx  # Individual slot with state toggle
│   │   │   ├── ChargeSelector.tsx
│   │   │   └── DroneList.tsx
│   │   ├── stats/
│   │   │   ├── StatsPanel.tsx  # Collapsible stats card
│   │   │   ├── ResistBar.tsx   # EM/Therm/Kin/Exp bar
│   │   │   ├── CapDisplay.tsx  # Capacitor stability display
│   │   │   └── DpsDisplay.tsx
│   │   ├── market/
│   │   │   ├── CategoryTree.tsx
│   │   │   ├── ItemList.tsx
│   │   │   └── ItemSearchBar.tsx
│   │   └── shared/
│   │       ├── EVEIcon.tsx     # EVE type icon from CDN
│   │       └── StatRow.tsx
│   ├── hooks/
│   │   ├── useApi.ts           # Axios wrapper for backend calls
│   │   ├── useFit.ts           # Fit state management
│   │   └── useMarket.ts        # Market data hooks
│   ├── store/
│   │   └── index.ts            # Zustand global state
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces mirroring API models
│   └── constants/
│       └── colors.ts           # EVE-themed dark palette
│
├── scripts/
│   ├── trim_sde.py             # Script to trim eve.db to fitting-relevant tables
│   └── build_android.sh        # Android build automation
│
└── README.md
```

---

## 5. FastAPI Backend — Endpoint Specification

All endpoints are served on `http://localhost:8765`. The React Native app hits this on device.

### 5.1 Fits

```
GET    /fits                          List all fits (FitLite objects)
POST   /fits                          Create new fit {shipID, name}
GET    /fits/{fit_id}                 Get full fit with all modules/stats
PUT    /fits/{fit_id}                 Update fit name/notes
DELETE /fits/{fit_id}                 Delete fit
POST   /fits/{fit_id}/duplicate       Duplicate a fit
GET    /fits/{fit_id}/stats           Get computed stats (EHP, DPS, cap, speed, etc.)
GET    /fits/{fit_id}/validate        Validate fit, return list of issues

POST   /fits/{fit_id}/modules         Add module to fit {typeID, slot, position}
DELETE /fits/{fit_id}/modules/{pos}   Remove module from slot
PUT    /fits/{fit_id}/modules/{pos}/state  Set module state {state: offline|online|active|overload}
PUT    /fits/{fit_id}/modules/{pos}/charge  Set charge {typeID}

POST   /fits/{fit_id}/drones          Add drone stack {typeID, count}
DELETE /fits/{fit_id}/drones/{typeID}
PUT    /fits/{fit_id}/drones/{typeID}/active {count}

POST   /fits/{fit_id}/implants        Add implant {typeID}
DELETE /fits/{fit_id}/implants/{typeID}
POST   /fits/{fit_id}/boosters        Add booster {typeID}
DELETE /fits/{fit_id}/boosters/{typeID}

GET    /fits/{fit_id}/export/eft      Export as EFT string
GET    /fits/{fit_id}/export/dna      Export as DNA string
POST   /fits/import/eft               Import from EFT {eftString}
POST   /fits/import/esi               Import from ESI fit object
```

### 5.2 Ships & Market

```
GET    /ships                         List all ships (grouped by race/class)
GET    /ships/search?q={query}        Search ships by name
GET    /ships/{typeID}                Get ship details + base attributes

GET    /market/categories             Full market category tree
GET    /market/search?q={query}&slot={slot}  Search modules/items
GET    /market/item/{typeID}          Get item details + attributes
GET    /market/item/{typeID}/variations  Get T1/T2/faction/deadspace/officer variations
```

### 5.3 Stats

```
GET    /fits/{fit_id}/stats/ehp?damagePattern={patternID}
GET    /fits/{fit_id}/stats/dps?damagePattern={patternID}&targetProfile={profileID}
GET    /fits/{fit_id}/stats/cap
GET    /fits/{fit_id}/stats/navigation
GET    /fits/{fit_id}/stats/targeting
GET    /fits/{fit_id}/stats/full      All stats in one call (preferred for mobile)
```

The `/stats/full` endpoint is the primary one the mobile app calls after any fit change. Returns a single JSON object with all stat categories.

### 5.4 Graphs

```
GET    /graphs/dps-range?fitIDs={ids}&targetSig={sig}&targetVelocity={vel}
GET    /graphs/dps-time?fitIDs={ids}&distance={dist}
GET    /graphs/ehp-speed?fitIDs={ids}
```

Returns arrays of `{x, y}` data points for the React Native chart components.

### 5.5 Characters

```
GET    /characters                    List characters (builtin + ESI-linked)
GET    /characters/{id}               Get character + skills
PUT    /characters/{id}/skill/{skillID}  Set skill level (for manual chars)
POST   /characters/esi/init           Begin ESI OAuth flow, returns auth URL
POST   /characters/esi/callback       Handle OAuth callback {code, state}
DELETE /characters/esi/{id}           Remove ESI character
POST   /characters/esi/{id}/refresh   Force token refresh
```

### 5.6 Settings & Meta

```
GET    /settings
PUT    /settings
GET    /damage-patterns
POST   /damage-patterns
PUT    /damage-patterns/{id}
DELETE /damage-patterns/{id}
GET    /target-profiles
POST   /target-profiles
PUT    /target-profiles/{id}
DELETE /target-profiles/{id}
GET    /prices?typeIDs={ids}          Batch price fetch
GET    /meta/version                  App + SDE version info
```

---

## 6. Stats Response Schema

The `/fits/{id}/stats/full` endpoint should return:

```json
{
  "fitID": 42,
  "shipName": "Dramiel",
  "shipTypeID": 17932,
  "validation": {
    "valid": true,
    "issues": []
  },
  "tank": {
    "shield": { "hp": 1250, "em": 0.0, "therm": 0.20, "kin": 0.40, "exp": 0.50 },
    "armor":  { "hp": 800,  "em": 0.50, "therm": 0.35, "kin": 0.25, "exp": 0.10 },
    "hull":   { "hp": 600,  "em": 0.33, "therm": 0.33, "kin": 0.33, "exp": 0.33 },
    "ehp": {
      "uniform": 4200.0,
      "em": 3100.0,
      "therm": 3500.0,
      "kin": 4000.0,
      "exp": 5200.0
    },
    "effectivehp": 4200.0
  },
  "dps": {
    "turret": 320.5,
    "missile": 0.0,
    "drone": 110.0,
    "total": 430.5,
    "volley": 1200.0
  },
  "capacitor": {
    "stable": false,
    "stableAt": null,
    "timeToEmpty": 148.3,
    "capacity": 900.0,
    "rechargeRate": 112000
  },
  "navigation": {
    "maxVelocity": 4200.0,
    "agility": 0.355,
    "alignTime": 2.8,
    "warpSpeed": 6.0,
    "signatureRadius": 32.0
  },
  "targeting": {
    "maxTargetRange": 52000,
    "scanResolution": 800,
    "maxLockedTargets": 6,
    "sensorStrength": { "type": "radar", "value": 18.0 }
  },
  "fitting": {
    "cpu": { "used": 312.0, "total": 425.0 },
    "powergrid": { "used": 175.0, "total": 220.0 },
    "calibration": { "used": 250, "total": 400 },
    "droneBandwidth": { "used": 25.0, "total": 25.0 },
    "droneBay": { "used": 25.0, "total": 40.0 }
  },
  "price": {
    "hull": 45000000.0,
    "fit": 120000000.0,
    "total": 165000000.0
  }
}
```

---

## 7. ESI / OAuth Flow (Mobile)

PYFA desktop uses a local HTTP server on a random port to receive the OAuth callback. On mobile, this is replaced with a **deep link**.

### Flow

1. App calls `POST /characters/esi/init` → backend generates state, PKCE verifier, returns `authUrl` (login.eveonline.com/oauth/authorize?...)
2. App opens `authUrl` in the **system browser** using `expo-web-browser` (`openAuthSessionAsync`)
3. CCP redirects to `pyfa-mobile://esi-callback?code=...&state=...`
4. Expo handles the deep link, sends code+state to `POST /characters/esi/callback`
5. Backend exchanges code for tokens via `esiAccess.py`, stores in saveddata.db

### Config Required

- Register a custom URI scheme `pyfa-mobile://esi-callback` in `app.json` (Expo)
- Set the same redirect URI in the CCP ESI application registration
- Backend `service/esi.py` refactor: remove `server.py` local HTTP server, expose `initOAuth()` and `handleCallback(code, state)` methods that the FastAPI routes call directly

### Token Storage

Tokens stored in `saveddata.db` via the existing `eos/saveddata/` SSO models. The mobile backend handles token refresh on a background timer (same as PYFA desktop's auto-refresh logic from `service/esi.py`).

---

## 8. SDE Trimming Script

File: `scripts/trim_sde.py`

The full EVE SDE is large. For a fitting tool, we only need:

**Tables to KEEP:**
- `invTypes` (typeID, name, groupID, categoryID, basePrice, published)
- `invGroups` (groupID, name, categoryID)
- `invCategories` (categoryID, name)
- `dgmTypeAttributes` (typeID, attributeID, valueInt, valueFloat)
- `dgmAttributes` (attributeID, name, defaultValue, highIsGood, stackable, unitID, displayName)
- `dgmTypeEffects` (typeID, effectID, isDefault)
- `dgmEffects` (effectID, name, effectCategory, preExpression, postExpression, etc.)
- `invTypeMaterials` (minimal — for reprocessing if desired)
- `mapSolarSystems` (for future: system security for fitting adjustments)
- `chrRaces` (raceID, raceName)
- `eveIcons` (iconID, iconFile) — for rendering ship/module icons

**Tables to DROP:**
- Industry tables (blueprints, reactions, etc.)
- Sovereignty tables
- Wars, killmails
- NPC market orders
- Planet interaction
- Wormhole tables (keep basic wh types in invTypes/Groups)
- Translation tables (keep English only for v1)

Expected size reduction: ~600MB full SDE → ~40–60MB trimmed SQLite.

**Script structure:**
```python
# scripts/trim_sde.py
# Usage: python trim_sde.py --input eve_full.db --output eve.db
# Copies only fitting-relevant tables and filters to published=1 types only
```

---

## 9. Mobile Bundling Notes

### Android (Recommended First Target)

Use **Chaquopy** (Gradle plugin) to bundle CPython 3.11 and run the FastAPI backend as an Android Service.

- Chaquopy handles pip dependencies inside the APK
- Backend runs as a foreground service, starts on app launch
- React Native app waits for `http://localhost:8765/meta/version` to respond before rendering
- SQLite files are bundled as app assets, copied to app's internal storage on first run

**Key Gradle config:**
```groovy
python {
    pip {
        install "fastapi"
        install "uvicorn"
        install "sqlalchemy"
        install "requests"
        install "requests-cache"
        install "logbook"
    }
}
```

### iOS (Secondary Target)

iOS is more restrictive about background processes and bundled runtimes.

Option A: **Kivy/Pyobjus approach** — bundle Python via Briefcase (BeeWare). Viable but complex build pipeline.

Option B: **Transpile hot-path to TypeScript** — For iOS only, port the EOS stat calculation layer to TypeScript using the Python code as a reference. This avoids the Python bundling problem entirely at the cost of maintaining two implementations of the math layer.

**Recommendation:** Target Android first. Assess iOS bundling complexity after Android is stable. The FastAPI + Chaquopy approach is well-documented for Android and significantly lowers early risk.

---

## 10. UI/UX Specification

### Design Language

- **Dark theme only** (matches EVE aesthetic) — background `#0D0D0D`, surface `#1A1A2E`, accent `#B8860B` (EVE gold), danger `#CC2200`
- Use EVE's type icon CDN: `https://images.evetech.net/types/{typeID}/icon?size=64`
- Ship renders: `https://images.evetech.net/types/{typeID}/render?size=128`

### Screen Map

#### Tab 1: Fittings Browser
- Left: searchable list of fits grouped by ship class
- Tap fit → opens Fitting Editor
- Long press → context menu (duplicate, delete, export)
- FAB: create new fit (opens ship picker)

#### Fitting Editor Screen
- **Top bar:** ship name, character selector dropdown, DPS / EHP / cap quick stats
- **Center:** Ship slot layout
  - Section headers: HIGH SLOTS (n/n), MID SLOTS, LOW SLOTS, RIGS, SUBSYSTEMS
  - Each slot: module icon + name, state indicator dot (offline=grey, online=green, active=blue, overload=orange)
  - Tap slot → opens module picker (market browser filtered to valid slot)
  - Long press module → context menu (set state, set charge, remove)
  - Empty slot shows "— Empty —" with `+` icon
- **Bottom sheet (expandable):** tabbed additions panel
  - Tab: Drones | Implants & Boosters | Fleet Bonuses
- **Stats button (bottom right):** expands full stats sheet (modal bottom sheet)

#### Stats Bottom Sheet
Sections (collapsible):
1. Offense — DPS breakdown (turret / missile / drone), volley, damage pattern selector
2. Defense — Shield/armor/hull bars with resist display, EHP
3. Capacitor — stable/unstable indicator, time to empty or stable%, cap chain display
4. Navigation — velocity, align time, warp speed, sig radius
5. Targeting — scan res, target range, locked targets, sensor type/strength
6. Fitting — CPU/PG/Calibration used/total with color coding
7. Price — hull / fit / total with Jita price note

#### Tab 2: Market Browser
- Search bar (debounced, 300ms)
- Category tree (collapsible sections: Ships, Modules by slot, Charges, Drones, Implants, etc.)
- Item list with: icon, name, slot indicator, T/T2/Faction/Deadspace/Officer variation tabs at bottom
- Tap item → Item Detail Sheet: attributes, description, "Add to current fit" button

#### Tab 3: Settings
- Character management (list of chars, add ESI character button)
- Damage patterns editor
- Target profiles editor
- Price provider toggle
- Appearance preferences
- SDE version + update check

#### Graph Screen (accessed from fitting editor menu)
- Full-screen chart with Victory Native
- Available graph types: DPS vs Range, DPS vs Time, EHP vs Speed
- Multi-fit comparison: drag fits from browser into graph
- Target controls: signature radius, velocity sliders
- Export as image button

### Key Mobile UX Adaptations from Desktop

| Desktop PYFA | Mobile Adaptation |
|---|---|
| Left panel (ship browser) + center (fitting) side-by-side | Tab navigation; fit browser is separate tab |
| Drag-and-drop module from market | Tap slot → inline module picker |
| Right-click context menus | Long press → action sheet |
| Resizable split panels | Bottom sheets, collapsible sections |
| Persistent graph window | Dedicated graph screen with back navigation |
| Inline stats pane | Expandable bottom sheet over fitting view |
| Desktop menu bar (File, Edit, etc.) | Screen-level action menus + FABs |

---

## 11. Data Flow on Fit Change

When the user modifies a fit (add/remove module, change state), the following should happen:

```
User action (tap/gesture)
  → Optimistic UI update (show module immediately)
  → POST/PUT to backend API
  → Backend: calls service/fit.py → EOS → recalculates all stats
  → Backend: returns updated stats JSON
  → React Native: updates Zustand store
  → Stats components re-render
```

Target: < 200ms round-trip for stat recalculation (EOS is fast; latency is local loopback).

---

## 12. Implementation Phases

### Phase 1 — Backend Foundation
1. Set up project structure (`backend/`, `mobile/`)
2. Copy `eos/`, `graphs/`, `utils/` from PYFA repo unchanged
3. Copy and refactor `service/` (remove wx imports, stub ESI OAuth)
4. Create `api/main.py` with FastAPI app skeleton
5. Implement core routes: `/fits`, `/fits/{id}/stats/full`, `/ships`, `/market/search`
6. Validate EOS works via direct Python calls and via API
7. Write `scripts/trim_sde.py` and produce `eve.db`

### Phase 2 — Android Bundling
1. Scaffold Expo project with Expo Router
2. Set up Chaquopy in Android build
3. Implement background service that starts FastAPI/uvicorn
4. Implement startup screen with backend health check polling
5. Verify localhost API calls work from RN on Android

### Phase 3 — Core Fitting UI
1. Fitting browser (list, create, delete)
2. Ship picker screen
3. Fitting editor: slot grid + module state
4. Market browser (category tree + search)
5. Module picker (from slot tap)
6. Stats bottom sheet (all stat categories)

### Phase 4 — ESI & Characters
1. ESI OAuth flow (deep link)
2. Character management screen
3. Character-aware stat calculation
4. ESI fitting import/export
5. Token auto-refresh

### Phase 5 — Advanced Features
1. Graph screen (Victory Native charts)
2. Damage pattern editor
3. Target profile editor
4. Multi-fit comparison in graphs
5. Price data integration
6. EFT clipboard import/export

### Phase 6 — Polish & iOS
1. Full dark theme polish
2. EVE icon CDN integration
3. Performance profiling (stat recalc, list rendering)
4. iOS bundling investigation / implementation
5. App store preparation

---

## 13. Key Dependencies

### Backend (`backend/requirements.txt`)
```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
requests>=2.31.0
requests-cache>=1.1.0
logbook>=1.7.0
python-dateutil>=2.8.2
roman>=3.3
pydantic>=2.0.0
```
Remove from PYFA's original requirements:
- `wxPython` — removed
- `matplotlib` — removed (graphs rendered in RN)
- `Pillow` — removed (no image processing needed)

### Frontend (`mobile/package.json`)
```json
{
  "expo": "~51.0.0",
  "expo-router": "~3.5.0",
  "react-native": "0.74.x",
  "react-navigation/native": "^6.0.0",
  "zustand": "^4.5.0",
  "axios": "^1.6.0",
  "victory-native": "^40.0.0",
  "expo-web-browser": "~13.0.0",
  "expo-linking": "~6.3.0",
  "@shopify/flash-list": "^1.6.0",
  "react-native-bottom-sheet": "^4.6.0",
  "react-native-gesture-handler": "~2.16.0",
  "react-native-reanimated": "~3.10.0"
}
```

---

## 14. Constraints and Known Risks

| Risk | Mitigation |
|---|---|
| Chaquopy licensing (commercial for Play Store) | Evaluate BeeWare/Briefcase as alternative; Chaquopy free tier may cover initial builds |
| iOS Python bundling complexity | Defer iOS; assess after Android is stable |
| SDE update cadence (EVE patches) | Bundle a static SDE version; implement `db_update.py`-style in-app update check |
| ESI deep link on Android back-stack | Use `expo-web-browser` `openAuthSessionAsync` which handles this correctly |
| EOS license (GPL-3.0) | The entire project must remain GPL-3.0 — ensure all code contributions comply |
| Large bundle size (Python runtime + SQLite) | Target < 80MB APK; trim SDE aggressively, use ABI splits |
| Performance on low-end Android | Profile EOS stat calls; cache last stat result in-process; use FlashList for virtualized lists |

---

## 15. Notes for Claude Code

- When working on the backend, always start EOS with the correct db paths from `config.py`. The trimmed `eve.db` must be in the expected location before any `eos.db` imports.
- `service/fit.py` uses a singleton pattern (`Fit.getInstance()`). Preserve this pattern but ensure it is thread-safe under uvicorn's async context (use a lock or run EOS calls in a thread executor: `await asyncio.get_event_loop().run_in_executor(None, eos_call)`).
- All EOS operations are synchronous/blocking. Wrap them in `run_in_executor` calls in FastAPI route handlers to avoid blocking the event loop.
- When adding FastAPI routes, mirror the method signatures from `service/fit.py` as closely as possible to reduce translation bugs.
- The `eos/saveddata/fit.py` `FitLite` class is used for list views (cheap to construct). Use this for the `GET /fits` list endpoint; only compute full stats on `GET /fits/{id}/stats/full`.
- Do not modify `eos/` files unless absolutely necessary. Keep it as a clean copy of the upstream PYFA eos module for easier future updates.
