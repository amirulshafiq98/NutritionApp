# calculations.py
from config_manager import SETTINGS # Accesses configuration values like macro percentages.

def calculate_bmi(weight_kg, height_cm):
    # Calculates Body Mass Index (BMI).
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi):
    # Categorises the calculated BMI into standard health classifications
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    elif 30 <= bmi < 34.9:
        return "Obesity Class I"
    elif 35 <= bmi < 39.9:
        return "Obesity Class II"
    else:
        return "Obesity Class III (Morbid Obesity)"

def calculate_bmr(age, sex, weight_kg, height_cm):
    # Calculates Basal Metabolic Rate (BMR) using the Mifflin-St Jeor equation.
    if sex == 'M':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    return bmr

def calculate_tdee(bmr, activity_factor):
    # Calculates Total Daily Energy Expenditure (TDEE)
    return bmr * activity_factor

def get_macro_recommendations(calories, macro_percentages, weight_kg=None):
    # Calculates the recommended daily intake for protein, carbohydrates, and fats in grams
    CALORIES_PER_GRAM = {
        "protein": 4,
        "carb": 4,
        "fat": 9
    }

    protein_g = (calories * macro_percentages["protein"]) / CALORIES_PER_GRAM["protein"]
    carb_g = (calories * macro_percentages["carb"]) / CALORIES_PER_GRAM["carb"]
    fat_g = (calories * macro_percentages["fat"]) / CALORIES_PER_GRAM["fat"]

    # Protein calculation could be further refined based on g/kg body weight for specific cases
    return {
        "protein_g": protein_g,
        "carb_g": carb_g,
        "fat_g": fat_g,
        "protein_pct": macro_percentages["protein"],
        "carb_pct": macro_percentages["carb"],
        "fat_pct": macro_percentages["fat"]
    }

def get_micronutrient_guidelines(medical_condition):
    # Access the micronutrient_guidelines from the loaded SETTINGS
    all_guidelines = SETTINGS.get("micronutrient_guidelines", {})
    
    # Return specific guidelines if available, otherwise fall back to general
    return all_guidelines.get(medical_condition, all_guidelines.get("general", {}))