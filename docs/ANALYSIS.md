# ANALYSIS

This document analyzes the all the provide requirements and performs the necessary analyzis to determine the scope of the project and bring utmost specificity of expected output. We will use [REQUIREMENTS.md](REQUIREMENTS.md) as primary source of truth for our analysis and back up the details from remaining PRDs.

## Project Scope

This is a simple python-based project that provide a local cli to perform basic unit conversion with a few features and constraints. This project is specifically tailored to be beginner friendly while covering some of the curcial parts of the programming and pythonic concepts.

This is the most simple python project meant for learning. Since the complexity of the project is bare minimum, this help me think, reason and develop the project in a more old-fashion way[^1].

### Domain Logic

This application is a simple unit convertor and it's main job is to help the specified persona in the PRDs to perform basic unit conversion.

> [!TIP]
>
> Unit is a basic means of a universally valid measurment system. It can be used to measure various physically conceptual entities like length, weight, time, temperature, and many more.
>
> We have multiple units of measument for various physical entities because historical, cultural, and practical reasons that evolved over centuries before global standardization.
>
> Due to the long impact of multiple measuments and for legacy support of various research and work done by many people around world, we have come up with standard way to covert various units and normarlize the value for their respective purposes.

After part of this application, the client primary goal is to have a local tool that can be run from a command line and documented clearly enough for a new team member to copy the example commands.

And based on the clients requirements, they specifically mentioned the following units[^2]:

