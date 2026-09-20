#!/usr/bin/env python3
"""Validate the portable physics-editing skill suite without host tooling."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = (ROOT, ROOT.parent / "physics-paper-editing-section", ROOT.parent / "physics-paper-principles")
ADAPTERS = {"runtime-cursor.md", "runtime-codex.md", "runtime-claude.md"}
FORBIDDEN = re.compile(
    r"AskQuestion|\bTasks?\b|run_in_background|readonly:|findings\.jsonl|findings_path|~/.cursor|~/.codex"
)
REQUIRED = {
    ROOT: {"runtime-contract.md", "portability-test-matrix.md", *ADAPTERS},
    ROOT.parent / "physics-paper-editing-section": {"SKILL.md", "README.md"},
    ROOT.parent / "physics-paper-principles": {"SKILL.md", "README.md"},
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


for directory, names in REQUIRED.items():
    for name in names:
        if not (directory / name).is_file():
            fail(f"missing {directory.name}/{name}")

for directory in SUITE:
    skill = directory / "SKILL.md"
    text = skill.read_text()
    if not re.search(r"^name:\s*[-a-z0-9]+$", text, re.M):
        fail(f"invalid name frontmatter: {skill}")
    if "compatibility:" not in text:
        fail(f"missing compatibility frontmatter: {skill}")

for directory in SUITE:
    for path in directory.rglob("*.md"):
        if path.name in ADAPTERS or path.name == "README.md":
            continue
        match = FORBIDDEN.search(path.read_text())
        if match:
            fail(f"platform token {match.group(0)!r} in core file {path}")

contract = (ROOT / "runtime-contract.md").read_text()
for required in ("recommended", "parent", "custom", "user_confirmed", "snapshot_id", "result_path", "agents.json"):
    if required not in contract:
        fail(f"runtime contract lacks {required!r}")

state = (ROOT / "job-state.md").read_text()
for required in ("schema_version", '"event":"completion"', "agent_id", "started_at", "completed_at", "resolution_source"):
    if required not in state:
        fail(f"job-state schema lacks {required!r}")

print("PASS: portable skill suite structure and neutral-core boundary")
