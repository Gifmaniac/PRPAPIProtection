import logging

logger = logging.getLogger(__name__)

def detect_unkown_account(current_user_id, account_user_id):
    logger.warning(f"Unauthorized access attempt detected: User {current_user_id} trying to access account of user {account_user_id}")

def detect_insufficient_balance(account_balance, trade_amount):
    logger.warning(f"Insufficient balance detected: Account balance {account_balance} is less than trade amount {trade_amount}")

def detect_currency_mismatch(account_currency, required_currency):
    logger.warning(f"Currency mismatch detected: Account currency {account_currency} does not match required currency {required_currency}")

def detect_bola_attempt(current_user_id, source_account_id, account_owner_id):
    logger.warning(f"Possible BOLA attack detected: User {current_user_id} trying to access account {source_account_id} owned by user {account_owner_id}")