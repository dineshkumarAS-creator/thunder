import random
import string
from datetime import datetime
from typing import Dict, Any
import hashlib

def generate_shipment_number() -> str:
    """
    Generate unique shipment number format: TF-YYYYMMDD-XXXXX
    """
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"TF-{date_str}-{random_str}"

def generate_quote_number() -> str:
    """
    Generate unique quote number format: Q-YYYYMM-XXXXX
    """
    date_str = datetime.now().strftime("%Y%m")
    random_str = ''.join(random.choices(string.digits, k=5))
    return f"Q-{date_str}-{random_str}"

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency with proper symbols"""
    symbols = {
        "USD": "$",
        "INR": "₹",
        "CNY": "¥",
        "EUR": "€"
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def calculate_cbm(length: float, width: float, height: float, unit: str = "cm") -> float:
    """Calculate CBM from dimensions"""
    if unit == "cm":
        return (length * width * height) / 1000000
    elif unit == "m":
        return length * width * height
    elif unit == "inch":
        return (length * width * height) / 61023.7
    else:
        return 0

def validate_gstin(gstin: str) -> bool:
    """Validate Indian GSTIN"""
    pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
    import re
    return bool(re.match(pattern, gstin))

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove special characters
    import re
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:250] + '.' + ext
    return filename

def generate_file_hash(file_path: str) -> str:
    """Generate MD5 hash for file verification"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def dict_to_query_params(params: Dict[str, Any]) -> str:
    """Convert dict to query parameter string"""
    return "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
