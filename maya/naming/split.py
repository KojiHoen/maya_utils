import string


def process_sections(sections, mode_func, match_func):
    """
    :param list sections:
    :param func mode_func:
    :param func match_func:
    :return: Split sections
    :rtype: list
    """
    sections_extended = []

    for section in sections:
        sections_extended.extend(
            mode_func(
                section,
                match_func,
            )
        )

    return sections_extended


def split(sections, match_func):
    """
    :param list sections:
    :param func match_func:
    :return: Split sections
    :rtype: list
    """
    return process_sections(sections, split_section, match_func)


def extract(sections, match_func):
    """
    :param list sections:
    :param func match_func:
    :return: Split sections
    :rtype: list
    """
    return process_sections(sections, extract_section, match_func)


# ----------------------------------------------------------------------------


def extract_section(section, match_func):
    """
    Extract sections based on a match function. It groups matches together
    based on matching state of the function.

    :param section:
    :param match_func:
    :return:
    """
    # variables
    part = ""
    length = len(section)
    sections = []
    match_state = None

    # extract sections
    for i, s in enumerate(section):
        # get state
        state = match_func(s)

        # validate state
        if i == 0:
            match_state = state
        else:
            if match_state != state:
                sections.append(part)
                part = ""

        # append to part and update match state
        part += s
        match_state = state

        # make sure to add last part
        if i == length - 1:
            sections.append(part)

    return sections


def split_section(section, match_func):
    """
    Split sections based on a match function. It groups sections together
    until it finds the next string that matches. It will also combine groups
    together if the matches are successive.

    :param str section:
    :param func match_func:
    :return: Split sections
    :rtype: list
    """
    # variables
    sections = []
    indices = []

    # get length
    length = len(section)

    # get split indices
    for i, s in enumerate(section):
        if match_func(s):
            indices.append(i)

    # validate indices
    if not indices:
        return [section]

    # catch counting indices
    _indices = indices[:]
    for i in range(len(indices)-2, 0, -1):
        num = _indices[i]
        if num-1 == _indices[i-1] and num+1 == _indices[i+1]:
            indices.remove(num)

    # add end
    if length not in indices:
        # only remove the trailing index if its in the list and if its not the
        # only index in the list
        if length - 1 in indices and indices.index(length-1) != 0:
            indices.remove(length - 1)

        indices.append(length)

    # add start
    if 0 not in indices:
        indices.insert(0, 0)

    # split section based on indices
    start = indices[:-1]
    end = indices[1:]

    for s, e in zip(start, end):
        sections.append(section[s:e])

    return sections


# ----------------------------------------------------------------------------


def is_upper_case(s):
    """
    :param str s:
    :return: Upper case state
    :rtype: bool
    """
    return True if s in string.ascii_uppercase else False


def is_digit(s):
    """
    :param str s:
    :return: Digit state
    :rtype: bool
    """
    return s.isdigit()


# ----------------------------------------------------------------------------


def split_upper_case(sections):
    """
    :param list sections:
    :return: Upper case split sections
    :rtype: list
    """
    return split(sections, is_upper_case)


def extract_digits(sections):
    """
    :param list sections:
    :return: Digit split sections
    :rtype: list
    """
    return extract(sections, is_digit)
