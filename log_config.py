import logging

# Set up logging to a file
file_handler = logging.FileHandler('log_file.log')
file_handler.setLevel(logging.DEBUG)

# Set up logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Set up the root logger
def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':

    logger = init_logger()

    # Example usage
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
