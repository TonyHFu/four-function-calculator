import re

stored_operation = None  # Storing for repeat operations like 6+== (18)
stored_argument = None  # Storing for repeat operations like 6+== (18)

current_operation = None  # For knowing which operations to perform and where to store new operand
first_operation = None  # Either + or -
second_operation = None  # Either * or /

base_argument = 0  # Storing the first operand
second_argument = None  # Storing the second operand for + or - (goes after * and - in order of operations)
third_argument = None  # Storing the third operand to * or / with second

current_value = 0  # For display

operation_in_progress = False  # To decide if new input should overwrite existing input
negation_just_happened = False  # Makes new input overwrite existing input
equal_just_happened = False  # Tells program to check stored operations and arguments for repeat actions like 6+==

is_decimal = False  # For input with decimal places
decimal_place = 0  # To track which decimal place new digit should be on

temp_operand = None  # For collecting temporary inputs not ready for storage e.g. 123\n45 => 12345 not 45 overwrite 123


def display(debug):
    global second_argument, base_argument, current_value, operation_in_progress, \
        stored_operation, current_operation, second_operation, third_argument, temp_operand

    if debug:
        print(f"current_value: {current_value}")
        print(f"base_argument: {base_argument}")
        print(f"second_argument: {second_argument}")
        print(f"third_argument: {third_argument}")
        print(f"temp_operand: {temp_operand}")
        print(f"stored_operation: {stored_operation}")
        print(f"stored_argument: {stored_argument}")
        print(f"current_operation: {current_operation}")
        print(f"first_operation: {first_operation}")
        print(f"second_operation: {second_operation}")
        print(f"operation in progress: {operation_in_progress}")
    else:
        print(current_value)


# For updating the base_argument using the first operation and base_argument and second_argument
def update_base():
    global second_argument, base_argument, current_value, first_operation, operation_in_progress

    # If first operation was not there
    if first_operation is None or second_argument is None:
        # If there was a second operation but no first operation, perform second operation
        if second_operation is not None:
            if second_operation == "*":
                result = base_argument * second_argument
            if second_operation == "/":
                result = base_argument / second_argument

        # If there were no operations, base is just base
        else:
            result = base_argument

    # If there is a first operation and a second operand, perform operation
    elif first_operation == "+":
        result = base_argument + second_argument
    elif first_operation == "-":
        result = base_argument - second_argument

    # After operation is done, reset second argument
    second_argument = None
    # Should now display new base
    current_value = result
    # There are no operations in progress now
    operation_in_progress = True
    return result


# Updating the second operand using second and third operands and the second operation
def update_second():
    global second_argument, second_operation, third_argument

    # If there is no second operation going on, second operand remains same
    if second_operation is None or third_argument is None:
        result = second_argument

    # If there is, then do operation
    elif second_operation == "*":
        result = second_argument * third_argument
    elif second_operation == "/":
        result = second_argument * third_argument

    return result


# Hard clear, may implement clear item later
def reset():
    global second_argument, base_argument, current_value, operation_in_progress, \
        stored_operation, current_operation, second_operation, third_argument, \
        first_operation, temp_operand, stored_argument, negation_just_happened, equal_just_happened, \
        is_decimal, decimal_place
    stored_operation = None
    stored_argument = None
    current_operation = None
    first_operation = None
    base_argument = 0
    second_argument = None
    third_argument = None
    current_value = 0
    operation_in_progress = False
    second_operation = None
    negation_just_happened = False
    temp_operand = None
    equal_just_happened = False
    is_decimal = False
    decimal_place = 0


# Adding a temporary operand into first, second, or third place
def add_operand(temp):
    global second_argument, base_argument, current_value, operation_in_progress, stored_operation, \
        current_operation, second_operation, third_argument, first_operation

    # If currently on second order operation (* or /), add to second or third depending on if second already exists
    if current_operation is not None and re.match(r"[/\*]", current_operation):
        if second_argument is None:
            second_argument = temp
        else:
            third_argument = temp
    # Overwrite base in cases like 123=\n45 => 45
    elif not operation_in_progress:
        base_argument = temp
    # Set as second operand in all other cases e.g. 45+23 => second = 23
    else:
        second_argument = temp


