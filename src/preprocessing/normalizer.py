import re
import dateparser
from babel.numbers import parse_decimal
from babel import Locale
import warnings

# Suppress DeprecationWarnings from dateparser
warnings.filterwarnings("ignore", category=DeprecationWarning)

# -----------------------------
# Date Normalization
# -----------------------------
def normalize_date(text):
    """Normalize any date string to YYYY-MM-DD format."""
    date_obj = dateparser.parse(text)
    if date_obj:
        return date_obj.strftime("%Y-%m-%d")
    return None

# -----------------------------
# Number Normalization
# -----------------------------
def normalize_number(text):
    """Convert numbers like 1,000 or 1.2M to standard float."""
    text = text.replace(",", "").strip().upper()

    # Handle shorthand like 1K, 2M, etc.
    multiplier = 1
    if text.endswith("K"):
        multiplier = 1_000
        text = text[:-1]
    elif text.endswith("M"):
        multiplier = 1_000_000
        text = text[:-1]
    elif text.endswith("B"):
        multiplier = 1_000_000_000
        text = text[:-1]

    try:
        value = float(parse_decimal(text, locale=Locale.parse('en')))
        return value * multiplier
    except Exception:
        try:
            return float(text) * multiplier
        except ValueError:
            return None

# -----------------------------
# Currency Normalization
# -----------------------------
def normalize_currency(text):
    """
    Normalize currency values like $100, ₹5,000, €200 -> {'currency': 'USD', 'amount': 100.0}
    """
    currency_symbols = {
        "$": "USD",
        "₹": "INR",
        "€": "EUR",
        "£": "GBP",
        "¥": "JPY",
        "₩": "KRW",
        "₽": "RUB",
        "₺": "TRY",
    }

    text = text.strip().replace(",", "")

    # Match symbols like ₹, $, €, etc.
    symbol_match = re.match(r"([₹$€£¥₩₽₺])\s?(\d+(\.\d+)?)", text)
    if symbol_match:
        symbol = symbol_match.group(1)
        amount = symbol_match.group(2)
        currency_code = currency_symbols.get(symbol, "UNK")
        return {"currency": currency_code, "amount": float(amount)}

    # Match codes like USD 100, INR500
    code_match = re.match(r"([A-Za-z]{3})\s?(\d+(\.\d+)?)", text)
    if code_match:
        currency_code = code_match.group(1).upper()
        amount = code_match.group(2)
        return {"currency": currency_code, "amount": float(amount)}

    return None

# -----------------------------
# Unified Function
# -----------------------------
def normalize_text_value(text):
    """
    Try to identify and normalize text as date, currency, or number.
    Returns a dict with type and normalized value.
    """
    # Try currency first
    currency_val = normalize_currency(text)
    if currency_val:
        return {"type": "currency", "value": currency_val}

    # Try number next
    num_val = normalize_number(text)
    if num_val is not None:
        return {"type": "number", "value": num_val}

    # Finally, try date
    date_val = normalize_date(text)
    if date_val:
        return {"type": "date", "value": date_val}

    return {"type": "text", "value": text}

# -----------------------------
# Wrapper for multi-line text
# -----------------------------
def normalize_text(text):
    """
    Detect and normalize dates, currencies, and numbers in multi-line text.
    Returns a list of normalized results.
    """
    results = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        results.append(normalize_text_value(line))
    return results

# -----------------------------
# Test block
# -----------------------------
if __name__ == "__main__":
    samples = [
        "October 2, 2025",
        "₹5,000",
        "$100.50",
        "1,234.56",
        "2.5M",
        "2025/10/04",
        "USD 1200"
    ]
    for s in samples:
        print(f"{s} -> {normalize_text_value(s)}")
