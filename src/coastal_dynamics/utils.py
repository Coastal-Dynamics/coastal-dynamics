import hashlib
import socket
import os
import logging
import warnings
import json

from math import log10, floor

import numpy as np


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


def find_free_port():
    """Finds an available port to serve a panel app."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))  # Bind to an available port
        return s.getsockname()[1]  # Get assigned port


def launch_app(app):
    """Launches panel app, returns string with address of app"""

    # Turn of warnings in notebooks
    logging.getLogger().setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")

    # find available port
    port = find_free_port()

    # launch app
    app.show(port=port, threaded=True, verbose=False)

    # generate printed address
    if "JUPYTERHUB_USER" not in list(os.environ.keys()):
        address = f"http://localhost:{port}"

    else:
        user = os.environ["JUPYTERHUB_USER"]

        address = f"https://coastal.citg.tudelft.nl/codebook/user/{user}/proxy/{port}/"

    return "See the app at: " + address


def load_notebook(file_path):
    """Load notebook as json"""
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
    return notebook


def save_notebook(notebook, new_file_path):
    """Save the modified notebook"""
    with open(new_file_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=4, ensure_ascii=False)
    return


# NOT NEEDED ANYMORE SINCE WE ARE USING RELATIVE FILE PATHS EVERYWHERE
# def path(fpath):
#     """Returns path to the database files, either for global users of the jupyter hub
#     or when using a local file path.

#     fpath (str): string containing local file path
#         example: "database/1_coastal_classification/1_earthquakes_sample.parquet"
#     """


#     # users that run locally
#     if "JUPYTERHUB_USER" not in list(os.environ.keys()):
#         p = "./" + fpath

#     # users of HUB
#     else:
#         p = "/var/" + fpath

#     return Path(p)
