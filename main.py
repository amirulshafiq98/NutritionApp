# main.py

import tkinter as tk
from gui.app import NutritionApp 
from logger_config import setup_logging, app_logger # Manages application logging for operational insights

if __name__ == "__main__":
    # Ensure logging is set up before any other application processes begins
    setup_logging()
    app_logger.info("Application starting up.")

    # Initialise the main Tkinter window for the UI
    root = tk.Tk()

    # Create an instance of the main application
    app = NutritionApp(root)

    # Start the Tkinter event loop
    root.mainloop()

    # Log that the application is closing after the main window is shut down
    app_logger.info("Application closed.")