# DDR 2: Core System Components

In this document, we will discuss various core system components that are critical for the core logic that we've decided upon. Consider this as a directly continuation of [DDR1](DDR1_CoreSystemLogic). Here're a few things that are currently on para with the current core logic:

- [Use of Decimal](#use-of-decimal)
- [Input validation](#input-validation)
- [Handling precision](#handling-precision)
- [Handling Alias](#handling-alias)

> [!IMPORTANT]
>
> I know this the most simplest and most common project that every beginner deals starts with. So I took a different approach to think about it in a deeper level. If you have read thought this document and have some thoughts to share, I would love to hear them from you, please share your though on the [GitHub Discussion](https://github.com/iamwatchdogs/Unit-Converter-py/discussions/2).

## Use of Decimal

The use of `Decimal` class from python-native `decimal` modules is up for discussion because as many think it could be an overkill for such small project, I believe this is probably one to the right usecase to use this class for precision handling. And we're going to breakdown everything into the following sections to take a closer look,

- [Why do we need to worry about floating point precision?](#why-do-we-need-to-worry-about-floating-point-precision)
- [Why Decimal might be an overkill?](#why-decimal-might-be-an-overkill)
- [Why Decimal will be part of the final design implementation?](#why-decimal-will-be-part-of-the-final-design-implementation)
- [How to use it?](how-to-use-it)

### Why do we need to worry about floating point precision?

I won't be doing in-depth explaining this concept and I'll be pretty vague enough for you to have a fundamental idea of these things to make sense. Here's a small brief for people who don't know/understand how the floating point data are stored in by the modern programming languages:

Generally while storing the integer number, relatively low-level programming languages _(like C)_ stores them, by default, as signed integer of 32-bits where the signed bit is stored as MSB using 2's complement logic. But for better flexibility, modern programming languages _(like python)_ stores them as signed integer of 64-bits by default where most of the most of the bits were allocated for metadata and referential pointers & stuff, so that it can handle the growing number easily and the developer doesn't have to worry about it. Just an FYI, in python specifically, there's no MSB to handle the signed bit instead it stores that info in metadata.

In other words, you can think of integer being stored as two part i.e., signed bit to say whether the number is mathematically positive or negative and then the actual value of then number. But coming to floating-point data, we have an additional part and with a different naming convention called mantissa.

The floating point are stored within memory based on scientific notation where we can express a given floating point number using $mantissa \ (or) \ significand \ (or) \ precision$, $base \ (or) \ radix$ and $exponent$. Basically, we can express the same floating point number using the expression,

$$
floating\text{-}point \ expr = mantissa \times base^{\text{  } exponent}
$$

where,

- $mantissa$ is the actual number value _(include the fractional/decimal part)_.
- $base$ is the number representation or number system _(the number system we use is base-10 i.e., decimal and the number system used by machines is base-2 i.e., binary)_.
- $exponent$ is the value by which we can scale the $base$ value. In other words, it helps us shift the decimial point on a real number from left to right based on value.

This is the current standard used for all programming languages and compuated-based system by default because floating point represent allows us to be more flexible with the fractional part _(value comes after decimal point)_ by modifying the $exponent$. You can think of value of $\pi = 3.14...$, it only has a single number before the decimal point & huge fractional part and in situation like this it's a better trade of use trade more space for the fractional part instead of the integer part. And floating point representation help us achieve the same thing, that is why the dataypes is called `float` it's an shortform for floating-point representation because the decimal point is floating across the space allocated to mantissa _(theortically)_.

To be more practical, this system is implemented using the IEEE-754 standard where the floating-point representation still similar to the scientific notation, but since we're building this for hardware that run on electronic impulses that can be though binary ones and zeroes, the standard suggests that we perform some normalization and then use the following mathematical formula to reconstruct it's original value:

$$
\begin{aligned}
	&(-1)^{\ s} \ \times \ (1 \ . \ M)_{2} \ \times \ 2^{\ E-bias} \\
	\text{where,} \\
	&\begin{aligned}
		s &= \text{signed bit value.} \\
		M &= \text{Normazliaed binary mantissa value.} \\
		E &= \text{Exponent value.} \\
		bias &= \text{Exponent bias value that can compuated using } 2^{n-1}-1 \\
		    &\quad \text{ (where n is bits allocated to the biased exponent value)}
	\end{aligned}
\end{aligned}
$$

> [!NOTE]
>
> Please research about it if you want to know more about what and why it's happening. If I keep on explaining everything, It will take forever to finish this document.

Also just as an FYI, you might or might not have heard about the float16, float32, float64 precision while hearing things about AI/ML (or) maybe you might have also heard about the quantization of local LLM where they make lower the precision of the weights to make them take much lesser space so that it can fit into consumer grade hardware and stuff. It's all possible due to this IEEE754 standard.

So, to answer the main question, do I need to worry about floating point precision? Typically you don't have too, but when it comes to some very niche usecases such as finance, embedded systems, etc. Most of these usecases still used fixed point representation i.e., fixed sized for integer part and decimal part respectively.

And coming to our usecase, it's pretty much on the edge of this decision that needs to be take.

### Why Decimal might be an overkill?

For people who don't know much about `Decimal` from python-native `decimal` module, it's based on General Decimal Arithmetic Specification _(GDA)_ and IEEE 854‑1987 instead of typical binary IEEE754 floating-point representation. So, what difference does this make you might ask...

In typical binary IEEE754 floating-point representation can only maintain actual precision till a certain degree. For example, python uses float64 by default thus maintaining the precision upon 15-digits of fractional part but beyond that it starts to break. In other words, a simple decimal arithmetic operation such $0.1 + 0.2$ would result in $0.30000000000000004$, thus failing to display basic decimal arithmetic of $0.1 + 0.2 = 0.3$. If you check it right now, most of the programming languages that you know might produce similar results i.e., $0.1 + 0.2 \ne 0.3$ due to IEEE754.

> [!TIP]
>
> If you're wondering, "then why would the ML project use float16 _(half precision)_, float32 _(single precision)_ or even float64 _(double precision)_ if the error of unwanted values gets accumulated over operation?"
>
> It's very valid question, but if you think about it the fundamental idea of getting ML algorithm is to make the model better by effective training patterns and algorithms. This is means that despite the possibility of error during the training process, the floating point values gets adjusted to yield better results throughout the process of iteration. Hence, it wouldn't matter if we have some slight error rate that is added way past 15 decimal point precision.
>
> This explain why you might not get the exact sample model weight if you decided to rerun the same workflow from scratch. In order to make the model behaviour more predectiable and reproducible we use concepts such as seeds, etc to make it act a bit more deterministic. But in reailty they're never truly deterministic.
>
> Please do note that all the about concept is specific to training phase and not inferencing, the weights are generally frozen during the inferencing phase so the model produces same results. And the reason why LLMs produce different responses for the same input is total a different reason and the answer lies within the fundamental architecture of how the transformer model is built. The LLMs are probabilistic in nature and we nudge some parameters such as temperature, top-k, etc to force the transformer model to generate more deterministic results.

This is a big no no when it comes to very mission critical usecases such as finance and custom hardware. This is where the General Decimal Arithmetic Specification _(GDA)_ and IEEE854‑1987 stands out.

The IEEE854-1987 highly encourages the idea of radix-independent floating point representation _(primarily using strings)_, thus not limiting to data to be stored and used speciically base-2 number system _(i.e., in binary)_. The GDA, on other hand, encourages the idea of having a controlled context to handle to define the arithmetic model of the decimal defined and used.

To summarize, while IEEE854-1987 is radix/base independent system, the GDA is more specifically for decimal arithmetic thus setting the radix to base-10 by default.

In other words, since we're defining the precision and the arithmetic model, there almost no is possibility of such errors discussed above for greater extends. Thus helping us yield mathematically accurate decimal arithmetic that is directly being computed in base-10 number system i.e., `Decimal('0.1') + Decimal('0.2') = Decimal('0.3')`.

Coming back to the original question, why `Decimal` might be an over kill?

Well, you see it's very critical to have some precision integrity for mission critical usecases like finance, by our usecase is a simple unit converter and all we're trying to make simple conversion.

Consider the fact that, issue might occur when we're dealing with precision over 15 decimal points _(while using the default `float`)_. but until then, `Decimal` might look like an overkill and might be unnecessary bloat to our application.

### Why Decimal will be part of the final design implementation?

Now that we have laid of everything we need to know about why we need `Decimal` and why it could be an overkill, it's try to see why I prefer this to ber part of the final design implementation.

To be honest, I don't have much to say apart from adding more precision for a better accurate and controlled result. It could be an over kill consider the scope of this project since almost none of the conversion logic might not go beyond 15-decimal point precision.

But this is a perfect tool to keep the have a better control over the arithematic model that is being implemented within the this application.

And as a personal reason, I really want to atleast try the `Decimal` since I never really got to use it and since this one an edge whether to included or excluded from the finl design, I tip the plate on favor to be part of the final design implementation.

### How to use it?

Well, all the details and usage of the `Decimal` and the context are clearly mentioned on the [official docs](https://docs.python.org/3/library/decimal.html). But here's a small brief of it:

- **Decimal**: This is class that helps us define the decimal datatype object. It is suggested to provide string input while creating decimal object to avoid the same precision issue.
- **Context**: Based on GDA standard, context allows you to define the arithematic model of how we define and perform operation on decimal objects. This can be achieve multiple ways i.e., by using `getcontext()`, `setcontext()`, `localcontext()`.
- **Signals**: Signals are the important behaviour that ensure certain arithematic operations are handled properly. For example, if we have cleared all the signal traps then division by zero would result in Infinity instead of throwing `DivisionByZero` exception.

Here's a sample code:

```py
from decimal import Decimal, BasicContext, setcontext

# Sets the arithematic model with basic configuration context
setcontext(BasicContext)

x = Decimal(input("Input value: "))

# Assuming c & k values are predefined in the namespace,
# Replicating f(x) = x * c + k,
print(f"result: {x.fma(c, k)}")
```

And for our use case, it's not necessary to set a context because the `DefaultContext` does almost everything that we need. So, all we need to do is need to do is quantaize the end result to the precision provided by the end user.

## Input validation

The main concept of input validation is to ensure the system has more realistic and physically meaningful end results from the out. We can implement so many kind of validations to ensure that the system stay more predictable and align with physical world, but we're only going to validate just enough to stay meaningful to the physical definition.

To be more specific, we are going to implement only two validations i.e.,

- By default, negative number are not accepted _(like there can't be -10km in real physical world)_
- Next specific to temperature unit category as they have physical numerical threshold based on the units.

In anycase, these are the only input validation that we're preforming at the moment. The logic should stay simple and straight-forward while ensuring any changes/refactoring doesn't take greater efforts in the future if the requirement changes.

So, let's start with the very first simplest logic of implementing the validation i.e., using a simple conditional statement which would look something as following,

```py
class NegativeInputError(ValueError):
    pass

# --- In main program ---
if input_value < 0:
    raise NegativeInputError("Please provide a positive integer value.") from None
```

But this is incomplete, because we haven't considered temperature category...

Unlike other physical that doesn't make sense when you says -1.35 seconds, some unit like Celsius and Fahrenheit. And in the real world physical constraints, the temperature has minimum and maximum thresholding value.

Based on what we just discussed, you might thinking of implement minimalistic changes as following:

```py
class ThresholdError(ValueError):
    pass

class UpperLimitExceededError(ThresholdError):
    pass

class LowerLimitExceededError(ThresholdError):
    pass

# --- In main program ---
from_unit_datanode: UnitDataNode = GLOBAL_REGISTRY[from_unit]

if from_unit_datanode.category == UnitCategory.TEMPERATURE:
    if  input_val > max_temp_val:
        raise UpperLimitExceededError(
            "The input is greater than maximum thresholding temperature value."
        ) from None
    if input_val < min_temp_val:
        raise LowerLimitExceededError(
            "The input is lower than minimum thresholding temperature value."
        ) from None
if input_val < 0:
    raise NegativeInputError("Please provide a positive integer value.") from None
```

This could work, but we're missing out a huge part of this logic i.e., the min and max value are not same for all the units. In other words, each temperature unit has it's own min/max values. So, we need to add this logic at a more abstract layer i.e., at class level.

We can achieve this by create a subclass from the current `UnitDataNode` dataclass and then we extend the baseclass to hold on the min & max values. Let's try putting it to code,

```py
@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues

@dataclass(frozen=True, slots=True)
class TemperatureUnitDataNode(UnitDataNode):
    upper_limit: Decimal
    lower_limit: Decimal

    category: UnitCategory = field(init=False, default=UnitCategory.TEMPERATURE)
```

Yea, apart from the thing we discussed, I took the liberaty to set the UnitCategory which is kinda obvious thing to do. Now, if we take this back to this dataclass back to our previous logic,

```py
# --- In main program ---
if from_unit_datanode.category == UnitCategory.TEMPERATURE:
    if  input_val > from_unit_datanode.upper_limit:
        raise UpperLimitExceededError("The input is greater than maximum thresholding temperature value.")
    if input_val < from_unit_datanode.lower_limit:
        raise LowerLimitExceededError("The input is lower than minimum thresholding temperature value.")
if input_val < 0:
    raise NegativeInputError("Please provide a positive integer value.")
```

Yes, we finally achieved our verification. But this looks ugly as hell and we won't want this logic directly on the main driver program.

Well, we can hide all of this within a function like `validate()`, but them you have to pass the `from_unit_datanode` to get the values of `category`, `upper_limit` and `lower_limit` and then you need to the actual `input_value` to perform the total validation. I says it's smelly code when I smell one _(\*cricket noises)_...

Anyway... All I was trying to say is that this is not much scalable. It's not that desirable to write them in such if-else conditions that will grow in spagatti code in future. I am aware that this is a small project and doesn't need to do additional things to perform these checks. And there're better ways to handle it.

So, we start by moving this validation logic as into the dataclass making it as a method that uses the upper and lower limits which are members of the dataclass.

```py
@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues

@dataclass(frozen=True, slots=True)
class TemperatureUnitDataNode(UnitDataNode):
    upper_limit: Decimal
    lower_limit: Decimal

    category: UnitCategory = field(init=False, default=UnitCategory.TEMPERATURE)

    def validate_input(self, input_val: Decimal) -> None:
        if input_val > self.upper_limit:
            raise UpperLimitExceededError(
                "The input is greater than maximum thresholding temperature value."
            ) from None
        elif input_val < self.lower_limit:
            raise LowerLimitExceededError(
                "The input is lower than minimum thresholding temperature value."
            ) from None
```

Now our original logic becomes much more simpler to read and maintain with a slight meaningful cost of coupling the logic _(which is acceptable)_,

```py
# --- In main program ---
if from_unit_datanode.category == UnitCategory.TEMPERATURE:
    from_unit_datanode.validate_input(input_val)
if input_val < 0:
    raise NegativeInputError("Please provide a positive integer value.")
```

That's much better, but for me it's still doesn't feel right...

If you observe close, we're trying to check for the negative value by default and only perform the thresholding logic when it comes to temperature category. So, what if we add the same method within the base class to check for negative number by default and then override this logic within the subclass. This could greatly help us abstract out the logic,

```py
@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues

    def validate_input(self, input_val: Decimal) -> None:
        if input_val < 0:
            raise NegativeInputError("Please provide a positive integer value.") from None

@dataclass(frozen=True, slots=True)
class TemperatureUnitDataNode(UnitDataNode):
    upper_limit: Decimal
    lower_limit: Decimal

    category: UnitCategory = field(init=False, default=UnitCategory.TEMPERATURE)

    @override
    def validate_input(self, input_val: Decimal) -> None:
        if input_val > self.upper_limit:
            raise UpperLimitExceededError(
                "The input is greater than maximum thresholding temperature value."
            ) from None
        elif input_val < self.lower_limit:
            raise LowerLimitExceededError(
                "The input is lower than minimum thresholding temperature value."
            ) from None
```

This is great, now the whole validation logic boils down to,

```py
# --- In main program ---
from_unit_datanode.validate_input(input_val)
```

This is great, we have abstract out the whole logic and it's way more readable. But there's an issue with this approach...

The reason we create/use methods is to perform an reusable action by access the member of that instance. But we're not using any instance member within the baseclass, and theortically it would be far better if we make it as an static method since it doesn't use any instance members and only evaluates based on input value. But we do try to make it as a static method in base class and instance method in child class, there would be a huge inconsistency in how we call these Callables.

Some many call it "necessary evil" to make their lives much simpler and some people will refactor it a little to make it more meaningful to use i.e., adding upper and lower thresholds within the base class itself. The implementation would look something like this:

```py
@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues
    lower_limit: Decimal = Decimal('0')
    upper_limit: Decimal | None = None

    def validate_input(self, input_val: Decimal) -> None:
        if input_val < self.lower_limit:
            raise LowerLimitExceededError(
                "The input is lower than minimum thresholding temperature value."
            ) from None
        elif self.upper_limit is not None and input_val > self.upper_limit:
            raise UpperLimitExceededError(
                "The input is greater than maximum thresholding temperature value."
            ) from None

@dataclass(frozen=True, slots=True)
class TemperatureUnitDataNode(UnitDataNode):
    category: UnitCategory = field(init=False, default=UnitCategory.TEMPERATURE)
```

This may see good and justifiable than pervious logics, but there're huge issues...

- During runtime, one can modify the value of `lower_limit` in the base class instance. And if we try to set a static value and set the `init` to  `False` in the base class, then we need to override it with a default value and set the `init` to `True` in subclass. We have lesser flexibility.
- Since we pushed the unified logic into the base class, we are losing out the `NegativeInputError` exception.
- The values `lower_limit` & `upper_limit` and validation logic is tight coupled with the dataclasses.

To resolve these issue, we can use the concept of composition to decouple this logic. Before that, let's try to understand why we're doing this.

If you look close enough, the members _(`upper_limit`, `lower_limit` and `validate_input`)_ doesn't really feel like exactly part of the container we're trying to keep. The whole logic around it feel like an external factor, trying it's best to be part of the original class. An by add these members, we're guess for all the future hierarchy to expect these members _(values and behaviour)_.

This happens due to "is-a" relationship and this can be resolve using "has-a" relationship. In other words, we move from "this behaviour is what define this class" to "this class has this functionality". To put more simple, we need to make it from "validation is part of the original definition of the dataclass" to "the dataclass has a validator".

If you look close enough, validators are just a small logic that just perform validation based on respective inputs. So, we can break them as an external logic _(maybe like an class or something)_ and add it as an memeber into the existing dataclass via composition.

Since we're outsouring the validation logic, we can use a simple strategy pattern to create some concert strategies for various uses cases and in our case it's for handling non-negative inputs and for handling range based inputs.

And when we put it code, we end up with something as following,

```py
class Validator(Protocol):
    @abstractmethod
    def __call__(self, input_val: Decimal) -> None: ...

@dataclass(frozen=True, slots=True)
class NonNegativeValidator:
    def __call__(self, input_val: Decimal) -> None:
        if input_val < 0:
            raise NegativeInputError("Please provide a positive integer value.") from None

@dataclass(frozen=True, slots=True)
class RangeValidator:
    upper_limit: Decimal
    lower_limit: Decimal

    def __call__(self, input_val: Decimal) -> None:
        if input_val < self.lower_limit:
            raise LowerLimitExceededError(
                "The input is lower than minimum thresholding temperature value."
            ) from None
        elif input_val > self.upper_limit:
            raise UpperLimitExceededError(
                "The input is greater than maximum thresholding temperature value."
            ) from None

@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues
    validator: Validator = field(default_factory=NonNegativeValidator)

    def validate_input(self, input_val: Decimal) -> None:
        self.validator(input_val)

# --- While defining the Global Registry ---
GLOBAL_REGISTRY: Final[Mapping[AvailableUnits, UnitDataNode]] = MappingProxyType({
    "kilometer": UnitDataNode(
        name="kilometer",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=ConstantValues(multiplier=1000.0)
    ),
    "meter": UnitDataNode(
        name="meter",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=ConstantValues(multiplier=1.0)
    ),
    ...,
    "celsius": UnitDataNode(
        name="celsius",
        base_unit="kelvin",
        category=UnitCategory.Temperature,
        constants=ConstantValues(multiplier=1, offset=273.15),
        validator=RangeValidator(lower_limit=Decimal('0'), upper_limit=Decimal('inf'))
    ),
    ...
})
```

This looks much clear and remove unnecessary inheritance when we outsource the validation handling logic to external classes. Since, we are handing off the state management to the validation type class (upper & lower limits), we don't have to worry about handling the them by creating them a subclass from `UnitDataNode`.

> [!TIP]
>
> FYI, `Protocol` is another way to create an interface in python apart from the commonly used `ABC`s. The major difference between the `ABC`s and `Protocol`s are that how they enforce the abstraction mechanism. For `ABC`s, we typically write abstract methods to define the interface and subclass needs to inherit them and override these methods to become concert class thus enforcing normial typing. The `Protocol`s are more into [duck typing](https://www.google.com/search?q=duck+typing&oq=duck+typing) where the logic doesn't necessarily have to be in a hierarchical structure like inheritance, but needs requires to maintain the defined structure.
>
> The reason, I preferred `Protocol`s here compared to `ABC`s is that we're only checking for one specific definition of a single method and do not want to have a strict hierarchical structure of inheritance.

But if you look close enough, these's a huge issue in this implementation. If you look close enough, we're creating unnecessary objects from `NonNegativeValidator` class, when all we need is a simple execute a stateless function. So, we can convert this into a simple function and set it as a default value instead of default factory,

```py
class Validator(Protocol):
    @abstractmethod
    def __call__(self, input_val: Decimal) -> None: ...


def non_negative_validator(input_val: Decimal) -> None:
    if input_val < 0:
        raise NegativeInputError("Please provide a positive integer value.") from None

@dataclass(frozen=True, slots=True)
class RangeValidator:
    upper_limit: Decimal
    lower_limit: Decimal

    def __call__(self, input_val: Decimal) -> None:
        if input_val < self.lower_limit:
            raise LowerLimitExceededError(
                "The input is lower than minimum thresholding temperature value."
            ) from None
        elif input_val > self.upper_limit:
            raise UpperLimitExceededError(
                "The input is greater than maximum thresholding temperature value."
            ) from None

@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues
    validator: Validator = field(default=non_negative_validator)

    def validate_input(self, input_val: Decimal) -> None:
        self.validator(input_val)
```

Now this is way better than unnecessary objects, just for a stateless function call. But now, we have another problem. Yes, the code works without any issue, but it's not consistant. We have a plain function and a class that generates callable objects. So to make it consistant, we need to convert one of them into a similar pattern and since we can't achieve that using calls without bad logic, we have to convert the `RangeValidator` into a function.

But this is not that simple, since `RangeValidator` is not a stateless function. It needs upper and lower limit, so we create this refactor this class from an object factory _(i.e., class)_ to function factory _(i.e., higher order function)_. Since python treats all the functions as first class citizens, we are simply treat them as objects in general _(because they are object indeed)_, so we write a function wrapper that return the function by setting the state recieved as input args.

In other words, Implementation can be simplified as following,

```py
type Validator = Callable[[Decimal], None]

def non_negative_validator(input_val: Decimal) -> None:
    if input_val < 0:
        raise NegativeInputError("Please provide a positive integer value.") from None

def range_validator_factory(/, upper_limit: Decimal, lower_limit: Decimal) -> Validator:
    def validator(input_val: Decimal) -> None:
        if input_val < lower_limit:
            raise LowerLimitExceededError(
                "The input is lower than minimum thresholding temperature value."
            ) from None
        elif input_val > upper_limit:
            raise UpperLimitExceededError(
                "The input is greater than maximum thresholding temperature value."
            ) from None
    return validator

@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues
    validator: Validator = field(default=non_negative_validator)

    def validate_input(self, input_val: Decimal) -> None:
        self.validator(input_val)

# --- While defining the Global Registry ---
GLOBAL_REGISTRY: Final[Mapping[AvailableUnits, UnitDataNode]] = MappingProxyType({
    "kilometer": UnitDataNode(
        name="kilometer",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=ConstantValues(multiplier=1000.0)
    ),
    "meter": UnitDataNode(
        name="meter",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=ConstantValues(multiplier=1.0)
    ),
    ...,
    "celsius": UnitDataNode(
        name="celsius",
        base_unit="kelvin",
        category=UnitCategory.Temperature,
        constants=ConstantValues(multiplier=1, offset=273.15),
        validator=range_validator_factory(
            lower_limit=Decimal('0'),
            upper_limit=Decimal('inf')
        )
    ),
    ...
})
```

Now, this is more pratical and non-smelly code that can be shipped. This also much more scalable and less bloated, now that we have decoupled the logic using strategy pattern.

## Handling precision

For handling precision, we would typically use `round()` function to get the job done. But since we're using `Decimal` datatype it would be better if use the native methods to handle the precision, native methods such as `Decimal.quantize()`.

### `round()` vs `Decimal.quantize()`

Yes, `round()` is still valid and would work for the same purpose, but in the end the `round()` function calls the `Decimal.__round__()` method which hardcodes rounding mode to `MPD_ROUND_HALF_EVEN` _(even if we explicitly set rounding mode to another within the given context of the respective thread)_ and returns an `int` datatype if there's not `ndigit` value else returns a Decimal that is computed by `mpd_qquantize()` function from the **libmpdec** library which part of underlying CPython source that can be found in `_decimal.c`.

> [!TIP]
>
> Just to give you some context, the `round()` function is a higher abstracted function that indirectly calls the dunder method `__round__()` from the input instance that include basic primiative such as int, float, etc. If we try to round an unrealistic datatype such as `str`, it will throw an `TypeError` saying that `__round__()` method is missing.
>
> And for our situation, both `round()` function and `Decimal.quanatize()` method indirectly or directly calls the underlying `mpd_qquantize()` function from the underlying library **libmpdec** that can found within `_decimal.c` source code which is part of original CPython.
>
> I really don't wanna dive too deep into the explain, but just to give you some more context, the **libmpdec** is a low-level C library written by Stefan Krah and this unix naming convention breaks down this library into three part i.e., lib-mp-dec where dec stands for decimal, mp stands for multi-precision and lib stands for library. This library is created and used for performing correctly rounded decimal mathematics.
>
> And the function that is being called by both `Decimal.quantize()` and `round()` is `mpd_qquantize()` which is a low level c function where the mpd stands for multi-precision decimal, q _(before quantize)_ stands for quite _(to quitetly handle the rounding without raising any errors)_ and quantize is change continuous value into fixed values.

And unlike the `round()` function that does all the shenanigans to make the resultant output feel more native to more general pythonic use, the `Decimal.quantize()` methods provides us with more control and directly calls the underlying low level function `mpd_qquantize()` while keeping the end result as Decimal datatype. Don't get me wrong, `round()` solves a particular set of problem which `Decimal.quantize()` solves a different set of problem and for our usecase, `Decimal.quantize()` is the one which perfectly aligns.

### Using `Decimal.quantize()` to handle precision

So, how do we do it using `Decimal.quantize()`? Well, we need another Decimal to provide the precision of the current decimal. For example,

```py
actual_value = Decimal('3.141592653589793')
precision_dec = Decimal('0.001')

resultant_value = actual_value.quantize(precision_dec)
print(resultant_value)      # Output: 3.142 (with default context)
```

But for our usecase we're not hardcoding value such as `precision_dec` for quantize method; the user will be provide the input as an whole number value and not a decimal number as shown in the above example. So, how can we include this graundality? This is where the `scaleb()` method comes in...

The `scaleb()` stands for scale-base and this methods take performs the IEEE754 standard of scaleB operation which is to scale/adjust the exponent value of base/radix of the first operand i.e., $scaleB( x, y ) = x \times base^{y}$. And this IEE754 scaleB operation is implemented in the Decimal class as `x.scaleb(y)`, in other words the default Decimal deals with radix/base of 10 and we adjust the exponent to create the our desired `precision_dec` from the above example.

Let's see this in implementation of the above code snippet example,

```py
input_value = input('Enter the decimal value: ')                        # Assume '3.141592653589793'
precision_value = int(input('Enter the rounding precision value: '))    # Assume '3'

actual_value = Decimal(input_value)
precision_dec = Decimal('1').scaleb(-precision_value)

resultant_value = actual_value.quantize(precision_dec)
print(resultant_value)                                                  # Output: 3.142 (with default context)
```

What happened, why the give negative sign before the `precision_value` and it still works? might be the question popping up in your mind. If you think about it, you do that the answer infront of you.

When we provide a positive number here say `Decimal(1).scaleb(3)`, it would result in `Decimal('1000')` or to be more accurate `Decimal('1E+3')` because it was scaling the exponent on the base-10 radix thus mathematically translating it to $1 \times 10^{3}$. But we need are trying to round of the precision of the decimal point number, so we use put a negative sign before the `precision_value` to get out desired result i.e., `Decimal('0.001')`.

And using that precision decimial, we use the `Decimal.quantize()` method to handle the precision that user has requested. Another thing to note is that, the rounding mode is set to `ROUND_HALF_EVEN` because of the `DefaultContext`. And in this rounding mode, the floating point will be rounded to it's closet even number i.e., 2.5 => 2 and 3.5 => 4. This is also known as Banker's Rounding.

Since the end user might be expecting more of a classicaly text book definition of rounding _(i.e., Symmetric Arithmetic Rounding)_, we need to modify or override the existing mode of rounding with `ROUND_HALF_UP`. The `ROUND_HALF_UP` rounds a given number towards the nearest neighbor, and rounds halfway cases (such as 5) up and away from zero i.e., 2.5 => 3, 3.4 => 3.

Another point to remember is that, precision can also be handled with a negative value both in terms of technical implementation and for physical unit that we're tying to handle. To keep it more simple, we have chosen to avoid handle negative preicision atleast for the v1 version of this application and following the same pattern suggested in the [UIUX.md](../UIUX) docs.

So finally our logic can be translated to reusable function as following,

```py
class InvalidPrecisionError(ValueError):
    pass

def handle_precision(input_val: Decimal, precision_val: int, /, rounding_mode=ROUND_HALF_UP) -> Decimal:
    if precision_val < 0:
        raise InvalidPrecisionError(
            f"Invalid precision '{precision_val}'. Please provide a non-negative integer for precision."
        ) from None
    return input_value.quantize(Decimal(1).scaleb(-precision_val), rounding=rounding_mode)
```

So yea, that pretty much sums up the logic that we're trying to implement.

## Handling Alias

For handling alias, I have given a lot of though on how to implement this approach and after of evaluation I keep ending upon the same simple approach that could work perfectly both in terms of design implementation and performance.

Let's start with the most obvious one...

### Using an additional simple alias dictionary

Well, we just create an additional dictionary that holds the mapping from aliases to concert full unit names that we're using as index for `GLOBAL_REGISTRY`. Then we use a function to get the final `UnitDataNode` from the input value and raise and `KeyError` if we could find it from any of the in any of the data structures we have.

```py
# Assume `GLOBAL_REGISTRY` is already present in the global namespace

LengthUnitAlias = Literal["km", "m", "cm", "mi", "yd", "ft", "in"]
WeightUnitAlias = Literal["kg", "g", "lb", "oz"]
TimeUnitAlias = Literal["d", "hr", "min", "s"]
TemperatureUnitAlias = Literal["C", "K", "F"]

AvailableAlias = LengthUnitAlias | WeightUnitAlias | TimeUnitAlias | TemperatureUnitAlias

class InvalidUnitError(KeyError):
    pass

ALIAS: Final[Mapping[AvailableAlias, AvailableUnits]] = MappingProxyType({
    "km": "kilometer",
    "m": "meter",
    "cm": "centimeter",
    ...
})

def get_unitdatanode(input_val: str) -> UnitDataNode:
   if input_val in GLOBAL_REGISTRY:
      return GLOBAL_RESIGTRY[input_val]

   if input_val in ALIAS:
      return GLOBAL_RESISTRY[ALIAS[input_val]]

   raise InvalidUnitError(f"{input_val} is not a valid unit.") from None
```

So yea, this is might most of us might have imagine implementing the obvious logic that we have discussed. But performance wise this is not the best solution. Yes, dicts are hash tables _(or hashmaps, whatever you want to call them)_ and take $O(1)$ for lookups and retrieving the values. So, what might be the issue you might think?

The answer becomes obvious if you correctly answer the question: "How many total number of times does the lookups happen _(all possible cases)_?"

If think the answer is only two times, you are heavily mistaken. The correct is five times. Yes it's four times because we're checking for the value in dictionary in the conditional `if` statement and then we're also trying to retrieve the value in the return statements.

If it's still not clear for you, let's could the number of total lookup performed in that function:

1. Performed lookup on `GLOBAL_REGISTRY` in the first conditional `if` statement.
2. Performed another lookup for `GLOBAL_REGISTRY` to retrieve the `UnitDataNode` to return the object.
3. Performed lookup on `ALIAS` in the seconds conditional `if` statement.
4. Performed another lookup on `ALIAS` to retrieve the `AvailableUnits` string value that will be used as index for `GLOBAL_REGISTRY`.
5. Performing yet another lookup on `GLOBAL_REGISTRY` using the value from the above step to return the object.

I hope that clears out your doubts. But one can argue that all of then are $O(1)$ and we're doing it like 5 times which still result in $O(1)$. Well, you are not wrong but there's a better way to handle this.

If you remember the [zen of python](https://peps.python.org/pep-0020/), it says "There should be one-- and preferably only one --obvious way to do it." and python gives has an obvious way to handle such scenarios.

Let's see the the preferable and obvious way to implement the solution:

```py
def get_unitdatanode(input_val: str) -> UnitDataNode:
    index_val: str = ALIAS.get(input_val, input_val)
    unit_node: UnitDataNode | None = GLOBAL_REGISTRY.get(index_val)

    if unit_node is None:
        raise InvalidUnitError(f"{input_val} is not a valid unit.") from None

    return unit_node
```

Well, the code speaks for itself but let me break it down anyway. We have used the `dict.get()` method index of `dict.__getitem__()` _(which directly translates to `d[]` where `d` is a sample python dict)_. If you remember this method and how it's different from the indexing using square brackets works then answers becomes obvious to you.

Unlike `dict.__getitem__()` method, the `dict.get()` method accepts an optional argument called `default`. This `default` value is set to `None` by default _(duh, it's called optional for a reason)_. So basically, we can try to retrieve a value if it's present within the dictionary or else it's return the `default` value. So, we can either set some default value or get `None` by default. Hence, it will not throw any `KeyError` by default unlikes `dict.__getitem__()` method.

The best part of all of this take same $O(1)$ time complexity, thus helping us club the conditional lookup and retrieval lookup into a single step. So, we use the `dict.get()` method initial to convert any possible alias value into the acceptable index value for `GLOBAL_REGISTRY` using `ALIAS` and then try to `get` the value from `GLOBAL_REGISTRY` and if we get `None`, then the user didn't provided a proper input unit name or alias thus raising the `InvalidUnitError`.

> [!TIP]
>
> The approach implemented here widely resembles the **"Look Before You Leap"** _(LBYL)_ approach and for what I seen before, many people try to implement LBYL in more imperative way to say true to the definition but I chose more functional way to handle things since it's pretty obvious for the give problem statement.
>
> Some people argue that I should have chosen **"Easier to Ask for Forgiveness than Permission"** _(EAFP)_ approach as it's more pythonic. But I feel like, we should proritize the simplicity and readability of the source code more than choose between pythonic coding or not.

This is the implementation that is going to be part of final design implementation, but before we do that let's see some other

### Using an Unified Registry

The basic idea of having an Unified Registry is to kind of to create a immutiable mappings of dictionary which is derived from both `GLOBAL_REGISTRY` and `ALIAS` where all the full unit names and their aliases will be pointing to the same instance of `UnitDataNode`.

And since, we have merged both `GLOBAL_REGISTRY` and `ALIAS` the input unit name and the possible alias will either be in this dictionary or not, thus only a single call of `dict.get()` could suffice the whole logic.

```py
# Assume `GLOBAL_REGISTRY` is already present within the global namespace.
ALIAS: Final[Mapping[AvailableAlias, UnitDataNode]] = MappingProxyType({
    "km": GLOBAL_REGISTRY["kilometer"],
    "m": GLOBAL_REGISTRY["meter"],
    "cm": GLOBAL_REGISTRY["centimeter"],
    ...
})

type TUnifiedRegistry = Mapping[AvailableUnits | AvailableAlias, UnitDataNode]

UNIFIED_REGISTRY: Final[TUnifiedRegistry] = MappingProxyType(GLOBAL_REGISTRY | ALIAS)
```

But there are huge concerns...

- If we are creating a new dictionary from existing `GLOBAL_REGISTRY` and `ALIAS`, then we're heavily trading space complexity for single boost in time complexity. In other words, we end up with three dictionaries from which we're using only one for actual task, where other two are only used for initialization.
- Say, if we create only the `UNIFIED_REGISTRY` instead of having two `GLOBAL_REGISTRY` and `ALIAS` dictionaries, then it would become harder to maintain. Another major issue within this approach is that we can not point towards the same instance of `UnitDataNode` until it's created.

As you can see, we're having huge tradeoffs just to get a hint of improve in number of looksup performed. Comparing this with, the first obvious solution we came is way better balance between space and time complexity tradeoff.

### Shouldn't alias be part of the `UnitDataNode` instance?

Well, if you think of adding alias as a field in the `UnitDataNode` dataclass it would only make things more difficult.

Would it make sense to add this as a field to the dataclasse? Yes, to an extend. Ok, let me be the devil's advocate for this one to make you understand what I meant by that...

It would be meaningful to have the alias as a field in the `UnitDataNode` dataclass because it more meaningful to have a value close to it's original container of data. It would make more sense, when we add that one particular alias to that one particular instance of the `UnitDataNode` class.

But this comes with a huge cost in terms of lookup... You see, if provide the alias as a field in the object being stored in the `GLOBAL_REGISTRY`, it on the other side of the hashtable or hashmap i.e., we will lose the ability to perform $O(1)$ lookups because we need to go through each and every object present within the `GLOBAL_REGISTRY` checking whether the alias is present or not, thus increasing the time complexity to $O(n)$ _(where n is the total number of units)_.

```py
# Assume if we added alias as an additional field within `UnitDataNode`, then
def get_unitdatanode(input_val: str) -> UnitDataNode:
    unit_node: UnitDataNode | None = GLOBAL_REGISTRY.get(input_val)

    if unit_node is None:
        unit_node: UnitDataNode | None = next(
            (unit for unit in GLOBAL_REGISTRY.values() if unit.alias == input_val),
            None
        )

    if unit_node is None:
        raise InvalidUnitError(f"{input_val} is not a valid unit.") from None

    return unit_note
```

So verdict for this approach is that, as much as it would make sense to be part of that instance it would add up more complexity just for the sake of being semantically right. So, this is a huge no go.

## Conclusion

All of the abstract problems related to the previous DDR have been address with concert implementation and reasoning of why we chose a certain approach. This document successfully address major concerns that are related to the core logic of the application, atleast for the v1 implementation.

## Author's Note

Documenting the whole thought process and evaluating while I process my responses with the facts from online references and AI-suggestions, I was able to make better judgement of choosing the most optimal path I could possible reach for v1 adaptation. As much as I wanted to finish these document and get on with real coding, putting in time to research and evaluate my thought made my objective more clear and backed by more proof of why one could work and another couldn't.

I will be more honest and say that I was not expecting the document and evaluate all my thought would take such significant amount of time. I really do want to finish up with these documents so that I can start working with code and feel more productive, but putting time to document, research, verify, reflect and validate _(while constantly fight my urgues to skip all and get starting with code)_ helped me think, research, reason, evaluate and choose the most optimal outcome that is possible.

Maybe the idea of "each line you're gonna write is going to be pain in the as$ tomorrow" kept me in line and stay focused to help me keep on going while everyone keep chasing the newer, faster and better tech. I'm not gonna lie, I had to be part of this fast-pace thing, so that I can surive in the current market where the dumbest people _(who don't understand the fundamental idea of AI)_ thinks developers are totally optional and the LLMs & tech around it keeps getting better and better.

But even these times I really don't want to lose focus on the concept of building strong foundation on which everything is based on. I really hope that all time that I put into this small project and thinking-researching-reasoning-reflecting would help me in future in one way or the other.

And to the person who is patiently reading all of my docs trying to understand the system, I really hope that you're not only learning the fundamental concepts such as IEEE-754 that I have discussed earlier but also build the required intutation to perform deliberate research and reasoning to support your answers if you want to stay in the IT as a long term goal. I know this not might be the best way to do it, but I personally feel like documenting a lot without any external resource _(unless for research, verification/validation purposes)_ will rewire your mind to build effective system in future.

Just so you know, the reasons why these LLMs _(the dumb guess software)_ are way powerful than there're supposed is because of chain-of-though reasoning. They literally generate words as thinking/reasoning after all the system prompts, context and user input before they generate the actual expected output. So, why don't you do that same to build your chain of reasoning to be more effective? Trust me, we all have some serious hardware and software present between the thick skull and our chain-of-thought works way better than how LLMs work.
