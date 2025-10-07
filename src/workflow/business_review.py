# src/workflow/business_review.py

import sys
import os

# Add 'src' to path to fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.normalizer import normalize_text_value

# Simulated business rules
def business_rule_check(data):
    """
    Apply simple business rules on normalized data.
    Example rule: amount should be positive.
    """
    results = []
    for item in data:
        if item['type'] == 'currency':
            amount = item['value']['amount']
            if amount <= 0:
                results.append({'item': item, 'status': 'Failed'})
            else:
                results.append({'item': item, 'status': 'Passed'})
        else:
            results.append({'item': item, 'status': 'Checked'})
    return results

# Simulated human review workflow
def human_review(results):
    """
    Simulate human review: flag any 'Failed' items.
    """
    for r in results:
        if r['status'] == 'Failed':
            r['human_review'] = 'Review Required'
        else:
            r['human_review'] = 'No Action Needed'
    return results

if __name__ == "__main__":
    # Sample input (normally from OCR + normalizer)
    sample_texts = ["Invoice date: October 2, 2025", "Amount: $1200"]

    # Step 1: Normalize text
    normalized = [normalize_text_value(text) for text in sample_texts]

    # Step 2: Apply business rules
    checked = business_rule_check(normalized)

    # Step 3: Human review
    reviewed = human_review(checked)

    print("✅ Final Business & Human Review Workflow Result:")
    for r in reviewed:
        print(r)
