# results_panel.py

import tkinter as tk
from tkinter import ttk
from config_manager import SETTINGS # Used for referencing specific settings like calorie adjustment values
from logger_config import app_logger # Logs information about the display process.

class ResultsPanel(ttk.LabelFrame):
    def __init__(self, parent):
        # Initialise the LabelFrame to create a titled section for results
        super().__init__(parent, text="Nutrition Plan Results", padding="10 10 10 10")
        self.parent = parent
        self.grid_columnconfigure(0, weight=1) # Allows the text area to expand horizontally.

        # Create a Text widget for displaying multi-line results
        self.results_text = tk.Text(self, wrap=tk.WORD, height=20, width=80, font=("Courier New", 10))
        self.results_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.results_text.config(state=tk.DISABLED) # Prevent user editing

        # Add a scrollbar to the text widget, crucial for viewing long reports
        self.results_scroll = ttk.Scrollbar(self, command=self.results_text.yview)
        self.results_scroll.grid(row=0, column=1, sticky="ns")
        self.results_text.config(yscrollcommand=self.results_scroll.set)

    def display_plan(self, patient_data, calculated_results):
        # Formats and inserts the patient's input data and the calculated nutrition results into the `results_text` area
        self.results_text.config(state=tk.NORMAL) # Temporarily enable editing to insert text
        self.results_text.delete(1.0, tk.END) # Clear any previous content.
        app_logger.debug(f"Preparing to display results for: {patient_data['medical_condition_description']}")

        output_lines = []

        # Section for Patient Information:
        output_lines.append("--- Patient Information ---")
        output_lines.append(f"Age: {patient_data['age']} years")
        output_lines.append(f"Sex: {patient_data['sex']}")
        output_lines.append(f"Weight: {patient_data['weight_kg']:.1f} kg")
        output_lines.append(f"Height: {patient_data['height_cm']:.1f} cm")
        output_lines.append(f"Activity Level: {patient_data['activity_level_description']}")
        output_lines.append(f"Medical Condition: {patient_data['medical_condition_description']}")
        if patient_data['medical_condition'] == 'diabetes':
            output_lines.append(f"  Diabetes Subtype: {patient_data['diabetes_subtype']}")
        output_lines.append(f"Weight Goal: {patient_data['weight_goal_description']}")
        output_lines.append("")

        # Section for Health Metrics:
        output_lines.append("--- Health Metrics ---")
        output_lines.append(f"BMI: {calculated_results['bmi']:.2f} kg/m²")
        output_lines.append(f"BMI Classification: {calculated_results['bmi_classification']}")
        output_lines.append("")

        # Section for Calorie & Macronutrient Recommendations:
        output_lines.append("--- Calorie & Macronutrient Recommendations ---")
        output_lines.append(f"Basal Metabolic Rate (BMR): {calculated_results['bmr']:.0f} kcal/day")
        output_lines.append(f"Total Daily Energy Expenditure (TDEE): {calculated_results['tdee']:.0f} kcal/day")
        
        # Clarify calorie adjustments based on the user's weight goal
        if patient_data['weight_goal'] == "loss":
            output_lines.append(f"Target Calories (for Weight Loss): {calculated_results['adjusted_tdee']:.0f} kcal/day (adjusting by -{SETTINGS['calorie_adjustments']['weight_loss_deficit_kcal']} kcal)")
        elif patient_data['weight_goal'] == "gain":
            output_lines.append(f"Target Calories (for Weight Gain): {calculated_results['adjusted_tdee']:.0f} kcal/day (adjusting by +{SETTINGS['calorie_adjustments']['weight_gain_surplus_kcal']} kcal)")
        else:
            output_lines.append(f"Target Calories (for Weight Maintenance): {calculated_results['adjusted_tdee']:.0f} kcal/day")

        macros = calculated_results['macros']
        output_lines.append("Macronutrient Breakdown:")
        output_lines.append(f"  Protein: {macros['protein_g']:.0f}g ({macros['protein_pct']:.0%})")
        output_lines.append(f"  Carbohydrates: {macros['carb_g']:.0f}g ({macros['carb_pct']:.0%})")
        output_lines.append(f"  Fats: {macros['fat_g']:.0f}g ({macros['fat_pct']:.0%})")
        output_lines.append("")

        # Section for Micronutrient Guidelines:
        output_lines.append("--- General Micronutrient Guidelines ---")
        for nutrient, guideline in calculated_results['micronutrient_guidelines'].items():
            output_lines.append(f"  {nutrient}: {guideline}")
        output_lines.append("")

        # Section for Specific Dietary Considerations/Warnings:
        output_lines.append("--- Important Dietary Considerations ---")
        warnings_list = []
        medical_condition = patient_data['medical_condition']

        # Add condition-specific advice
        if medical_condition == "diabetes":
            warnings_list.append("For Diabetes, focus on consistent carbohydrate intake and complex carbohydrates.")
            warnings_list.append("  - Monitor blood sugar levels regularly.")
            warnings_list.append("  - Prioritize whole foods, fiber-rich vegetables, and lean proteins.")
            warnings_list.append("  - Distribute carbohydrate intake throughout the day.")
            warnings_list.append("  - Avoid skipping meals, especially if on medication that lowers blood sugar.")

        if medical_condition == "hypertension":
            warnings_list.append("For Hypertension, focus on a low-sodium diet (e.g., DASH diet). Consult a healthcare professional.")

        if medical_condition == "heart_disease":
            warnings_list.append("For Heart Disease, limit saturated fats to less than 7% of total calories. Consult a healthcare professional.")

        if warnings_list:
            for warning in warnings_list:
                output_lines.append(f"  - {warning}")
        else:
            output_lines.append("  No specific warnings based on your inputs or conditions.")

        # Disclaimer at the end for proper context
        output_lines.append("\n--- IMPORTANT DISCLAIMER ---")
        output_lines.append("These are *estimates* and *examples* based on general guidelines.")
        output_lines.append("Always consult a qualified healthcare professional (like a Registered Dietitian) for personalized nutrition therapy, especially for specific medical conditions.")

        # Insert all lines into the text widget
        self.results_text.insert(tk.END, "\n".join(output_lines))
        self.results_text.config(state=tk.DISABLED) # Revert to read-only

    def get_content(self):
        """
        Retrieves all text currently displayed in the results panel.
        This is primarily used when saving the displayed report to a file.
        """
        return self.results_text.get(1.0, tk.END)

    def clear_results(self):
        """
        Clears all content from the results display area.
        """
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        app_logger.info("Results display cleared in UI.")