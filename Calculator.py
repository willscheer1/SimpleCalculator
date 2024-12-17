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
        self.buttons["numerical"].insert(2, self.create_button("."))

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
        if self.state == "eq":
            self.clearAll()

        if self.state == "none":
            self.output.config(text=value)

        elif self.state == "num" and len(self.output["text"]) < 11: # max output length of 12
            self.output["text"] += value

        elif self.state == "op":
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
        if self.state == "num":
            if not self.val1:
                self.val1 = self.output["text"]
            else:   # operate on previosly entered values
                self.val2 = self.output["text"]
                self.val1 = self.operator(self.val1, self.val2)
                self.output.config(text=self.val1)  # set output value
            # store operator
            if self.operator:
                self.prev_operator = self.operator
            self.operator = operator

        elif self.state == "op":
            self.operator = operator

        elif self.state == "eq":
            # case: equals button pressed immediatly after entering first value
            if not self.val1:
                self.val1 = self.output["text"]
            # case: build on to previously equated operation
            if self.operator:
                self.prev_operator = self.operator
            self.operator = operator
        
        self.set_state("op")

    def equals(self):
        """
        """
        if self.state == "num":
            if self.val1:
                self.val2 = self.output["text"]
                self.val1 = self.operator(self.val1, self.val2)
                self.output.config(text=self.val1)
        
        elif self.state == "op":
            if self.val1 and self.val2:
                self.operator = self.prev_operator
                self.val1 = self.operator(self.val1, self.val2)
                self.output.config(text=self.val1)
        
        elif self.state == "eq" and self.val1:
            self.val1 = self.operator(self.val1, self.val2)
            self.output.config(text=self.val1)

        self.set_state("eq")

    def set_output(self, value):
        """
        Cleans output value and displays to output window.

        Parameters:
            value (str): Raw output value.
        """
        # handle values with length > 12 (scientific notation?)
        # handle un-needed decimals (trailing zeros i.e 1.00)
        # replace all self.output.configs to this function
        pass
  
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
        """
        # ensure logic variables are updated if needed, not just visual output value
        pass

    def percent(self):
        """
        """
        # ensure logic variables are updated if needed, not just visual output value
        pass

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
