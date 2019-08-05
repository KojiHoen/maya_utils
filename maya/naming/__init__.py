from maya import cmds
from . import split, types, num, sides, resolutions, order
from .. import path


def conform(name):
    """
    Conform a parsed name to the studio naming convention for Maya.
    If the name exists as a node, it will take into account the node type
    of this node as part of the naming process.

    This script will attempt to conform whatever the name is to the naming
    convention documented on confluence:

    https://kinosis.atlassian.net/wiki/spaces/SP/pages/298254354/Asset+In-Application+Guide

    :param str name:
    :return: Conformed name
    :rtype: str
    """
    # get base name as a starting point in case the provided string contains
    # grouping and namespace information
    base = path.get_base(name)

    # split the base in different sections using different functions
    sections = base.split("_")
    sections = split.extract_digits(sections)
    sections = split.split_upper_case(sections)

    # lower case sections
    sections = [s.lower() for s in sections]

    # catch measurements
    sections = num.convert_measurements(sections)

    # catch side
    sections = sides.move_side(sections)

    # catch resolutions
    sections = resolutions.move_resolution(sections)

    # check if name exists
    if cmds.objExists(name):
        sections = types.add_type(name, sections)

    # catch digits
    sections = num.add_padding_to_digits(sections)
    sections = num.move_last_digit(sections)

    return "_".join(sections)
