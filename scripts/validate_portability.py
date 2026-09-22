#!/usr/bin/env python3
"""Validate the portable version-2 physics-editing skill suite."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = (
    ROOT,
    ROOT.parent / "physics-paper-editing-section",
    ROOT.parent / "physics-paper-principles",
)
ADAPTERS = {"runtime-cursor.md", "runtime-codex.md", "runtime-claude.md"}
CORE_FORBIDDEN = re.compile(
    r"\b(?:gpt-[\w.-]+|claude-[\w.-]+)\b|one verifier assignment per sentence",
    re.I,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


required = {
    ROOT: {
        "SKILL.md",
        "adaptive-routing.md",
        "quality-contract.md",
        "scaffolded-mode.md",
        "review-prompts.md",
        "runtime-contract.md",
        "language-coverage.md",
        "portability-test-matrix.md",
        "legacy-v1/LEGACY.md",
        *ADAPTERS,
    },
    ROOT.parent / "physics-paper-editing-section": {
        "SKILL.md",
        "stages.md",
        "cross-skill.md",
        "chunk-contract.md",
        "legacy-v1/LEGACY.md",
    },
    ROOT.parent / "physics-paper-principles": {
        "SKILL.md",
        "physical-lead.md",
        "sentence.md",
        "narrative.md",
        "math.md",
        "legacy-v1/LEGACY.md",
    },
}

for directory, names in required.items():
    for name in names:
        if not (directory / name).is_file():
            fail(f"missing {directory.name}/{name}")

for directory in SUITE:
    skill = directory / "SKILL.md"
    text = skill.read_text()
    if not re.search(r"^name:\s*[-a-z0-9]+$", text, re.M):
        fail(f"invalid name frontmatter: {skill}")

for path in ROOT.glob("*.md"):
    if path.name in ADAPTERS or path.name == "README.md":
        continue
    match = CORE_FORBIDDEN.search(path.read_text())
    if match:
        fail(f"nonportable or v1 token {match.group(0)!r} in active core {path.name}")

routing = (ROOT / "adaptive-routing.md").read_text()
for value in (
    "harness_version: 2",
    "direct | guided | independent",
    "strong",
    "economy",
    "unknown",
):
    if value not in routing:
        fail(f"adaptive routing lacks {value!r}")

coverage = (ROOT / "language-coverage.md").read_text()
for value in ("selective", "exhaustive", "sentence_results", "chunk_snapshot_id"):
    if value not in coverage:
        fail(f"language coverage lacks {value!r}")

quality = (ROOT / "quality-contract.md").read_text()
for axis in ("scientific_fidelity", "physics_lead", "formal_validity", "prose"):
    if axis not in quality:
        fail(f"quality contract lacks {axis!r}")

physical = (ROOT.parent / "physics-paper-principles" / "physical-lead.md").read_text()
for diagnostic in ("Factor round-trip", "Inline-substitution test", "Payoff test"):
    if diagnostic not in physical:
        fail(f"physical lead lacks {diagnostic!r}")

print("PASS: portable physics-editing v2 structure and contracts")
