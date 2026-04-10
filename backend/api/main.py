"""
PYFA Mobile — FastAPI application entry point.

Start with:
    uvicorn backend.api.main:app --host 127.0.0.1 --port 8765 --workers 1

On Android this module is invoked by the Chaquopy background service:
    from backend.api.main import start_server
    start_server()
"""

import asyncio
import sys
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logbook import Logger

pyfalog = Logger(__name__)

# ---------------------------------------------------------------------------
# Bootstrap — must happen before any eos.db import
# ---------------------------------------------------------------------------

def _bootstrap():
    """Initialise config paths and EOS database connections."""
    # Add backend/ to sys.path so relative imports resolve correctly when
    # running as a subprocess on Android.
    backend_dir = os.path.dirname(os.path.dirname(__file__))
    repo_root = os.path.dirname(backend_dir)
    for p in (backend_dir, repo_root):
        if p not in sys.path:
            sys.path.insert(0, p)

    import config
    config.defPaths()
    config.defLogging()

    # Import eos.db to trigger SQLAlchemy table creation / mapping
    import eos.db  # noqa: F401


# ---------------------------------------------------------------------------
# Lifespan — runs once at startup and shutdown
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    pyfalog.info("PYFA Mobile backend starting up")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _bootstrap)
    yield
    pyfalog.info("PYFA Mobile backend shutting down")


# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PYFA Mobile API",
    description="Local REST API exposing the PYFA EOS fitting engine to the React Native mobile app.",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the React Native dev client (Metro bundler) to reach the API during
# development without CORS issues.  In production on-device all traffic is
# loopback anyway.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

from backend.api.routes import (  # noqa: E402 — imports after bootstrap
    fits,
    ships,
    market,
    characters,
    stats,
    graphs,
    esi,
    price,
    settings as settings_router,
)

app.include_router(fits.router,       prefix="/fits",       tags=["fits"])
app.include_router(ships.router,      prefix="/ships",      tags=["ships"])
app.include_router(market.router,     prefix="/market",     tags=["market"])
app.include_router(characters.router, prefix="/characters", tags=["characters"])
app.include_router(stats.router,      prefix="/fits",       tags=["stats"])
app.include_router(graphs.router,     prefix="/graphs",     tags=["graphs"])
app.include_router(esi.router,        prefix="/characters/esi", tags=["esi"])
app.include_router(price.router,      prefix="/prices",     tags=["price"])
app.include_router(settings_router.router, prefix="/settings", tags=["settings"])


# ---------------------------------------------------------------------------
# Meta endpoint
# ---------------------------------------------------------------------------

@app.get("/meta/version", tags=["meta"])
async def get_version():
    import config
    return {"version": config.version or "unknown"}


@app.get("/health", tags=["meta"])
async def health():
    """Polled by the React Native startup screen until the backend is ready."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Standalone entry point (for development / Android service)
# ---------------------------------------------------------------------------

def start_server(host: str = "127.0.0.1", port: int = 8765):
    import uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host=host,
        port=port,
        workers=1,
        log_level="info",
    )


if __name__ == "__main__":
    start_server()
