from maya import cmds, OpenMaya
from .. import math, path


__all__ = [
    "matrix_from_3_points",
    "matrix_from_3_points_selection"
]


def matrix_from_3_points(s1, s2, s3=None):
    """
    Get the transformation matrix in world space based on 2 or 3 points.
    The first two points will determine the z-direction and the center of
    those two points will be the position. The 3rd point selection is
    optional, it determines the x-direction which results in a better
    y-direction as well.

    :param str s1:
    :param str s2:
    :param str/None s3:
    :return: Matrix
    :rtype: list
    """
    # get start and end and determine locator position
    start_positions = cmds.xform(s1, query=True, ws=True, t=True)
    start_positions = path.split_list(start_positions, 3)
    start = math.get_average_vector([OpenMaya.MVector(*p) for p in start_positions])

    end_positions = cmds.xform(s2, query=True, ws=True, t=True)
    end_positions = path.split_list(end_positions, 3)
    end = math.get_average_vector([OpenMaya.MVector(*p) for p in end_positions])

    pos = (start + end) * 0.5

    # get side vector
    if s3:
        side_positions = cmds.xform(s3, query=True, ws=True, t=True)
        side_positions = path.split_list(side_positions, 3)
        side = math.get_average_vector([OpenMaya.MVector(*p) for p in side_positions])
        side = (side - pos).normal()

    else:
        side = OpenMaya.MVector(1, 0, 0)

    # get forward vector
    forward = (end - pos).normal()

    # flip side vector based on the signed angle
    # this needs to be done to ensure the created matrix follows the
    # right hand rule.
    signed_angle = math.get_signed_angle(side, forward)
    if signed_angle < 0:
        side *= -1

    # construct vectors for matrix
    up = (forward ^ side).normal()
    side = up ^ forward

    # construct matrix
    return math.channels_to_matrix_list(side, up, forward, pos)


def matrix_from_3_points_selection():
    """
    Get the transformation matrix in world space based on a 2 or 3 point
    selection. The first two points will determine the z-direction and the
    center of those two points will be the position. The 3rd point selection
    is optional, it determines the x-direction which results in a better
    y-direction as well.

    :return: Matrix
    :rtype: list
    """
    # validate selection order
    if not cmds.selectPref(query=True, trackSelectionOrder=True):
        raise RuntimeError("Make sure tracking of the selection order is enabled in the preferences!")

    # get selection
    sel = cmds.ls(os=True, fl=True)

    # validate selection
    if len(sel) < 2:
        raise RuntimeError("Select at least 2 components!")

    return matrix_from_3_points(*sel[:3])
