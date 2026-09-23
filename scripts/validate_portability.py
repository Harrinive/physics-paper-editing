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
STALE_ACTIVE_TERMS = re.compile(
    r"\b(?:language_reviewer|math_reviewer|reviewer_model_profile|section_snapshot_id)\b"
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

for directory in SUITE:
    for path in directory.rglob("*.md"):
        if "legacy-v1" in path.parts:
            continue
        match = STALE_ACTIVE_TERMS.search(path.read_text())
        if match:
            fail(f"stale active-v2 term {match.group(0)!r} in {path}")

routing = (ROOT / "adaptive-routing.md").read_text()
for value in (
    "harness_version: 2",
    "execution_path: direct | reviewed",
    "review_profile: standard | high_risk",
    "formal_review_scope: none | changed | dependency_closure | all_in_scope",
    "strong",
    "economy",
    "unknown",
):
    if value not in routing:
        fail(f"adaptive routing lacks {value!r}")

coverage = (ROOT / "language-coverage.md").read_text()
for value in (
    "selective",
    "exhaustive",
    "sentence_results",
    "checked_sentence_ids",
    "principle_hits",
    "chunk_snapshot_id",
):
    if value not in coverage:
        fail(f"language coverage lacks {value!r}")
if "Coverage selects which sentences" not in coverage or "all 15 sentence principles" not in coverage:
    fail("language coverage lacks mandatory canon closure")
for value in ("only when current-snapshot evidence is", "ordinary synchronous direct edit"):
    if value not in coverage:
        fail(f"language coverage does not scope snapshot state: missing {value!r}")

quality = (ROOT / "quality-contract.md").read_text()
for axis in (
    "scientific_fidelity",
    "physics_lead",
    "formal_validity",
    "terminology_notation",
    "prose",
):
    if axis not in quality:
        fail(f"quality contract lacks {axis!r}")
if "Canon binding" not in quality:
    fail("quality contract lacks canon binding")
if "ordinary synchronous direct edit" not in quality:
    fail("quality contract makes snapshot state ambiguous for direct edits")

section_skill = (ROOT.parent / "physics-paper-editing-section" / "SKILL.md").read_text()
for value in ("pause the entire section", "immutable original section"):
    if value not in section_skill:
        fail(f"section contract lacks required source-defect/recovery rule: {value!r}")

chunk_contract = (ROOT.parent / "physics-paper-editing-section" / "chunk-contract.md").read_text()
if "section_candidate_snapshot_id" not in chunk_contract:
    fail("section chunk contract does not identify the candidate snapshot explicitly")

if not re.search(r"unsupported candidate assertion is at least\s+medium risk", routing):
    fail("routing does not classify source-supported scientific repairs")

reviews = (ROOT / "review-prompts.md").read_text()
for value in (
    "Terminology-and-notation reviewer",
    "Principle specialist",
    "FORMAL_REVIEW_SCOPE",
    "exact paths to every applicable canon file",
):
    if value not in reviews:
        fail(f"review assignments lack {value!r}")

runtime = (ROOT / "runtime-contract.md").read_text()
for value in (
    "choice: standing",
    "continue without requesting",
    "Runtime adapter selection",
    "source-original.txt",
    "context revision and applicable object-ledger revision",
    "role_model_policy:",
    "formal_reviewer:",
):
    if value not in runtime:
        fail(f"runtime contract lacks {value!r}")

section_state = (ROOT.parent / "physics-paper-editing-section" / "disk-layout.md").read_text()
for value in (
    "source-original.txt",
    "source-boundaries.json",
    "context revision",
    "context-revision or applicable object-ledger-revision",
):
    if value not in section_state:
        fail(f"section persistence lacks {value!r}")

principles = (ROOT.parent / "physics-paper-principles" / "SKILL.md").read_text()
if "Every principle in an applicable canon file is mandatory" not in principles:
    fail("principles skill does not declare the canon mandatory")

sentence = (ROOT.parent / "physics-paper-principles" / "sentence.md").read_text()
if "Terminology-and-notation delta" not in sentence:
    fail("sentence principles lack terminology-and-notation delta")
if "concise first-use gloss" not in sentence:
    fail("sentence principle 14 does not preserve useful orientation")

math = (ROOT.parent / "physics-paper-principles" / "math.md").read_text()
if "only when the statement's intended meaning" not in math:
    fail("math quantifier audit still makes nontriviality unconditional")

narrative = (ROOT.parent / "physics-paper-principles" / "narrative.md").read_text()
if "Relation chain" not in narrative or "absence of" not in narrative:
    fail("narrative logic detector still requires universal causality")

for name in ("narrative.md", "math.md"):
    active_canon = (ROOT.parent / "physics-paper-principles" / name).read_text()
    if re.search(r"coworker-loop|(?:narrative|math) workers", active_canon, re.I):
        fail(f"retired worker architecture remains in active canon {name}")

physical = (ROOT.parent / "physics-paper-principles" / "physical-lead.md").read_text()
for diagnostic in ("Factor round-trip", "Inline-substitution test", "Payoff test"):
    if diagnostic not in physical:
        fail(f"physical lead lacks {diagnostic!r}")

print("PASS: portable physics-editing v2 static structure checks")
