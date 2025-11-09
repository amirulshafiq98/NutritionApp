# user_input.py

import streamlit as st
from calculations import (
    calculate_bmi,
    classify_bmi,
    calculate_bmr,
    calculate_tdee,
    get_macro_recommendations,
    get_micronutrient_guidelines
)
from config_manager import SETTINGS

def show_calculator():
    st.header("Patient Information")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=0, max_value=100, value=0, step=1)
        sex = st.selectbox("Sex", ["Select...", "M", "F"])
        height_cm = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=0.0, step=0.1, format="%.1f")
    with col2:
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=0.0, step=0.1, format="%.1f")

    # Activity and medical condition
    activity_levels = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Extra active (physical job)": 1.9
    }
    activity_description = st.selectbox("Activity Level", list(activity_levels.keys()))
    activity_factor = activity_levels[activity_description]

    medical_conditions = {
        "General": "general",
        "Diabetes": "diabetes",
        "Renal Disease": "renal_disease",
        "Hypertension": "hypertension",
        "Heart Disease": "heart_disease"
    }
    medical_condition_description = st.selectbox("Medical Condition", list(medical_conditions.keys()))
    medical_condition = medical_conditions[medical_condition_description]

    diabetes_subtype = st.selectbox("Diabetes Subtype", ["Type 1", "Type 2", "Gestational"]) \
        if medical_condition == "diabetes" else None

    weight_goal_options = {
        "Maintain Weight": "maintenance",
        "Lose Weight": "loss",
        "Gain Weight": "gain"
    }
    
    weight_goal_description = st.selectbox("Weight Goal", list(weight_goal_options.keys()))
    weight_goal = weight_goal_options[weight_goal_description]

    if st.button("Calculate Nutrition Plan"):
        if age == 0 or weight_kg == 0 or height_cm == 0 or sex == "Select...":
            st.error("⚠️ Please enter valid values for age, sex, weight, and height before calculating.")
        else:
            bmi = calculate_bmi(weight_kg, height_cm)
            bmi_classification = classify_bmi(bmi)
            bmr = calculate_bmr(age, sex, weight_kg, height_cm)
            tdee = calculate_tdee(bmr, activity_factor)

            adjusted_tdee = tdee
            if weight_goal == "loss":
                adjusted_tdee -= SETTINGS["calorie_adjustments"]["weight_loss_deficit_kcal"]
                min_cal = SETTINGS["min_calories"]["female"] if sex == "F" else SETTINGS["min_calories"]["male"]
                adjusted_tdee = max(adjusted_tdee, min_cal)
            elif weight_goal == "gain":
                adjusted_tdee += SETTINGS["calorie_adjustments"]["weight_gain_surplus_kcal"]

            macro_percentages = SETTINGS["macro_percentages"].get(
                medical_condition, SETTINGS["macro_percentages"]["general"]
            )
            macros = get_macro_recommendations(adjusted_tdee, macro_percentages, weight_kg)
            micronutrients = get_micronutrient_guidelines(medical_condition)

            # Display
            st.success("Nutrition Plan Calculated Successfully!")
            st.subheader("Health Metrics")
            st.write(f"**BMI:** {bmi:.1f} ({bmi_classification})")
            st.write(f"**BMR:** {bmr:.0f} kcal/day")
            st.write(f"**TDEE:** {tdee:.0f} kcal/day")
            st.write(f"**Adjusted Calories:** {adjusted_tdee:.0f} kcal/day")

            st.subheader("Macronutrient Recommendations")
            st.write(f"**Protein:** {macros['protein_g']:.0f}g ({macro_percentages['protein']:.0%})")
            st.write(f"**Carbohydrates:** {macros['carb_g']:.0f}g ({macro_percentages['carb']:.0%})")
            st.write(f"**Fats:** {macros['fat_g']:.0f}g ({macro_percentages['fat']:.0%})")

            st.subheader("Micronutrient Guidelines")
            st.json(micronutrients)
