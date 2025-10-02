import re
from collections import Counter

DOC_KEYWORDS = {
    "invoice": ["invoice", "bill to", "invoice no", "amount due", "tax"],
    "receipt": ["receipt", "total paid", "amount paid", "change"],
    "contract": ["agreement", "party", "whereas", "term", "witness"],
    "resume": ["curriculum vitae", "resume", "experience", "education", "skills"],
    "purchase_order": ["purchase order", "po number", "supplier", "ship to"],
    "bank_statement": ["account number", "balance", "statement period", "posted"]
}

def detect_doc_type(ocr_text: str):
    text = ocr_text.lower()
    scores = {dtype: sum(text.count(k) for k in keys) for dtype, keys in DOC_KEYWORDS.items()}
    best = max(scores.items(), key=lambda x: x[1])
    doc_type, val = best
    total = sum(scores.values()) or 1
    confidence = val / total
    return {
        "doc_type": doc_type,
        "confidence": round(confidence, 3),
        "scores": scores
    }
if __name__ == "__main__":
    sample_text = """
    Invoice No: 12345
    Bill To: Rahul
    Amount Due: $500
    Tax: $50
    """
    result = detect_doc_type(sample_text)
    print("Detected Document Type:", result)
