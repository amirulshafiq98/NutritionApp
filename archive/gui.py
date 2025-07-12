# gui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog # Import filedialog here
import sys
import io # FIX: ADDED THIS LINE TO IMPORT THE IO MODULE

from config_manager import SETTINGS
from logger_config import app_logger

# Import calculations functions
from calculations import calculate_bmr, calculate_tdee, get_macro_recommendations, calculate_bmi, classify_bmi, get_micronutrient_guidelines

class NutritionApp:
    def __init__(self, master):
        self.master = master
        master.title("Nutrition Therapy Calculator")
        master.geometry("1000x800")
        master.resizable(True, True)

        # Initialize Tkinter variables to store input values
        self.age_var = tk.IntVar(value=30)
        self.sex_var = tk.StringVar(value="M")
        self.weight_var = tk.DoubleVar(value=70.0)
        self.height_var = tk.DoubleVar(value=170.0)
        
        # Variables for dropdowns (OptionMenu)
        self.activity_level_var = tk.StringVar()
        self.medical_condition_var = tk.StringVar()
        self.weight_goal_var = tk.StringVar()

        # Frame for Input Section
        self.input_frame = ttk.LabelFrame(master, text="Patient Information & Goals", padding="10 10 10 10")
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure columns within the input_frame to expand
        self.input_frame.grid_columnconfigure(0, weight=1) # Labels
        self.input_frame.grid_columnconfigure(1, weight=2) # Input fields

        # Frame for Results Section
        self.results_frame = ttk.LabelFrame(master, text="Nutrition Plan Results", padding="10 10 10 10")
        self.results_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        master.grid_rowconfigure(1, weight=1) 
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder for output labels
        self.results_text = tk.Text(self.results_frame, wrap=tk.WORD, height=20, width=80, font=("Courier New", 10))
        self.results_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.results_text.config(state=tk.DISABLED) # Make it read-only initially

        # Create the widgets for inputs and the Calculate button
        self.create_input_widgets()
        self.create_buttons()

    def create_input_widgets(self):
        row_idx = 0

        # Age Input
        ttk.Label(self.input_frame, text="Age (years):").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(self.input_frame, textvariable=self.age_var, width=10).grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        # Sex Input (Radio Buttons)
        ttk.Label(self.input_frame, text="Sex:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        sex_frame = ttk.Frame(self.input_frame)
        sex_frame.grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        ttk.Radiobutton(sex_frame, text="Male", variable=self.sex_var, value="M").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sex_frame, text="Female", variable=self.sex_var, value="F").pack(side=tk.LEFT, padx=5)
        row_idx += 1

        # Weight Input
        ttk.Label(self.input_frame, text="Weight (kg):").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(self.input_frame, textvariable=self.weight_var, width=10).grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        # Height Input
        ttk.Label(self.input_frame, text="Height (cm):").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(self.input_frame, textvariable=self.height_var, width=10).grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        # Activity Level (OptionMenu)
        ttk.Label(self.input_frame, text="Activity Level:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.activity_levels = {
            "1. Sedentary (little or no exercise)": 1.2,
            "2. Lightly active (light exercise/sports 1-3 days/week)": 1.375,
            "3. Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
            "4. Very active (hard exercise/sports 6-7 days a week)": 1.725,
            "5. Super active (very hard exercise/sports & a physical job)": 1.9
        }
        activity_options = list(self.activity_levels.keys())
        self.activity_level_var.set(activity_options[0]) # Set default
        self.activity_menu = ttk.OptionMenu(self.input_frame, self.activity_level_var, activity_options[0], *activity_options)
        self.activity_menu.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
        row_idx += 1

        # Medical Condition (OptionMenu)
        ttk.Label(self.input_frame, text="Medical Condition:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.medical_conditions = {
            "General/Healthy": "general",
            "Diabetes": "diabetes",
            "Renal Disease": "renal_disease",
            "Hypertension": "hypertension",
            "Heart Disease": "heart_disease"
        }
        medical_options = list(self.medical_conditions.keys())
        self.medical_condition_var.set(medical_options[0]) # Set default
        self.medical_menu = ttk.OptionMenu(self.input_frame, self.medical_condition_var, medical_options[0], *medical_options)
        self.medical_menu.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
        row_idx += 1

        # Weight Goal (OptionMenu)
        ttk.Label(self.input_frame, text="Weight Goal:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.weight_goals = {
            "Maintain current weight": "maintain",
            "Lose weight": "lose",
            "Gain weight": "gain"
        }
        goal_options = list(self.weight_goals.keys())
        self.weight_goal_var.set(goal_options[0]) # Set default
        self.weight_goal_menu = ttk.OptionMenu(self.input_frame, self.weight_goal_var, goal_options[0], *goal_options)
        self.weight_goal_menu.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
        row_idx += 1
        
        # Add a clear label indicating instructions or tips within the input frame
        ttk.Label(self.input_frame, text="Enter your details above and click 'Calculate' for your nutrition plan.",
                  font=("Arial", 9, "italic")).grid(row=row_idx, column=0, columnspan=2, pady=10)

    def create_buttons(self):
        # Frame for Buttons (e.g., Calculate, Clear, Save)
        self.button_frame = ttk.Frame(self.master, padding="5 5 5 5")
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)


        self.calculate_button = ttk.Button(self.button_frame, text="Calculate Nutrition Plan", command=self.calculate_plan)
        self.calculate_button.grid(row=0, column=0, padx=5, pady=5)

        self.save_button = ttk.Button(self.button_frame, text="Save Plan to File", command=self.save_plan)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Results", command=self.clear_results)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)


    def calculate_plan(self):
        """
        Gathers inputs from GUI, performs calculations, and displays results.
        """
        self.results_text.config(state=tk.NORMAL) # Enable text widget to write
        self.results_text.delete(1.0, tk.END) # Clear previous results
        app_logger.info("Calculate button clicked.")

        # --- Input Gathering and Validation (from GUI widgets) ---
        try:
            age = self.age_var.get()
            sex = self.sex_var.get()
            weight_kg = self.weight_var.get()
            height_cm = self.height_var.get()
            
            # Get selected value from OptionMenu (the actual factor/key)
            selected_activity_desc = self.activity_level_var.get()
            activity_factor = self.activity_levels[selected_activity_desc]

            selected_medical_desc = self.medical_condition_var.get()
            medical_condition = self.medical_conditions[selected_medical_desc]
            app_logger.debug(f"Medical condition selected (internal key): {medical_condition}")

            selected_weight_goal_desc = self.weight_goal_var.get()
            weight_goal = self.weight_goals[selected_weight_goal_desc]
            app_logger.debug(f"Weight goal selected (internal key): {weight_goal}")

            # Basic Validation (more robust validation can be added here)
            if not all([age, sex, weight_kg, height_cm, activity_factor, medical_condition, weight_goal]):
                raise ValueError("All fields must be filled.")
            if age <= 0 or weight_kg <= 0 or height_cm <= 0:
                raise ValueError("Age, Weight, and Height must be positive numbers.")
            
            # --- Perform Calculations (using functions from calculations.py) ---
            patient_data = {
                'age': age, 'sex': sex, 'weight_kg': weight_kg, 'height_cm': height_cm,
                'activity_factor': activity_factor, 'activity_level_description': selected_activity_desc,
                'medical_condition': medical_condition, 'weight_goal': weight_goal
            }

            calculated_results = {}
            calculated_results['bmi'] = calculate_bmi(weight_kg, height_cm)
            calculated_results['bmi_category'] = classify_bmi(calculated_results['bmi'])
            
            calculated_results['bmr'] = calculate_bmr(age, sex, weight_kg, height_cm)
            calculated_results['tdee'] = calculate_tdee(calculated_results['bmr'], activity_factor)
            
            # FIX: Add weight_goal to calculated_results for display_results
            calculated_results['weight_goal'] = weight_goal 

            # Adjust calories based on weight goal and SETTINGS
            recommended_calories = calculated_results['tdee'] # Start with TDEE as the baseline
            if weight_goal == "lose":
                original_recommended_calories = recommended_calories - SETTINGS['calorie_adjustments']['weight_loss_deficit_kcal']
                
                if sex == 'F' and original_recommended_calories < SETTINGS['min_calories']['female']:
                    recommended_calories = SETTINGS['min_calories']['female']
                elif sex == 'M' and original_recommended_calories < SETTINGS['min_calories']['male']:
                    recommended_calories = SETTINGS['min_calories']['male']
                else:
                     recommended_calories = original_recommended_calories

            elif weight_goal == "gain":
                recommended_calories = calculated_results['tdee'] + SETTINGS['calorie_adjustments']['weight_gain_surplus_kcal']
            calculated_results['recommended_calories'] = recommended_calories


            calculated_results['protein_g'], calculated_results['carb_g'], calculated_results['fat_g'] = \
                get_macro_recommendations(recommended_calories, medical_condition, weight_kg)
            
            calculated_results['micronutrient_guidelines'] = get_micronutrient_guidelines(medical_condition)

            # Store the final calculated data for potential saving
            self.last_patient_data = patient_data
            self.last_calculated_results = calculated_results

            # --- Display Results ---
            self.display_results(patient_data, calculated_results)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Validation Error: {e}")
            app_logger.error(f"GUI Input Validation Error: {e}")
        except tk.TclError:
            messagebox.showerror("Input Error", "Please ensure Age, Weight, and Height are valid numbers.")
            app_logger.error("GUI Tkinter Variable Conversion Error. User likely entered non-numeric text.")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An unexpected error occurred during calculation: {e}")
            app_logger.critical(f"An unexpected error occurred during GUI calculation: {e}", exc_info=True)
        finally:
            self.results_text.config(state=tk.DISABLED) # Disable text widget after writing

    def display_results(self, patient_data, calculated_results):
        """
        Formats and displays the results in the Text widget.
        """
        app_logger.debug(f"Displaying results for medical condition: {patient_data['medical_condition']}")

        output_lines = []
        output_lines.append("--- Personalized Nutrition Plan ---")
        output_lines.append(f"Your Body Mass Index (BMI): {calculated_results['bmi']:.2f} ({calculated_results['bmi_category']})")
        output_lines.append(f"Basal Metabolic Rate (BMR): {calculated_results['bmr']:.0f} kcal/day")
        output_lines.append(f"Total Daily Energy Expenditure (TDEE): {calculated_results['tdee']:.0f} kcal/day")

        if calculated_results['weight_goal'] in ["lose", "gain"]:
            output_lines.append(f"Recommended Daily Calories for {calculated_results['weight_goal'].capitalize()}ing weight: {calculated_results['recommended_calories']:.0f} kcal")
        else:
            output_lines.append(f"Recommended Daily Calories (Maintain): {calculated_results['recommended_calories']:.0f} kcal")

        output_lines.append("\nMacronutrient Distribution:")
        output_lines.append(f"  Protein: {calculated_results['protein_g']:.1f} grams")
        output_lines.append(f"  Carbohydrates: {calculated_results['carb_g']:.1f} grams")
        output_lines.append(f"  Fats: {calculated_results['fat_g']:.1f} grams")
        
        output_lines.append("\nMicronutrient Guidelines:")
        if calculated_results['micronutrient_guidelines']:
            for nutrient, guideline in calculated_results['micronutrient_guidelines'].items():
                output_lines.append(f"  - {nutrient.replace('_', ' ').title()}: {guideline}")
        else:
            output_lines.append("  No specific micronutrient guidelines for your condition at this time.")

        output_lines.append("\nImportant Notes and Warnings:")
        warnings_list = []
        if calculated_results['bmi_category'] == "Underweight":
            warnings_list.append("Your BMI suggests you might be underweight. Please consult a healthcare professional.")
        elif calculated_results['bmi_category'].startswith("Obesity"):
            warnings_list.append(f"Your BMI suggests you are in an obesity category ({calculated_results['bmi_category']}). Please consult a healthcare professional for personalized guidance.")
        
        # Check against min_calories only if the recommended calories were capped
        if patient_data['sex'] == 'F' and calculated_results['recommended_calories'] == SETTINGS['min_calories']['female']:
            warnings_list.append(f"Warning: Female recommended calories ({calculated_results['recommended_calories']:.0f}) were capped at minimum ({SETTINGS['min_calories']['female']} kcal). Please consult a healthcare professional for safe guidance.")
        elif patient_data['sex'] == 'M' and calculated_results['recommended_calories'] == SETTINGS['min_calories']['male']:
            warnings_list.append(f"Warning: Male recommended calories ({calculated_results['recommended_calories']:.0f}) were capped at minimum ({SETTINGS['min_calories']['male']} kcal). Please consult a healthcare professional for safe guidance.")


        # Medical condition specific warnings
        if patient_data['medical_condition'] == "renal_disease":
            warnings_list.append("\n!!! IMPORTANT WARNING for Renal Disease Patients !!!")
            warnings_list.append("This tool provides *generalized* estimates. Renal disease nutrition is highly complex.")
            warnings_list.append("Fluid, potassium, and phosphorus restrictions are critical and individualized.")
            warnings_list.append("ALWAYS consult a nephrologist and a Registered Dietitian specializing in renal nutrition.")
            warnings_list.append("These calculations DO NOT replace professional medical advice.")
            warnings_list.append("Fluid restrictions: Individualized. Consult RD.") 
        if patient_data['medical_condition'] == "diabetes":
            warnings_list.append("Fiber Recommendation for Diabetes: Aim for 25-30 grams of fiber per day.")
            warnings_list.append("Meal Timing Suggestions for Diabetes:")
            warnings_list.append("- Aim for consistent meal and snack times daily.")
            warnings_list.append("- Distribute carbohydrate intake evenly throughout the day.")
            warnings_list.append("- Avoid skipping meals, especially if on medication that lowers blood sugar.")
        if patient_data['medical_condition'] == "hypertension":
            warnings_list.append("For Hypertension, focus on a low-sodium diet (e.g., DASH diet). Consult a healthcare professional.")
        if patient_data['medical_condition'] == "heart_disease":
            warnings_list.append("For Heart Disease, limit saturated fats to less than 7% of total calories. Consult a healthcare professional.")

        if warnings_list:
            for warning in warnings_list:
                output_lines.append(f"  - {warning}")
        else:
            output_lines.append("  No specific warnings based on your inputs or conditions.")
        
        output_lines.append("\n--- IMPORTANT DISCLAIMER ---")
        output_lines.append("These are *estimates* and *examples* based on general guidelines.")
        output_lines.append("Always consult a qualified healthcare professional (like a Registered Dietitian) for personalized nutrition therapy, especially for specific medical conditions.")

        self.results_text.insert(tk.END, "\n".join(output_lines))

    def save_plan(self):
        """
        Prompts user for filename and saves the last calculated nutrition plan.
        """
        if not hasattr(self, 'last_patient_data') or not hasattr(self, 'last_calculated_results'):
            messagebox.showwarning("Save Error", "Please calculate a nutrition plan first before saving.")
            app_logger.warning("Attempted to save plan before calculation.")
            return

        # FIX: Call filedialog.asksaveasfilename() to get the file_path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Nutrition Plan"
        )

        if file_path: # FIX: Only proceed if a file path was selected
            # Temporarily redirect text output to a string
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            # Render the results into the StringIO buffer
            self.display_results(self.last_patient_data, self.last_calculated_results)
            
            # Get the string content and restore stdout
            report_content = sys.stdout.getvalue()
            sys.stdout = old_stdout

            try:
                with open(file_path, 'w') as f:
                    f.write(report_content)
                messagebox.showinfo("Save Successful", f"Nutrition plan saved successfully to:\n{file_path}")
                app_logger.info(f"Nutrition plan successfully saved to: {file_path}")
            except IOError as e:
                messagebox.showerror("Save Error", f"Error saving file: {e}")
                app_logger.error(f"Error saving nutrition plan to {file_path}: {e}")
            except Exception as e: # Catch any other unexpected errors during save
                messagebox.showerror("Save Error", f"An unexpected error occurred during save: {e}")
                app_logger.critical(f"An unexpected error occurred while saving the nutrition plan: {e}", exc_info=True)
        else: # User cancelled the save dialog
            app_logger.info("Save operation cancelled by user.")
            print("Save operation cancelled.") # This print will go to the VS Code terminal


    def clear_results(self):
        """Clears the results display area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        app_logger.info("Results display cleared.")


if __name__ == "__main__":
    app_logger.info("Starting GUI application.")
    root = tk.Tk()
    app = NutritionApp(root)
    root.mainloop() # This starts the Tkinter event loop
    app_logger.info("GUI application closed.")