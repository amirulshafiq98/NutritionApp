![Dietitian](https://github.com/user-attachments/assets/8d54447d-f93f-4bcb-938d-d1508d573f8b)

# Project Background

This project was inspired by my desire to create an app that was all encompassing featuring tools like scanning texts on the back of a food label and giving you information on each of the ingredients used. The information would include things like which ingredients are banned in certain countries or which additive has the potential to cause cancer and the like. While coding such an app would be a huge undertaking (requiring me to own a Mac for one), I figured I would start small to test my idea. This led me to create a nutirtion calculator which considers the users information to recommend the amount of macro and micronutrients that a person would need. The goal was to build something that could serve as a useful starting point for individuals to understand their basic nutritional requirements, especially when considering different activity levels, weight goals, or common medical conditions like diabetes or hypertension.

The main output of this application is a clear, easy-to-read nutrition plan, designed to give users a practical estimate of their daily caloric intake and how those calories should be distributed across protein, carbohydrates, and fats. It also provides general advice for specific health conditions, making the information more relevant and actionable. This helps bridge the gap between general advice and a slightly more personalised approach, serving as an initial guide before consulting a professional. While the eventual goal would be to make this calculator factor in many other things that a hospital dietitian would (e.g. time to eat) this could prove to be a good foundation for the potential of this app. Hopefully, I manage to finish this project and incorporate this calculator to my crazy idea of a nutrtion app providing users with the neccessary information on the food they eat.

# Overview
The Nutrition Calculator is a desktop application built with Python using Graphical User Interface (GUI). Its main purpose is to provide individuals with an estimate of their daily nutritional needs, including calories and macronutrients (protein, carbs, fats), based on their personal details, activity level, and specific health goals or conditions. Think of it as a helpful digital assistant that provides a quick, estimated nutritional snapshot (Note: this does not replace medical advice from professionals).

The app takes your age, sex, weight, height, and lifestyle choices, then calculates key health metrics like BMI and Basal Metabolic Rate (BMR). It then provides tailored calorie targets and a breakdown of how much protein, carbohydrates, and fats you might need, alongside general guidelines for important micronutrients. This makes it easier for someone to understand their basic dietary requirements at a glance.

# How to Use

<img width="1000" height="828" alt="GUI" src="https://github.com/user-attachments/assets/49fbca69-764a-4dd0-97be-a2ad92ce7701" />

Using the Nutrition Therapy Calculator is straightforward:

1. **Launch the App:** Run the main.py file to open the application window as seen in the image above.

2. **Input Your Information:** Fill in the fields for your age, weight, and height. Select your sex, activity level, and any relevant medical conditions. If you choose "Diabetes" as a medical condition, an additional dropdown for "Diabetes Subtype" will appear to help refine the recommendations. Finally, select your weight goal (Maintain, Lose, or Gain).

3. **Calculate Your Plan:** Click the "Calculate Nutrition Plan" button. The application will process your inputs and display a detailed nutritional report in the lower panel.
(You'll insert a screenshot of the GUI with the results displayed here)

4. **Save Your Plan (Optional):** If you want to keep a record of your personalised plan, click the "Save Plan" button. This will prompt you to choose a location on your computer to save the report as a text file (.txt).

5. **Clear Results (Optional):** Click "Clear Results" to erase the current plan from the display and prepare for a new calculation.

Project Structure
The project is organised into several distinct folders and files. This helps keep everything tidy and makes it easier to understand where different parts of the app's logic live.


Nutrition Calculator/
<br> ├── gui/                     &emsp; &emsp; &emsp; &emsp; # Handles all the visual parts of the app (windows, buttons, text areas)
<br> │   ├── app.py               &emsp; &emsp; &emsp; &emsp; # The main brain for the app's window and how different parts talk to each other
<br> │   ├── input_panel.py       &emsp; &emsp; &emsp; &emsp; # Manages where you type in your information and select options
<br> │   └── results_panel.py     &emsp; &emsp; &emsp; &emsp; # Shows you the calculated nutrition plan
<br> ├── app.log                  &emsp; &emsp; &emsp; &emsp; # A diary for the app, recording what it's doing (like when you click buttons or if something goes wrong)
<br> ├── calculations.py          &emsp; &emsp; &emsp; &emsp; # Where all the math happens (like calculating BMI or calorie needs)
<br> ├── clear_log.py             &emsp; &emsp; &emsp; &emsp; # A small helper tool to clean out the app's diary (app.log)
<br> ├── config_manager.py        &emsp; &emsp; &emsp; &emsp; # Manages how the app uses its settings, like default calorie adjustments
<br> ├── logger_config.py         &emsp; &emsp; &emsp; &emsp; # Sets up how the app writes its diary entries (logs)
<br> ├── main.py                  &emsp; &emsp; &emsp; &emsp; # The file you run to start the whole app
<br> ├── README.md                &emsp; &emsp; &emsp; &emsp; # This file, explaining the project
<br> └── settings.json            &emsp; &emsp; &emsp; &emsp; # A special file where you can adjust some numbers the app uses (like macro percentages)


## Technical Details
I built this application using Python because it's excellent for handling calculations and building graphical interfaces relatively quickly.

**Tkinter for the Look and Feel:** I used Tkinter. This allowed me to design a user-friendly window with input fields, buttons, and a results display. Choosing Tkinter meant I could focus on the core functionality without needing to learn complex external GUI frameworks such as PyQt and Kivy.

**Organised Code (Modular Design):** I divided the code into different files and folders (like the gui/ folder and calculations.py). The idea behind this was to keep specific tasks separate. For instance, all the math formulas are in calculations.py, while the parts that create the interface are in the gui/ folder. This makes the code easier to read, manage, and update, because if I want to change how BMI is calculated, I know exactly which file to look in.

**External Settings (settings.json):** Instead of hardcoding all the numbers (like how many calories to subtract for weight loss), I put them in a settings.json file. This is a common way to make an application more flexible. It means you (or I) can easily tweak these values without having to change the main program code.

**Input Handling and Error Checking:** I made sure the app checks the information you type in (like age or weight) to make sure they are reasonable numbers. If you accidentally type text where a number should be, the app will let you know. This helps prevent the app from crashing and ensures the calculations are based on valid data.

**Logging System:** The app keeps a log (app.log) of what it is doing. This is to keep track if something went wrong or just working as intended in the application.

## Configuration

This application's behaviour can be customised through the settings.json file, which is located in the main project directory. This file lets you adjust key parameters without needing to touch the Python code.

<img width="789" height="917" alt="JSON" src="https://github.com/user-attachments/assets/ed85fadd-48b7-44e6-9cae-20ccd81486e4" />

You can modify these values to:

- Change the calorie deficit/surplus for weight loss/gain.

- Adjust the minimum recommended calorie intake for males and females.

- Tweak the default macronutrient percentages for different conditions.

- Control the level of detail in the application's log file and console output.

# Future Enhancements
I have several ideas to expand the functionality and utility of this application:

- **User Profiles:** Implement a way to save and load different user profiles, so returning users don't have to re-enter their data every time.

- **Database Integration:** Store patient data and calculated plans in a small local database (like SQLite) for better management and retrieval.

- **More Advanced Calculations:** Incorporate additional, more complex nutritional models or specific algorithms for a wider range of conditions.

- **Graphical Representation:** Add simple charts or graphs to visually represent progress or recommendation breakdowns (e.g., a pie chart for macros).

- **Unit Conversion:** Include an option for users to input their weight and height in imperial units (pounds, inches) for convenience.

- **Expand Configurability:** Move micronutrient guidelines from code to the settings.json file to allow for easier customisation without code changes.

## Disclaimer

This Nutrition Calculator provides estimates and examples based on general nutritional guidelines. This application is for informational and educational purposes only and should NOT be considered medical advice. Always consult a qualified healthcare professional, such as a Registered Dietitian or a medical doctor, for personalised nutrition therapy, diagnosis, and treatment, especially if you have specific medical conditions or dietary needs. The creators of this application are not responsible for any health outcomes or decisions made based on the information provided by this tool.

## License

This project is licensed under the [MIT License](https://github.com/amirulshafiq98/NutritionApp/blob/main/LICENSE).
