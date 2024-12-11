import tkinter as tk
import tkinter.font as tkFont

class Calculator:
    """
    Class containing calculator UI and operation logic.
    """

    def __init__(self):
        """
        Initializes a Calculator object.
        """
        # ################# #
        #  Style Variables  #
        # ################# #
        # --light

        # --dark
        self.window_bgcolor_dark = "#000"
        self.button_txtcolor_dark = "#FFF"
        self.button_func_bgcolor_dark = "#666"
        self.button_num_bgcolor_dark = "#222"
        self.button_op_bgcolor_dark = "#f8af47"


        # ################# #
        #   Create Window   #
        # ################# #
        self.window = tk.Tk()
        self.window.minsize(300, 400)
        self.window.title("Simple Calculator")


        # #################### #
        #  Create Output Area  #
        # #################### #
        self.output = tk.Label(self.window, bg=self.window_bgcolor_dark)
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
        self.clear_button = self.create_button("AC", self.button_func_bgcolor_dark, self.button_txtcolor_dark)
        self.displaymode_button = self.create_button("\u263C", self.button_num_bgcolor_dark, self.button_txtcolor_dark)
        
        # -functional buttons
        self.buttons["functional"] = [
            self.clear_button,
            self.create_button("+/-", self.button_func_bgcolor_dark, self.button_txtcolor_dark),
            self.create_button("%", self.button_func_bgcolor_dark, self.button_txtcolor_dark),
        ]
    
        # -numerical buttons
        for i in range(10):
            self.buttons["numerical"].append(self.create_button(str(i), self.button_num_bgcolor_dark, self.button_txtcolor_dark))
        # --non-numerical buttons that follow same styling as numerical buttons, ordered for easy placing in grid
        self.buttons["numerical"].insert(0, self.displaymode_button)
        self.buttons["numerical"].insert(2, self.create_button(".", self.button_num_bgcolor_dark, self.button_txtcolor_dark))

        # -operational buttons
        self.buttons["operational"] = [
            self.create_button("\u2797", self.button_op_bgcolor_dark, self.button_txtcolor_dark),   # division
            self.create_button("\u2716", self.button_op_bgcolor_dark, self.button_txtcolor_dark),   # multiplication
            self.create_button("\u2796", self.button_op_bgcolor_dark, self.button_txtcolor_dark),   # minus
            self.create_button("\u2795", self.button_op_bgcolor_dark, self.button_txtcolor_dark),   # plus
            self.create_button("\u3013", self.button_op_bgcolor_dark, self.button_txtcolor_dark)    # equals
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
        # configure columns to fill width of window
        for i in range(4):
            self.window.columnconfigure(i, weight=1)

        # configure rows to fill height of window
        self.window.rowconfigure(0, weight=6)
        for i in range(1, 6):
            self.window.rowconfigure(i, weight=1)


    def create_button(self, text, bg_color, text_color, function=None):
        """
        Creates Tkinter button widget.

        Parameters:
            text (str): Text value displayed on button.
            bg_color (str): Hex value for background color of button.
            text_color (str): Hex value for text color.
            function (function): Function called when button is clicked.
        
        Returns:
            Button Widget: A button widget with the specified attributes.
        """
        return tk.Button(self.window,
                         text=text,
                         bg=bg_color,
                         fg=text_color,
                         font=("Monospace", 16),
                         padx=0,
                         pady=0
                        )

    def run(self):
        """
        Calls mainloop function on class window object.
        """
        self.window.mainloop()
