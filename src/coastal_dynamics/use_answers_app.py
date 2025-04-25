from pathlib import Path
import json
import os

import panel as pn


class UseAnswersApp:
    """
    Class for creating and serving an application that allows users to use or 'reset' their previously given answers.
    """
    def __init__(self, notebook_prefix="1a"):
        self.saved_answers_path = Path("./saved_answers.json")

        # get notebook prefix
        self.notebook_prefix = notebook_prefix

    def serve(self):
        """
        Function for building the application.
        
        Returns:
            application (pn.Column)
        """
        return self.build_app()

    def get_number_saved_answers(self):
        """
        Computes the number of given answers present in any previous saves.
        
        Returns:
            number of given answers (int)
        """
        # check if the file exists
        if os.path.exists(self.saved_answers_path):
            # read the file
            with open(self.saved_answers_path, "r") as f:
                saved_answers = json.load(f)

            # get the number of questions that have previously been answered
            n_questions = len(
                [
                    key
                    for key in list(saved_answers.keys())
                    if self.notebook_prefix in key
                ]
            )

        else:
            n_questions = 0

        return n_questions

    def build_app(self):
        """
        Build the app (with all text and buttons).
        
        Returns:
            app (pn.Column)
        """
        self.n_questions = self.get_number_saved_answers()
        self.n_questions_removed = 0

        self.explanation_text = pn.pane.Markdown(
            f"""
            ### Use saved answers

            We found saved answers for {self.n_questions} questions.
            """
        )

        self.help_text = str(
            """
            If you want to use your saved answers, you can skip this interface and move on to the rest of the notebook. This will load your previous answers and use them to pre-fill the questions in this notebook (as soon as you run the corresponding cells). You can then change the answers if you want to.

            If you want to disregard your saved answers, select the button "Disregard saved answers". This will delete your previous answers (for this notebook) and you will have to answer all (non-coding) questions again.
            """,
        )
        self.help_text_widget = pn.widgets.StaticText(value=" ")

        self.help_button = pn.widgets.Button(name="Help", button_type="default")

        # self.use_saved_answers_button = pn.widgets.Button(
        #     name="Use saved answers", button_type="default"
        # )
        self.disregard_saved_answers_button = pn.widgets.Button(
            name="Disregard saved answers", button_type="default"
        )
        self.are_you_sure_button = pn.widgets.Button(
            name="Are you sure?", button_type="danger", visible=False
        )

        self.ready_to_go_text_widget = pn.widgets.StaticText(value=" ")
        self.ready_to_go_text = """You can now continue with the notebook."""

        @pn.depends(
            self.help_button.param.value,
            # self.use_saved_answers_button.param.value,
            self.disregard_saved_answers_button.param.value,
            self.are_you_sure_button.param.value,
        )
        def main(
            help_button_value,
            # use_saved_answers_button_value,
            disregard_saved_answers_button_value,
            are_you_sure_button_value,
        ):
            """Function to keep track of button presses.
            
            Arguments:
                help_button_value (bool)
                use_saved_answers_button_value (bool) --> OUTDATED
                disregard_saved_answers_button_value (bool)
                are_you_sure_button_value (bool)
                
            """
            if help_button_value:
                self.help_text_widget.value = self.help_text
            else:
                str(" ")

            # if use_saved_answers_button_value:
            #     self.ready_to_go_text = (
            #         f"{self.n_questions} saved answers were loaded."
            #         + self.ready_to_go_text
            #     )
            #     self.disable_widgets()

            if disregard_saved_answers_button_value:
                self.are_you_sure_button.visible = True

            if are_you_sure_button_value:
                self.remove_question_keys()

            return None

        app = pn.Column(
            self.explanation_text,
            self.help_button,
            self.help_text_widget,
            # self.use_saved_answers_button,
            pn.Row(self.disregard_saved_answers_button, self.are_you_sure_button),
            self.ready_to_go_text_widget,
            main,
        )

        return app

    def disable_widgets(self):
        """
        Function to disable all widgets.
        
        Returns:
            True
        """
        for widget in [
            # self.use_saved_answers_button,
            self.disregard_saved_answers_button,
            self.are_you_sure_button,
        ]:
            widget.disabled = True

        self.ready_to_go_text_widget.value = self.ready_to_go_text

        return True

    def remove_question_keys(self, fp=Path("saved_answers.json")):
        """
        Function to remove previously saved answers (i.e., question keys) from served question apps.
        """
        if os.path.exists(fp):
            # read the file
            with open(self.saved_answers_path, "r") as f:
                saved_answers = json.load(f)

            # remove the question keys
            for key in list(saved_answers.keys()):
                if self.notebook_prefix in key:
                    saved_answers.pop(key)
                    self.n_questions_removed += 1

            # write the file again
            with open(self.saved_answers_path, "w") as f:
                json.dump(saved_answers, f)

            self.ready_to_go_text = (
                f"{self.n_questions_removed} answers were removed. "
                + self.ready_to_go_text
            )

        self.disable_widgets()

    def rename_saved_answers(self, fname):
        """Function to rename saved answer file to a new file."""
        with open(self.saved_answers_path, "r") as f:
            saved_answers = json.load(f)

        with open(fname, "w") as f:
            json.dump(saved_answers, f)

        self.remove_question_keys()

        self.disable_widgets()
