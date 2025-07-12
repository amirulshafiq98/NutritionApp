# main_ver1.py

from calculations import calculate_bmr, calculate_tdee, get_macro_recommendations, calculate_bmi, classify_bmi, get_micronutrient_guidelines

def get_numeric_input(prompt, value_type=float, min_val=None, max_val=None, error_msg="Invalid input. Please enter a positive number."):
    while True:
        try:
            value = value_type(input(prompt))
            if value <= 0:
                raise ValueError("Value must be greater than zero.")
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be at least {min_val}.")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be at most {max_val}.")
            if value == 999:
                exit ("Exiting the program.")
            return value
        except ValueError as e:
            print(e if str(e) else error_msg)

def get_sex_input():
    while True:
        sex = input("Enter your sex (M/F): ").upper()
        if sex in ['M', 'F']:
            return sex
        else:
            print("Invalid input. Please enter 'M' or 'F'.")

def get_activity_level():
    activity_levels = { # Changed to plural for better naming consistency
        1: 1.2,   # Sedentary
        2: 1.375, # Lightly active
        3: 1.55,  # Moderately active
        4: 1.725, # Very active
        5: 1.9    # Super active
    }

    print("\nNow, let's consider your activity level:")
    print("1. Sedentary (little or no exercise)")
    print("2. Lightly active (light exercise/sports 1-3 days/week)")
    print("3. Moderately active (moderate exercise/sports 3-5 days/week)")
    print("4. Very active (hard exercise/sports 6-7 days a week)")
    print("5. Super active (very hard exercise/sports & a physical job)")

    while True:
        try:
            level = int(input("Enter your activity level (1-5): "))
            if level in activity_levels:
                return activity_levels[level]
            else:
                print("Invalid input. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_medical_condition():
    conditions = {
        1: "general",
        2: "diabetes",
        3: "renal_disease",
        4: "hypertension", # Corrected typo from "hypertenstion"
        5: "heart_disease"
    }
    print("\nSelect your medical condition by number:")
    print("1. General/Healthy")
    print("2. Diabetes")
    print("3. Renal Disease (Non-dialysis, consult healthcare provider!)")
    print("4. Hypertension")
    print("5. Heart Disease")

    while True:
        try:
            choice = int(input("Enter your condition (1-5): ")) # Updated prompt based on added conditions
            if choice in conditions:
                return conditions[choice]
            else:
                print("Invalid choice. Please enter a number between 1-5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.") # Updated error message

def get_weight_goal():
    print("\nWhat is your weight goal?")
    print("1. Maintain current weight")
    print("2. Lose weight (e.g., aiming for 0.5-1 kg/week)")
    print("3. Gain weight (e.g., aiming for 0.5-1 kg/week)")
    while True:
        try:
            goal_choice = int(input("Enter your choice (1-3): "))
            if goal_choice == 1:
                return "maintain"
            elif goal_choice == 2:
                return "lose"
            elif goal_choice == 3:
                return "gain"
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    print("--- Nutrition Therapy Calculator ---")

    # Get all patient data with validation
    age = get_numeric_input("Enter your age in years: ", int, min_val=1, max_val=120)
    sex = get_sex_input()
    weight_kg = get_numeric_input("Enter your weight in kilograms (e.g., 70.5): ", min_val=20, max_val=300)
    height_cm = get_numeric_input("Enter your height in centimeters (e.g., 175.0): ", min_val=50, max_val=250)
    
    activity_factor = get_activity_level() 
    
    medical_condition = get_medical_condition()
    
    micronutrient_guidelines = get_micronutrient_guidelines(medical_condition)

    bmi = calculate_bmi(weight_kg, height_cm)
    bmi_category = classify_bmi(bmi)
    print(f"\nYour Body Mass Index (BMI): {bmi:.2f} ({bmi_category})")

    # Perform calculations
    try:
        bmr = calculate_bmr(age, sex, weight_kg, height_cm)
        tdee = calculate_tdee(bmr, activity_factor)
        
        weight_goal = get_weight_goal()
        
        recommended_calories = tdee 

        if weight_goal == "lose":
            # Typical deficit for 0.5-1 kg (1-2 lbs) per week
            recommended_calories = tdee - 500 
            # Add a safety net for dangerously low calories
            if recommended_calories < 1200 and sex == 'F':
                print("\nWarning: Calculated calories for weight loss are very low. Please consult a healthcare professional for safe guidance.")
                recommended_calories = 1200 # Set a floor
            elif recommended_calories < 1500 and sex == 'M':
                print("\nWarning: Calculated calories for weight loss are very low. Please consult a healthcare professional for safe guidance.")
                recommended_calories = 1500 # Set a floor
        elif weight_goal == "gain":
            # Typical surplus for 0.5-1 kg (1-2 lbs) per week
            recommended_calories = tdee + 500

        protein_g, carb_g, fat_g = get_macro_recommendations(tdee, medical_condition, weight_kg)

        # Display results
        print("\n--- Your Personalized Nutrition Plan ---")
        print(f"Basal Metabolic Rate (BMR): {bmr:.0f} kcal/day")
        print(f"Total Daily Energy Expenditure (TDEE): {tdee:.0f} kcal/day")
        
        # CONDITIONAL DISPLAY: Only show "Recommended Daily Calories" if a goal was set
        if weight_goal == "lose" or weight_goal == "gain":
            print(f"Recommended Daily Calories for {weight_goal.capitalize()}ing weight: {recommended_calories:.0f} kcal")

        print("\nMacronutrient Distribution:")
        print(f"Protein: {protein_g:.1f} grams")
        print(f"Carbohydrates: {carb_g:.1f} grams")
        print(f"Fats: {fat_g:.1f} grams")
        
        print("\nMicronutrient Guidelines:")
        if micronutrient_guidelines: # Check if there are guidelines to print
            for nutrient, guideline in micronutrient_guidelines.items():
                print(f"- {nutrient.replace('_', ' ').title()}: {guideline}")
        else:
            print("No specific micronutrient guidelines for your condition at this time.")

        # Additional warnings based on BMI
        if bmi_category == "Underweight":
            print("\nWarning: Your BMI suggests you might be underweight. Please consult a healthcare professional.")
        elif bmi_category.startswith("Obesity"): # Catches all Obesity classes
            print("\nWarning: Your BMI suggests you are in an obesity category. Please consult a healthcare professional for personalized guidance.")
        
        # Display medical condition-specific warnings/guidelines
        if medical_condition == "renal_disease":
            print("\n!!! IMPORTANT WARNING for Renal Disease Patients !!!")
            print("This tool provides *generalized* estimates. Renal disease nutrition is highly complex.")
            print("Fluid, potassium, and phosphorus restrictions are critical and individualized.")
            print("ALWAYS consult a nephrologist and a Registered Dietitian specializing in renal nutrition.")
            print("These calculations DO NOT replace professional medical advice.")
            print("Fluid restrictions: Individualized. Consult RD.") 

        if medical_condition == "diabetes":
            print("\nFiber Recommendation for Diabetes: Aim for 25-30 grams of fiber per day.")
            print("Meal Timing Suggestions for Diabetes:")
            print("- Aim for consistent meal and snack times daily.")
            print("- Distribute carbohydrate intake evenly throughout the day.")
            print("- Avoid skipping meals, especially if on medication that lowers blood sugar.")
        
        if medical_condition == "hypertension":
            print("\nWarning: For Hypertension, focus on a low-sodium diet (e.g., DASH diet). Consult a healthcare professional.")
        
        if medical_condition == "heart_disease":
            print("\nWarning: For Heart Disease, limit saturated fats to less than 7% of total calories. Consult a healthcare professional.")


        print("\n--- IMPORTANT DISCLAIMER ---")
        print("These are *estimates* and *examples* based on general guidelines.")
        print("Always consult a qualified healthcare professional (like a Registered Dietitian) for personalized nutrition therapy, especially for specific medical conditions.")

    # Error handling
    except ValueError as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your inputs and try again.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")