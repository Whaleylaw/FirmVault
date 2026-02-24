"""
PII Masker for Migration and Pre-Commit Defense-in-Depth

Detects and tokenizes personally identifiable information (PII) patterns
in text and YAML frontmatter. Supports SSN, phone, date of birth, and
email patterns with a firm email allowlist.

Token format: [PII_TYPE-N] (e.g., [SSN-1], [PHONE-2])

The firm email allowlist ensures that firm-internal email addresses
(e.g., sarena@whaleylawfirm.com) are NOT masked -- they are not PII
in this context.

Usage:
    from scripts.migrate.pii_masker import mask_pii, mask_frontmatter_pii

    masked, tokens = mask_pii("Call 502-555-1234 for SSN 123-45-6789")
    # masked == "Call [PHONE-1] for [SSN-2]"
    # tokens == [{"token": "[PHONE-1]", "type": "PHONE", ...}, ...]

    fm, tokens = mask_frontmatter_pii({"phone": "502-555-1234", "name": "Jane"})
    # fm == {"phone": "[PHONE-1]", "name": "Jane"}
"""

import json
import re
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# PII Pattern Definitions
# ---------------------------------------------------------------------------

# Word boundary anchors prevent false positives on case numbers and zip codes.
# SSN: exactly 3-2-4 digits with dash or space separators.
# Negative lookbehind/lookahead prevents matching within longer digit strings.
PII_PATTERNS: dict[str, re.Pattern] = {
    "SSN": re.compile(
        r'(?<!\d)'               # not preceded by a digit
        r'\d{3}[-\s]\d{2}[-\s]\d{4}'
        r'(?!\d)'               # not followed by a digit
    ),
    "PHONE": re.compile(
        r'(?<!\d)'
        r'(?:\+1[-\s.]?)?'      # optional country code
        r'\(?\d{3}\)?'          # area code with optional parens
        r'[-\s.]?'              # separator
        r'\d{3}'                # exchange
        r'[-\s.]?'              # separator
        r'\d{4}'                # subscriber
        r'(?!\d)'               # not followed by a digit
    ),
    "DOB": re.compile(
        r'\b'
        r'(?:0[1-9]|1[0-2])'   # month 01-12
        r'[/-]'
        r'(?:0[1-9]|[12]\d|3[01])'  # day 01-31
        r'[/-]'
        r'(?:19|20)\d{2}'      # year 1900-2099
        r'\b'
    ),
    "EMAIL": re.compile(
        r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    ),
}

# Firm emails that should NOT be masked (they are not PII in this context)
FIRM_EMAIL_ALLOWLIST: set[str] = {
    "sarena@whaleylawfirm.com",
    "aaron@whaleylawfirm.com",
}


# ---------------------------------------------------------------------------
# Core Masking Functions
# ---------------------------------------------------------------------------

def mask_pii(
    text: str, case_id: str = ""
) -> tuple[str, list[dict[str, str]]]:
    """Mask PII patterns in body text, returning masked text and token list.

    Scans text for SSN, PHONE, DOB, and EMAIL patterns. Each match is
    replaced with a token like [SSN-1], [PHONE-2], etc. Firm-allowlisted
    emails are skipped.

    Parameters
    ----------
    text : str
        The text to scan and mask.
    case_id : str, optional
        Case identifier for token map metadata (not used in token itself).

    Returns
    -------
    tuple[str, list[dict]]
        (masked_text, token_list) where each token dict has keys:
        "token", "type", "original", and optionally "case_id".
    """
    if not text:
        return text, []

    tokens: list[dict[str, str]] = []

    # Collect all matches with positions first, then replace from end to start
    # to preserve position accuracy.
    matches: list[tuple[int, int, str, str]] = []  # (start, end, type, value)

    for pii_type, pattern in PII_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group()
            # Skip allowlisted firm emails
            if pii_type == "EMAIL" and value.lower() in FIRM_EMAIL_ALLOWLIST:
                continue
            matches.append((match.start(), match.end(), pii_type, value))

    # Sort by position (start), then by length descending for overlapping matches
    # to prefer longer matches. Then deduplicate overlapping spans.
    matches.sort(key=lambda m: (m[0], -(m[1] - m[0])))
    filtered: list[tuple[int, int, str, str]] = []
    last_end = -1
    for start, end, pii_type, value in matches:
        if start >= last_end:
            filtered.append((start, end, pii_type, value))
            last_end = end

    # Replace from end to start to preserve positions
    result = text
    for start, end, pii_type, value in reversed(filtered):
        token_num = len(tokens) + 1
        token = f"[{pii_type}-{token_num}]"
        token_entry: dict[str, str] = {
            "token": token,
            "type": pii_type,
            "original": value,
        }
        if case_id:
            token_entry["case_id"] = case_id
        tokens.append(token_entry)
        result = result[:start] + token + result[end:]

    # Tokens were appended in reverse order; reverse to match reading order
    tokens.reverse()
    # Renumber tokens sequentially after sorting
    for i, tok in enumerate(tokens, 1):
        old_token = tok["token"]
        new_token = f"[{tok['type']}-{i}]"
        if old_token != new_token:
            result = result.replace(old_token, new_token)
            tok["token"] = new_token

    return result, tokens


def mask_frontmatter_pii(
    frontmatter: dict[str, Any], case_id: str = ""
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Mask PII in frontmatter dict fields.

    Scans specific frontmatter fields (phone, email, address, fax, ssn)
    for PII patterns and masks them. Handles nested dicts and lists
    recursively.

    Parameters
    ----------
    frontmatter : dict
        The YAML frontmatter dict to scan.
    case_id : str, optional
        Case identifier for token map metadata.

    Returns
    -------
    tuple[dict, list[dict]]
        (masked_frontmatter, token_list) where frontmatter is a new dict
        with PII-containing fields masked.
    """
    if not frontmatter:
        return frontmatter, []

    # Fields known to contain PII
    pii_field_names = {
        "phone", "email", "address", "fax", "ssn",
        "cell_phone", "home_phone", "work_phone",
        "mailing_address", "physical_address",
        "social_security", "date_of_birth", "dob",
    }

    all_tokens: list[dict[str, str]] = []
    result = _mask_dict_recursive(frontmatter, pii_field_names, case_id, all_tokens)
    return result, all_tokens


def _mask_dict_recursive(
    data: Any,
    pii_fields: set[str],
    case_id: str,
    tokens: list[dict[str, str]],
) -> Any:
    """Recursively mask PII in dict/list structures."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, str) and key.lower() in pii_fields:
                masked, new_tokens = mask_pii(value, case_id)
                # Offset token numbering based on existing count
                for tok in new_tokens:
                    idx = len(tokens) + 1
                    old_token = tok["token"]
                    new_token = f"[{tok['type']}-{idx}]"
                    if old_token != new_token:
                        masked = masked.replace(old_token, new_token)
                        tok["token"] = new_token
                    tokens.append(tok)
                result[key] = masked
            else:
                result[key] = _mask_dict_recursive(value, pii_fields, case_id, tokens)
        return result
    elif isinstance(data, list):
        return [
            _mask_dict_recursive(item, pii_fields, case_id, tokens)
            for item in data
        ]
    else:
        return data


# ---------------------------------------------------------------------------
# Token Map I/O
# ---------------------------------------------------------------------------

def write_token_map(tokens: list[dict[str, str]], output_path: Path) -> None:
    """Write a token map to JSON for future PII reversal if needed.

    Parameters
    ----------
    tokens : list[dict]
        Token list from mask_pii() or mask_frontmatter_pii().
    output_path : Path
        Path to write the JSON token map file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(tokens, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
