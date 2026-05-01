# P01. Client Unit Conversion Desk

| Tier |       Phase        |               Concept                |  Effort   | Interface | Python |
| :--: | :----------------: | :----------------------------------: | :-------: | :-------: | :----: |
| Easy | Python Foundations | Functions, dictionaries, CLI parsing | 1-2 weeks |    CLI    | 3.12+  |

## Source Of Truth

Build from this file. `CLIENT_PRD.md`, `SME_PRD.md`, and `COUNCIL_PRD.md` explain the decision history and rationale. If documents conflict, this `PROJECT_CARD.md` wins for implementation.

## Learning Scope

This project intentionally covers basic Python functions, dictionaries, string normalization, validation, simple exceptions, CLI argument parsing, plain text output, Stage 1 standard-library logging, and basic elapsed-time measurement with `time.perf_counter()`.

It also introduces the professional repository workflow that every later project must keep: uv project management, Ruff linting and formatting, mypy type checking, pytest tests with coverage, pre-commit hooks, GitHub Actions, release automation, and clear documentation.

This project intentionally does not cover persistence, batch files, GUI/TUI design, APIs, external unit libraries, scientific unit catalogues, advanced logging libraries, `cProfile`, concurrency, or complex architecture patterns.

## Learning Objective

Build a small local CLI that converts one value from one supported unit to another supported unit while keeping the conversion logic separate from CLI parsing and output rendering.

The objective is not to memorize conversion factors. The objective is to learn how a small problem becomes a real Python project: normalize input, validate categories, call pure functions, return structured results, map expected failures to helpful messages, and prove the behavior with tests.

## Learning Outcomes

After completing this project, you should be able to explain how dictionaries can act as a simple registry, why aliases must be resolved before category checks, why temperature conversion needs formulas instead of only multiplication factors, and how a domain error differs from a programming bug.

You should also be able to create a uv-based project, expose a console command, configure Ruff and mypy, write CLI and domain tests, reach 100% first-party coverage, set up pre-commit, and run the same checks in GitHub Actions.

## Why This Project

Unit conversion is the right first project because the behavior is obvious but not empty. A calculator is too broad and can become a pile of unrelated operations. A todo app introduces persistence before the learner has practiced clean function boundaries. A file-processing project introduces paths and I/O too early.

This project is better for this slot because it keeps the problem small while still requiring real engineering decisions. The learner must decide how to represent units, how to handle aliases, how to distinguish unknown units from incompatible categories, how to display rounded results, and how to keep the CLI from swallowing the domain logic.

## Problem Statement

Operations staff need a local command for common measurement conversions. They currently use web searches and spreadsheets, which causes inconsistent rounding, copy mistakes, and confusion when a conversion is unsupported.

Build a command-line tool that accepts a numeric value, a source unit, and a target unit. It prints a clear converted result when the request is valid and a clear error when the request is invalid.

## Primary Persona

The primary user is an operations assistant preparing shipment notes. They understand everyday units but should not need to understand Python internals, conversion registries, or stack traces.

This user values short successful output and specific error messages. They do not want an interactive app, a database, an online service, or a long report for a one-line conversion.

## Target System

The project must run on macOS, Linux, and Windows. Path handling is minimal in this project, but all tooling and scripts should still avoid operating-system assumptions.

## Expected Outcome

A user can run:

```bash
uv run unit-convert 10 km miles
```

Expected output should contain equivalent information to:

```text
10 km = 6.2137 miles
```

The exact precision may differ, but it must be documented and tested.

## Project Scope

### Required Scope

- Convert between supported length, weight, time, and temperature units.
- Support documented aliases for common units.
- Reject cross-category conversions.
- Reject unknown units.
- Reject invalid numeric input.
- Reject negative length, weight, or time unless explicitly documented otherwise.
- Allow negative temperatures.
- Provide help text with examples.
- Provide Stage 1 logging through the standard-library `logging` module.
- Measure elapsed time for the command path using `time.perf_counter()`.
- Include tests for domain behavior and CLI behavior.

### Optional Scope

- Add `--precision` to control display rounding.
- Add `--json` output for automation.
- Add Rich formatting for clearer error messages.
- Add a `units` command that lists supported units.
- Add area or volume after the required categories are complete.

### Stretch Scope

- Implement a Typer version on a branch or in `ANALYSIS.md` as a comparison against `argparse`.
- Add a small generated README table of supported units.
- Add shell completion only after the basic command is complete.

## Non-Goals

Do not build currency conversion, live exchange rates, spreadsheet import, batch conversion files, conversion history, user accounts, localization, GUI, TUI, web app, API, database storage, or a scientific unit catalogue.

## Core Requirements

Use uv for project management and commit `uv.lock`. Use Ruff for linting and formatting, mypy for type checking, pytest plus coverage tooling for tests, pre-commit for local checks, and GitHub Actions for CI. Keep all public functions type hinted.

The conversion logic must not depend on CLI parsing or printing. The CLI can parse strings and render messages, but the domain layer must own unit lookup, category validation, and conversion.

## Domain Rules

Length, weight, and time conversions use a base-unit factor model. Temperature conversions use formulas. A unit belongs to exactly one category. Aliases resolve to canonical unit names before validation. Cross-category conversion is invalid even when both units are known.

Display precision is a presentation concern. Internal calculations may use more precision than the final output, but the final output must be deterministic.

## Expected Behaviors

### Valid Length Conversion

```bash
uv run unit-convert 2 km m
```

Expected behavior: prints a result equivalent to `2 km = 2000 m`.

### Valid Time Conversion

```bash
uv run unit-convert 2 hours minutes
```

Expected behavior: prints a result equivalent to `2 hours = 120 minutes`.

