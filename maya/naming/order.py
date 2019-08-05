def move_to_last(name, sections):
    """
    Move a name to the end of the sections list.
    If the name is not part of the list the sections will be returned as they
    were parsed.

    :param str name:
    :param list sections:
    :return: Sections
    :rtype: list
    """
    if name in sections:
        sections.reverse()
        sections.remove(name)
        sections.reverse()
        sections.append(name)

    return sections
