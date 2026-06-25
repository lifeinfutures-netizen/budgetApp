# BudgetApp Agent Guide

## Project Description

BudgetApp is a Python CLI household budget app that stores and reads transactions from CSV files. Core behavior should stay simple, testable, and friendly to command-line workflows.

## Coding Rules

- Use type hints for every function signature.
- Keep each function at 50 lines or fewer.
- Prefer small pure functions for CSV parsing, transaction filtering, balance calculation, and reporting.
- Keep data structures explicit. A transaction should expose clear fields such as `date`, `type`, `category`, `description`, `amount`, and `memo` when those fields are available.

## TDD Rules

- Write the test first before implementing any new behavior.
- Run the new test and confirm it fails for the expected reason before implementation.
- Implement only enough code to make the test pass, then refactor while keeping tests green.

## Quality Rules

- Keep cyclomatic complexity at 10 or below for every function.
- Split branching-heavy logic into smaller functions before complexity grows.
- Do not add broad refactors while implementing a single feature unless the refactor is required to preserve the quality rules.

## Quality Review Rules

- Before every commit, run the `qa_engineer` subagent for quality review.
- The `qa_engineer` review must check tests, type hints, function length, cyclomatic complexity, edge cases, and whether TDD was followed.
- Fix all blocking findings before committing.

## Test Commands

- `pytest`
- `radon cc`

## Commit Rules

- Commit after one feature is developed and verified.
- Push after committing the completed feature.
- Keep each commit focused on one feature or one quality improvement.