while True:
    display(False)
    command = input(">").lower().replace(" ", "")

    # To quit
    if command == "q":
        break

    if command == "c":
        reset()

    for letter in command:

        if letter != "." and not re.match(r"\d", letter):
            # Get out of decimal mode
            is_decimal = False
            decimal_place = 0
            
        # Initialize decimal mode
        if letter == ".":
            is_decimal = True
            decimal_place = 1

        # If number, add number to temporary argument
        if re.match(r"\d", letter):
            # Get out of just equal mode (for repeat ='s i.e. 6+== => 18)
            if equal_just_happened:
                current_operation = None
                first_operation = None
                second_operation = None
                equal_just_happened = False
            # Get out of just negation mode so not overwriting existing temp_operand
            if negation_just_happened:
                temp_operand = None
                negation_just_happened = False
            # Adding to temporary operand
            if temp_operand is not None:
                if is_decimal:
                    temp_operand += int(letter) / (10 ** decimal_place)
                    decimal_place += 1
                else:
                    temp_operand = temp_operand * 10 + int(letter)
            else:
                temp_operand = int(letter)
            # Updating display value
            current_value = temp_operand

        # if + or -:
        if re.match(r"[+-]", letter):
            # Get out of just equal mode : i.e. 6+== => 18
            if equal_just_happened:
                current_operation = None
                first_operation = None
                second_operation = None
                equal_just_happened = False

            # Add in temporary operand and store it for repeat actions
            if temp_operand is not None:
                add_operand(temp_operand)
                stored_argument = temp_operand
                temp_operand = None

            # update second argument
            if current_operation == "*" or current_operation == "/":
                second_argument = update_second()

            # update base argument
            base_argument = update_base()

            # update operations
            current_operation = letter
            first_operation = letter
            stored_operation = letter

        if letter == "=":
            # Add in temporary operand
            if temp_operand is not None:
                add_operand(temp_operand)
                stored_argument = temp_operand
                temp_operand = None

            # update second argument
            if current_operation == "*" or current_operation == "/":
                second_argument = update_second()

            # If equal just happened i.e. 6+==, Or if on first = i.e. 6+=:
            # use stored operation and stored argument
            if (equal_just_happened and stored_argument is not None and stored_operation is not None) or \
                    (current_operation is not None and
                     second_argument is None and third_argument is None):
                current_operation = stored_operation
                second_argument = stored_argument
                # If stored operation was second order,
                # make first order None so second order is called when updating base
                if stored_operation == "*" or stored_operation == "/":
                    first_operation = None

            # Update and cleanup
            base_argument = update_base()
            operation_in_progress = False
            third_argument = None
            current_value = base_argument
            is_decimal = False
            decimal_place = 0
            equal_just_happened = True

        if re.match(r"[/\*]", letter):
            # If second order operation, * or /, similar to + and -,
            # but no need to update base operand
            if equal_just_happened:
                current_operation = None
                first_operation = None
                second_operation = None
                equal_just_happened = False
            if temp_operand is not None:
                add_operand(temp_operand)
                stored_argument = temp_operand
                current_value = temp_operand
                temp_operand = None

            second_argument = update_second()
            second_operation = letter
            current_operation = letter
            stored_operation = letter
            current_value = second_argument

        if letter == "!":
            # Negates the latest operand
            current_value *= -1
            if temp_operand is not None:
                temp_operand *= -1
                negation_just_happened = True
            elif third_argument is not None:
                third_argument *= -1
            elif second_argument is not None:
                second_argument *= -1
            else:
                base_argument *= -1

        if letter == "%":
            # % changes temporary operand to percentage of base if currently
            # doing + or -
            # and divides temp operand by 100 if currently doing * or /
            # i.e. 50+20%= => 60 and 50*20%= => 10
            if temp_operand is not None:
                if current_operation == "+" or current_operation == "-":
                    temp_operand = base_argument * temp_operand * 0.01
                else:
                    temp_operand *= 0.01
                current_value = temp_operand
            else:
                # Update the base if there is nothing more current
                if second_argument is None and current_operation is None:
                    base_argument *= 0.01
                    current_value = base_argument
                # Update the second argument otherwise
                elif second_argument is None:
                    temp_operand = base_argument
                    if current_operation == "+" or current_operation == "-":
                        temp_operand = base_argument * temp_operand * 0.01
                    else:
                        temp_operand *= 0.01
