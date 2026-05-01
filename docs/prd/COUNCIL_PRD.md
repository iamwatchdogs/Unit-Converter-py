# Council PRD: Client Unit Conversion Desk

## Document Role

This document records the final technical decision for P01 after reading the client PRD and SME PRD. The council perspective represents a senior developer, a staff engineer, and a senior architect resolving scope, structure, trade-offs, and quality gates. It is intentionally more technical than the client PRD and more decisive than the SME PRD.

## Inputs Reviewed

The council reviewed the client's need for a small local conversion tool, the SME's recommendation to keep the implementation explicit and beginner-friendly, and the portfolio-wide constraints around uv, Ruff, mypy, tests, pre-commit, GitHub Actions, documentation, logging, profiling, and public GitHub publishing.

The strongest signal from the client PRD is that the user wants deterministic answers and helpful errors, not a broad unit platform. The strongest signal from the SME PRD is that the project should teach basic Python boundaries rather than outsource the core learning to a units library.

## Core Technical Decision

The project will be a command-first CLI with a small pure domain layer. The conversion logic will be independent from CLI parsing, logging configuration, and output formatting. The required implementation should be simple enough that a learner can explain every function, but complete enough to pass a professional repository checklist.

The council rejects any design that turns this first project into a framework showcase. Classes are not required. A database is not required. External unit-conversion libraries are not allowed for the core behavior because they remove the central learning exercise.

## Accepted Decisions

| Decision                                    | Rationale                                                                                         |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Use CLI as the only primary interface       | The workflow is one command and one answer; GUI/TUI/API would add ceremony without learning value |
| Use a registry-based design                 | Dictionaries naturally teach lookup, normalization, categories, and data-driven branching         |
| Keep conversion logic pure                  | Pure functions are easy to test and prevent CLI details from contaminating business behavior      |
| Use `argparse` for the first implementation | It is enough for the problem and teaches standard CLI mechanics                                   |
| Use standard-library `logging`              | This starts the logging maturity ladder without hiding configuration complexity                   |
| Use elapsed-time measurement only           | The workload is too small for real profiling, but timing builds measurement habits                |
| Require full tests and type hints           | Small projects are the right place to build quality habits before complexity increases            |

## Rejected Decisions

The council considered using a third-party units package. It was rejected because the first project should force the learner to model aliases, categories, and formulas directly. A package could be discussed in `ANALYSIS.md`, but the core behavior must be implemented by the learner.

The council considered making the tool interactive. It was rejected because a prompt loop would blur the user's clarified CLI expectation and introduce state handling before the learner needs it.

The council considered storing conversion history. It was rejected because persistence belongs later in the portfolio. This project should stay focused on functions, dictionaries, CLI parsing, validation, logging, and tests.

## Architecture Boundary Decision

The codebase should have clear boundaries even if it remains small. A reasonable shape is a domain module for units and conversions, a CLI module for argument parsing and exit-code handling, and a presentation helper for formatting results and errors. The exact file names are implementation freedom, but the boundaries are not optional.

The domain layer must not import the CLI parser, print to stdout, read environment variables, or configure logging. It should accept normalized or raw values, validate them, and return structured results or raise documented domain errors.

The CLI layer may parse strings, call the domain layer, configure logging, render output, and map expected failures to exit codes. It should not duplicate conversion rules.

## Interface Decision

Primary interface: CLI.

The required command shape is:

```bash
unit-convert VALUE FROM_UNIT TO_UNIT
```

The command may include optional flags such as `--precision`, `--verbose`, `--debug`, or `--json`, but optional flags must not be necessary for the basic examples to work. The project must not become a TUI, GUI, web app, API, or service.

## Observability And Profiling Decision

This project is Stage 1. Use native logging and terminal diagnostics only. The logger should show normal diagnostic events only when the user opts in with a flag or configured log level. Normal successful output should remain the conversion result, not a log stream.

Use `time.perf_counter()` for a simple elapsed-time measurement. The measurement can be shown only in debug output or recorded in `ANALYSIS.md`; it should not clutter normal conversion output.

## Error Contract

Expected user errors should be handled deliberately. Unknown units, cross-category conversions, invalid numeric values, missing arguments, and unsupported negative physical quantities should produce clear messages and non-zero exit codes. Unexpected internal errors should not expose raw tracebacks unless debug mode is enabled.

The council recommends documenting a small exit-code contract:

| Code | Meaning                          |
| ---: | -------------------------------- |
|    0 | Conversion succeeded             |
|    1 | User input was invalid           |
|    2 | Command invocation was malformed |
|    3 | Unexpected internal error        |

## Test Strategy

Tests should cover the domain layer first because that is where most correctness risk lives. CLI tests should prove argument parsing, output formatting, help text, and exit codes. Logging tests should be minimal; they should verify that debug or verbose mode emits useful diagnostics without testing every character of a log line.

The suite must include:

- valid length, weight, time, and temperature conversions
- alias normalization
- negative temperature support
- cross-category rejection
- unknown-unit rejection
- invalid-number rejection
- CLI success output
- CLI failure output
- help text presence
- elapsed-time path exercised without asserting a strict duration

## Documentation Decision

The README must be practical. It should show installation, usage, supported categories, supported units, aliases, precision behavior, examples, errors, exit codes, and developer workflow. `ANALYSIS.md` should explain why this project intentionally avoids a broad unit library, persistence, GUI, and deeper profiling. `DESIGN.md` should explain the registry, domain/CLI boundary, and error model.

## Council Verdict

The council approves P01 as a deliberately small but complete Python foundations project. The project is successful when it proves the learner can build a clean, typed, tested, documented CLI around simple domain logic without overengineering.

## References

- [Client PRD](CLIENT_PRD.md)
- [SME PRD](SME_PRD.md)
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [Python time.perf_counter documentation](https://docs.python.org/3/library/time.html#time.perf_counter)
- [uv documentation](https://docs.astral.sh/uv/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [pytest documentation](https://docs.pytest.org/)
