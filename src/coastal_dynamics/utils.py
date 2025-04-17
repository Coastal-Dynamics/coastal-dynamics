import hashlib
import numpy as np
from math import log10, floor


def hash_answer(answer, question_type, sig_figs=None):
    """Hash a single answer or a list of answers based on the question type."""
    if question_type == "multiple_selection":
        # For multiple_selection, directly hash each answer in the list
        return [hashlib.sha256(ans.encode()).hexdigest() for ans in answer]
    elif question_type == "text":
        # For text questions, normalize to lower case before hashing
        return hashlib.sha256(answer.lower().encode()).hexdigest()
    elif question_type == "multiple_choice":
        # For multiple_choice and numeric, directly hash the answer
        return hashlib.sha256(str(answer).encode()).hexdigest()
    elif question_type == "numeric":
        # if sig_figs:
        #     answer = np.format_float_positional(
        #         float(answer),
        #         precision=sig_figs,
        #         unique=False,
        #         fractional=False,
        #         trim="k",
        #     )
        if sig_figs:
            answer = round_sig(
                float(answer),
                sig_figs,
            )
        return hashlib.sha256(str(answer).encode()).hexdigest()
    else:
        msg = f"Unsupported question type: {question_type}"
        raise ValueError(msg)


def round_sig(x, sig):
    """Round a given number x to a certain amount of significant figures, and return this number in as float"""
    # Handle zero input explicitly
    if x == 0:
        return 0

    # Calculate the rounding precision
    precision = sig - int(floor(log10(abs(x)))) - 1

    # Compute rounded value
    factor = 10**precision
    adjusted_x = x * factor

    if adjusted_x % 1 == 0.5:  # Check if it ends in an exact 5
        adjusted_x = adjusted_x + 0.5  # Push up if it's exactly halfway

    return round(adjusted_x) / factor
