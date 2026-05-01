# SME PRD: Client Unit Conversion Desk

## Document Role

This document translates the client request into feasible project guidance. The SME perspective focuses on unit-conversion scope, Python beginner suitability, tooling choices, testing risks, and the minimum professional workflow expected from the repository. It does not finalize the internal architecture; that is handled by `COUNCIL_PRD.md`.

## SME Interpretation

The client wants a deterministic, local, one-command unit converter. The learning value is not in the conversion formulas alone. The learning value is in turning a tiny problem into a well-structured Python project without hiding behind a framework or growing unnecessary abstractions.

This project should deliberately feel small. The learner should spend time on function boundaries, dictionaries, normalization, exceptions, CLI parsing, logging basics, tests, and documentation. The project should not become a library for every unit system, a GUI, a database-backed tool, or a scientific calculator.

## Feasibility Assessment

The project is feasible for an early Python learner in one to two weeks of free-time work. The domain is familiar, the input size is tiny, and there is no external system dependency. That makes it a strong first project for practicing end-to-end engineering hygiene.

The main risk is overbuilding. A learner may be tempted to install a full units library, generate a large conversion catalogue, or create class hierarchies for every unit. Those choices would hide the intended fundamentals. The recommended implementation is a small explicit conversion registry backed by dictionaries and simple functions.

## Research Findings

Python's standard library already provides the core capabilities needed for this project. `argparse` is the appropriate baseline CLI parser because it is built into Python and teaches the learner how command arguments, options, help text, and exit behavior work without external abstraction. The Python logging module is appropriate at this stage because the project intentionally starts with native logging before later projects introduce higher-level logging libraries. `time.perf_counter()` is the appropriate timing primitive for simple elapsed-time measurement because it is intended for measuring short durations with a high-resolution clock.

`Decimal` is worth considering for parsing and formatting because it avoids some surprising binary floating-point display artifacts. However, making every conversion constant a `Decimal` can distract from the beginner focus. The SME recommendation is to choose one numeric strategy, document it, and test the displayed output. Either `float` plus explicit rounding or `Decimal` plus explicit quantization is acceptable for this first project, as long as behavior is deterministic and explained.

The project should use external tooling for repository quality because the user has made that a portfolio-wide rule. `uv` should manage the project and lock dependencies. Ruff should handle linting and formatting. mypy should type-check the project. pytest and coverage tooling should verify behavior. pre-commit and GitHub Actions should run the same checks before changes are accepted.

## Tooling Options

| Concern     | Recommended baseline  | Optional alternative | SME guidance                                                           |
| ----------- | --------------------- | -------------------- | ---------------------------------------------------------------------- |
| CLI parsing | `argparse`            | Typer or Click       | Start with `argparse`; optionally compare Typer later in `ANALYSIS.md` |
| Output      | Plain text            | Rich                 | Plain text is enough; Rich is optional for clearer error panels        |
| Logging     | `logging`             | none                 | Use native logging now so later projects can compare its pain points   |
| Timing      | `time.perf_counter()` | none                 | No profiler is needed because the workload is trivial                  |
| Testing     | pytest                | unittest             | pytest is consistent with the portfolio workflow                       |
| Packaging   | uv + pyproject        | none                 | Required by portfolio contract                                         |

## Domain Clarifications

The supported unit list should be intentionally small and explicit. The learner should not import a large units database because the goal is to design the conversion map. Every supported unit should have a canonical name, aliases, category, and conversion method.

Length, weight, and time can use base-unit factors. Temperature should use formulas because Celsius, Fahrenheit, and Kelvin do not share a simple multiplication-only relationship. This difference is important for learning because it prevents the learner from assuming every conversion can be represented by one factor.

Aliases should normalize user input before validation. For example, `km`, `kilometer`, and `kilometers` can all resolve to the same canonical unit. Category checking must happen after alias resolution. That order lets the tool distinguish "known but incompatible" from "unknown."

## Logging And Observability Recommendation

This project is Stage 1 in the portfolio's observability ladder. It should use the standard-library `logging` module and terminal-only diagnostics. The learner should configure a logger, emit a few meaningful events, and learn that user-facing output and developer diagnostics are different things.

Recommended events are command start, validation failure, conversion success, and unexpected internal failure. The logs should not include arbitrary business notes or large raw input payloads. Because the tool receives only three arguments, safe diagnostic logging is straightforward.

## Profiling Recommendation

Use `time.perf_counter()` to measure elapsed time for one command execution path. The measurement is educational, not a performance target. The learner should record in `ANALYSIS.md` why deeper profiling is unnecessary: the program performs constant-size dictionary lookups and one formula or multiplication.

No `cProfile`, pyinstrument, benchmark suite, or memory profiler should be required for this project. Those tools appear later when data structures and application workflows make them meaningful.

## Testing Recommendation

The test suite should focus on behavior, not implementation shape. It should prove valid conversions, aliases, cross-category rejection, unknown-unit rejection, invalid-number rejection, negative-temperature support, and CLI help behavior.

Floating-point comparisons should not assert long unrounded decimals. If the implementation uses floats, tests should compare rounded output or use approximate numeric checks. If the implementation uses `Decimal`, tests should assert the documented quantized result.

## SME Recommendation

Build a small CLI around a pure conversion function and a small explicit registry. Keep the domain layer independent from `argparse`, logging, and printing. Use native logging and elapsed-time measurement only. Treat optional Rich output and Typer comparison as extensions after the required behavior is complete.

The project should remain visibly beginner-friendly while still meeting the portfolio's engineering standards. That means typed functions, tests, documentation, linting, formatting, CI, and release automation are required, but large abstractions and broad unit catalogues are not.

## References

- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [Python time.perf_counter documentation](https://docs.python.org/3/library/time.html#time.perf_counter)
- [Python decimal documentation](https://docs.python.org/3/library/decimal.html)
- [uv documentation](https://docs.astral.sh/uv/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [pytest documentation](https://docs.pytest.org/)
- [pre-commit documentation](https://pre-commit.com/)
