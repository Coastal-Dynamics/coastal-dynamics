import json
import os
from pathlib import Path
from typing import Literal

import panel as pn
import pandas as pd

import coastal_dynamics as cd


class Question:
    """Base class for different types of questions with encryption functionality.

    This class provides common functionalities for question widgets including encryption of answers.

    Attributes:
        name (str): The name of the question widget.
        question_text (str): The text of the question.
        feedback_widget (pn.widgets.StaticText): The widget to display feedback.
        submit_button (pn.widgets.Button): The button to submit the answer.
    """

    def __init__(
        self,
        question_name: str,
        question_text: str,
        question_feedback: dict[Literal["correct", "incorrect"], str],
    ):
        self.name = question_name
        self.question_text = question_text
        self.feedback = question_feedback
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create and initialize the Panel widgets for the question."""
        self.question_widget = pn.widgets.StaticText(
            name=self.name, value=self.question_text, sizing_mode="stretch_width"
        )
        self.submit_button = pn.widgets.Button(name="Submit", width=75)
        self.feedback_widget = pn.widgets.StaticText(sizing_mode="stretch_width")

    def serve(self) -> pn.Column:
        """Serve the question as a Panel column."""
        msg = "This method should be implemented by subclasses"
        raise NotImplementedError(msg)

    def check_answer(self, event) -> None:
        """Check the submitted answer against the correct answer."""
        msg = "This method should be implemented by subclasses"
        raise NotImplementedError(msg)

    def hash_answer(self, answer, question_type, sig_figs=None):
        """Delegate the hashing of an answer to the coastal_dynamics module."""
        return cd.hash_answer(answer, question_type, sig_figs=sig_figs)

    def save_answer(self, key, answer):
        """Add the answer to the question stats"""
        if not os.path.exists(Path("saved_answers.json")):
            with open(Path("saved_answers.json"), "w") as f:
                json.dump({"sample_key": "sample_answer"}, f)

        with open(Path("saved_answers.json"), "r") as f:
            json_data = json.load(f)

        if type(answer) in [str, int, float, list]:
            json_data[key] = answer

        with open(Path("saved_answers.json"), "w") as f:
            json.dump(json_data, f)

        return
