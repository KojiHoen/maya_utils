from . import order


# ----------------------------------------------------------------------------


RESOLUTIONS = set(["low", "mid", "high"])


# ----------------------------------------------------------------------------


def move_resolution(sections):
    """
    Catch resolution names in the sections and move them to the end of the
    sections list.

    :param list sections:
    :return: Resolution sections
    :rtype: list
    """
    match = RESOLUTIONS & set(sections)
    for m in match:
        order.move_to_last(m, sections)

    return sections
