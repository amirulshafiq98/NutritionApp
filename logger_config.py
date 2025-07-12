# logger_config.py

import logging 
import os 
from config_manager import SETTINGS # Imports logging-specific configuration from settings.json

# Global logger instance used throughout the application
app_logger = None

def setup_logging():
    # Configures the main application logger
    global app_logger

    log_settings = SETTINGS.get("logging", {}) # Get logging-specific settings
    log_file_name = log_settings.get("file_name", "app.log")
    file_level_str = log_settings.get("file_level", "INFO").upper()
    console_level_str = log_settings.get("console_level", "WARNING").upper()

    # Map string names from settings to logging's internal level constants
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    file_level = LEVELS.get(file_level_str, logging.INFO)
    console_level = LEVELS.get(console_level_str, logging.WARNING)

    # Get the main logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Prevent adding duplicate handlers if the function is called multiple times
    if not logger.handlers:
        # File Handler: Directs logs to a specified file
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(file_level) 
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console Handler: Directs logs to the standard output (terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Assign the configured logger to the global `app_logger` for easy access throughout the application
    app_logger = logger

# Call `setup_logging` automatically when this module is imported
setup_logging()