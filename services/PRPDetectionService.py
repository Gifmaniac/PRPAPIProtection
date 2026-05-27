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

max_report_payload = 10
def detect_report_payload(report_request):
    if len(report_request) > max_report_payload:
        logger.warning(f"Possible attack detected: Report request payload size {len(report_request)} exceeds the maximum allowed {max_report_payload}")


def detect_excessive_access(user_id, user_permissions, required_permission, endpoint):
    if required_permission not in user_permissions:
        logger.warning(f"Possible attack detected: User {user_id} tried to access {endpoint} with permissions {user_permissions} trying to access resource requiring {required_permission}")
    
def detect_excessive_access(user_id, user_permissions, required_permission, endpoint):
        logger.warning(f"Possible attack detected: User {user_id} tried to access {endpoint} with permissions {user_permissions} trying to access resource requiring {required_permission}")

def detect_ban_user(user_id, endpoint, banned_user_id):
    logger.critical(f"Account banned: User {user_id} accessed {endpoint} to bring the ban hammer to {banned_user_id}")