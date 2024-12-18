import tkinter as tk

class Calculator:
    """
    Class containing calculator UI and operation logic.
    """

    def __init__(self):
        """
        Initializes a Calculator object.
        """

        # Variables for storing logic values
        self.val1 = ""
        self.val2 = ""
        self.operator = None
        self.prev_operator = None
        self.state = "none" # handles input based on previous input
        # possible values:
        # -"none": none
        # -"num": number
        # -"op": operator
        # -"eq": equals


        # ################# #
        #   Create Window   #
        # ################# #
        self.window = tk.Tk()
        self.window.minsize(300, 400)
        self.window.title("Simple Calculator")


        # #################### #
        #  Create Output Area  #
        # #################### #
        self.output = tk.Label(self.window,
                               text="0",
                               font=("Monospace", 32),
                               anchor="se",
                               padx=15,
                               pady=5
                               )
        self.output.grid(row=0, column=0, columnspan=4, sticky="nsew")


        # ################# #
        #   Create Buttons  #
        # ################# #
        # -groups buttons by styling for easy switch between light/dark mode
        self.buttons = {
            "functional": [],
            "numerical": [],
            "operational": []
        }

        # -buttons with changing text value
        self.clear_button = self.create_button("AC", self.clearAll)
        self.displaymode_button = self.create_button("\u263C", self.switch_display)
        
        # -functional buttons
        self.buttons["functional"] = [
            self.clear_button,
            self.create_button("+/-", self.change_sign),
            self.create_button("%", self.percent),
        ]
    
        # -numerical buttons
        for i in range(10):
            self.buttons["numerical"].append(self.create_button(str(i), lambda num=str(i): self.num_input(num)))
        # --non-numerical buttons that follow same styling as numerical buttons, ordered for easy placing in grid
        self.buttons["numerical"].insert(0, self.displaymode_button)
        self.buttons["numerical"].insert(2, self.create_button(".", self.decimal))

        # -operational buttons
        self.buttons["operational"] = [
            self.create_button("\u2797", lambda op=self.divide: self.operate(op)),      # division
            self.create_button("\u2716", lambda op=self.multiply: self.operate(op)),    # multiplication
            self.create_button("\u2796", lambda op=self.subtract: self.operate(op)),    # minus
            self.create_button("\u2795", lambda op=self.add: self.operate(op)),         # plus
            self.create_button("\u3013", self.equals)    # equals
        ]


        # ################################### #
        #      Place buttons in 5x5 grid      #
        #  (0-indexed, row 0 is output area)  #
        # ################################### #
        # -placing functional buttons in row 1, columns 0-2
        for i in range(3):
            self.buttons["functional"][i].grid(row=1, column=i, sticky="nsew")

        # -placing operational buttons in rows 1-5, column 3
        for i in range(5):
            self.buttons["operational"][i].grid(row=i + 1, column=3, sticky="nsew")

        # -placing numerical buttons in rows 2-5, columns 0-2
        self.btn_index = 0
        for row in range(5, 1, -1):
            for col in range(3):
                self.buttons["numerical"][self.btn_index].grid(row=row, column=col, sticky="nsew")
                self.btn_index += 1


        # ########################## #
        #  Row/Column Configuration  #
        # ########################## #
        # -configure columns to fill width of window
        for i in range(4):
            self.window.columnconfigure(i, weight=1)

        # -configure rows to fill height of window
        self.window.rowconfigure(0, weight=6)   # weight 6 on output window to make larger
        for i in range(1, 6):
            self.window.rowconfigure(i, weight=1)

        # ############# #
        #  Set Styling  #
        # ############# #
        self.mode = "light"
        self.switch_display()   # calculator will initiate with dark stylings


    def create_button(self, text, function=None):
        """
        Creates Tkinter button widget.

        Parameters:
            text (str): Text value displayed on button.
            function (function): Function called when button is clicked.
        
        Returns:
            Button Widget: A button widget with the specified attributes.
        """
        return tk.Button(self.window,
                         text=text,
                         font=("Monospace", 16),
                         command=function
                        )
    
    def switch_display(self):
        """
        Switches calculator to either light or dark mode based on current styling.
        """
        if self.mode == "dark":
            # light mode settings
            bg_color = "#EEE"
            txt_color = "#000"
            func_btn_color = "#999"
            num_btn_color = "#CCC"
            op_btn_color = "#f9b658"
            self.displaymode_button.config(text = "\U0001F312") # moon symbol
            self.mode = "light"
        else:
            # dark mode settings
            bg_color = "#000"
            txt_color = "#FFF"
            func_btn_color = "#666"
            num_btn_color = "#222"
            op_btn_color = "#f8af47"
            self.displaymode_button.config(text = "\u263C") # sun symbol
            self.mode = "dark"

        # change widget styling
        self.output.config(bg = bg_color, fg = txt_color)
        for btn_type in self.buttons:
            for btn in self.buttons[btn_type]:
                btn.config(fg = txt_color)
                if btn_type == "functional":
                    btn.config(bg = func_btn_color)
                elif btn_type == "numerical":
                    btn.config(bg = num_btn_color)
                else:
                    btn.config(bg = op_btn_color)
                
    def num_input(self, value):
        """
        Adds given value to the output window of the calculator.

        Parameters:
            value (str): Value corresponding to the number on the button clicked.
        """
        # start new operation if number hit after equal
        if self.state == "eq":
            self.clearAll()

        # beginning fresh operation
        if self.state == "none":
            # if 0 negated, add entered value after '-' sign
            if self.output["text"][0] == "-":
                self.output.config(text="-" + value)
            # decimal value < 1 (ie 0.5)
            elif self.output["text"][-1] == ".":
                self.output["text"] += value
            # if not negated or decimal, just replace the 0
            else:
                self.output.config(text=value)

        # if number already entered, append following entered values to end
        elif (self.state == "num") and (self.output["text"] != "0") and (len(self.output["text"]) < 11): # max output length of 11
            self.output["text"] += value

        # if operator button pressed, start entry of new value
        elif self.state == "op":
            # new value is a decimal < 1
            if self.output["text"][-1] == "." and float(self.val1) != 0: # float(self.val1) != 0 ensures new value is started if '0.' is entered before operator button is clicked
                self.output["text"] += value
            else:   
                self.output.config(text=value)

        self.set_state("num")

    def operate(self, operator):
        """
        Stores entered values and operations based on operator button clicked.
        Calculates stored operations if series of operations entered and displays result
        to the output window.

        Parameters:
            operator (function): The operation function to be performed on the entered values
                                    based on the operator button that is clicked.
        """
        # user clicked an operator button after entering a number (or using the default 0 as first value)
        if self.state == "num" or self.state=="none":
            if not self.val1:
                self.val1 = self.output["text"]
            else:   # operate on previosly entered values
                self.val2 = self.output["text"]
                self.val1 = self.operator(self.val1, self.val2)
                self.set_output(self.val1)
            # store operator
            if self.operator:
                self.prev_operator = self.operator
            self.operator = operator

        # operator button was pressed immediatly after another operator button,
        # stored operator changes to last pressed operator button
        elif self.state == "op":
            self.operator = operator

        # user wants to operate on the result of a previous operation
        elif self.state == "eq":
            # case: equals button pressed immediatly after entering first value - ignore fact equal button was clicked
            if not self.val1:
                self.val1 = self.output["text"]
            # case: user wants to build on to previously equated operation - store operator and wait for next value to be entered
            if self.operator:
                self.prev_operator = self.operator
            self.operator = operator
        
        self.set_state("op")

    def equals(self):
        """
        Performs an operation using stored values and the stored operator.
        """
        # if previously stored value and operator, perform operation with stored value and current output value
        if self.state == "num":
            if self.val1:
                self.val2 = self.output["text"]
                self.val1 = self.operator(self.val1, self.val2)
                self.set_output(self.val1)
        
        # if equals pressed immediatly after an operator button, 
        # ignore the operator button and repeat last operation
        elif self.state == "op":
            if self.val1 and self.val2: # ensures a previous operation exists
                self.operator = self.prev_operator
                self.val1 = self.operator(self.val1, self.val2)
                self.set_output(self.val1)
        
        # repeat previous operation using the result of that operation as val1
        elif self.state == "eq" and self.val1:
            self.val1 = self.operator(self.val1, self.val2)
            self.set_output(self.val1)

        self.set_state("eq")

    def set_output(self, value):
        """
        Cleans output value and displays to output window.

        Parameters:
            value (str): Raw output value.
        """
        cleaned_value = value

        # value is a whole number
        if float(value) % 1 == 0:
            # remove trailing 0's
            cleaned_value = str(int(float(value)))  
            # value is larger than 11 digits -> convert to scientifc notation
            if len(cleaned_value) > 11:
                cleaned_value = "{:.2e}".format(float(cleaned_value))

        # value is decimal value
        else:
            # value has leading 0's creating a value large than 11 digits -> convert to scientific notation
            if cleaned_value[:11] == "0.000000000":
                cleaned_value = "{:.2e}".format(cleaned_value)
            # value is larger than 11 digits -> round decimals place to keep value at most 11 digits
            elif len(cleaned_value) > 11:
                cleaned_value = cleaned_value[:11]
            # remove trailing 0's
            while cleaned_value[-1] == "0":
                cleaned_value = cleaned_value[:len(cleaned_value) - 1]
        
        # set output to cleaned value
        self.output.config(text=cleaned_value)
          
    def clearAll(self):
        """
        Resets the output window to 0 and resets all logic variables.
        """
        self.output.config(text="0")
        self.val1 = ""
        self.val2 = ""
        self.operator = None
        self.prev_operator = None
        self.state = "none"

    def divide(self, dividend, divisor):
        """
        Function for dividing one value by another value.

        Parameters:
            dividend (str): Number to be divided.
            divisor (str): Number dividen is divided by.

        Rerturns:
            (str): The quotient of the dividend and the divisor.
        """
        # divide by 0 error
        if float(divisor) == 0:
            self.clearAll()
            return "Div 0 Error"
        return str(float(dividend) / float(divisor))

    def multiply(self, val1, val2):
        """
        Function used for multiplying 2 values.

        Parameters:
            val1 (str): First value to be multiplied.
            val2 (str): Second value to be multiplied.

        Returns:
            (str): Product of val1 and val2.
        """
        return str(float(val1) * float(val2))

    def subtract(self, minuend, subtrahend):
        """
        Function to subtract one value from another.

        Parameters:
            minuend (str): Starting value of the subtraction problem.
            subtrahend (str): Value being taken away from the starting value.
        
        Returns:
            (str): The difference between the minuend and the subtrahend.
        """
        return str(float(minuend) - float(subtrahend))

    def add(self, val1, val2):
        """
        Function for adding two values together.

        Parameters:
            val1 (str): First value to be added.
            val2 (str): Second value to be added.
        
        Returns:
            (str): The sum of val1 and val2.
        """
        return str(float(val1) + float(val2))

    def change_sign(self):
        """
        Changes current output value to negative if positive, or positive if negative.
        """
        # get change in sign value
        if self.output["text"][0] == "-":
            changed_value = self.output["text"][1:]
        else:
            changed_value = "-" + self.output["text"]
        # update val1 if current output corresponds to the value stored in val1
        if (self.state == "op" or  self.state =="eq") and (float(self.output["text"]) == float(self.val1)):
            self.val1 = changed_value
        # update the output value
        self.output.config(text=changed_value)

    def percent(self):
        """
        Converts value in output window to a decimal percentage.
        """
        percentage = str(float(self.output["text"]) / 100)
        # update val1 if current output corresponds to the value stored in val1
        if (self.state == "op" or  self.state =="eq") and (float(self.output["text"]) == float(self.val1)):
            self.val1 = percentage
        # update the output value
        self.output.config(text=percentage)

    def decimal(self):
        """
        Adds decimal point to current output window value.
        """
        # start new value if clicked after an operator
        if self.state == "op":
            self.output.config(text="0")
        # start fresh operation if pressed after equals 
        elif self.state =="eq":
            self.clearAll()
            self.output.config(text="0")
        # update the output value
        if self.output["text"].find(".") == -1 and len(self.output["text"]) < 11:
            self.output["text"] += "."

    def set_state(self, state):
        """
        Sets the current state of the calculator object.

        Parameters:
            state (str): State the calculator object will be set to.
        """
        self.state = state

    def run(self):
        """
        Calls mainloop function on class window object.
        """
        self.window.mainloop()
