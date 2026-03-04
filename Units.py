#!/usr/bin/env python3
"""Compare two unit mapping JSON files for differences.

Usage:
    python Units.py [file_a] [file_b]

Defaults:
    file_a = Units.ClaudeSonnet4.6.json
    file_b = Units.GPT-5.2-Codex-Max.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

DEFAULT_A = "Units.ClaudeSonnet4.6.json"
DEFAULT_B = "Units.GPT-5.2-Codex-Max.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_val(val: Any) -> str:
    return json.dumps(val, ensure_ascii=True)


def compare_maps(map_a: Dict[str, Any], map_b: Dict[str, Any]):
    differences = []
    all_keys = set(map_a) | set(map_b)

    for key in sorted(all_keys):
        in_a = key in map_a
        in_b = key in map_b
        if not in_a:
            differences.append(f"Missing in A: {key}")
            continue
        if not in_b:
            differences.append(f"Missing in B: {key}")
            continue

        val_a = map_a[key]
        val_b = map_b[key]
        if val_a != val_b:
            differences.append(
                f"Value diff for {key}: A={format_val(val_a)} vs B={format_val(val_b)}"
            )

    return differences


def list_nulls(label: str, mapping: Dict[str, Any]):
    non_null_count = sum(1 for v in mapping.values() if v is not None)
    null_keys = sorted(k for k, v in mapping.items() if v is None)
    lines = [f"Mapped values in {label}: {non_null_count}\n"]
    if not null_keys:
        lines.append(f"Null values in {label}: none")
        return "\n".join(lines)
    lines.append(f"Null values in {label} ({len(null_keys)}):")
    lines.extend(null_keys)
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    base_dir = Path(__file__).resolve().parent
    path_a = Path(argv[1]) if len(argv) > 1 else base_dir / DEFAULT_A
    path_b = Path(argv[2]) if len(argv) > 2 else base_dir / DEFAULT_B

    if not path_a.exists():
        print(f"File A not found: {path_a}", file=sys.stderr)
        return 1
    if not path_b.exists():
        print(f"File B not found: {path_b}", file=sys.stderr)
        return 1

    map_a = load_json(path_a)
    map_b = load_json(path_b)

    differences = compare_maps(map_a, map_b)
    if differences:
        print("Differences:\n" + "\n".join(differences))
    else:
        print(f"No differences found between\n  {path_a}\nand\n  {path_b}")

    print()
    print(list_nulls("A", map_a))
    print()
    print(list_nulls("B", map_b))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
