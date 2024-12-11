import tkinter as tk

class Calculator:
    """
    Class containing calculator UI and operation logic.
    """

    def __init__(self):
        """
        Initializes a Calculator object.
        """
        # ################# #
        #   Create Window   #
        # ################# #
        self.window = tk.Tk()
        self.window.minsize(300, 400)
        self.window.title("Simple Calculator")


        # #################### #
        #  Create Output Area  #
        # #################### #
        self.output = tk.Label(self.window)
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
        self.clear_button = self.create_button("AC")
        self.displaymode_button = self.create_button("\u263C", self.switch_display)
        
        # -functional buttons
        self.buttons["functional"] = [
            self.clear_button,
            self.create_button("+/-"),
            self.create_button("%"),
        ]
    
        # -numerical buttons
        for i in range(10):
            self.buttons["numerical"].append(self.create_button(str(i)))
        # --non-numerical buttons that follow same styling as numerical buttons, ordered for easy placing in grid
        self.buttons["numerical"].insert(0, self.displaymode_button)
        self.buttons["numerical"].insert(2, self.create_button("."))

        # -operational buttons
        self.buttons["operational"] = [
            self.create_button("\u2797"),   # division
            self.create_button("\u2716"),   # multiplication
            self.create_button("\u2796"),   # minus
            self.create_button("\u2795"),   # plus
            self.create_button("\u3013")    # equals
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
        self.window.rowconfigure(0, weight=6)
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
                
            


    def run(self):
        """
        Calls mainloop function on class window object.
        """
        self.window.mainloop()
