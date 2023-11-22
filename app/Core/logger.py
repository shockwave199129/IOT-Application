import os
import logging

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create a directory for log files if it doesn't exist
if not os.path.exists('log'):
    os.makedirs('log')

# Define the log file path
log_file_path = 'log/iot-app.log'

# Create a file handler and set its formatter
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
