from maya import OpenMaya
from .selection import to_mdag_path


__all__ = [
    "to_mfn_nurbs_surface",
    "point_from_uv",
    "tangents_from_uv",
]


def to_mfn_nurbs_surface(surface):
    """
    :param str surface:
    :return: MFnMesh
    :rtype: OpenMaya.MFnMesh
    """
    dag = to_mdag_path(surface)
    nurbs_surface_fn = OpenMaya.MFnNurbsSurface(dag)

    return nurbs_surface_fn


def point_from_uv(surface, u, v):
    """
    :param str surface:
    :param float/int u:
    :param float/int v:
    :return: Position
    :rtype: OpenMaya.MPoint
    """
    pos = OpenMaya.MPoint()
    nurbs_surface_fn = to_mfn_nurbs_surface(surface)
    nurbs_surface_fn.getPointAtParam(u, v, pos, OpenMaya.MSpace.kWorld)

    return pos


def tangents_from_uv(surface, u, v):
    """
    :param str surface:
    :param float/int u:
    :param float/int v:
    :return: U-tangent, V-tangent
    :rtype: OpenMaya.MVector, OpenMaya.MVector
    """
    u_tangent = OpenMaya.MVector()
    v_tangent = OpenMaya.MVector()

    nurbs_surface_fn = to_mfn_nurbs_surface(surface)
    nurbs_surface_fn.getTangents(
        u,
        v,
        u_tangent,
        v_tangent,
        OpenMaya.MSpace.kWorld
    )

    return u_tangent, v_tangent


