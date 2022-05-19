## Intro

This is a four-function calculator like the one on iOS

It runs in the command line simply by

`python3 four-function-calculator.py`

## Features

Beyond the simple features of adding, subtracting, multiplying, and dividing, it also handles:

1. Repeat operations:  
   example: `>6+==` will output `18` as 6 is added to itself
   twice
2. Percentage:  
   example: `>150+6%=` will output `159` which is 150 plus the 6% of 150 (useful for calculating taxes for example)  
   example: `>150*6%=` on the otherhand will print `9` which is just the tax part
3. Negation:  
   example: `>15!+12.3!=` will print `-27.3`
4. Handles 1 key at a time:  
   when you press `enter`, the output is what you'd expect to see on the calculator screen given the series of key presses.
   example:
   ```
   >123
   123
   >4
   1234
   ```
   because the input never technically finished

## How it works

On a high level, the calculator works by keeping track of 3 operands and 2 operations.

The two types of operations are either `+-` or `*/`. This is because order of operations tell us that multiplication and division happen before addition and subtraction.

Therefore, we only need to keep track of up to 3 operands at a time as everytime a new multiplication or division happens, we can operate on the second and third operand and return a new second operand, and when a new addition or subtraction happens, we can operate on the first and second operands and return a new first operand.

## Improvements

Although I have taken steps to create as many of the iOS four-function calculator functionalities as possible, there are still steps for improvement:

1. Handling clear item:  
   `>c` currently clears everything and resets calculator to initial state. On iOS, there is the option of clearing an individual item instead of the whole state. However, from experimentation, I have noticed that this functionality behaves differently on an iPhone vs on a Macbook
2. Possible other scenarios I have not thought about:  
   This exercise showed me how many intricacies are behind the four-function calculator. By playing around with different inputs, I found out that there are a lot more functionalities that aren't obvious like the repeat operations and how clear item is implemented differently on different calculators. I'm sure there are things that I have not thought of as well.
3. Code refactoring:  
   My initial solution to this problem was done in about an hour, but I found more intricacies of the calculator at that point and spent 4 more hours to create a better solution. As this is also my first Python project in a while, I then spent another hour refactoring the code into a class based solution
