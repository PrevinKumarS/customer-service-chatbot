"""
guards.py — Input guardrails for PII, off-topic, and prompt injection detection.
"""

import re

def detect_pii(text: str) -> bool:
    """
    Detects potential PII like emails, phone numbers, or credit card patterns.
    """
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    # Basic 16-digit card pattern
    card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    
    if re.search(email_pattern, text) or re.search(phone_pattern, text) or re.search(card_pattern, text):
        return True
    return False

def detect_prompt_injection(text: str) -> bool:
    """
    Detects common prompt injection phrases.
    """
    injection_keywords = [
        "ignore previous instructions",
        "ignore all instructions",
        "system prompt",
        "you are now a",
        "bypass",
        "forget everything"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in injection_keywords)

def validate_input(text: str) -> (bool, str):
    """
    Orchestrates input validation.
    Returns (is_safe, message)
    """
    if detect_prompt_injection(text):
        return False, "Security Alert: Potential prompt injection detected. Please rephrase your request."
    
    if detect_pii(text):
        return False, "Privacy Alert: Please do not share sensitive information like account numbers, emails, or phone numbers."
    
    if not text.strip():
        return False, "Please enter a valid banking query."
        
    return True, ""