import re

IS_DEBUG_MODE = False

class Calculator:
    def __init__(self):
        self.stored_operation = None  # Storing for repeat operations like 6+== (18)
        self.stored_argument = None  # Storing for repeat operations like 6+== (18)

        self.current_operation = None  # For knowing which operations to perform and where to store new operand
        self.first_operation = None  # Either + or -
        self.second_operation = None  # Either * or /

        self.base_argument = 0  # Storing the first operand
        self.second_argument = None  # Storing the second operand for + or - (goes after * and - in order of operations)
        self.third_argument = None  # Storing the third operand to * or / with second
        
        self.current_value = 0  # For display
        self.operation_in_progress = False  # To decide if new input should overwrite existing input

        self.negation_just_happened = False  # Makes new input overwrite existing input
        self.equal_just_happened = False  # Tells program to check stored operations and arguments for repeat actions like 6+==

        self.is_decimal = False  # For input with decimal places
        self.decimal_place = 0  # To track which decimal place new digit should be on

        self.temp_operand = None  # For collecting temporary inputs not ready for storage e.g. 123\n45 => 12345 not 45 overwrite 123



    def display(self, debug):
        """Prints current value to screen

        Parameters
        ---------
        debug : Boolean
            determines how much info to print
        
        Returns
        -------
        None
        """

        if debug:
            print(f"current_value: {self.current_value}")
            print(f"base_argument: {self.base_argument}")
            print(f"second_argument: {self.second_argument}")
            print(f"third_argument: {self.third_argument}")
            print(f"temp_operand: {self.temp_operand}")
            print(f"stored_operation: {self.stored_operation}")
            print(f"stored_argument: {self.stored_argument}")
            print(f"current_operation: {self.current_operation}")
            print(f"first_operation: {self.first_operation}")
            print(f"second_operation: {self.second_operation}")
            print(f"operation in progress: {self.operation_in_progress}")
        else:
            print(self.current_value)


    def update_base(self):
        """For updating the base_argument using the first operation and base_argument and second_argument

        Parameters
        ---------
        None 

        Returns
        -------
        int or float
            new base_argument value 
        """
 
        # If first operation was not there
        if self.first_operation is None or self.second_argument is None:
            # If there was a second operation but no first operation, perform second operation
            if self.second_operation is not None:
                if self.second_operation == "*":
                    result = self.base_argument * self.second_argument
                if self.second_operation == "/":
                    result = self.base_argument / self.second_argument

            # If there were no operations, base is just base
            else:
                result = self.base_argument

        # If there is a first operation and a second operand, perform operation
        elif self.first_operation == "+":
            result = self.base_argument + self.second_argument
        elif self.first_operation == "-":
            result = self.base_argument - self.second_argument

        # After operation is done, reset second argument
        self.second_argument = None
        # Should now display new base
        self.current_value = result
        # There are no operations in progress now
        self.operation_in_progress = True
        return result


    def update_second(self):
        """Updating the second operand using second and third operands and the second operation

        Parameters
        ---------
        None 

        Returns
        -------
        int or float
            new second_argument value 
        """

        # If there is no second operation going on, second operand remains same
        if self.second_operation is None or self.third_argument is None:
            result = self.second_argument

        # If there is, then do operation
        elif self.second_operation == "*":
            result = self.second_argument * self.third_argument
        elif self.second_operation == "/":
            result = self.second_argument * self.third_argument

        return result


    def reset(self):
        """Hard clear, may implement clear item later

        Parameters
        ---------
        None 

        Returns
        -------
        None
        """

        self.stored_operation = None
        self.stored_argument = None
        self.current_operation = None
        self.first_operation = None
        self.base_argument = 0
        self.second_argument = None
        self.third_argument = None
        self.current_value = 0
        self.operation_in_progress = False
        self.second_operation = None
        self.negation_just_happened = False
        self.temp_operand = None
        self.equal_just_happened = False
        self.is_decimal = False
        self.decimal_place = 0


    def add_operand(self):
        """Adding a temporary operand into first, second, or third place

        Parameters
        ---------
        None 

        Returns
        -------
        None
        """

        # If currently on second order operation (* or /), add to second or third depending on if second already exists
        if self.current_operation is not None and re.match(r"[/\*]", self.current_operation):
            if self.second_argument is None:
                self.second_argument = self.temp_operand
            else:
                self.third_argument = self.temp_operand
        # Overwrite base in cases like 123=\n45 => 45
        elif not self.operation_in_progress:
            self.base_argument = self.temp_operand
        # Set as second operand in all other cases e.g. 45+23 => second = 23
        else:
            self.second_argument = self.temp_operand


    def handle_not_decimal(self):
        """Gets out of decimal mode

        Parameters
        ---------
        None 

        Returns
        -------
        None
        """

        self.is_decimal = False
        self.decimal_place = 0


    def handle_is_decimal(self):
        """Goes into decimal mode

        Parameters
        ---------
        None 

        Returns
        -------
        None
        """

        # Do not reset decimal places if already in decimal mode
        if self.is_decimal:
            return

        self.is_decimal = True
        self.decimal_place = 1


    def equal_did_not_just_happen(self):
        """Handles setting equal_just_happened to False and clean up operations

        Parameters
        ---------
        None

        Returns
        -------
        None
        """
        self.current_operation = None
        self.first_operation = None
        self.second_operation = None
        self.equal_just_happened = False


    def handle_digit(self, digit):
        """Handles adding in new digit

        Parameters
        ---------
        digit: string
            new input digit 

        Returns
        -------
        None
        """

        # Get out of just equal mode (for repeat ='s i.e. 6+== => 18)
        if self.equal_just_happened:
            self.equal_did_not_just_happen()            
        # Get out of just negation mode so not overwriting existing self.temp_operand
        if self.negation_just_happened:
            self.temp_operand = None
            self.negation_just_happened = False
        # Adding to temporary operand
        if self.temp_operand is not None:
            if self.is_decimal:
                self.temp_operand += int(digit) / (10 ** self.decimal_place)
                self.decimal_place += 1
            else:
                self.temp_operand = self.temp_operand * 10 + int(digit)
        else:
            if self.is_decimal:
                self.temp_operand = 0 + int(digit) / (10 ** self.decimal_place)
                self.decimal_place += 1
            else:
                self.temp_operand = int(digit)
        # Updating display value
        self.current_value = self.temp_operand


    def handle_plus_minus(self, operator):
        """Handles plus or minus operation

        Parameters
        ---------
        operator: string
            either "+" or "-"

        Returns
        -------
        None
        """
        
        # Get out of just equal mode : i.e. 6+== => 18
        if self.equal_just_happened:
            self.equal_did_not_just_happen()

        # Add in temporary operand and store it for repeat actions
        if self.temp_operand is not None:
            self.add_operand()
            self.stored_argument = self.temp_operand
            self.temp_operand = None

        # update second argument
        if self.current_operation == "*" or self.current_operation == "/":
            self.second_argument = self.update_second()

        # update base argument
        self.base_argument = self.update_base()

        # update operations
        self.current_operation = operator
        self.first_operation = operator
        self.stored_operation = operator


    def handle_equal(self):
        """Handles equals key pressed

        Parameters
        ---------
        None

        Returns
        -------
        None
        """

        # Add in temporary operand
        if self.temp_operand is not None:
            self.add_operand()
            self.stored_argument = self.temp_operand
            self.temp_operand = None

        # update second argument
        if self.current_operation == "*" or self.current_operation == "/":
            self.second_argument = self.update_second()

        # If equal just happened i.e. 6+==, Or if on first = i.e. 6+=:
        # use stored operation and stored argument
        if (self.equal_just_happened and self.stored_argument is not None and self.stored_operation is not None) or \
                (self.current_operation is not None and
                self.second_argument is None and self.third_argument is None):
            self.current_operation = self.stored_operation
            self.second_argument = self.stored_argument
            # If stored operation was second order,
            # make first order None so second order is called when updating base
            if self.stored_operation == "*" or self.stored_operation == "/":
                self.first_operation = None

        # Update and cleanup
        self.base_argument = self.update_base()
        self.operation_in_progress = False
        self.third_argument = None
        self.current_value = self.base_argument
        self.is_decimal = False
        self.decimal_place = 0
        self.equal_just_happened = True
    

    def handle_multiply_divide(self, operator):
        """Handles multiply or divide operation

        Parameters
        ---------
        operator: string
            either "*" or "/"

        Returns
        -------
        None
        """
       
        # Get out of just equal mode : i.e. 6+== => 18
        if self.equal_just_happened:
            self.equal_did_not_just_happen()

        # Add in temporary operand and store it for repeat actions
        if self.temp_operand is not None:
            self.add_operand()
            self.stored_argument = self.temp_operand
            self.temp_operand = None

        # update second argument
        self.second_argument = self.update_second()
        self.second_operation = operator
        self.current_operation = operator

        # storing operator
        self.stored_operation = operator

        # updating current display value
        if self.second_argument is None:
            self.current_value = self.base_argument
        else :
            self.current_value = self.second_argument


    def handle_negation(self):
        """Handles negation "!"

        Parameters
        ---------
        None

        Returns
        -------
        None
        """

        # Negates the latest operand
        self.current_value *= -1
        if self.temp_operand is not None:
            self.temp_operand *= -1
            self.negation_just_happened = True
        elif self.third_argument is not None:
            self.third_argument *= -1
        elif self.second_argument is not None:
            self.second_argument *= -1
        else:
            self.base_argument *= -1

    
    def handle_percent(self):
        """Changes temporary operand to percentage of base if currently
        doing + or - and divides temp operand by 100 if currently doing * or /
        \ni.e. 50+20%= => 60 and 50*20%= => 10

        Parameters
        ---------
        None

        Returns
        -------
        None
        """

        # Updates temp_operand if it's there        
        if self.temp_operand is not None:
            if self.current_operation == "+" or self.current_operation == "-":
                self.temp_operand = self.base_argument * self.temp_operand * 0.01
            else:
                self.temp_operand *= 0.01
            self.current_value = self.temp_operand
        else:
            # Update the base if there is nothing more current
            if self.second_argument is None and self.current_operation is None:
                self.base_argument *= 0.01
                self.current_value = self.base_argument
            # Update the second argument otherwise
            elif self.second_argument is None:
                self.temp_operand = self.base_argument
                if self.current_operation == "+" or self.current_operation == "-":
                    self.temp_operand = self.base_argument * self.temp_operand * 0.01
                else:
                    self.temp_operand *= 0.01

def calculate():
    calculator = Calculator()

    while True:
        calculator.display(IS_DEBUG_MODE)
        
        command = input(">").lower().replace(" ", "")
        
        # To quit
        if command == "q":
            break

        # Hard clear
        if command == "c":
            calculator.reset()

        # Different actions depending on key pressed
        for key in command:
            
            # Not decimal and not number gets out of decimal mode
            if key != "." and not re.match(r"\d", key):
                calculator.handle_not_decimal()
                    
            # Decimal 
            if key == ".":
                calculator.handle_is_decimal()

            # If number, add number to temporary argument
            if re.match(r"\d", key):
                calculator.handle_digit(key)

            # + or -:
            if re.match(r"[+-]", key):
                calculator.handle_plus_minus(key)
            
            # Equals sign
            if key == "=":
                calculator.handle_equal()

            # Multiply or divide
            if re.match(r"[/\*]", key):
                calculator.handle_multiply_divide(key)
            
            # Negation
            if key == "!":
                calculator.handle_negation()
            
            # Percentage
            if key == "%":
                calculator.handle_percent()
                
    
if __name__ == "__main__":
    calculate()

