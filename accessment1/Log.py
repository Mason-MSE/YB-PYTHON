from functools import wraps
import time
import re
from Config import *
import logging
from pathlib import Path
import sys
# Create logs folder if not exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# log file name — you can also use date in filename
LOG_FILE = LOG_DIR / "app.log"

# ------------------ Basic Configuration ------------------
def setup_logger():
    logger = logging.getLogger("CarRentalApp")
    logger.setLevel(logging.DEBUG)          # capture everything

    # 1. Console handler — colorful or clean
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)   # usually INFO on console

    # 2. File handler — always DEBUG level
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # You can use colorful console if you like (optional)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(message)s',
        datefmt='%H:%M:%S'
    )

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent duplicate logs when importing multiple times
    logger.propagate = False

    return logger


# Global logger — you only call setup once
logger = setup_logger()


# Optional: shortcut functions
def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def exception(msg=None, *args, **kwargs):
    logger.exception(msg or "Exception occurred", *args, **kwargs)

def log_execution(func):
    #Aspect: log method execution and parameters
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args={args} kwargs={kwargs}")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[LOG] {func.__name__} finished in {end - start:.4f}s, result={result}")
        return result
    return wrapper

# ANSI color codes
RED = "\033[31m"     # SQL keywords
GREEN = "\033[32m"   # Parameter values
YELLOW = "\033[33m"  # Execution time
RESET = "\033[0m"



# List of common SQL keywords (can extend)
SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
    "UPDATE", "SET", "DELETE", "JOIN", "LEFT", "RIGHT", "INNER",
    "OUTER", "ON", "GROUP", "BY", "ORDER", "LIMIT", "OFFSET",
    "AND", "OR", "NOT", "IS", "NULL", "IN", "AS", "DISTINCT",
    "CREATE", "TABLE", "ALTER", "DROP", "INDEX", "VIEW", "TRIGGER",
    "UNION", "ALL", "HAVING", "EXISTS", "BETWEEN", "LIKE","TIMESTAMP",
    "CASE", "WHEN", "THEN", "ELSE", "END", "PRIMARY", "KEY", "IF"
    "TIMESTAMP","IF","FOREIGN", "REFERENCES", "AUTO_INCREMENT","INTO","DEFAULT","CURRENT_TIMESTAMP"
    ,"YEAR","CURDATE","TIMESTAMPDIFF","STRFTIME","TEXT","INTEGER","DATETIME","BOOLEAN","DATE"
]

# Build a regex pattern to match keywords, case-insensitive
KEYWORD_PATTERN = re.compile(r'\b(' + '|'.join(SQL_KEYWORDS) + r')\b', re.IGNORECASE)

def debug_sql(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        
        # Execute the actual function
        result = func(self, *args, **kwargs)
        
        if DEBUG_SQL:
            sql = args[0] if len(args) > 0 else kwargs.get('sql', '')
            params = args[1] if len(args) > 1 else kwargs.get('params', ())
            
            # Replace placeholders with colored values
            formatted_sql = sql
            for p in params:
                value_str = f"{GREEN}'{p}'{RESET}" if isinstance(p, str) else f"{GREEN}{p}{RESET}"
                formatted_sql = formatted_sql.replace("?", value_str, 1)
            
            # Uppercase and colorize SQL keywords
            def repl(match):
                return f"{RED}{match.group(0).upper()}{RESET}"
            
            formatted_sql = KEYWORD_PATTERN.sub(repl, formatted_sql)
            
            elapsed = (time.time() - start_time) * 1000  # ms
            print(f"[SQL DEBUG] {formatted_sql} {YELLOW}[{elapsed:.2f} ms]{RESET}")
        
        return result
    return wrapper