### Valid Temperature Edge Case

```bash
uv run unit-convert -40 c f
```

Expected behavior: converts successfully because negative temperatures are valid.

### Cross-Category Error

```bash
uv run unit-convert 10 kilometers kilograms
```

Expected behavior: exits non-zero and explains that a length unit cannot be converted to a weight unit.

### Unknown Unit Error

```bash
uv run unit-convert 5 parsecs meters
```

Expected behavior: exits non-zero if `parsecs` is unsupported, names `parsecs` as the unknown token, and points the user toward supported units.

### Invalid Number Error

```bash
uv run unit-convert abc kg lb
```

Expected behavior: exits non-zero and explains that `abc` is not a valid numeric value.

## Error Handling Requirements

Expected user errors must not produce tracebacks in normal mode. Unknown units, cross-category conversions, invalid numeric values, unsupported negative values, and malformed invocations should each have a clear message and a documented exit code.

Unexpected internal errors should exit with a separate code and a concise diagnostic. If debug mode is implemented, it may show a traceback for developer troubleshooting.

Recommended exit codes:

| Code | Meaning                          |
| ---: | -------------------------------- |
|    0 | Conversion succeeded             |
|    1 | User input was invalid           |
|    2 | Command invocation was malformed |
|    3 | Unexpected internal error        |

## Data Model Requirements

The implementation must represent these concepts clearly:

- canonical unit name
- aliases
- category
- base-unit factor or temperature formula
- conversion request
- conversion result
- expected domain error

These may be dictionaries, dataclasses, named tuples, or simple typed structures. Do not introduce persistence.

## Primary Interface Contract

Primary interface: CLI.

The user provides all required input through command arguments:

```bash
unit-convert VALUE FROM_UNIT TO_UNIT
```

The help output must include supported categories and at least three example commands. Rich formatting is optional only for clearer output; this project must not become a TUI, GUI, API, or service.

## Observability And Profiling

Use Stage 1 observability. Configure standard-library logging, keep logs terminal-only, and make diagnostic output opt-in through a flag such as `--verbose` or `--debug`.

Recommended log events are command start, validation failure, conversion success, and unexpected internal failure. Do not log arbitrary business notes or large raw payloads.

Use `time.perf_counter()` to measure elapsed time for the command path. The timing result may appear only in debug output or in `ANALYSIS.md`. Do not use `cProfile` for this project.

## Documentation Requirements

The repository must include:

| Document          | Required content                                                                              |
| ----------------- | --------------------------------------------------------------------------------------------- |
| `README.md`       | installation, usage, examples, supported units, aliases, precision, errors, exit codes        |
| `ANALYSIS.md`     | requirement interpretation, why the scope is small, numeric strategy, logging/profiling notes |
| `DESIGN.md`       | conversion registry, module boundaries, error model, testing strategy                         |
| `CONTRIBUTING.md` | setup, checks, how to add a unit safely                                                       |

## Repo Expectations

The project must be a public GitHub repository. It must include a license, changelog, issue templates, pull request template, pre-commit configuration, `pyproject.toml`, `uv.lock`, and tests using synthetic examples only.

## Automation Pipeline

GitHub Actions must run on push and pull request. The CI workflow must run Ruff format check, Ruff lint, mypy, pytest, and coverage reporting. A release workflow should build and publish artifacts when a version tag or GitHub release is created, using trusted publishing where applicable.

## Acceptance Criteria

- Valid conversions work for all required categories.
- Aliases resolve before category checking.
- Cross-category conversions fail with a specific message.
- Unknown units fail with a specific message.
- Invalid numeric values fail with a specific message.
- Negative temperatures work.
- Negative length, weight, and time are rejected unless explicitly documented otherwise.
- CLI help includes examples and supported categories.
- Logging is configured through the standard library.
- Elapsed-time measurement exists and is documented.
- Domain logic is testable without invoking the CLI.
- CLI success and failure paths are tested.
- First-party source coverage reaches 100%.
- Ruff, mypy, pytest, and GitHub Actions are configured.

## Physical Constraints

The command should complete effectively instantly for one conversion on a normal laptop. Do not optimize beyond straightforward dictionary lookup and direct calculation. If timing is recorded, use it as evidence that deeper profiling would be unnecessary at this scale.

## Architect Guidance

Keep the design boring. A small conversion registry and pure functions are enough. Let the project teach the discipline of simple boundaries rather than the appearance of architecture.

Do not create one class per unit. Do not let the CLI parser decide conversion rules. Do not duplicate aliases in multiple places. Do not use an external unit library for the required behavior.

## Implementation Freedom

You may choose exact command name, package name, supported aliases, numeric representation, output precision, and whether to use plain text or optional Rich formatting. You may choose whether conversion errors are represented as custom exceptions or result objects.

You may not remove the required categories, skip type checking, skip tests, or move business logic into the CLI handler.

## Anti-Patterns To Avoid

- using a third-party units package for the core behavior
- adding a database for conversion history
- using classes only to look object-oriented
- printing from the domain layer
- accepting invalid cross-category conversions silently
- comparing long floating-point strings in tests
- logging tracebacks to normal users
- turning a one-command CLI into a TUI or GUI

## References

- [Client PRD](prd/CLIENT_PRD.md)
- [SME PRD](prd/SME_PRD.md)
- [Council PRD](prd/COUNCIL_PRD.md)
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [Python time.perf_counter documentation](https://docs.python.org/3/library/time.html#time.perf_counter)
- [Python decimal documentation](https://docs.python.org/3/library/decimal.html)
- [uv documentation](https://docs.astral.sh/uv/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [pytest documentation](https://docs.pytest.org/)
