from maya import cmds, OpenMaya
from .. import api, path, math, selection

__all__ = [
    "matrix_from_parameter",
    "create_matrices_on_curve",
    "matrix_from_curve_point_selection"
]


def matrix_from_parameter(curve, parameter):
    """
    Get the matrix of a point on curve at given parameter.

    :param str curve:
    :param float parameter:
    :return: Matrix
    :rtype: list
    """
    point_at_param = api.curves.get_point_at_parameter(curve, parameter)
    pos = math.vectors.list_to_vector([point_at_param.x, point_at_param.y, point_at_param.z])
    curve_tangent = api.curves.get_tangent_at_parameter(curve, parameter)

    up_vector = OpenMaya.MVector(0, 1, 0)
    side = (up_vector ^ curve_tangent).normal()
    up = (curve_tangent ^ side).normal()

    matrix_list = math.matrices.channels_to_matrix_list(side, up, curve_tangent, pos)

    return matrix_list


def create_matrices_on_curve(curve, count):
    """
    Creates multiple matrices in uniform distance on curve based on desired
    number of points. When count is 1 it will return a single matrix on the
    middle of the curve.

    :param str curve:
    :param int count:
    :return: Dictionary with parameter and corresponding matrix
    :return: Matrix at parameter 0.5
    :rtype: matrix, dict
    :raise ValueError: Raises ValueError when count is 0 or below 0.
    """
    if count <= 0:
        raise ValueError("Please set count higher than 0")

    matrix_dict = {}

    if count == 1:
        matrix = matrix_from_parameter(curve, 0.5)
        matrix_dict[0.5] = matrix
        return matrix_dict

    increment = 1.0 / (count - 1)
    curve_length = api.curves.get_curve_length(curve)
    for c in range(count):
        length = curve_length * increment * c
        parameter = api.curves.get_parameter_from_length(curve, length)
        matrix = matrix_from_parameter(curve, parameter)
        matrix_dict[parameter] = matrix
    return matrix_dict


def matrix_from_curve_point_selection():
    """
    Get the matrix transformation values at any given point on curve.

    :return: Matrix
    :rtype: list
    """
    sel = cmds.ls(sl=1)
    _, u_value = selection.filter_objects_from_components(sel, component=".u")
    curve, component, value = path.split_component(u_value[0])

    return matrix_from_parameter(curve, value)
