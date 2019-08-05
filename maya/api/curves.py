from maya import OpenMaya
from .selection import to_mdag_path


__all__ = [
    "to_mfn_nurbs_curve",
    "get_curve_length",
    "get_tangent_at_parameter",
    "get_point_at_parameter",
    "get_parameter_from_length"
]


def to_mfn_nurbs_curve(curve):
    """
    :param str curve:
    :return: MFnNurbsCurve
    :rtype: OpenMaya.MFnNurbsCurve
    """
    dag = to_mdag_path(curve)
    nurbs_curve_fn = OpenMaya.MFnNurbsCurve(dag)

    return nurbs_curve_fn


def get_curve_length(curve):
    """
    :param str curve:
    :return: Length
    :rtype: float
    """
    curve_fn = to_mfn_nurbs_curve(curve)
    curve_length = curve_fn.length()

    return curve_length


def get_tangent_at_parameter(curve, parameter):
    """
    :param str curve:
    :param float parameter:
    :return: Tangent
    :rtype: OpenMaya.MFnNurbsCurve
    """
    curve_fn = to_mfn_nurbs_curve(curve)
    tangent = curve_fn.tangent(parameter, OpenMaya.MSpace.kWorld)

    return tangent


def get_point_at_parameter(curve, parameter):
    """
    :param str curve:
    :param float parameter:
    :return: Point
    :rtype: OpenMaya.MPoint
    """
    curve_fn = to_mfn_nurbs_curve(curve)
    point = OpenMaya.MPoint()
    curve_fn.getPointAtParam(parameter, point, OpenMaya.MSpace.kWorld)

    return point


def get_parameter_from_length(curve, length):
    """
    :param str curve:
    :param float length:
    :return: Parameter
    :rtype: float
    """
    curve_fn = to_mfn_nurbs_curve(curve)
    parameter = curve_fn.findParamFromLength(length)

    return parameter


