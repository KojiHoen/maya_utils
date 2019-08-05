SIDES_MAPPER = {
    "r": "r",
    "right": "r",
    "l": "l",
    "left": "l",
    "m": "m",
    "middle": "m",
}
SIDES = set(SIDES_MAPPER.keys())


# ----------------------------------------------------------------------------


def move_side(sections):
    """
    Catch sides names in the sections and move them to the front of the
    sections list. It will also convert long name sides to short names.

    :param list sections:
    :return: Side sections
    :rtype: list
    """
    match = SIDES & set(sections)
    for m in match:
        sections.remove(m)
        sections.insert(0, SIDES_MAPPER.get(m))

    return sections
