from . import order


# ----------------------------------------------------------------------------


PADDING = 3
MEASUREMENTS_MAPPER = {
    "pt": "pt",
    "point": "pt",
    "mm": "mm",
    "millimeter": "mm",
    "cm": "cm",
    "centimeter": "cm",
    "m": "m",
    "meter": "m",
    "km": "km",
    "kilometer": "km",
}
MEASUREMENTS = set(MEASUREMENTS_MAPPER.keys())


# ----------------------------------------------------------------------------


def convert_measurements(sections):
    """
    Based on the matching MEASUREMENTS the sections will be combined
    conforming to the measurements naming convention.

    :param list sections:
    :return: Combined measurements sections
    :rtype: list
    """
    # variables
    v = ""
    indices = []
    sections_edit = sections[:]

    # get matching measurements
    sections_set = set(sections)
    match = MEASUREMENTS & sections_set

    # get matches
    for m in match:
        # get indices
        index = sections.index(m)
        indices.append(index)

        # get digit before measurement
        if index != 0 and sections[index-1].isdigit():
            indices.append(index-1)

    # sort indices
    indices.sort()
    indices.reverse()
    indices.append(-2)

    # merge measurements and digits
    for i, n in zip(indices[:-1], indices[1:]):
        m = sections[i]
        m = MEASUREMENTS_MAPPER.get(m, m)

        v = m + v
        sections_edit.pop(i)

        if n != i - 1:
            sections_edit.insert(i, v)
            v = ""

    return sections_edit


def add_padding_to_digits(sections):
    """
    :param sections:
    :return: Padded digits sections
    :rtype: list
    """
    return [
        s.zfill(PADDING) if s.isdigit() else s
        for s in sections
    ]


def move_last_digit(sections):
    """
    Move the last digit found to the last place on the list.
    This needs to be done to conform with the naming convention of
    numerations.

    :param sections:
    :return: Digit move sections
    :rtype: list
    """
    # get digits
    digits = [s for s in sections if s.isdigit()]

    # validate digits
    if not digits:
        return sections

    # move digit
    order.move_to_last(digits[-1], sections)

    return sections
