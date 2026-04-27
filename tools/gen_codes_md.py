#!/usr/bin/env python3
"""
Regenerate CODES.md from codes.json.

Run after editing codes.json:

    python3 tools/gen_codes_md.py

Produces a per-category table, browsable on GitHub without running anything.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


SEVERITY_LABEL = {
    "info": "info",
    "warn": "warn",
    "err": "error",
    "cat": "critical",
}


def cell(s: str) -> str:
    """Escape a string for a markdown table cell."""
    return (
        s.replace("\\", "\\\\")
         .replace("|", "\\|")
         .replace("\r", "")
         .replace("\n", " ")
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "lenigma" / "codes.json").read_text())

    groups: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for code, entry in data.items():
        cat = entry.get("category") or "Uncategorised"
        groups[cat].append((code, entry))

    out: list[str] = []
    out.append("# Error code reference")
    out.append("")
    out.append("Auto-generated from `codes.json` by `tools/gen_codes_md.py`. "
               "If you edit `codes.json`, regenerate this file.")
    out.append("")
    out.append(f"**{len(data)} codes** across {len(groups)} categories.")
    out.append("")

    # Table of contents
    out.append("## Categories")
    out.append("")
    for cat in sorted(groups):
        anchor = cat.lower().replace(" ", "-").replace("&", "")
        anchor = "".join(c for c in anchor if c.isalnum() or c == "-")
        anchor = anchor.replace("--", "-").strip("-")
        out.append(f"- [{cat}](#{anchor}) — {len(groups[cat])} codes")
    out.append("")

    for cat in sorted(groups):
        out.append(f"## {cat}")
        out.append("")
        out.append("| Code | Severity | Description | Solutions |")
        out.append("|------|----------|-------------|-----------|")
        for code, entry in sorted(groups[cat]):
            sev_raw = entry.get("severity") or ""
            sev = SEVERITY_LABEL.get(sev_raw, sev_raw)
            desc = entry.get("description", "")
            repairs = entry.get("repairs") or []
            if repairs:
                rep_text = "<br>".join(cell(r) for r in repairs)
            else:
                rep_text = "—"
            out.append(
                f"| `{cell(code)}` | {cell(sev)} | {cell(desc)} | {rep_text} |"
            )
        out.append("")

    (root / "CODES.md").write_text("\n".join(out))
    print(f"wrote CODES.md with {len(data)} entries across "
          f"{len(groups)} categories")


if __name__ == "__main__":
    main()
