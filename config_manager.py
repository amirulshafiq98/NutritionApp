# config_manager.py

import json 
import os 

# Specifies the location of the configuration file
CONFIG_FILE_PATH = 'settings.json'

def get_default_settings():
    # Defines the baseline, default settings for the application
    return {
    "calorie_adjustments": {
        "weight_loss_deficit_kcal": 500,
        "weight_gain_surplus_kcal": 500
    },

    "min_calories": {
        "female": 1200,
        "male": 1500
    },

    "macro_percentages": {
        "general": {"protein": 0.20, "carb": 0.55, "fat": 0.25},
        "diabetes": {"protein": 0.20, "carb": 0.50, "fat": 0.30},
        "renal_disease": {"protein": 0.10, "carb": 0.60, "fat": 0.30},
        "hypertension": {"protein": 0.20, "carb": 0.55, "fat": 0.25},
        "heart_disease": {"protein": 0.20, "carb": 0.55, "fat": 0.25}
    },
    
    "micronutrient_guidelines": {
        "general": {
            "Sodium": "2300 mg/day",
            "Potassium": "3500-4700 mg/day",
            "Fiber": "25-38 grams/day",
            "Added Sugars": "<10% of total calories",
            "Saturated Fat": "<10% of total calories"
        },
        "diabetes": {
            "Sodium": "2300 mg/day",
            "Potassium": "3500-4700 mg/day",
            "Fiber": "25-30 grams/day (important for blood sugar control)",
            "Added Sugars": "Minimize strictly",
            "Saturated Fat": "<7% of total calories"
        },
        "renal_disease": {
            "Sodium": "<2000 mg/day (often stricter, consult RD)",
            "Potassium": "Highly individualized (often restricted, consult RD)",
            "Phosphorus": "Highly individualized (often restricted, consult RD)",
            "Fluid Intake": "Highly individualized (often restricted, consult RD)"
        },
        "hypertension": {
            "Sodium": "<2300 mg/day (aim for <1500 mg/day for significant reduction - DASH diet)",
            "Potassium": "4700 mg/day (from food sources, unless contraindicated by renal issues)",
            "Saturated Fat": "<10% of total calories"
        },
        "heart_disease": {
            "Sodium": "<2300 mg/day (aim for <1500 mg/day)",
            "Saturated Fat": "<7% of total calories"
        }
    },
    
    "logging": {
        "file_name": "app.log",
        "file_level": "INFO",
        "console_level": "WARNING"
    }
}

def load_settings():
    # Attempts to load application settings from 'settings.json'
    default_settings = get_default_settings()
    final_settings = default_settings.copy()

    try:
        if not os.path.exists(CONFIG_FILE_PATH):
            print(f"Settings file '{CONFIG_FILE_PATH}' not found. Creating with default settings.")
            save_settings(default_settings)
            return default_settings

        with open(CONFIG_FILE_PATH, 'r') as f:
            loaded_settings = json.load(f)

            # Merges loaded settings into default settings
            def update_dict(d, u):
                for k, v in u.items():
                    if isinstance(v, dict) and isinstance(d.get(k), dict):
                        d[k] = update_dict(d[k], v)
                    else:
                        d[k] = v
                return d
            
            final_settings = update_dict(final_settings, loaded_settings)
            
            return final_settings

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {CONFIG_FILE_PATH}. Using default settings.")
        return default_settings
    except Exception as e:
        print(f"An unexpected error occurred while loading settings from {CONFIG_FILE_PATH}: {e}. Using default settings.")
        return default_settings

def save_settings(settings_to_save):
    # Writes the current application settings dictionary to the 'settings.json' file
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(settings_to_save, f, indent=4) # 'indent=4' makes the JSON human-readable
    except Exception as e:
        print(f"Error: Could not save settings to {CONFIG_FILE_PATH}: {e}")

# Load settings when this module is imported
SETTINGS = load_settings()