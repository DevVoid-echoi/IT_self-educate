import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
DEFAULT_ALERT_LOG_PATH = os.path.join(LOG_DIR, "alerts.log")

def setup_alert_logger(log_file=DEFAULT_ALERT_LOG_PATH):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger("AlertLogger")
    logger.setLevel(logging.WARNING)

    if not logger.handlers:
        file_handler=logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

alert_logger = setup_alert_logger()

def log_alert(ip:str, failed_attempts: str, window_seconds: int):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_msg = (f"[ALERT] Possible brute-force attack | "
                f"IP={ip} | FailedAttempts={failed_attempts} | Window={window_seconds}s")

    print(f"\033[91m{now_str} {alert_msg}\033[0m")

    sec_logger = logging.getLogger("SecurityLogger")
    sec_logger.warning(alert_msg)

    for handlers in sec_logger.handlers:
        handlers.flush()
    
    alert_logger.warning(alert_msg)