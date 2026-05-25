import logging

logger = logging.getLogger(__name__)

def detect_insufficient_balance(account_balance, trade_amount):
    logger.warning(f"Insufficient balance detected: Account balance {account_balance} is less than trade amount {trade_amount}")

def detect_currency_mismatch(account_currency, required_currency):
    logger.warning(f"Currency mismatch detected: Account currency {account_currency} does not match required currency {required_currency}")

def detect_bola_attempt(current_user_id, source_account_id, account_owner_id):
    logger.warning(f"Possible BOLA attack detected: User {current_user_id} trying to access account {source_account_id} owned by user {account_owner_id}")

def detect_mass_assignment_attempt(user_id, updated_fields, requested_fields):
    logger.warning(f"Possible Mass Assignment attack detected: User {user_id} trying to update fields {updated_fields} which are not in the allowed fields {requested_fields}")

def detect_repeated_mass_assignment_attempt(user_id, updated_fields, requested_fields, attempts):
    logger.critical(f"Critical: Repeated Mass Assignment attempts detected for UserID={user_id}. trying to update fields {updated_fields} which are not in the allowed fields {requested_fields}. Attempts={attempts}")

def detect_brute_force_attempt_login(email, endpoint, ip_address, user_agent, attempt_count):
    logger.warning(f"Possible Brute Force attack detected: Email {email} trying to access endpoint {endpoint} from IP {ip_address} with User-Agent {user_agent}. Attempts: {attempt_count}")

def detect_repeated_brute_force_attempt_login(email, endpoint, ip_address, user_agent, attempt_count):
    logger.critical(f"Critical: Repeated Brute Force attack detected: Email {email} trying to access endpoint {endpoint} from IP {ip_address} with User-Agent {user_agent}. Attempts: {attempt_count}") 

def detect_brute_force_attempt_login_locked(email):
    logger.critical(f"Critical: Brute Force attack detected: Email {email} has been temporarily locked due to multiple failed login attempts")