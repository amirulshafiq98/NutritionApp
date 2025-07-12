# input_panel.py

import tkinter as tk
from tkinter import ttk
from config_manager import SETTINGS # Used for potential future validation ranges or default values

class InputPanel(ttk.LabelFrame):
    def __init__(self, parent, app_instance_reference):
        # Initialise the LabelFrame with a descriptive title
        super().__init__(parent, text="Patient Information & Goals", padding="10 10 10 10")
        self.parent = parent
        self.app_instance = app_instance_reference # Reference to the main app for callbacks

        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2) 

        # Initialise Tkinter variables (StringVar, etc.) to hold input values
        self.age_str_var = tk.StringVar(value="")
        self.sex_var = tk.StringVar(value="M")
        self.weight_kg_str_var = tk.StringVar(value="")
        self.height_cm_str_var = tk.StringVar(value="")
        self.activity_level_var = tk.StringVar()
        self.medical_condition_var = tk.StringVar()
        self.weight_goal_var = tk.StringVar()
        self.diabetes_subtype_var = tk.StringVar()

        # Define specific options for dropdowns
        self.diabetes_subtypes = ["Type 1", "Type 2", "Gestational"]
        self.activity_levels = {
            "Sedentary (little or no exercise)": 1.2,
            "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
            "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
            "Very active (hard exercise/sports 6-7 days/week)": 1.725,
            "Extra active (very hard exercise/physical job)": 1.9
        }
        self.medical_conditions = {
            "None": "general",
            "Diabetes": "diabetes",
            "Renal Disease": "renal_disease",
            "Hypertension": "hypertension",
            "Heart Disease": "heart_disease"
        }
        self.weight_goals = {
            "Maintain Weight": "maintenance",
            "Lose Weight": "loss",
            "Gain Weight": "gain"
        }

        # Call a helper method to build and place all the input widgets
        self._create_widgets()

        # Set initial default selections for dropdown menus
        self.activity_level_var.set(list(self.activity_levels.keys())[0])
        self.medical_condition_var.set(list(self.medical_conditions.keys())[0])
        self.weight_goal_var.set(list(self.weight_goals.keys())[0])
        self.diabetes_subtype_var.set(self.diabetes_subtypes[0])

        # Configure dynamic visibility for the diabetes subtype field
        self.medical_condition_var.trace_add("write", self.medical_condition_fields)

        # Call it once at initialisation to set the correct initial state
        self.medical_condition_fields()

    def _create_widgets(self):
        # This method systematically creates and places each input field and its label.
        ttk.Label(self, text="Age (years):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(self, textvariable=self.age_str_var).grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self, text="Sex:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.sex_radio_container = ttk.Frame(self)
        self.sex_radio_container.grid(row=1, column=1, sticky="w", padx=5, pady=2) 
        self.sex_radio_container.grid_columnconfigure(0, weight=1)
        self.sex_radio_container.grid_columnconfigure(1, weight=1)
        ttk.Radiobutton(self.sex_radio_container, text="Male", variable=self.sex_var, value="M") \
            .grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Radiobutton(self.sex_radio_container, text="Female", variable=self.sex_var, value="F") \
            .grid(row=0, column=1, sticky="w")

        ttk.Label(self, text="Weight (kg):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(self, textvariable=self.weight_kg_str_var).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self, text="Height (cm):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(self, textvariable=self.height_cm_str_var).grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self, text="Activity Level:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.activity_level_menu = ttk.OptionMenu(
            self, self.activity_level_var, "", *list(self.activity_levels.keys())
        )
        self.activity_level_menu.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self, text="Medical Condition:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.medical_condition_menu = ttk.OptionMenu(
            self, self.medical_condition_var, "", *list(self.medical_conditions.keys())
        )
        self.medical_condition_menu.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        # Initialise widgets for Diabetes Subtype and Weight Goal.
        self.diabetes_subtype_label = ttk.Label(self, text="Diabetes Subtype:")
        self.diabetes_subtype_menu = ttk.OptionMenu(
            self, self.diabetes_subtype_var, "", *self.diabetes_subtypes
        )
        self.weight_goal_label = ttk.Label(self, text="Weight Goal:")
        self.weight_goal_menu = ttk.OptionMenu(
            self, self.weight_goal_var, "", *list(self.weight_goals.keys())
        )

        self.instruction_label = ttk.Label(self, text="Fill in all fields and click 'Calculate'.")
        self.calculate_button = None # Placeholder as the actual button is passed from app.py.

    def set_calculate_button(self, button):
        # Receives the main 'Calculate' button from the `NutritionApp` class.
        self.calculate_button = button
        self.medical_condition_fields()

    def medical_condition_fields(self, *args):
        # Dynamically adjusts the layout based on the selected medical condition.
        selected_medical_condition = self.medical_condition_var.get()
        current_row = 6

        if self.medical_conditions.get(selected_medical_condition) == "diabetes":
            self.diabetes_subtype_label.grid(row=current_row, column=0, sticky="w", padx=5, pady=2)
            self.diabetes_subtype_menu.grid(row=current_row, column=1, sticky="ew", padx=5, pady=2)
            current_row += 1
        else:
            self.diabetes_subtype_label.grid_forget() # Hide the label
            self.diabetes_subtype_menu.grid_forget() # Hide the dropdown
            self.diabetes_subtype_var.set(self.diabetes_subtypes[0]) # Reset value when hidden

        # These elements are always shown, but their row position depends on the above logic
        self.weight_goal_label.grid(row=current_row, column=0, sticky="w", padx=5, pady=2)
        self.weight_goal_menu.grid(row=current_row, column=1, sticky="ew", padx=5, pady=2)
        current_row += 1

        self.instruction_label.grid(row=current_row, column=0, columnspan=2, pady=10)
        current_row += 1

        if self.calculate_button:
            self.calculate_button.grid(row=current_row, column=0, columnspan=2, pady=10)

    def validate_and_get_numeric_inputs(self):
        # Retrieves raw string inputs, validates them for correctness and reasonable ranges,
        age_str = self.age_str_var.get()
        weight_kg_str = self.weight_kg_str_var.get()
        height_cm_str = self.height_cm_str_var.get()
        parsed_data = {}

        # Individual validation for each numeric input
        if not age_str:
            return False, None, "Age cannot be empty."
        try:
            age = int(age_str)
            if not (1 <= age <= 120):
                return False, None, "Please enter a realistic age between 1 and 120 years."
            parsed_data["age"] = age
        except ValueError:
            return False, None, "Please enter a valid number for Age."

        if not weight_kg_str:
            return False, None, "Weight cannot be empty."
        try:
            weight_kg = float(weight_kg_str)
            if not (20 <= weight_kg <= 300):
                return False, None, "Please enter a realistic weight between 20 and 300 kg."
            parsed_data["weight_kg"] = weight_kg
        except ValueError:
            return False, None, "Please enter a valid number for Weight."

        if not height_cm_str:
            return False, None, "Height cannot be empty."
        try:
            height_cm = float(height_cm_str)
            if not (50 <= height_cm <= 250):
                return False, None, "Please enter a realistic height between 50 and 250 cm."
            parsed_data["height_cm"] = height_cm
        except ValueError:
            return False, None, "Please enter a valid number for Height."
            
        # Collect and store non-numeric inputs directly
        parsed_data["sex"] = self.sex_var.get()
        parsed_data["activity_factor"] = self.activity_levels.get(self.activity_level_var.get())
        parsed_data["activity_level_description"] = self.activity_level_var.get()
        
        selected_medical_desc = self.medical_condition_var.get()
        medical_condition_key = self.medical_conditions.get(selected_medical_desc, "general")
        parsed_data["medical_condition"] = medical_condition_key
        parsed_data["medical_condition_description"] = selected_medical_desc

        selected_weight_goal_desc = self.weight_goal_var.get()
        weight_goal_key = self.weight_goals.get(selected_weight_goal_desc, "maintenance")
        parsed_data["weight_goal"] = weight_goal_key
        parsed_data["weight_goal_description"] = selected_weight_goal_desc

        if medical_condition_key == "diabetes":
            parsed_data["diabetes_subtype"] = self.diabetes_subtype_var.get()
        else:
            parsed_data["diabetes_subtype"] = "N/A" # Default to N/A if not relevant

        return True, parsed_data, None

    def get_all_inputs(self):
        # A helper method to retrieve all current input values directly as a dictionary
        selected_activity_desc = self.activity_level_var.get()
        selected_medical_desc = self.medical_condition_var.get()
        selected_weight_goal_desc = self.weight_goal_var.get()

        medical_condition_key = self.medical_conditions.get(selected_medical_desc, "general")
        weight_goal_key = self.weight_goals.get(selected_weight_goal_desc, "maintenance")

        inputs = {
            "age_str": self.age_str_var.get(),
            "sex": self.sex_var.get(),
            "weight_kg_str": self.weight_kg_str_var.get(),
            "height_cm_str": self.height_cm_str_var.get(),
            "activity_factor": self.activity_levels.get(selected_activity_desc),
            "activity_level_description": selected_activity_desc,
            "medical_condition": medical_condition_key,
            "medical_condition_description": selected_medical_desc,
            "weight_goal": weight_goal_key,
            "weight_goal_description": selected_weight_goal_desc
        }

        if medical_condition_key == "diabetes":
            inputs["diabetes_subtype"] = self.diabetes_subtype_var.get()
        else:
            inputs["diabetes_subtype"] = "N/A"

        return inputs