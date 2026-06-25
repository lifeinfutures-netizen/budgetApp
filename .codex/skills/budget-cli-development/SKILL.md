---
name: budget-cli-development
description: Develop and review the BudgetApp Python CLI household budget project. Use when implementing CSV transaction features, tests, CLI behavior, quality gates, or commit preparation for this repository, especially when TDD, type hints, function length, radon complexity, pytest, and qa_engineer review rules must be followed.
---

# Budget CLI Development

## Overview

Use this skill to work on BudgetApp, a CSV-based Python CLI household budget app. Keep changes test-first, small, typed, and easy to review.

## Workflow

1. Read `AGENTS.md` before changing code.
2. Inspect the relevant sample CSV under `data/` before designing behavior.
3. Write or update tests before implementation.
4. Run the targeted test and confirm it fails for the expected reason.
5. Implement the smallest change that satisfies the test.
6. Run `pytest`.
7. Run `radon cc` and confirm every function remains complexity 10 or below.
8. Before commit, invoke or follow the `.codex/agents/qa_engineer.md` review checklist.
9. Commit one completed feature at a time, then push.

## Coding Rules

- Add type hints to every function signature.
- Keep each function at 50 lines or fewer.
- Prefer small pure functions for parsing, filtering, summaries, and calculations.
- Keep transaction field names stable and explicit.
- Use standard library CSV tools for CSV parsing and writing.

## TDD Rules

- Write tests before implementation.
- Cover normal cases, empty input, malformed or missing CSV values, and numeric conversion when relevant.
- Use sample files in `data/` for realistic fixtures when helpful.
- Do not broaden implementation beyond the behavior covered by the current feature tests.

## Quality Gates

- Run `pytest`.
- Run `radon cc`.
- Keep cyclomatic complexity at 10 or below.
- Use `qa_engineer` before commit to check tests, type hints, function length, complexity, CSV edge cases, and commit readiness.

## Commit Discipline

- Make one focused commit per completed feature.
- Push after the feature commit.
- If Git is unavailable in the local shell, report that clearly and leave the working tree ready for commit.
