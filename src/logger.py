import logging

def get_logger(name: str) -> logging.Logger:
    """
    About:
        Creates and configures a logger that outputs messages to both
        a log file ('data_update.log') and the console.

    Inputs:
        name (str) - The name of the logger, often the module's __name__.

    Outputs:
        logging.Logger - Configured logger instance ready for use.
    """
    # Configure the logging system with level, format, and handlers
    logging.basicConfig(
        level=logging.INFO,  # Set default logging level
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        handlers=[
            logging.FileHandler("data_update.log"),  # Write logs to file
            logging.StreamHandler()                  # Print logs to console
        ]
    )
    # Return a logger object with the specified name
    return logging.getLogger(name)