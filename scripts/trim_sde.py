#!/usr/bin/env python3
"""
SDE Trimming Script
===================
Copies only fitting-relevant tables from a full EVE SDE SQLite database
into a smaller output database suitable for bundling in the mobile app.

Usage:
    python scripts/trim_sde.py --input eve_full.db --output backend/data/eve.db

Expected size reduction: ~600 MB full SDE → ~40–60 MB trimmed SQLite.

Tables kept (Section 8 of pyfa-mobile-spec.md):
  invTypes, invGroups, invCategories,
  dgmTypeAttributes, dgmAttributes,
  dgmTypeEffects, dgmEffects,
  invTypeMaterials, mapSolarSystems,
  chrRaces, eveIcons

All other tables are dropped.  Only published=1 invTypes are copied.
All translation columns beyond English are stripped (en-only for v1).
"""

import argparse
import sqlite3
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Tables to include and any WHERE filters to apply
# ---------------------------------------------------------------------------

TABLES: dict[str, str | None] = {
    "invTypes":           "published = 1",
    "invGroups":          None,
    "invCategories":      None,
    "dgmTypeAttributes":  None,
    "dgmAttributes":      None,
    "dgmTypeEffects":     None,
    "dgmEffects":         None,
    "invTypeMaterials":   None,
    "mapSolarSystems":    None,
    "chrRaces":           None,
    "eveIcons":           None,
}

# Columns in these tables that hold non-English translations — drop them
# to reduce size (English suffix is empty string "").
_TRANSLATION_SUFFIXES = ("_de", "_fr", "_it", "_ja", "_ko", "_ru", "_zh")


def _drop_translation_columns(cursor, table: str, columns: list[str]) -> list[str]:
    """Return only the columns that are not localisation-only extras."""
    return [
        c for c in columns
        if not any(c.lower().endswith(suf) for suf in _TRANSLATION_SUFFIXES)
    ]


def _get_columns(cursor, table: str) -> list[str]:
    cursor.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cursor.fetchall()]


def trim_sde(input_path: Path, output_path: Path, verbose: bool = True):
    if not input_path.exists():
        print(f"ERROR: Input database not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()
        if verbose:
            print(f"Removed existing output: {output_path}")

    src = sqlite3.connect(str(input_path))
    dst = sqlite3.connect(str(output_path))

    src.row_factory = sqlite3.Row
    dst.execute("PRAGMA journal_mode=WAL")
    dst.execute("PRAGMA synchronous=NORMAL")

    src_cur = src.cursor()
    dst_cur = dst.cursor()

    total_rows = 0

    for table, where_clause in TABLES.items():
        # Check table exists in source
        src_cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
        )
        if src_cur.fetchone() is None:
            if verbose:
                print(f"  SKIP  {table} (not in source)")
            continue

        all_cols = _get_columns(src_cur, table)
        cols = _drop_translation_columns(src_cur, table, all_cols)
        col_list = ", ".join(f'"{c}"' for c in cols)

        # Read schema from source, rewrite for trimmed columns
        src_cur.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
        )
        create_sql_row = src_cur.fetchone()
        if create_sql_row is None:
            continue

        # Recreate the table in the destination with the kept columns only
        # Rather than parsing the CREATE statement, we use CREATE TABLE AS SELECT
        query = f"SELECT {col_list} FROM \"{table}\""
        if where_clause:
            query += f" WHERE {where_clause}"

        dst_cur.execute(f'DROP TABLE IF EXISTS "{table}"')
        dst_cur.execute(f'CREATE TABLE "{table}" AS {query}')
        dst.commit()

        count_q = f'SELECT count(*) FROM "{table}"'
        if where_clause:
            src_cur.execute(f'SELECT count(*) FROM "{table}" WHERE {where_clause}')
        else:
            src_cur.execute(f'SELECT count(*) FROM "{table}"')
        row_count = src_cur.fetchone()[0]
        total_rows += row_count

        if verbose:
            kept_note = f"(filtered by: {where_clause})" if where_clause else ""
            print(f"  COPY  {table:<28}  {row_count:>8} rows  cols {len(all_cols)}→{len(cols)}  {kept_note}")

    # Rebuild indexes from source for the kept tables
    src_cur.execute(
        "SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL"
    )
    for idx_name, tbl_name, idx_sql in src_cur.fetchall():
        if tbl_name in TABLES and idx_sql:
            try:
                dst_cur.execute(idx_sql)
            except sqlite3.OperationalError:
                pass  # Index may reference dropped columns — skip

    dst.commit()
    dst.execute("VACUUM")
    dst.close()
    src.close()

    input_size_mb = input_path.stat().st_size / 1_048_576
    output_size_mb = output_path.stat().st_size / 1_048_576

    if verbose:
        print()
        print(f"Done.  {total_rows:,} total rows copied.")
        print(f"  Input:   {input_size_mb:.1f} MB  ({input_path})")
        print(f"  Output:  {output_size_mb:.1f} MB  ({output_path})")
        print(f"  Reduction: {(1 - output_size_mb / input_size_mb) * 100:.0f}%")


def main():
    parser = argparse.ArgumentParser(description="Trim EVE SDE for PYFA Mobile")
    parser.add_argument("--input",  required=True, help="Path to full eve_full.db")
    parser.add_argument("--output", default="backend/data/eve.db",
                        help="Output path (default: backend/data/eve.db)")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    trim_sde(
        input_path=Path(args.input),
        output_path=Path(args.output),
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
