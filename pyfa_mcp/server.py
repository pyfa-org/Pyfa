from __future__ import annotations

import argparse
from typing import Any

from mcp.server.fastmcp import FastMCP

from .runtime import FitResolutionError, RuntimeConfig, initialize_runtime


def create_server(config: RuntimeConfig | None = None) -> FastMCP:
    resolved_config = config or RuntimeConfig.defaults()
    server = FastMCP(
        "pyfa",
        instructions=(
            "Use this server to inspect Pyfa fits and hulls. "
            "Start with list_fits when you need fit identifiers, then use get_fit_stats or compare_fits."
        ),
    )

    def runtime():
        return initialize_runtime(resolved_config)

    @server.resource("fit://all", mime_type="application/json")
    def fit_index() -> dict[str, Any]:
        return runtime().list_fits()

    @server.resource("fit://{fit_id}", mime_type="application/json")
    def fit_details_resource(fit_id: str) -> dict[str, Any]:
        return runtime().get_fit_details(fit_id)

    @server.resource("ship://{ship_name}", mime_type="application/json")
    def ship_profile_resource(ship_name: str) -> dict[str, Any]:
        return runtime().get_ship_profile(ship_name)

    @server.tool(description="List saved Pyfa fits. Optionally filter by fit or ship name.", structured_output=True)
    def list_fits(query: str | None = None) -> dict[str, Any]:
        return runtime().list_fits(query=query)

    @server.tool(description="Return detailed stats for a saved fit by ID or name.", structured_output=True)
    def get_fit_stats(fit: str) -> dict[str, Any]:
        return runtime().get_fit_details(fit)

    @server.tool(description="Compare two saved fits by ID or name and report the stat deltas.", structured_output=True)
    def compare_fits(fit_a: str, fit_b: str) -> dict[str, Any]:
        return runtime().compare_fits(fit_a=fit_a, fit_b=fit_b)

    @server.tool(description="Create and save a new empty fit from an exact ship type name.", structured_output=True)
    def create_fit(ship_name: str, fit_name: str | None = None) -> dict[str, Any]:
        return runtime().create_fit(ship_name=ship_name, fit_name=fit_name)

    @server.tool(description="Return the baseline stats for an empty hull by exact ship type name.", structured_output=True)
    def get_ship_profile(ship_name: str) -> dict[str, Any]:
        return runtime().get_ship_profile(ship_name)

    @server.prompt(description="Create a comparison workflow prompt for two Pyfa fits.")
    def compare_fits_prompt(fit_a: str, fit_b: str, question: str = "Which fit better matches the intended role, and why?") -> str:
        return (
            f"Use the Pyfa MCP server to compare '{fit_a}' and '{fit_b}'. "
            f"Start with compare_fits, drill into get_fit_stats for any surprising deltas, then answer: {question}"
        )

    @server.prompt(description="Create an analysis workflow prompt for a single fit.")
    def analyze_fit_prompt(fit: str, goal: str = "Summarize the fit's strengths, weaknesses, and best use cases.") -> str:
        return (
            f"Use the Pyfa MCP server to inspect fit '{fit}'. "
            f"Start with get_fit_stats, reference fit://{fit} if you need the full payload, then answer: {goal}"
        )

    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Pyfa MCP server over stdio.")
    parser.add_argument("--game-db", default=None, help="Path to Pyfa eve.db. Defaults to ./eve.db.")
    parser.add_argument(
        "--savedata-db",
        default=None,
        help="Path to the Pyfa saveddata SQLite DB. Defaults to ~/.pyfa/saveddata.db.",
    )
    parser.add_argument(
        "--build-game-db-if-missing",
        action="store_true",
        help="Build eve.db with db_update.py when it is missing from the repository root.",
    )
    args = parser.parse_args(argv)

    config = RuntimeConfig.defaults(
        game_db=args.game_db,
        savedata_db=args.savedata_db,
        build_game_db_if_missing=args.build_game_db_if_missing,
    )

    try:
        initialize_runtime(config)
    except (FileNotFoundError, FitResolutionError, RuntimeError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")

    create_server(config).run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
