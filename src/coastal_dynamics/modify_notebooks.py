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
