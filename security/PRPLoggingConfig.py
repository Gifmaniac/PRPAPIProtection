import logging
import os

# Configure logging
log_file = os.path.join(os.path.dirname(__file__), '..', 'Logs', 'security_warnings.log')
logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='a'
)


