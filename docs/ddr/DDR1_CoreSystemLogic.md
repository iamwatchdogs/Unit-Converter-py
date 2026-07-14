# DDR 1: Core System Logic

In this document, we will discuss and evaluate all the possible design implementations to find the most optimal solution for the core logic of the application. After thinking about all the possible design implementations, I have come up with the following implementations:

- [Direct function mapping](#direct-function-mapping)
- [Matrices of Precomputed values](#matrices-of-precomputed-values)
- [Conversion via Normalization Proxy](#conversion-via-normalization-proxy)

> [!NOTE]
>
> These are the raw thought processes that I have spent days choosing the right design implementation for this problem statement, with the given constraints.
> After I had laid out all of my thinking and ended up with these three solutions, I compared them with the existing solution to get a more practical approach to implementation.
>
> Also please mind the naming for the identified, I'm just laying out my raw idea and through process so please bare with me when I try my best to express my chain of though I went through to design this small application.

> [!IMPORTANT]
>
> I know this the most simplest and most common project that every beginner deals starts with. So I took a different approach to think about it in a deeper level. If you have read thought this document and have some thoughts to share, I would love to hear them from you, please share your though on the [GitHub Discussion](https://github.com/iamwatchdogs/Unit-Converter-py/discussions/2).

## Direct function mapping

This is the most basic and straightforward implementation. We're discussing this implementation because we need to state the most obvious solution that every beginner developer implements without thinking. There's also another reason we need to discuss this implementation.

The **direct function mapping** method is simply writing each individual unit conversion logic as its own individual function _(like `km_to_m()`)_. They can wrap them in individual classes for each category or save them in their own modules to differentiate between categories, but the underlying logic is simple, using an individual function for each unique combination.

> [!TIP]
>
> One can say, this is the direct embodiment of the Imperative Paradigm, or to be more specific, the Procedural Paradigm; since we're writing functions where we manually specify how we do conversion.

### Evaluation of First Approach

- The complexity of this approach is very low, since every single combination of units is laid out as individual functions.
- The scalability of this approach is really bad, both abstraction-wise and implementation-wise.
  - If one were to add a new unit to this current system, they would have to write all possible combinations, both `from` and `to`.
  - Since there's no abstraction layer, they need to be manually mapped to the respective inputs.
  - The approach itself is suggesting an implementation where the whole application is tightly coupled to the individual function that we define.
- Maintainability will become a nightmare for this approach, since everything is defined within its own individual functions.
  - It would be easy if we knew the exact issue, but when that's not clear, it would become a nightmare to scroll over multiple conversion functions.
  - Pointing to scalability, we have seen how much worse it can be to add a new unit; now, imagine modifying or removing an existing unit. You have to ensure all combinations are properly updated to provide expected outcomes.
  - In other words, even for a minor change in an abstract unit, we need to perform major refactoring at various parts of the codebase.
  - On the same note, it is difficult to say if all the possible cases are properly handled or not.
- Coming to testability, it's more of a perspective thing but it's pretty straight forward...
  - From one perspective, one could say the testability of the application is good for this approach since all of them are functions, and it's easy to check each function.
  - But I personally think it's a downgrade since we're increasing the test suite for unnecessary functional tests.
  - While testing, you need to have a meaningful test coverage that checks the core functionality, not the very building blocks of the core functionality.
  - It doesn't make any sense to test each function to test the core functionality of the application.
  - But due to the fragility of this approach, we're deemed to test every function, and this doesn't scale well.
- Performance could be compratively great than other approaches.
  - Ok, hear me out. We have no state or no referential data structure or any other fancy compute logic to get the result.
  - The only viable metric that came from this approach is considerable and came up in our discussion, due to zero overhead.
  - **Depending on how one implements this**, one could achieve the best possible performance for this solution. Design-wise, at least.

### Final Verdict of First Approach

<div align="center">

| Metric  | PRD Alignment | Complexity | Scalability | Maintainability | Testability | Performance     |
| ------- | :-----------: | :--------: | :---------: | :-------------: | :---------: | :-------------: |
| Results | Low           | Low        | Low         | Low             | Low         | Relatively High |

</div>

The nature of the design highly promotes tightly coupled and straightforward logic that is not considerate of further extensibility or maintainability, making it more suitable for a purely performance-paced approach that could perfectly fit the scope of this project. I mean, think about it for a second, we're designing a stateless application that evaluates the whole logic per each run, what else could be a more performance-effective solution than this one?

Despite all of this thinking and reasoning, I personally wouldn't proceed with this approach due to major concerns about other metrics. At the end of the day, we're writing code so that other humans can understand, while having a reasonably better approach to achieve better performance. And to put the cherry on top, this type of approach is heavily discouraged on original PRDs and related documents.

## Matrices of Precomputed values

In this approach, we're introducing some minor abstract over the previous approach while introducing the concept of a referential data structure (or) a registry. Here, we break down the concept of how the basic unit conversion formulas work to find some middle ground to introduce a common abstraction for better manageability.

The main concept of the **matrices of precomputed values** is to create a registry of matrices that contains simplified & precomputed values from the original formulas. The fundamental implementation idea is to create multiple matrices per category, where each unique matrix contains precomputed values that can be indexed based on users `from` and `to` unit types.

### How does this work?

Now that you have the base idea, let's take a step back and take a closer look at this approach:

From the previous approach, we have observed that many major concerns and issues exist because we don't have a proper abstraction layer to accommodate various metrics. So, we introduce a layer of abstraction by creating a unified operation logic that makes use of a simple data structure that retrieves precomputed values based on user input unit types as following,

$$
UnitCategory \ Matrix \ =
\begin{array}{cc}
& \begin{array}{cccc} &to_1 && to_2 & \ \ \cdots & to_n \end{array} \\
\begin{array}{r}
&from_1 \\
&from_2 \\
& \ \ \ \ \ \vdots \\
&from_m
\end{array} &
\begin{bmatrix}
pc_{11} & pc_{12} & \cdots & pc_{1n} \\
pc_{21} & pc_{22} & \cdots & pc_2n \\
\vdots & \vdots & \ddots & \vdots \\
pc_{m1} & pc_{m2} & \cdots & pc_{mn}
\end{bmatrix}
\end{array}
\begin{aligned}
&where, \\
&&from_{x} &= \text{ from-unit type of the specific unit category.} \\
&&to_{y} &= \text{ to-unit type of the specific unit category.} \\
&&pc_{xy} &= \text{ precomputed value based on } from_x \text{ unit and } to_y \text{ unit.}
\end{aligned}
$$

Now this is a single matrix for a unique unit category _(like length, mass, or time)_. We need to generate such matrices for all the categories and store them as a unified centralized data structure to access all of them. This can be called the global registry of the application.

```py
class UnitCategory(StrEnum):
    LENGTH      = "length"
    WEIGHT      = "weight"
    TIME        = "time"
    TEMPERATURE = "temperature"

@dataclass(frozen=True, slots=True)
class UnitCategoryData:
    name: str
    units: UnitCategory
    matrix: Final[tuple[tuple[float, ...], ...]]

GLOBAL_REGISTRY: Final[Mapping[UnitCategory, UnitCategoryData]] = MappingProxyType({
    UnitCategory.LENGTH: UnitCategoryData(
        name=UnitCategory.LENGTH.value,
        units=LengthUnits,
        matrix=LengthMatrix
    ),
    UnitCategory.WEIGHT: UnitCategoryData(
        name=UnitCategory.WEIGHT.value,
        units=WeightUnits,
        matrix=WeightMatrix
    ),
    UnitCategory.TIME: UnitCategoryData(
        name=UnitCategory.TIME.value,
        units=TimeUnit,
        matrix=TimeMatrix
    ),
    UnitCategory.TEMPERATURE: UnitCategoryData(
        name=UnitCategory.TEMPERATURE.value,
        units=TemperatureUnit,
        matrix=TemperatureMatrix
    )
})
```

Based on the current design, this abstraction has simplified the implementation within a few specific steps. Let's write some pseudocode to see how we can implement this...

```pascal
GLOBAL GLOBAL_RESIGTRY // Hardcoded with precomputed values as discussed above

FUNCTION convert(input_value, from_unit, to_unit)
  INPUT input_value
  INPUT from_unit
  INPUT to_unit

  SET precomputed_value = getPrecomputedValue(from_unit, to_unit)
  SET result = performOperation(input_value, precomputed_value)   // Keep the `performOperation` function abstract for now

  RETURN result
END FUNCTION

FUNCTION getPrecomputedValue(from_unit, to_unit)
  INPUT from_unit
  INPUT to_unit

  SET category = getCategory(from_unit, to_unit)                  // Keep the `getCategory` function abstract for now
  SET matrix = GLOBAL_RESIGTRY[category][matrix]

  RETURN matrix[from_unit][to_unit]
END FUNCTION
```

Perfect, we have laid out the basic algorithm to make this approach work. Let's test it out with one of the units that we're implementing...

$$
WeightMatrix \ =
\begin{array}{cc}
& \begin{array}{cccc} &kg &&&&&& g &&&&& lb &&&&& oz  \end{array} \\
\begin{array}{r}
&kg \\
&g \\
&lb \\
&oz
\end{array} &
\begin{bmatrix}
1 & 1000 & 2.20462 & 35.274 \\
0.001 & 1 & 0.00220462 & 0.035274 \\
0.453592 & 453.592 & 1 & 16 \\
0.0283495 & 28.3495 & 0.0625 & 1
\end{bmatrix}
\end{array}
$$

$$
\begin{aligned}
&\text{Let's consider, } \\ \\
&&\text{inputValue } &= 50 \\
&&\text{fromUnit } &= \text{Pounds (} lb \text{)} \\
&&\text{toUnit } &= \text{Kilograms (} kg \text{)}
\\
&\text{From } Matrix, \\
&&\text{precomputedValue } &= WeightMatrix \ [lb] \ [kg] \\ \\
&&&= 0.453592 \\ \\
&\text{Piecing everything together,} \\
&&f(x) &= operation \ ( \ x, \text{ precomputedValue }) \\
\text{} \\
&&f(50) &= operation \ ( \ 50, \ 0.453592 \ ) \\ \\
&&&= 50 \ \times \ 0.453592 \\ \\
&&&= 22.6796 \\ \\
&\text{Therefore,} \\
&& 50 \ lb &= 22.6796 \ kg
\end{aligned}
$$

Great, now we know our approach might work out.

But despite all that, we still haven't figured out how to implement the $operation()$ function. One might say, "Why don't you call $operation()$ as $multiplication()$ and implement the solution?"

Well, it's not that simple as you think. And there's a good reason why I called it $operation()$ instead of $multiplication()$ directly.

Let's take a few examples to understand the patterns within the conversion formulas,

$$
\begin{alignedat}{4}
x \text{ km} &= x \times 1000 \text{ m}
\qquad&
x \text{ m} &= x \times \frac{1}{1000} \text{ km}
\qquad&
x \ ^\circ\text{C} &= \left(x \ \times \ \frac{9}{5} + 32 \right) \ ^\circ\text{F}
\qquad&
x \ ^\circ\text{F} &= \left(\frac59 \times (x-32)\right) \ ^\circ\text{C}
\\
&&
&= x \times 0.001 \text{ km}
&
&= \left(x\times1.8+32\right) \ ^\circ\text{F}
&
&= \left(0.555(x-32)\right) \ ^\circ\text{C}
\\
&&&&&&
&= \left(x\times0.555-17.777\right) \ ^\circ\text{C}
\end{alignedat}
$$

If we look closely, the examples can be boiled down to the following patterns,

- Straightforward Multiplication ( $f(x) = x \ \times precomputedValue$ )
- Multiplication with an additive ( $f(x) = x \ \times precomputeValue + someConstantValue$ )

Now you might think these are two different patterns, but this logic can be specified into a single unified formula, i.e.,

$$
\begin{aligned}
&&f(x) &= x \ \times \ c + k \\
&where, \\
&&x &= \text{input value} \\
&&c &= \text{multiplier constant value (or) precomputed value} \\
&&k &= \text{offset constant value (or) additive value}
\end{aligned}
$$

Here $k \in \mathbb{R}$, when offset is zero then it becomes starighforward multiplication. Thus covering all cases.

Now that we have defined our $operation()$ logic properly, we have to update the precomputed matrices to accommodate with logic.

Right now, the matrices has contains only the precomputed values of multiplier (i.e., $c$ from the above equation). So, we expand the dimensionality of existing matices to contain offset value (i.e., $k$ from the above equation) too.

$$
UnitCategory \ Matrix \ =
\begin{array}{cc}
& \begin{array}{cccc} &&to_1 &&\quad\qquad to_2 && \  \ \cdots &&& to_n \end{array} \\
\begin{array}{r}
&from_1 \\
&from_2 \\
& \ \ \ \ \ \vdots \\
&from_m
\end{array} &
\begin{bmatrix}
(c_{11}, \ k_{11}) & (c_{12}, \ k_{12}) & \cdots & (c_{1n}, \ k_{1n}) \\
(c_{21}, \ k_{21}) & (c_{22}, \ k_{22}) & \cdots & (c_{2n}, \ k_{2n}) \\
\qquad \vdots &\qquad \vdots & \ddots &\qquad \vdots \\
(c_{m1}, \ k_{m1}) & (c_{m2}, \ k_{m2}) & \cdots & (c_{mn}, \ k_{mn})
\end{bmatrix}
\end{array}
\begin{aligned}
&where, \\
&&from_{x} &= \text{ from-unit type of the specific unit category.} \\
&&to_{y} &= \text{ to-unit type of the specific unit category.} \\
&&c_{xy} &= \text{ respective multiplier value.} \\
&&k_{xy} &= \text{ respective offset value.}
\end{aligned}
$$

In other words, we are changing our existing `UnitCategoryData` as following:

```py
# ------------- Previous Implementation -------------
@dataclass(frozen=True, slots=True)
class UnitCategoryData:
    name: str
    units: type[Enum]
    matrix: Final[tuple[tuple[float, ...], ...]]

# ------------- Current Implementation -------------
class PrecomputedConstants(NamedTuple):
    multiplier: float
    offset: float = 0.0

@dataclass(frozen=True, slots=True)
class UnitCategoryData:
    name: str
    units: type[Enum]
    matrix: Final[tuple[tuple[PrecomputedConstants, ...], ...]]
```

Now, the only logic that's missing from the whole equation is the finding the unit category to get the correct matrix to index these precomputed values. It's a simple and straight forward logic too,

```py
class UnitNotFound(ValueError):
    pass

class DifferentCategoryUnits(ValueError):
    pass

def find_unit_category(unit: str) -> UnitCategory:
    for category, category_data in GLOBAL_REGISTRY.items():
        if unit in category_data.units.__members__:
            return category

    raise UnitNotFound(f"Invalid {unit} unit.")

def get_category(from_unit: str, to_unit: str) -> UnitCategory:
    from_unit_category = find_unit_category(from_unit)
    to_unit_category = find_unit_category(to_unit)

    if from_unit_category == to_unit_category:
        return from_unit_category

    raise DifferentCategoryUnits(
        f"{from_unit} and {to_unit} are not from the same unit category."
    )
```

Piece everything together, we have a well defined working solution with good enough abstract that "can" scale.

### Optimization

Now that we have properly defined the chain-of-though on how we ended up with current working solution, we need to address the elephant in the room i.e., overhead. This approach has good manageable abstraction than the first approach, but this approach comes with a greater cost.

#### Global Registry

Since we're precomputing the required values that can be compatible with our unified conversion logic, there's relatively low overhead for doing some of repeatitve mathematical logic. But this is not the main issue.

We're loading all of the precomputed values that are not necessary for one specific config of input. Say, If I wanted to convert `hours` to `minutes`, I still have to reassign hardcoded and reconstruct the whole registry even though I want to perform for very one specific input config.

Include to this, we have to worry about the offset values. For most of the unit categories that we're dealing with doesn't need a offset value, the offset value is set to zero for all of them. In other words, we're allocating more space to say that we don't need and additive value.

All of these factors heavily contribute to the amortized cost in a really bad way.

This can not be avoided, since we need to all of the precomputed values need to be present in the application to work like an actual unit converter. So, we have to optimize them as much as possible.

Some of the viable optimization options are:

- Precomplie them using `mypyc`
- Serialize the global resigtry as pickle file.
- Break them down into dense and sparse matrices.
- Refactor the existing logic to have an offset flag to handle based on the situation.

And all of these options add unnecessary complexity for such simple project. Not to mention, all of these options are out of the scope and highly discouraged by the PRDs.

#### Unit Category Search

The existing logic for searching unit category is pretty good enough since it's almost like a linear search on a Hashset _(since we're searching among enum members)_. The only possible bad case is when there is not valid unit, which leads to $O(n)$ (where $n$ is the number of unit category) complexity.

One could say we could optimize it further by making while combining it with generator where we lazy load the data based on requirement, but it's overkill for such small dataset that we deal here and we would have far better performance when we using simple straight forward logic in situations like this...

### Evaluation of Second Approach

- The complexity of this approach is low-moderate to moderate, since we have introduced some abstract but it has a proper structure.
- The scalability of this approach is not that great,
  - It's not that great because as we add new units, the matices grow in size.
  - we might save in terms of execution speed since, precomputed values are indexed at $O(1)$ complexity but the space complexity is $O(n^2)$ (where $n$ is the number of units within a category).
  - Not to mention, the current nomarlize conversion logic (i.e., $f(x) = x \times c + k$) is a simple linear equation that works well for most set of unit categories. But epicly fails when it comes to any non-linear components such as exponential or logrithmic conversions used for units like decibles.
- Maintainability is relativity good compared to first approach, but it's still bad.
  - Since we have introduced a proper structure with the abstraction layer, it is more maintainability compared to previous approach.
  - Unlike first approach, you don't have to make huge refactors to the code base to make modification to existing logic or extend the compatible features.
  - But on the flip side, we're blindly trusting these precomputed values in terms of application and that could be a huge issue.
  - Maintaining the precomputed values can become little bit tough despite all of the values are placed in a single data structure.
- Coming to testability, it has greatly improved due since we have properly defined our abstraction. Thus makes it more easier have meaningful test coverages.
- And as of performance, it's a bit complicated...
  - Yes, we have best approach for getting category, we have precomputed values that can be indexed at $O(1)$ and the even the generalized formula takes $O(1)$. So it's the best possible solution right.
  - Yes, it's best solution in terms of theortical speed of the algorithm. But not that great, when it's comes to space complexity and the amortized cost.
  - For each run we're building and destroying the resgitry that contains badly set of badly-scalable data structures, this create a huge overhead that many might not realize.
  - To accommodate this we have some set of optimization, but they are out of the scope in terms of PRD.
  - Overally, the base approach gives moderate performance on average. But there could possibly be some cases where this approach can outperform the first approach.
- This approach is more aligned to the approaches suggested by the PRDs. Despite the PRDs being very vague about the resgitry concept, the correct approach satisfies the specified requirement.

### Final Verdict of Second Approach

<div align="center">

| Metric  | PRD Alignment | Complexity        | Scalability | Maintainability | Testability | Performance |
| ------- | :-----------: | :---------------: | :---------: | :-------------: | :---------: | :---------: |
| Results | High          | Low-to-Moderate   | Low         | Moderate        | High        | Moderate    |

</div>

Compared to the first approach, this is a huge improvement in multiple areas. This approach has a better structure that is mathematically sounding with a reasonable performance and most importantly perfectly aligns with the PRD requirements. This could a be a perfect solution to implement if this was meant for only learning purposes.

Despite all of this, I feel like there has to be a better way to implement build the unit converter. This is a really good approach that could be really fun to implement since they perfectly align with the PRDs. But when I think about it long enough, this is not pretty scalable and may not be worth of being part of something that might go for production.

I know, the whole point of this is to learn but I feel the system should be have a marginally smaller tradeoff to perfect scale and still maintain marginally good performance.

## Conversion via Normalization Proxy

In this approach, we will try to solve the same problem while keeping the fundamental idea of having a global registry but with a completely different ideaology. Here's instead of treating units as indexes, we see them more as node on a graph which feels similar to the [Hub-and-Spoke model](https://www.google.com/search?q=Hub-and-Spoke+model&oq=Hub-and-Spoke+model "what is hub-and-spoke?").

If it's not clear by the name of this approach, we are trying to have a proxy conversion by normalizing the input unit to a base unit and then we convert it back to the expected unit. That's pretty much the idea.

Yes, it does add an addition step to perform conversion but this approach is more flexible and scalable both in terms of units and categories. Since, we're identifying them as nodes (like $km \ (from) \ \rightarrow m \ (base) \ \rightarrow ft \ (to) \ $) we don't have to perform an additional search to find their category to later find and index the unit _(like in previous approach)_.

Similar to previous approach, we're maintaining a global registry and have some generalized formulas/operations that can perform the required conversion logic across multiple units from multiple categories. But having this simple shift in mathematical model, we can redesign the system to be more scalable, flexible and possibly the most optimal approach which can be good enough to be part of production system.

### How does this work?

Now that we have properly understood the base idea, let's see how it can be implemented...

In this approach, we are converting the input unit value into base unit and the base unit to the targeted output unit. So, we need two functions (i.e., one for normalization and another for denormalization) and set of constant values for the functions.

If you think about it, we do have a generalized formula that can convert from one unit to another (i.e., $f(x) \ = \ x \times \ c + k$) and if we want to make this formula work, then we need to have $c$ and $k$ values both ways. But if we think about it that way it will take us back to the old ways of second approach.

So if we want to use this generalized formula as normalization formula, we need to have an equivalent and opposite formula that results in starting value i.e., $g(f(x)) = x$. In other words, we need to derive an working inverse function for this generalized formula.

Let's derive the inverse function using basic pre algebra,

$$
\begin{aligned}
  \begin{aligned}
    \text{We are familiar with,} \\
      &\begin{aligned}
        &f(x) \ = \ x \times c + k \\
      where, \\
        &x \ = \ \text{ input value.} \\
        &c \ = \ \text{ multiplier constant.} \\
        &k \ = \ \text{ offset value.} \\
      \end{aligned} \\
    \text{Consider the following,} \\
      &\begin{aligned}
        &f(x) \  = \ y \\
        &g(a) \ = \ f^{-1}(a) \\
        \text{} \\
        &g(y) \ = \ g(f(x)) \ = \ f^{-1}(f(x)) \ =  \ x \\
      where, \\
        &f = \text{ same function as above.} \\
        &g = \text{ inverse function of } \mathbb{f} \text{.} \\
        &x = \text{ constant input value.} \\
        &y = \text{ constant output value.} \\
        &a = \text{ any substitutable value or expression} \\
      \end{aligned} \\
    \text{Let's derive the inverse function,} \\
      &\begin{aligned}
          f(x) &= x \times c + k \\
          y &= x \times c + k \\
          y - k &= x \times c \\
          \frac{y-k}{c} &= x \\
          x &= \frac{y-k}{c} \\
          f^{-1}(f(x)) &= \frac{y-k}{c} \\
          g(f(x)) &= \frac{y-k}{c} \\
          g(y) &= \frac{y-k}{c} \\
      \end{aligned} \\
    \text{Therefore,} \\
      &\begin{aligned} \\
     	  &f(x) &= x \times c + k &= y \\
        &g(y) &= \frac{y-k}{c} &= x \\
      \end{aligned} \\
  \end{aligned} \\
  \text{} \\
  \mathbb{g} \text{ is the inverse function derived from } \mathbb{f} \text{, }
  \text{where given the same constant values } \mathbb{c} \text{ and } \mathbb{k} \\
  f(x) \text{ can reproduce the value of } \mathbb{y} \text{ and } g(y) \text{ can reproduce the value of } \mathbb{x} \\
\end{aligned} \\
$$

Nice, now we have both normalization and denormalization functions. Let's test it out with an example,


$$
\begin{aligned}
  \begin{aligned}
  &\text{} \\
	\text{We know that,} \\
	\qquad\qquad\qquad\begin{aligned}
	  &\begin{aligned}
  		f(x) &= x \times c + k &= y \\
  		g(y) &= \frac{y - k}{c} &= x \\
	  \end{aligned} \\
		where, \\
    &\begin{aligned}
		  f &= \text{ the normalization function.} \\
      g &= \text{ the denormalization function.} \\
      x &= \text{ input value.} \\
      y &= \text{ output value.} \\
      c &= \text{ multiple constant value.} \\
      k &= \text{ offset constant value.} \\
    \end{aligned} \\
  \end{aligned} \\
  \text{} \\
  \text{Let's convert 5 hours to minutes,} \\
  \text{} \\
  \qquad\qquad\qquad\qquad\qquad\begin{aligned}
    x &= \ 5 \ hours \\
    y &= \ ? minutes
  \end{aligned} \\
  \text{} \\
  \text{From the precomputed values,} \\
  \text{} \\
	\qquad\qquad\qquad\qquad\qquad\begin{aligned}
    c &= 60 \\
    k &= 0
	\end{aligned} \\
  \text{} \\
  \text{Converting from hours to minutes,} \\
  \text{} \\
	\qquad\qquad\qquad\begin{aligned}
    \qquad\begin{aligned}
      f(x) &= x \times c + k \\
      \text{} \\
      f(5) &= 5 \times 60 + 0 \\
      y &= 5 \times 60 \\
      y &= 300
    \end{aligned} \\
    \begin{aligned}
      \text{Thus, 5 hours = 300 minutes}
    \end{aligned}
	\end{aligned} \\
  \text{} \\
  \text{Now, let's convert from minutes to hours using } \mathbb{g} \text{,} \\
  \text{} \\
  \qquad\qquad\qquad\begin{aligned}
    \qquad\begin{aligned}
      g(y) &= \frac{y - k}{c} \\
      \text{} \\
      g(300) &= \frac{300 - 0}{60} \\ \\
      x &= \frac{300}{60} \\ \\
      x &= 5
    \end{aligned} \\
    \begin{aligned}
      \text{Thus, 300 minutes = 5 hours}
    \end{aligned}
	\end{aligned}
  \end{aligned} \\
  \text{} \\
  \text{Hence proved, normalization and denormalization functions are working as expected.}
\end{aligned}
$$

With this example, we can confidently say our approach might work out.

You might think we still haven't figured out a way to convert from $Input$ to $Base$ to $Target$. But if you look close enough, we already have the answer i.e., if we change the constants of the function (i.e., $c$ and $k$) while denormalizing, we can get the expected result.

Let's take the same example and try to repeat the same operation while keep the base unit for time category as seconds,

$$
\qquad\qquad\qquad\qquad\begin{aligned}
  &\text{} \\
  \text{We knew,} \\
  \qquad\qquad\qquad\begin{aligned}
    f(x) &= x \times c + k &= y \\
    g(y) &= \frac{y - k}{c} &= x
  \end{aligned} \\
  \text{} \\
  \text{From precomputed values,} \\
  \text{} \\
  \qquad\qquad\qquad\begin{aligned}
    \text{} \\
    \text{For hours (input) to seconds (base),} \\
    \text{} \\
    \qquad\qquad\qquad\begin{aligned}
      c_{from} &= 3600 \\
      k_{from} &= 0
    \end{aligned} \\
    \text{} \\
    \text{For minutes (output) to seconds (base),} \\
    \text{} \\
    \qquad\qquad\qquad\begin{aligned}
      c_{to} &= 60 \\
      k_{to} &= 0
    \end{aligned}
  \end{aligned} \\
  \text{} \\
  \text{Based on all information,} \\
  \text{} \\
  \qquad\qquad\qquad\begin{aligned}
    \text{} \\
    \text{Let's convert input unit to base unit,} \\
    \text{} \\
    \qquad\qquad\begin{aligned}
        f(x) &= x \times c_{from} + k_{from} \\
        f(5) &= 5 \times 3600 + 0 \\
        y_{base} &= 5 \times 3600 \\
        y_{base} &= 18000
    \end{aligned} \\
    \text{} \\
    \qquad\text{Now we know, 5 hours = 18,000 seconds} \\
    \text{} \\
    \text{} \\
    \text{Let's go ahead and convert from base to target unit,} \\
    \text{} \\
    \qquad\qquad\begin{aligned}
        g(y_{base}) &= \frac{y_{base} - k_{to}}{c_{to}} \\
        g(18000) &= \frac{18000 - 0}{60} \\
        y_{target} &= \frac{18000}{60}  \\
        y_{target} &= 300
    \end{aligned} \\
    \text{} \\
    \qquad\text{Thus, 5 hours = 18000 seconds = 300 minutes} \\
    \text{} \\
  \end{aligned} \\
  \text{} \\
  \text{Hence proved,} \\
  \text{} \\
  \qquad\qquad\text{using different constants with }
  \mathbb{f} \text{ and } \mathbb{g}
  \text{ can help us achieve our goal of unit conversion.}
\end{aligned}
$$

Great, now we have full picture of what's happening and how it's happening, let's take a look at how we're going to implemented code-wise...

Starting with the global registry, we are gonna remodel previous data structure into a hashmap of data notes where each datanodes contains constant values to convert the current unit to base unit and other details which would end up something similar to the following,

```py
LengthUnits = Literal["kilometer", "meter", "centimeter", "mile", "yard", "foot", "inch"]
WeightUnits = Literal["kilogram", "gram", "pound", "ounce"]
TimeUnits = Literal["day", "hour", "minute", "second"]
TemperatureUnits = Literal["celsius", "kelvin", "fahrenheit"]

AvailableUnits = LengthUnits | WeightUnits | TimeUnits | TemperatureUnits

class UnitCategory(StrEnum):
    LENGTH      = "length"
    WEIGHT      = "weight"
    TIME        = "time"
    TEMPERATURE = "temperature"

class ConstantValues(NamedTuple):
    multiplier: float
    offset: float = 0.0

@dataclass(frozen=True, slots=True)
class UnitDataNode:
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: ConstantValues

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
    "centimeter": UnitDataNode(
        name="centimeter",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=ConstantValues(multiplier=0.01)
    ),
    ...
})
```

Since, we are thinking units as data node on a hop-and-spoke graph model using normalization and denormalization functions, the above data structure for the global registry well designed for the specific purpose. And the reason why it's suits perfectly is because we're dealing with only single dimension of constants (i.e., $any \ unit \rightarrow base \ unit$) where both input and output units are converting to base unit based on the function they're used.

In other words, we only needs a simple vector of data where all units points towards their respective base units and use their respective constants values for appropriate action _(i.e., normarlization or denormalization)_. Thus when the we want to add in more units, the global registry scales with $O(n)$ space complexity while the time complexity stays $O(1)$ theortically.

Now let's write a small pseudo code to put this to implementantation,

```pascal
GLOBAL GLOBAL_RESIGTRY // Hardcoded with precomputed values as discussed above

FUNCTION convert(input_value, from_unit, to_unit)
  INPUT input_value
  INPUT from_unit
  INPUT to_unit

  SET from_unit_datanode = GLOBAL_RESIGTRY[from_unit]
  SET to_unit_datanode = GLOBAL_RESIGTRY[to_unit]

  SET from_unit_multiplier = from_unit_datanode.constants.multiplier
  SET from_unit_offset = from_unit_datanode.constants.offset

  SET base_unit_value = normalizeToBase(input_value, from_unit_multiplier, from_unit_offset)

  SET to_unit_multiplier = to_unit_datanode.constants.multiplier
  SET to_unit_offset = to_unit_datanode.constants.offset

  SET base_unit_value = denormalizeToTarget(base_unit_value, to_unit_multiplier, to_unit_offset)

  RETURN base_unit_value
END FUNCTION

FUNCTION normalizeToBase(input_value, multiplier, offset)
  INPUT input_value
  INPUT multiplier
  INPUT offset

  SET result = value * multiplier + offset

  RETURN result
END FUNCTION

FUNCTION denormalizeToTarget(base_value, multiplier, offset)
  INPUT base_value
  INPUT multiplier
  INPUT offset

  SET result = (value - offset) /  multiplier

  RETURN result
END FUNCTION
```

That's perfect we have everything to put this to implementations, but do you feel like we are missing something???...

That's right, we're not checking for compatible unit categories. In previous implementation, we ensure both input & output units are from same category because we perform a search across the enums to get the required matrix. But in the current implementation, we have reduced the dimension of the data structure to a vector to be more suitable for the current approach. So, how do we resolve this in current approach?

Well, it's kinda obvious at this point but we have the relevant information in the data node themselves. And we could resolve this issue with simple if-condition thus eliminating the requirement to perform a $O(n)$ search across enums. On the point, we can also check whether the unit are valid units or not by checking on the hashset of the global registry.

```py
class InvalidNumericType(TypeError):
    pass

class UnitNotFound(ValueError):
    pass

class DifferentCategoryUnits(ValueError):
    pass

def convert(value: float, from_unit: str, to_unit: str) -> float:

    # ... Any Prior logic ...

    if not isinstance(value, (float, int)):
        raise InvalidNumericType(f"{str(value)} is not a numeric value.")

    if from_unit not in GLOBAL_REGISTRY:
        raise UnitNotFound(f"Invalid {from_unit} unit.")
    if to_unit not in GLOBAL_REGISTRY:
        raise UnitNotFound(f"Invalid {to_unit} unit.")

    from_unit_datanode: UnitDataNode = GLOBAL_REGISTRY[from_unit]
    to_unit_datanode: UnitDataNode = GLOBAL_REGISTRY[to_unit]

    if from_unit_datanode.category != to_unit_datanode.category:
        raise DifferentCategoryUnits(
            f"{from_unit} and {to_unit} are not from the same unit category."
        )

    # ... Remaining logic ...
```

> [!TIP]
>
> Now you might be think, "In the previous approach, we did have a `category` member so why didn't we do a comparison like this approach to find out whether the input and output units are within the same category".
>
> I understand your frustration. But if you look closely, we do need a search logic to determine the category from the provided units. So, it would have matter if we did the comparison the same way or not. So, I proceeded to check then around the search itself.


Thus concludes the full practical implementation of this approach with sounding implementations and proofs.

### Scalability

Talking about scalablity, it outperform from the both previous approaches that we have discussed prior to this approach. But that's not what I really want to discuss here. I'm talking about scalablity in terms of business logic.

> [!NOTE]
>
> This is just an possible implementation to extending the existing capabilities at an abstract level. This section is only exists as an extended discussion on a topic that was previous mentioned.
>
> In other words, this is not going to be part of the final design implementation---because this does not align with give requirements, lies outside the scope of the PRDs and most importantly to respect the princples of [YAGNI](https://www.google.com/search?q=YAGNI "what is YAGNI?").
>
> Consider this as an extended thinking/study that I made to properly cover all the possible factors that crossed the path while I want brainstroming about the design of this application.

In the previous approach, I have pointed out that that approach is kinda tightly coupled to the generalized formula derived from the observation. Since it's a simple linear equation, it makes us kinda hard to extend that approach to support non-linear conversion equations.

I mean, we can refactor to have an anonymous function for each category or set a flag to use the specific equation, but there is a far better and simpler way to implement it within the current implementation.

We can refactor the `UnitDataNode` using [strategy pattern](https://www.google.com/search?q=strategy+pattern+in+python). In other words, we create more than one concrete strategy that contains specific conversion logic _(i.e., normalization and denormalization functions)_ along with their relevant constants data structure.

Implement this approach would result in something similar to the following,

```py
LengthUnits = Literal["kilometer", "meter", "centimeter", "mile", "yard", "foot", "inch"]
WeightUnits = Literal["kilogram", "gram", "pound", "ounce"]
TimeUnits = Literal["day", "hour", "minute", "second"]
TemperatureUnits = Literal["celsius", "kelvin", "fahrenheit"]
PowerUnits = Literal["linear_ratio", "decibel"]

AvailableUnits = LengthUnits | WeightUnits | TimeUnits | TemperatureUnits | PowerUnits

TConstants = TypeVar("TConstants", bound=NamedTuple)

# ------------------------------------------------------------------------------------------

class UnitCategory(StrEnum):
    LENGTH      = "length"
    WEIGHT      = "weight"
    TIME        = "time"
    TEMPERATURE = "temperature"
    POWER       = "power"

class LinearConstants(NamedTuple):
    multiplier: float
    offset: float = 0.0

class LogarithmicConstants(NamedTuple):
    base_factor: float
    scale_factor: float

# ------------------------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AbstractUnitDataNode(ABC, Generic[TConstants]):
    name: AvailableUnits
    base_unit: AvailableUnits
    category: UnitCategory
    constants: TConstants

    @abstractmethod
    def normalize(self, value: float) -> float: ...

    @abstractmethod
    def denormalize(self, value: float) -> float: ...

@dataclass(frozen=True, slots=True)
class LinearUnitDataNode(AbstractUnitDataNode[LinearConstants]):
    def normalize(self, value: float) -> float:
        return value * self.constants.multiplier + self.constants.offset

    def denormalize(self, value: float) -> float:
        return (value - self.constants.offset) / self.constants.multiplier

@dataclass(frozen=True, slots=True)
class LogarithmicUnitDataNode(AbstractUnitDataNode[LogarithmicConstants]):
    def normalize(self, value: float) -> float:
        return self.constants.base_factor ** (value / self.constants.scale_factor)

    def denormalize(self, value: float) -> float:
        return self.constants.scale_factor * math.log10(value) if value > 0 else float('-inf')

# ------------------------------------------------------------------------------------------

GLOBAL_REGISTRY: Final[Mapping[AvailableUnits, AbstractUnitDataNode[Any]]] = MappingProxyType({
    "kilometer": LinearUnitDataNode(
        name="kilometer",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=LinearConfig(multiplier=1000.0)
    ),
    "meter": LinearUnitDataNode(
        name="meter",
        base_unit="meter",
        category=UnitCategory.LENGTH,
        constants=LinearConfig(multiplier=1.0)
    ),
    ...
    "decibel": LogarithmicUnitDataNode(
        name="decibel",
        base_unit="linear_ratio",
        category=UnitCategory.POWER,
        constants=LogarithmicConfig(base_factor=10.0, scale_factor=10.0)
    ),
    ...
})
```

> [!CAUTION]
>
> **The constant values and formula for logarithmic conversion and values are based on AI**. I really want to wrap this up and end this up quickly so that I can finish up this document and get on with the remaining docs so that I can move on to the actual development.
>
> Since this only to convey my approach for cleaner expandability via this approach, I just went for shortcut. The values and formula might or might not be true, but **the approach is still solid and stands true**.

So, there you have it. An possible working clean solution that can smoothly extend the functionality of the application.

But since the units are out of scope of the PRDs, this will not be part of design implementation _(atleast for now)_. You could as me to use this format since it would take less effort while refactoring if I were to extend it, but to respect the YAGNI principle, none of this will be implemented in the final draft of initial version of this application.

### Optimization

Now you might be thinking, what is there to optimize in this approach: we have optimized the space complexity down to $O(n)$ _(where, n stands for number of units)_ while maintaining the time complexity $O(1)$ and eliminating the need to perform category search.

What else could be optimized? Well, I though the same... I thought this is it, the most optimal solution. So, I went and search online on how the same problem statement are implemented at a production level and I found that this is the very same approach used in existing solutions like Pint, unyt, etc.

To keep it short, it's a base-centric approach where, during runtime, we precompute some additional constants from the precomputed values that we've hardcoded and cache these new values throughout the session of the application perform affine transformations in form of $(x + K) \times C$. Thus expanding the unit _(i.e., both input and target)_ from the base unit while brillinatly architecting the conversion logic to perform additive/subtrative arithematic operations before **relatively** compute heavy multiplication/division arithematic operation.

Despite all the benefits, I deemed this not suitable for the current application that I'm building. As much as I want to expand on that concept, it would get us anywhere in terms of optimization. The only reason, that approach will not work out is in terms of amortized cost. This is a one-shot application that performs a single unit conversion and doesn't retain any state/memory. If we proceed with that approach, the we would only be performing unnecessary computation for all the unit when we need atmost three of them. This is not good both in terms of space and time complexity. This approach would only make sense or would be valuable in production system that stay active for longer runs and hits caches to stay performant. To be more clear, this doesn't align with what we are building.

> I really spent quite an amount of time trying to understand this approach since it give me that millisecond of performance, but once I spent days trying to understand the math and architecture _(to which I don't fully understand)_ I had enough understanding to realize this approach doesn't align with what I'm building.

So, The only minor optimization that I can think of this approach is not to treat normalization and denormalization as a different step. I mean it kinda obvious when you think of it in terms of $f(x_{input}) = y_{base}$ and $g(y_{base}) = x_{output}$. I explained it in terms of two operation, just to explain the math and build the intuition but never meant to be the final design implementation.

If you think about it,

$$
\begin{aligned}
	\text{We know that,} \\
	&\begin{aligned}
    f(x) &= x \times c + k &= y \\
    \text{} \\
    g(R) &= f^{-1}(R) \\
    \text{} \\
    g(y) &= \frac{y - k}{c} &= x
	\end{aligned} \\
  \text{So we use them as,} \\
	&\begin{aligned}
	  f(x_{A}) &= x_{A} \ \times \ c_{A \rightarrow B} \ + \ k_{A \rightarrow B} &= y_{B} \\
    \text{} \\
    g(y_{B}) &= \frac{y_{B} \ - \ k_{C \rightarrow B}}{c_{C \rightarrow B}} &= x_{C} \\
    \text{} \\
	\end{aligned} \\
  &\begin{aligned}
    conversion \ (A \rightarrow C) &= g \circ f \ : \ A \to C \text{ defined as } (g \circ f)(x) = g(f(x))
  \end{aligned} \\
  \text{In other words,} \\
	&\begin{aligned}
    conversion \ (A \rightarrow B) &= g(f(x_A)) \\
    \text{} \\
    &= \frac{f(x_A) \ - \ k_{C \rightarrow B}}{c_{C \rightarrow B}} \\
    \text{} \\
    &= \frac{x_{A} \ \times \ c_{A \rightarrow B} \ + \ k_{A \rightarrow B} \ - \ k_{C \rightarrow B}}{c_{C \rightarrow B}} \\
	\end{aligned} \\
	&\begin{aligned}
	\end{aligned} \\
\end{aligned}
$$

Yea... I think that sums up everything. I really don't want to make this any more complex, just a simple straight forward solution that is probably the best suited for this problem statement.

### Evaluation of Second Approach

- The complexity of this approach is around moderate, since we're going round about the solution and trying to figure with a different approach mathematically.
- The scalability of this approach is way better than previous solutions,
  - The whole global registry is kinda like a big vector of units with just enough data to perform the conversion
  - If we talk in terms of space complexity, then it would $O(n)$ where n stands for number of units.
  - This scales well because all unit points towards their respective base unit and we can derived all units from base unit.
- Maintainability is fair better than last two approaches,
  - Since all we need to worry is to hardcode the proper precomputed values that are relevant from unit to it's respective base unit, it much more maintainable than the matrix approach.
  - Since we're defining proper abstractions and type, it would be much easier to catch bugs and any possible issues.
  - Also we want to extend it's capablitites to support more unit that require more than a simple affine transformation, then we can easily refactor the system using strategy pattern where we can define concrete strategy for each unique approach to handle conversion as shown above.
- Coming to testability, it has greatly improved due since we have properly defined our abstraction. Thus makes it more easier have meaningful test coverages.
- And as of performance, It far better than previous approach.
  - Yes, we're going some additional steps to achieve our goal but conceptually we're still $O(1)$ time complexity with $O(n)$ space complexity.
  - There might be some additional arithematic operation that needs to be performed during runtime, but this is way better trade of than previous approach where we had to perform $O(n)$ search on categories and index from $O(n^2)$ data structure to get the constants to perform the conversion.
- This approach is also aligned to the approaches suggested by the PRDs. Since we're meeting the requirement of using a global registry to contain all the details.

### Final Verdict of Third Approach

<div align="center">

| Metric  | PRD Alignment | Complexity | Scalability | Maintainability | Testability | Performance      |
| ------- | :-----------: | :--------: | :---------: | :-------------: | :---------: | :--------------: |
| Results | High          | Moderate   | High        | High            | High        | Moderate-to-High |

</div>

This could be the best optimal solution suited for the given problem statement while perfectly aligning with the PRDs. This way better trade of than the previous approach and has way better maintainability & scalablity than the first approach. Although the first approach could beat this approach purely in terms of performance, this is a way better overall solution to the problem statement.

To conclude the final verdict, this approach has been selected to be the core system of the design-implementation of the solution. This could the most optimal solution to that be justifiable in terms of mathematical proofing, architectural design and openness for extension of the functionality.

Although it's heavily reliant on the handcoded precomputed constant values, the design of this system make it more clear, easier and obvious to verify and fix any possible issue that may arise during development.

## Final Note

Before I end this design decision record, I need to clarify few thing despite how obvious they're. Here're the following this that were not mentioned prior to all the core system decision:

- [How to compute the constants?](#how-to-compute-the-constants?)
- [Base units](#base-units)

### How to compute the constants?

This is pretty basis concept, we're just going to a few example to drive the relationship between various unit within their respective category. But instead of calculating all of these values manually, I'll be referring to the original source of measurements to get all of the values that is required to hardcode into the respective data structure.

Just to demonstrate and example of how we can do this manually, I'm gonna pick temperature category unit since they do require an offset.

Let's keep it simple and take an example of getting the constant values required for celsius to fahrenheit,

$$
\begin{aligned}
	\text{We know that,} \\
	&\begin{aligned}
	  \text{Freezing Point of water: } &0^{\circ}\text{C} &= 32^{\circ}\text{F} \\
	  \text{Boiling Point of water: } &100^{\circ}\text{C} &= 212^{\circ}\text{F} \\
	\end{aligned} \\
	\text{From freezing point of water,} \\
	&\begin{aligned}
    f(x) &= x \times c + k \\
    \text{} \\
    f_{C \rightarrow F} \ (0) &= 0 \times c_{C \rightarrow F} + k_{C \rightarrow F} \\
    32 &= 0 + k_{C \rightarrow F} \\
    \text{} \\
    \text{} \\
    k_{C \rightarrow F} &= 32
	\end{aligned} \\
  \text{From boiling point of water,} \\
	&\begin{aligned}
    f_{C \rightarrow F} \ (100) &= 100 \times c_{C \rightarrow F} + k_{C \rightarrow F} \\
    212 &= 100 \times c_{C \rightarrow F} + 32 \\
    212 - 32 &= 100 \times c_{C \rightarrow F} \\
    \frac{180}{100} &= c_{C \rightarrow F} \\
    \text{} \\
    \text{} \\
    c_{C \rightarrow F} &= \frac{9}{5} \\
	\end{aligned} \\
  \text{Thus,} \\
	&\begin{aligned}
    f_{C \rightarrow F} \ (x) &= x \times c_{C \rightarrow F} + k_{C \rightarrow F} \\
    \text{} \\
    \text{} \\
    f_{C \rightarrow F} \ (x) &= x \times \frac{9}{5} + 32 \\
	\end{aligned}
\end{aligned}
$$

Similar for all the values that doesn't have any offset value, the $k$ value can be set to zero. This is how we derived the precomputed constant values.

### Base units

For the base units, I'm going to following the International System of Units (SI) that built upon seven fundamental base units. And as of our application, we're going need only four of them.

Here's the base units defined by the SI,

| Category    | Base Unit |
| :---------: | :-------: |
| Length      | Meter     |
| Mass/Weight | Kilogram  |
| Time        | Second    |
| Temperature | Kelvin    |

### Conclusion

With all of the information and thought process verified, refined and reviewed as part of the design decision record will the taken into account while designing the final implementation of the solution for the given problem statmen. I'm personally glad that I get to do document all of this manually while reasoning, revising and reviewing, just to get my thoughts straight and see my mistake more clearly even before I put it to implementation. This was a great learning and It would probably stick with me for a long time.
