# UI/UX Design

In document, we make some curical decision on the look and feel of the application, by defining the user interface and user experience of the application. This includes defining the command-line interface (CLI) of the application, the expected output format, and the behavior of the application in different scenarios.

> [!IMPORTANT]
>
> For the v1 of this application, the design choice of this application has been decided to be a simple command-line interface (CLI) application in a non-interactive mode. Later version might introduce interactive mode and other interfaces based on the updated requirements, but for now we will focus on the simple CLI interface.

The following UI/UX design choices were made after iterating and reevaluating with all the information provided by all the prd docs, REQUIREMENTS.md and `ANALYSIS.md` documents. The design choices were made to ensure that the application is easy to use, intuitive, and provides a good user experience.

## Expected Outcome

Here's a base model of expected output result and scenario,

```bash
# Primary Usage
unit_convert VALUE FROM_UNIT TO_UNIT

# Secordary Usage (i.e., with flags)
unit_convert [--value VALUE] [--from-unit FROM_UNIT] [--to-unit TO_UNIT]
             [--precision PRECISION] [--list-units] [--json] [--debug]
             [--verbose] [--help]
```

### Positive Scenarios

Based on the detailed provided by the requirements and prds, here're the possible positive scenarios

#### Basic Usage

`unit_convert 1 meters kilometers` should print to stdout as `1 meters = 0.001 kilometers`

```bash
# Primary input order would be,
# <VALUE> <FROM_UNIT> <TO_UNIT>
$ unit_convert 1 meters kilometers
1 meter = 0.001 kilometers

# If user is unsure of the order, then they can
# use `--from-unit` and `--to-unit` flags
$ unit_convert --from-unit meters --to-unit kilometers 1
1 meter = 0.001 kilometers
# --- OR ---
$ unit_convert 1 --from-unit meters --to-unit kilometers
1 meter = 0.001 kilometers
# --- OR ---
$ unit_convert 1 --from-unit=meters --to-unit=kilometers
1 meter = 0.001 kilometers

# Along with those flags, user can also use `--value`
# flag to specify the value.
$ unit_convert --value 1 --from-unit meters --to-unit kilometers
1 meter = 0.001 kilometers
# --- OR ---
$ unit_convert --value=1 --from-unit=meters --to-unit=kilometers
1 meter = 0.001 kilometers
```

> [!NOTE]
>
> Remember while printing the output the unit name should be normalized to their canonical form
> and they should be represented based on number unit value for meaningfulness.
> In other words, it should be `1 kilometer` not `1 kilometers`.

#### Alias Inputs

`unit_convert 1 km m` should print to stdout as `1 kilometers = 1000.00 meters`

```bash
# Here `km` means `kilometers` and `m` means `meters`
# thus they have been normalized to kilometers and meters
$ unit_convert 1 km m
1 kilometer = 1000.00 meters

# The canonical form typically are denoted as purals.
# The inputs that are singnular units should be normalized
# to match the canonical form.
$ unit_convert 1 kilometer meter
1 kilometer = 1000.00 meters
```

> [!NOTE]
>
> - The alias should be normalized to their canonical form.
> - If there are no decimal-point values in output, then output should be rounded with the precision of 2 by default.

#### Valid Input value

Typically, all the input values are positive values for time, weight and length units, but temperature units can be negative.

```bash
$ unit_convert -40 celsius fahrenheit
-40 celsius = -40.00 fahrenheit
```

> [!NOTE]
>
> Remember that despite some units of temperature support negative values, they still have a limited range of it.
>
> - Celsius: -273.15
> - Fahrenheit: -459.67

#### Precision

`unit-convert 2 minutes hours --precision 3` should print to stdout as `2 minutes = 0.033 hours`

```bash
$ unit-convert 2 minutes hours --precision 3
2 minutes = 0.033 hours
```

##### Meaningful Precision

`unit-convert 1 seconds hours --precision 3` should print to stdout as `1 seconds = 0.0003 hours`

```bash
# Since the precision is set to 3, the precision of 3
# would result in 0.000 and it wouldn't be meaningful,
# so we round it with precision to give a meaningful
# output as following example:
$ unit-convert 1 seconds hours --precision 3
1 seconds = 0.0003 hours
```

#### JSON Output

`unit-convert 2 minutes hours --precision 3 --json` should pretty print the result to stdout with json format as `{"from": {"value": "2", "unit": "minutes"}, "to": {"value": "0.033", "unit": "hours"}, "precision": "3"}`.

```bash
$ unit-convert 2 minutes hours --precision 3 --json
{
  "from": {
    "value": "2",
    "unit": "minutes"
  },
  "to": {
    "value": "0.033",
    "unit": "hours"
  },
  "precision": "3"
}

# If user didn't specify the precision, then the precision
# should defaults to 2 and it will be part of json result
$ unit-convert 2 minutes hours --json
{
  "from": {
    "value": "2",
    "unit": "minutes"
  },
  "to": {
    "value": "0.03",
    "unit": "hours"
  },
  "precision": "2"
}

# Same thing goes for meaningful precision
$ unit-convert 1 seconds hours --precision 3 --json
{
  "from": {
    "value": "1",
    "unit": "seconds"
  },
  "to": {
    "value": "0.0003",
    "unit": "hours"
  },
  "precision": "4"
}
```

