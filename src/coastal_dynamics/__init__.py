"""Tools for interactive teaching and learning with Jupyter notebooks."""

__author__ = """Floris Calkoen"""
__email__ = "floris@calkoen.nl"
__version__ = "0.0.11"

from .factory import QuestionFactory
from .io import read_questions, write_questions
from .multiple_choice import MultipleChoiceQuestion
from .multiple_selection import MultipleSelectionQuestion
from .numeric import NumericQuestion
from .question import Question
from .text import TextQuestion
from .utils import hash_answer, launch_app, load_notebook, save_notebook

from .industry import QuestionIndustry
from .modify_notebooks import clear_answers
from .use_answers_app import UseAnswersApp

__all__ = [
    "MultipleChoiceQuestion",
    "MultipleSelectionQuestion",
    "TextQuestion",
    "NumericQuestion",
    "QuestionFactory",
    "Question",
    "hash_answer",
    "launch_app",
    "load_notebook",
    "save_notebook",
    "read_questions",
    "write_questions",
    "QuestionIndustry",
    "clear_answers",
    "UseAnswersApp",
]
