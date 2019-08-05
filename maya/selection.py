from maya import cmds


def extend_with_shapes(selection):
    """
    :param list selection:
    :return: Extended selection
    :rtype: list
    """
    extended_selection = []

    shapes = cmds.listRelatives(
        selection,
        shapes=True,
        f=True,
        ni=True
    ) or []

    extended_selection.extend(cmds.ls(selection, long=True))
    extended_selection.extend(shapes)

    return extended_selection


def filter_by_type(selection, types):
    """
    :param list selection:
    :param str/list types:
    :return: Filtered selection
    :rtype: list
    """
    return cmds.ls(selection, type=types, long=True)


def filter_objects_from_components(selection, component="."):
    """
    Filter selection on objects and components. It is possible to alter the
    component search parameter so your filtered selection can only contain a
    certain type of component.

    :param list selection: 
    :param str component:
    :return: Filtered objects from components
    :rtype: tuple
    """
    components = []
    objects = []

    for s in selection:
        if not s.count(component):
            objects.append(s)
        else:
            components.append(s)

    return objects, components