> [!NOTE]
>
> Unlike the previous outputs that print the result to stdout while handling the semantic meaning of `1 kilometer` instead of `1 kilometers`, the JSON output is not meant to be human-readable and it is meant to be machine-readable.

#### Verbose mode

Verbose mode is just printing all the steps of the conversion to stdout. This includes reading inputs, normalizing units, performing conversion, and printing the result.

```bash
# These are sample logs and meant to give an basic idea of what verbose mode would look like.
$ unit-convert 1 seconds hours --precision 3 --verbose
[timestamp] [    INFO     ] Read input values: value=1, from_unit=seconds, to_unit=hours, precision=3, json=True
[timestamp] [    INFO     ] Normalizing units.
[timestamp] [    INFO     ] Performing conversion.
[timestamp] [    INFO     ] Printing result.
{
  "from": {
    "value": "1",
    "unit": "seconds"
  },
  "to": {
    "value": "0.0003",
    "unit": "hours"
  },
  "precision": "4"
}
[timestamp] [    INFO     ] Completed execution in 0.5 seconds.
[timestamp] [    INFO     ] Finished! Exiting with status code 0.
```

#### Debug mode

Debug mode goes further steps than verbose mode, by printing the function names, intermediate values and additional information that can be helpful for debugging the application. When both verbose and debug mode are enabled, the debug mode take the precedence, since verbose mode is a subset of debug mode.

```bash
# These are sample logs and meant to give an basic idea of what verbose mode would look like.
$ unit-convert 1 seconds hours --precision 3 --json --debug
[timestamp] [    DEBUG    ] [func:main] Starting the application in debug mode.
[timestamp] [    DEBUG    ] [func:main] perf counter initialized.
[timestamp] [    DEBUG    ] [func:parse_args] Parsing input args
[timestamp] [    INFO     ] Read input values: value=1, from_unit=seconds, to_unit=hours, precision=3, json=True
[timestamp] [    DEBUG    ] [func:normalize_units] Normalizing units: from_unit=seconds, to_unit=hours
[timestamp] [    INFO     ] Normalizing units.
[timestamp] [    DEBUG    ] [func:perform_conversion] Performing conversion.
[timestamp] [    INFO     ] Performing conversion.
[timestamp] [    DEBUG    ] [func:print_result] Generated json since `--json` flag is enabled.
[timestamp] [    INFO     ] Printing result.
{
  "from": {
    "value": "1",
    "unit": "seconds"
  },
  "to": {
    "value": "0.0003",
    "unit": "hours"
  },
  "precision": "4"
}
[timestamp] [    DEBUG    ] [func:main] Completed execution in 0.5 seconds.
[timestamp] [    INFO     ] Completed execution in 0.5 seconds.
[timestamp] [    INFO     ] Finished! Exiting with status code 0.
```

##### List all units

When user want to see all the available units, they can use `--list-units` flag to print all the available units to stdout.

Despite explicitly mentioned not to use any table format for the output. It's better to have an neat table format to print all the available units, since it is more readable and user-friendly. The table format should have the following columns:

```bash
$ unit-convert --list-units
------------------------------------
| Category    | Unit Name  | Alias |
| -------------------------------- |
| Length      | meter      | m     |
|             | kilometer  | km    |
|             | centimeter | cm    |
|             | mile       | mi    |
|             | yard       | yd    |
|             | foot       | ft    |
|             | inch       | in    |
| - - - - - - - - - - - - - - - -  |
| Weight      | gram       | g     |
|             | kilogram   | kg    |
|             | pound      | lb    |
|             | ounce      | oz    |
| - - - - - - - - - - - - - - - -  |
| Time        | second     | s     |
|             | minute     | min   |
|             | hour       | hr    |
|             | day        | d     |
| - - - - - - - - - - - - - - - -  |
| Temperature | Celsius    | C     |
|             | Fahrenheit | F     |
|             | Kelvin     | K     |
------------------------------------
```

### Negative Scenarios

Based on the detailed provided by the requirements and prds, here're the possible negative scenarios.

> [!IMPORTANT]
>
> Ensure all of the following things are implemented across all the negative scenarios:
> - For all of the following negative scenarios, the application should print an error message to stderr and exit with a non-zero status code.
> - When end user enables verbose mode or debug mode, ensure to properly capture the error message in those modes as well, since it can be helpful for debugging the application.

#### Invalid Input value

If end user provide an invalid input value, then the application should print an error message to stderr and exit with a non-zero status code.
This include all of the following cases:

- Non-numeric value for `VALUE` argument.
    ```bash
    $ unit_convert abc meters kilometers
    Error: Invalid value 'abc'. Please provide a numeric value for conversion.
    Exiting with status code 1.
    ```

