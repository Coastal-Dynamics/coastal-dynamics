import os
from pathlib import Path
import json

import panel as pn
import pandas as pd

from coastal_dynamics.factory import QuestionFactory


class QuestionIndustry:
    """
    An industry class for creating and managing question widgets for a jupyter notebook.

    Attributes:
        question_data (Dict[str, Any]): Dictionary containing data for all questions in a notebook

    Methods:
        serve: Serves a pn.column concatenating multiple questions.
    """

    def __init__(self, question_dict):
        self.question_dict = question_dict

        self.served_questions = []
        self.question_counter = 1

    def serve(self, key_list):
        """
        Serves a pn.column concatenating multiple questions.

        Arguments:
            key_list: list with keys referring to specific questions in the question database (.json)
        
        Returns:
            question widget (pn.Column) containing multiple questions
        """
        # initialize column
        question_col = pn.Column(
            width_policy="max"
        )  # note that the width_policy='max' kwarg is added within the serve function of each question type individually

        # loop through questions to be added
        for question_key in key_list:
            if not question_key in self.served_questions:
                self.served_questions.append(question_key)

                self.question_dict[question_key][
                    "name"
                ] = f"Q-{int(self.question_counter)}"

                self.question_counter += 1

            question = QuestionFactory(
                question_key, self.question_dict[question_key]
            ).serve(question_key)

            # check if any previous answer are available
            if not os.path.exists(Path("saved_answers.json")):
                with open(Path("saved_answers.json"), "w") as f:
                    json.dump({"sample_key": "sample_answer"}, f)

            with open(Path("saved_answers.json"), "r") as f:
                json_data = json.load(f)

            if question_key in json_data.keys():
                question[1].value = json_data[question_key]

            question_col.append(question)

        return question_col
