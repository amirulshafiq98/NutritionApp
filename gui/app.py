# app.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import sys
import io

from config_manager import SETTINGS # Accesses predefined application settings
from logger_config import app_logger # Used for logging events and errors within the app

from calculations import calculate_bmr, calculate_tdee, get_macro_recommendations, calculate_bmi, classify_bmi, get_micronutrient_guidelines
from gui.input_panel import InputPanel # Manages the user input fields
from gui.results_panel import ResultsPanel # Displays the calculated nutrition plan

class NutritionApp:
    def __init__(self, master):
        self.master = master
        master.title("Nutrition Therapy Calculator")
        master.geometry("1000x800")
        master.resizable(True, True)

        # Initialise the InputPanel to handle all user data entry
        self.input_panel = InputPanel(master, self)

        # Position the input panel at the top, allowing it to define its own internal layout
        self.input_panel.pack(pady=10, padx=10, fill=tk.BOTH, expand=False)

        # Create the 'Calculate' button. Defined here and then passed to InputPanel
        self.calculate_button = ttk.Button(self.input_panel, text="Calculate Nutrition Plan", command=self.calculate_plan)
        self.input_panel.set_calculate_button(self.calculate_button)

        # Initialise the ResultsPanel for displaying calculation outputs
        self.results_panel = ResultsPanel(master)
        self.results_panel.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Create a frame to group the 'Save Plan' and 'Clear Results' buttons
        self.button_frame = ttk.Frame(self.master, padding="5 5 5 5")
        self.button_frame.pack(pady=10)

        # Configure columns within this frame to distribute buttons evenly
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Setup 'Save Plan' button, linked to the `save_results` method
        self.save_button = ttk.Button(self.button_frame, text="Save Plan", command=self.save_results)
        self.save_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Setup 'Clear Results' button, linked to the `clear_results` method
        self.clear_button = ttk.Button(self.button_frame, text="Clear Results", command=self.clear_results)
        self.clear_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Store the last calculated data
        self.last_patient_data = None
        self.last_calculated_results = None

    def calculate_plan(self):
        # This method handles the primary application flow: input validation, calculation, and display
        app_logger.info("Calculation initiated by user.")
        try:
            # Delegate input validation and numeric conversion to the InputPanel
            is_valid, patient_data, error_message = self.input_panel.validate_and_get_numeric_inputs()

            if not is_valid:
                # If validation fails, display an error message and halt the calculation
                messagebox.showerror("Input Error", error_message)
                app_logger.warning(f"Calculation aborted due to invalid input: {error_message}")
                return
            
            # Extract validated numerical data for calculations
            age = patient_data["age"]
            sex = patient_data["sex"]
            weight_kg = patient_data["weight_kg"]
            height_cm = patient_data["height_cm"]
            activity_factor = patient_data["activity_factor"]
            medical_condition = patient_data["medical_condition"]
            weight_goal = patient_data["weight_goal"]
            diabetes_subtype = patient_data["diabetes_subtype"]

            # Perform sequential nutrition calculations
            bmi = calculate_bmi(weight_kg, height_cm)
            bmi_classification = classify_bmi(bmi)
            bmr = calculate_bmr(age, sex, weight_kg, height_cm)
            tdee = calculate_tdee(bmr, activity_factor)

            # Adjust TDEE based on the user's weight goal
            adjusted_tdee = tdee
            if weight_goal == "loss":
                adjusted_tdee -= SETTINGS["calorie_adjustments"]["weight_loss_deficit_kcal"]

                # Enforce a minimum calorie intake for safety, based on gender
                min_cal = SETTINGS["min_calories"]["female"] if sex == "F" else SETTINGS["min_calories"]["male"]
                
                if adjusted_tdee < min_cal:
                    adjusted_tdee = min_cal
                    app_logger.info(f"Adjusted TDEE capped at minimum for {sex}: {min_cal} kcal.")
                else:
                    app_logger.info(f"Adjusted TDEE for weight loss: {adjusted_tdee} kcal.")
            elif weight_goal == "gain":
                adjusted_tdee += SETTINGS["calorie_adjustments"]["weight_gain_surplus_kcal"]

            # Retrieve macronutrient percentages, defaulting to 'general' if no specific condition applies
            macro_percentages = SETTINGS["macro_percentages"].get(medical_condition, SETTINGS["macro_percentages"]["general"])

            # Calculate macronutrient grams based on adjusted TDEE and percentages
            macros = get_macro_recommendations(adjusted_tdee, macro_percentages, weight_kg)

            # Fetch micronutrient guidelines relevant to the specified medical condition
            micronutrient_guidelines = get_micronutrient_guidelines(medical_condition)

            # Consolidate all calculated results into a single dictionary for easy handling and display
            calculated_results = {
                "bmi": bmi,
                "bmi_classification": bmi_classification,
                "bmr": bmr,
                "tdee": tdee,
                "adjusted_tdee": adjusted_tdee,
                "macros": macros,
                "micronutrient_guidelines": micronutrient_guidelines
            }

            # Store the patient data and calculated results for potential saving
            self.last_patient_data = patient_data
            self.last_calculated_results = calculated_results

            # Display the results via the ResultsPanel, separating display logic
            self.results_panel.display_plan(patient_data, calculated_results)
            app_logger.info("Nutrition plan successfully calculated and displayed.")

        except Exception as e:
            # Catch any unexpected errors during calculation and provide user feedback
            messagebox.showerror("Error", f"An unexpected error occurred during calculation: {e}")
            app_logger.critical(f"Unexpected error during calculation: {e}", exc_info=True)

    def save_results(self):
        # Handles saving the currently displayed nutrition plan to a text file
        if self.last_patient_data is None or self.last_calculated_results is None:
            messagebox.showwarning("No Plan to Save", "Please calculate a nutrition plan first before saving.")
            return

        # Prompt the user to select a file path for saving
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Nutrition Plan"
        )

        if file_path:
            # Temporarily redirect standard output to capture the text generated by display_plan
            report_content = self.results_panel.get_content()
            
            if not report_content.strip(): # Add a check for empty content
                messagebox.showwarning("Empty Plan", "The results panel is empty. Please calculate a plan before saving.")
                app_logger.warning("Attempted to save an empty nutrition plan.")
                return

            try:
                # Write the captured content to the chosen file
                with open(file_path, 'w') as f:
                    f.write(report_content)
                messagebox.showinfo("Save Successful", f"Nutrition plan saved successfully to:\n{file_path}")
                app_logger.info(f"Nutrition plan saved to: {file_path}")
            except IOError as e:
                # Handle file system errors during saving
                messagebox.showerror("Save Error", f"Error saving file: {e}")
                app_logger.error(f"File saving error: {file_path}: {e}")
            except Exception as e:
                # Catch any other unexpected errors during the save process
                messagebox.showerror("Save Error", f"An unexpected error occurred during save: {e}")
                app_logger.critical(f"Unexpected error during save: {e}", exc_info=True)
        else:
            app_logger.info("Save operation cancelled by user.")

    def clear_results(self):
        # Resets the results display and clears any stored calculation data
        self.results_panel.clear_results()
        self.last_patient_data = None
        self.last_calculated_results = None
        app_logger.info("Results display and stored data cleared.")