| Category                                     | Example units the client expects                     |
| -------------------------------------------- | ---------------------------------------------------- |
| [Length](#length-conversion-logic)           | meter, kilometer, centimeter, mile, yard, foot, inch |
| [Weight](#weight-conversion-logic)           | gram, kilogram, pound, ounce                         |
| [Time](#time-conversion-logic)               | second, minute, hour, day                            |
| [Temperature](#temperature-conversion-logic) | Celsius, Fahrenheit, Kelvin                          |

#### Length Conversion Logic

Length is a category of unit that is used to measure the distance between two points. Amoungst them, meter, kilometer, centimeter, mile, yard, foot, and inch are the most common units.

Here're the related conversion logic,

- 1 kilometer = 1000 meters
- 1 meter = 100 centimeters
- 1 mile = 1760 yards
- 1 foot = 12 inches
- 1 mile = 5280 feet
- 1 mile = 63360 inches
- 1 yard = 3 feet
- 1 yard = 36 inches
- 1 kilometer = 1.609 mile
- 1 kilometer = 1094 yards
- 1 kilometer = 3281 feet
- 1 kilometer = 39370 inches

| X          | kilometer | meter   | centimeter | mile        | yard      | foot      | inch     |
| ---------- | --------- | ------- | ---------- | ----------- | --------- | --------- | -------- |
| kilometer  | 1         | 1000    | 100000     | 1.609       | 1094      | 3281      | 39370    |
| meter      | 0.001     | 1       | 100        | 0.000621371 | 1.09361   | 3.28084   | 39.3701  |
| centimeter | 0.00001   | 0.01    | 1          | 6.21371e-6  | 0.0109361 | 0.0328084 | 0.393701 |
| mile       | 0.621371  | 1609.34 | 160934     | 1           | 1760      | 5280      | 63360    |
| yard       | 0.0009144 | 0.9144  | 91.44      | 0.000568182 | 1         | 3         | 36       |
| foot       | 0.0003048 | 0.3048  | 30.48      | 0.000189394 | 0.333333  | 1         | 12       |
| inch       | 2.54e-5   | 0.0254  | 2.54       | 1.57828e-5  | 0.0277778 | 0.0833333 | 1        |

In other words,

$$
\begin{aligned}
1 \text{ kilometer} &= 1000.00 &&\text{ meters} \\
&= 100000.00 &&\text{ centimeters} \\
&= 1.60934 &&\text{ miles} \\
&= 1093.61 &&\text{ yards} \\
&= 3284 &&\text{ feet} \\
&= 39370.08 &&\text{ inches}
\end{aligned}
$$

#### Weight Conversion Logic

Weight is a category of unit that is used to measure the mass of an object. Amoungst them, gram, kilogram, pound, ounce are the most common units.

Here're the related conversion logic,

- 1 kilogram = 1000 grams
- 1 pound = 16 ounces
- 1 kilogram = 2.20462 pound
- 1 kilogram = 35.274 ounces

| X        | kilogram  | gram    | pound      | ounce    |
| -------- | --------- | ------- | ---------- | -------- |
| kilogram | 1         | 1000    | 2.20462    | 35.274   |
| gram     | 0.001     | 1       | 0.00220462 | 0.035274 |
| pound    | 0.453592  | 453.592 | 1          | 16       |
| ounce    | 0.0283495 | 28.3495 | 0.0625     | 1        |

In other words,

$$
\begin{aligned}
1 \text{ kilogram} &= 1000.00 &&\text{ grams} \\
&= 2.20462 &&\text{ pounds} \\
&= 35.274 &&\text{ ounces}
\end{aligned}
$$

#### Time Conversion Logic

Time is a category of unit that is used to measure the duration of an event. Amoungst them, second, minute, hour, day are the most common units.

Here're the related conversion logic,

- 1 day = 24 hours
- 1 hour = 60 minutes
- 1 minute = 60 seconds

| X      | day          | hour        | minute    | second |
| ------ | ------------ | ----------- | --------- | ------ |
| day    | 1            | 24          | 1440      | 86400  |
| hour   | 0.0416667    | 1           | 60        | 3600   |
| minute | 0.000694444  | 0.0166667   | 1         | 60     |
| second | 0.0000115741 | 0.000277778 | 0.0166667 | 1      |

In other words,

$$
\begin{aligned}
1 \text{ day} &= 24 &&\text{ hours} \\
&= 1440 &&\text{ minutes} \\
&= 86400 &&\text{ seconds}
\end{aligned}
$$

#### Temperature Conversion Logic

Temperature is a category of unit that is used to measure the temperature of an object. Amoungst them, Celsius, Fahrenheit, Kelvin are the most common units.

Here're the related conversion logic,

|            | Celsius                       | Kelvin                                 | Fahrenheit                             |
| ---------- | ----------------------------- | -------------------------------------- | -------------------------------------- |
| Celsius    | $x$                           | $x + 273.15$                           | $x \times \frac{9}{5} + 32$            |
| Kelvin     | $x - 273.15$                  | $x$                                    | $\frac{9}{5} \times (x - 273.15) + 32$ |
| Fahrenheit | $\frac{5}{9} \times (x - 32)$ | $\frac{5}{9} \times (x - 32) + 273.15$ | $x$                                    |

In other words,

$$
\begin{aligned}
1 \text{ celsius} &= 1 + 273.25 &&\text{ kelvin} &&= 274.15 &&\text{ kelvin} \\
&= 1 \times \frac{9}{5} + 32 &&\text{ fahrenheit} &&= 33.8 &&\text{ fahrenheit}
\end{aligned}
$$

### Functional Requirements

These are the very specific and crucial requirements that are required to be implemented in the project.

- A simple CLI interface with a very basic and minimalist design [^3].
- Coverations of input value from one unit to another unit within the same category [^4].
- Support only length, weight, time, and temperature units [^2].
- Handling input properly [^4], that includes:
  - Esnure user is provding inputs in the correct format.
  - Ensure the input value is a valid value for the input _(that includes negative values for temperature)_.
  - Ensure the input unit is a valid unit for the input.
  - Normarilze the input units to their canonical form.
  - Ensure there is no cross categrory conversion is performed.
- Providing a simple output [^5].
- Properly handling errors and exit status codes [^6].
- Added help flag to provide more details on how to use the application[^7].
- Providing optional features such as precision and json output [^8].
- Adding a logger for verbose and debugging the application [^9].
- Adding a timer as basic profiling tool [^9].

### Non-functional Requirements

These are the requirements that are not directly related to the core functionality of the project.

- Building the project using `uv` package manager [^10].
- Adding relevant unit test and having meaningful test coverage [^11].
- Using `ruff` for linting and `mypy` for type checking [^10].
- Configuring pre-commit hooks [^10].
- Using GitHub Actions for CI/CD [^9].
- Don't overcomplicate or overengineer simple project [^12] [^13] [^14].
- Data persistance is unnecessary, use simple data models [^15].
- Source code should be self-documenting.
- Everything should be neatly documented [^16].


## Appendix

[^1]: [Waterfalls model](https://en.wikipedia.org/wiki/Waterfall_model)

[^2]: [Required Conversion Categories | CLIENT_PRD.md](prd/CLIENT_PRD.md#required-conversion-categories)

[^3]: [Expected User Workflow | CLIENT_PRD.md](prd/CLIENT_PRD.md#expected-user-workflow)

[^4]: [Expected Behaviors | REQUIREMENTS.md](REQUIREMENTS.md#expected-behaviors)

[^5]: [Expected Outcome | REQUIREMENTS.md](REQUIREMENTS.md#expected-outcome)

[^6]: [Error Handling Requirements | REQUIREMENTS.md](REQUIREMENTS.md#error-handling-requirements)

[^7]: [Acceptance Criteria | REQUIREMENTS.md](REQUIREMENTS.md#acceptance-criteria)

[^8]: [Optional Features | REQUIREMENTS.md](REQUIREMENTS.md#optional-features)

[^9]: [Observability And Profiling | REQUIREMENTS.md](REQUIREMENTS.md#observability-and-profiling)

[^10]: [Core Requirements | REQUIREMENTS.md](REQUIREMENTS.md#core-requirements)

[^11]: [Test Strategy | COUNCIL_PRD.md](prd/COUNCIL_PRD.md#test-strategy)

[^12]: [Non-Goals | REQUIREMENTS.md](REQUIREMENTS.md#non-goals)

[^13]: [Architect Guidance | REQUIREMENTS.md](REQUIREMENTS.md#architect-guidance)

[^14]: [Anti-Patterns To Avoid | REQUIREMENTS.md](REQUIREMENTS.md#anti-patterns-to-avoid)

[^15]: [Data Model Requirements | REQUIREMENTS.md](REQUIREMENTS.md#data-model-requirements)

[^16]: [Documentation Requirements | REQUIREMENTS.md](REQUIREMENTS.md#documentation-requirements)
