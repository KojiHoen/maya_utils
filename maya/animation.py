import math
from maya import cmds
from . import attributes


def get_incoming_animation_curve(node, attr):
    """
    :param str node:
    :param str attr:
    :return: Incoming animation curve
    :rtype: str/None
    """
    plug = attributes.validate_attribute(node, attr)
    animation_curves = cmds.listConnections(plug, type="animCurve") or []

    if not animation_curves:
        return

    return animation_curves[0]


def get_animation_curve_range(node, attr):
    """
    Get the range between the maximum and minimum of the time of the keys on
    the animation curve attached to the attribute of the node.

    :param str node:
    :param str attr:
    :return: Animation range
    :rtype: list
    """
    # get animation curves attached to the attribute
    animation_curve = get_incoming_animation_curve(node, attr)

    # validate animation curve
    if not animation_curve:
        return []

    # get keys on animation curves
    animation_keys = cmds.keyframe(animation_curve, query=True, timeChange=True) or []

    # validate animation keys on animation curve
    if not animation_keys:
        return []

    # get values
    start = int(math.floor(min(animation_keys)))
    end = int(math.ceil(max(animation_keys)))

    return range(start, end)
