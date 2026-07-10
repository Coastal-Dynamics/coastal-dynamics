def clear_answers(
    notebook, begin_key="#BEGIN_CORRECT_ANSWER", end_key="#END_CORRECT_ANSWER"
):
    """Modify the notebook (i.e., remove all notebooks for a given beginning and end key).
    A notebook consists of a dictionary with keys:
        - "cells" (containing a list of cells)
        - "metadata"
        - "nbformat"
        - "nbformat_minor"
    We need to look at the "source" key of each cell in the list of cells.
    """

    number_of_answers_removed = 0

    # loop through cells
    for i_cell in range(len(notebook["cells"])):
        source = notebook["cells"][i_cell]["source"]

        for i, begin_line in enumerate(source):
            if begin_key in begin_line:
                for j, end_line in enumerate(source[i:]):
                    if end_key in end_line:
                        source = source[:i] + source[i + j + 1 :]

                        number_of_answers_removed += 1

                        break
                break

        notebook["cells"][i_cell]["source"] = source

    return notebook, number_of_answers_removed


def replace_popouts(notebook, popout_func="cd.launch_app"):
    number_of_popouts_removed = 0

    # loop through cells
    for i_cell in range(len(notebook["cells"])):
        source = notebook["cells"][i_cell]["source"]

        # replace popout function calls
        new_source = [line.replace(popout_func, "") for line in source]

        notebook["cells"][i_cell]["source"] = new_source

        if new_source != source:
            number_of_popouts_removed += 1

    return notebook, number_of_popouts_removed


def clear_notes(notebook, begin_key="#BEGIN_NOTE2TEAM", end_key="#END_NOTE2TEAM"):
    number_of_notes_removed = 0

    # loop through cells
    for i_cell in range(len(notebook["cells"])):
        source = notebook["cells"][i_cell]["source"]

        for i, begin_line in enumerate(source):
            if begin_key in begin_line:
                for j, end_line in enumerate(source[i:]):
                    if end_key in end_line:
                        source = source[:i] + source[i + j + 1 :]

                        number_of_notes_removed += 1

                        break
                break

        notebook["cells"][i_cell]["source"] = source

    return notebook, number_of_notes_removed
