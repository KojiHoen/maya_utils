from maya import OpenMaya
from .selection import to_mdag_path


__all__ = [
    "to_mfn_mesh",
    "closest_uv_from_point",
    "closest_normal_from_point"
]


def to_mfn_mesh(mesh):
    """
    :param str mesh:
    :return: MFnMesh
    :rtype: OpenMaya.MFnMesh
    """
    dag = to_mdag_path(mesh)
    mesh_fn = OpenMaya.MFnMesh(dag)

    return mesh_fn


def closest_uv_from_point(mesh, pos, uv_set=None):
    """
    Get the closest uv based in a point on world space.

    :param str mesh:
    :param pos: list
    :param uv_set: str
    :return: UV point
    :rtype: tuple
    """
    # get mesh
    mesh_fn = to_mfn_mesh(mesh)

    # uv variables
    float_point = OpenMaya.MFloatPoint(pos[0], pos[1], pos[2])
    reference_point = OpenMaya.MPoint(float_point)
    uv_array = [0.0, 0.0]
    uv_util = OpenMaya.MScriptUtil()
    uv_util.createFromList(uv_array, 2)

    uv_point = uv_util.asFloat2Ptr()

    # query uv point
    mesh_fn.getUVAtPoint(reference_point, uv_point, OpenMaya.MSpace.kWorld, uv_set)

    # get uv values
    u_value = OpenMaya.MScriptUtil.getFloat2ArrayItem(uv_point, 0, 0) or None
    v_value = OpenMaya.MScriptUtil.getFloat2ArrayItem(uv_point, 0, 1) or None

    return u_value, v_value


def closest_normal_from_point(mesh, pos):
    """
    Get the closest normal based in a point on world space.

    :param str mesh:
    :param pos: list
    :return: Normal
    :rtype: OpenMaya.MVector
    """
    # get mesh
    mesh_fn = to_mfn_mesh(mesh)

    # get point
    point = OpenMaya.MPoint(*pos)

    # get normal
    normal = OpenMaya.MVector()
    mesh_fn.getClosestNormal(point, normal, OpenMaya.MSpace.kWorld)

    return normal