- Negative numbers for scalar units (e.g., time, weight, length).
    ```bash
    $ unit_convert -5 meters kilometers
    Error: Invalid value '-5'. Please provide a positive numeric value for conversion.
    Exiting with status code 1.
    ```

- Out of range values for temperature units (e.g., below absolute zero).
    ```bash
    $ unit_convert -300 celsius fahrenheit
    Error: Invalid value '-300'. Temperature cannot be below absolute zero (-273.15 Celsius).
    Exiting with status code 1.

    $ unit_convert -500 fahrenheit celsius
    Error: Invalid value '-500'. Temperature cannot be below absolute zero (-459.67 Fahrenheit).
    Exiting with status code 1.
    ```

- Providing unrecognized units for `FROM_UNIT` or `TO_UNIT` arguments.
```bash
$ unit_convert 1 lightyears kilometers
Error: Unrecognized unit 'lightyears'. Please provide a valid unit for conversion.
Exiting with status code 1.

$ unit_convert 1 xadf aasdf
Error: Unrecognized units 'xadf' and 'aasdf'. Please provide valid units for conversion.
Exiting with status code 1.
```

- Providing cross category units for `FROM_UNIT` and `TO_UNIT` arguments (e.g., converting length to weight).
    ```bash
    $ unit_convert 1 meters grams
    Error: Cannot convert from 'meters' to 'grams'. Please provide units from the same category.
    Exiting with status code 1.

    $ unit_convert 1 hours celsius
    Error: Cannot convert from 'hours' to 'celsius'. Please provide units from the same category.
    Exiting with status code 1.
    ```

- Invalid precision value for `--precision` flag (e.g., negative number, non-integer).
    ```bash
    $ unit_convert 1 meters kilometers --precision abc
    Error: Invalid precision 'abc'. Please provide a non-negative integer for precision.
    Exiting with status code 1.

    $ unit_convert 1 meters kilometers --precision -1
    Error: Invalid precision '-1'. Please provide a non-negative integer for precision.
    Exiting with status code 1.

    $ unit_convert 1 meters kilometers --precision 0.78
    Error: Invalid precision '0.78'. Please provide a non-negative integer for precision.
    Exiting with status code 1.
    ```

##### Command invocation was malformed

If end user provide a malformed command invocation, then the application should print an error message to stderr and exit with a non-zero status code.

Whenever there is a malformed command invocation, the application should also print the usage information to stderr to help the user understand how to properly use the application and display the `--help` information.

This include all of the following cases:

- Missing required arguments (e.g., missing `VALUE`, `FROM_UNIT`, or `TO_UNIT`).
    ```bash
    $ unit_convert meters kilometers
    Error: Missing required arguments. Please provide VALUE, FROM_UNIT, and TO_UNIT for conversion.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert 1 kilometers
    Error: Missing required arguments. Please provide VALUE, FROM_UNIT, and TO_UNIT for conversion.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert 1
    Error: Missing required arguments. Please provide VALUE, FROM_UNIT, and TO_UNIT for conversion.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert
    Error: Missing required arguments. Please provide VALUE, FROM_UNIT, and TO_UNIT for conversion.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.
    ```

- Invalid flags or options (e.g., unrecognized flags, missing values for flags).
    ```bash
    $ unit_convert 1 meters kilometers --precision 3
    Error: Unrecognized flag '--precision'. Did you mean '--precision'?
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert 1 --to=kilometers --from=meters
    Error: Unrecognized flags '--to' and '--from'. Did you mean '--to-unit' and '--from-unit'?
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert --input-value=1 meters kilometers
    Error: Unrecognized flag '--input-value'. Did you mean '--value'?
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert --get-data="https://some-random-url"
    Error: Unrecognized flag '--get-data'.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert 1 meters kilometers --list-units
    Error: Unwanted input arguments. `--list-units` option should not have any input values.
    Usage: unit_covert --list-units
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.
    ```

- Conflicting flags (e.g., providing both positional arguments and flags for the same input).
    ```bash
    $ unit_convert 1 meters kilometers --from-unit meters
    Error: Conflicting input. Please provide either positional arguments or flags for input values, not both.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert 1 --from-unit meters kilometers
    Error: Conflicting input. Please provide either positional arguments or flags for input values, not both.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert 1 meters --to-unit kilometers
    Error: Conflicting input. Please provide either positional arguments or flags for input values, not both.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.

    $ unit_convert --value 1 meters kilometers
    Error: Conflicting input. Please provide either positional arguments or flags for input values, not both.
    Usage: unit_convert VALUE FROM_UNIT TO_UNIT [options]
    Try 'unit_convert --help' for more information.
    Exiting with status code 2.
    ```

#### Unexpected internal error

For any other unexpected internal error, should be handled in this scenarios. Since this application is designed to use mostly by end user who doesn't want to know the technical details, ensure the output stays brief and simple.

```bash
# Assume the following example fails to due some reason.
$ unit_convert 1 kilometers meters
Error: Unknown Internal Error Occurred. Please try again with debug mode.
Exiting with status code 3.
```
