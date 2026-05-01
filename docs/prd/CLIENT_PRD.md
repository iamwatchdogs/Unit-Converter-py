# Client PRD: Client Unit Conversion Desk

## Document Role

This document captures the client-facing requirement for the first portfolio project. It is written as the result of several clarification calls with a non-technical operations client. The client describes the problem, the expected behavior, the examples they care about, and the limits of the work. The client does not prescribe internal architecture, libraries, test tooling, or package structure.

## Client Background

The client is a small operations team that prepares shipping notes, internal worksheets, and quick customer responses. Their current process is inconsistent. One person searches the web for a unit conversion, another uses a spreadsheet, and another copies a previous note. These approaches usually work for obvious conversions, but they create avoidable mistakes when abbreviations differ, rounding differs, or the requested units do not belong to the same category.

The client wants a small local tool that gives the same answer every time for the same input. They do not want a website, a database, a login system, a desktop application, or a scientific calculation platform. They want a dependable desk utility that can be run from a command line and documented clearly enough for a new team member to copy the example commands.

## Primary User

The primary user is an operations assistant preparing shipment notes. They understand everyday units such as kilograms, pounds, kilometers, miles, hours, minutes, Celsius, and Fahrenheit. They do not want to learn programming terminology or inspect a configuration file before using the tool.

This user is comfortable following a written command example. They are not comfortable debugging stack traces or guessing why a conversion failed. If they type something unsupported, they expect the tool to say what was wrong and what kind of value would have worked.

## Secondary User

The secondary user is the learner building the project. From the client's point of view, the learner must produce something small but complete. The final tool should look simple from the outside while still showing careful handling of input, errors, rounding, documentation, and repeatable behavior.

## Interview-Derived Clarifications

The first client request sounded like "make a unit converter." After clarification, the client does not need every unit in the world. They need a small, documented list of everyday units and aliases that are common in office work.

The client also clarified that correctness is more important than feature count. If a unit is unsupported, the tool should reject it clearly rather than guessing. For example, if `stone`, `parsec`, or `cup` is not in the supported list, the tool should say so. It should not try to call an external service or silently approximate a result.

The client wants negative temperatures to work because they are valid real-world values. They do not expect negative length, weight, or time to be accepted unless the implementation explicitly documents a reason. The default expectation is that physical quantities such as length, weight, and duration should be non-negative.

The client agreed that rounding can be simple as long as it is consistent and documented. They do not require laboratory-grade precision. They want output that is readable in business notes and predictable in tests.

## Business Problem

The team loses time and introduces mistakes when routine conversions are done manually. The most common problems are wrong category conversions, inconsistent abbreviations, inconsistent decimal places, and unclear answers when a conversion is not supported.

A small local command-line tool solves the problem by giving one consistent conversion path. It should accept a value, a source unit, and a target unit. It should print the converted result when the request is valid, and it should print a helpful message when the request is invalid.

## Expected User Workflow

The user opens a terminal, copies a command from the README, replaces the value and units, and presses Enter. They read either one conversion result or one clear error message.

The tool should not ask follow-up questions interactively. If required input is missing, the user should be shown help text explaining the required shape of the command. This project is command-first CLI, not a TUI and not a form-based application.

## Required Conversion Categories

The client expects the first release to cover common units in these categories:

| Category    | Example units the client expects                     |
| ----------- | ---------------------------------------------------- |
| Length      | meter, kilometer, centimeter, mile, yard, foot, inch |
| Weight      | gram, kilogram, pound, ounce                         |
| Time        | second, minute, hour, day                            |
| Temperature | Celsius, Fahrenheit, Kelvin                          |

The exact supported list may be slightly adjusted by the builder, but the README must state the final list clearly. If a category is removed or reduced, the reason must be documented.

## Examples The Client Cares About

The client specifically wants these scenarios to behave sensibly:

| Scenario                  | Client expectation                                                    |
| ------------------------- | --------------------------------------------------------------------- |
| `10 km miles`             | Prints a mile value with documented precision                         |
| `2 hours minutes`         | Prints `120` or an equivalent formatted result                        |
| `-40 c f`                 | Converts successfully because negative temperatures are valid         |
| `10 kilometers kilograms` | Fails because length cannot become weight                             |
| `5 parsecs meters`        | Fails if `parsecs` is unsupported and says the source unit is unknown |
| `abc kg lb`               | Fails because the value is not numeric                                |

The client does not care whether the command uses `unit-convert`, `convert-units`, or another clear name, as long as the command name is documented and works after installation.

## User Experience Expectations

The normal successful output should be short. The client prefers a line similar to `10 km = 6.2137 miles`. A table is not required for the first release because the tool returns one answer at a time.

Error output should be direct and useful. If the user asks for an impossible category conversion, the tool should name both categories. If the user types an unknown unit, the tool should name the unknown token and point to the supported categories or a supported-units command if one exists.

The client does not want raw Python tracebacks during normal use. A debug mode may exist for the developer, but the default experience should be calm and non-technical.

## Logging And Diagnostics Expectations

The client does not ask for a log file. For this first project, terminal diagnostics are enough. The client is comfortable with an optional `--verbose` or `--debug` flag if the README explains that it is mainly for troubleshooting.

The tool should not log private business notes, shipment descriptions, or arbitrary command history. For this project, the only information worth logging is command start, input validation result, conversion category, and command completion. Even those logs should be simple because the project is meant to teach basic logging, not production observability.

## Performance Expectation

The client expects the tool to feel instant. It converts one value at a time, so performance should not become a design obsession. The only timing expectation is that the learner can measure elapsed time for the command path and record the result as part of the learning exercise.

## In Scope

- A local command-line conversion tool.
- A documented set of supported units and aliases.
- Valid conversions within the same category.
- Helpful rejection of unknown units, invalid numbers, and cross-category conversions.
- Consistent output precision.
- Basic help text with examples.
- Synthetic tests and documentation examples.

## Out Of Scope

- Currency conversion.
- Live exchange rates or online lookup.
- Scientific unit catalogues.
- Spreadsheet import.
- Batch conversion files.
- Persistent history.
- GUI, TUI, web app, or API.
- User accounts.
- Localization.

## Client Definition Of Done

The client will consider the project complete when a new user can install it, run the documented examples, get correct conversions for the supported units, and understand every normal failure message without reading the source code.

The client also expects the project repository to look professional: README, contribution notes, tests, linting, type checking, and automated checks should exist even though the tool itself is intentionally small.
