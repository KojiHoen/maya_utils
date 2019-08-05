from maya import cmds, OpenMaya
from .. import api, path, math, selection


__all__ = [
    "matrix_from_surface_point",
    "matrix_from_surface_point_selection"
]


def matrix_from_surface_point(surface, u, v):
    """
    Get the transformation matrix in world space based on a 1 surface point.
    The derivatives of the surface will be used to calculate the rotation
    values of the matrix.
k
    :param str surface:
    :param float/int u:
    :param float/int v:
    :return: Matrix
    :rtype: list
    """
    # query surface
    pos = api.surfaces.point_from_uv(surface, u, v)
    pos = math.vector_to_list(pos)
    forward, side = api.surfaces.tangents_from_uv(surface, u, v)

    # calculate up
    up = (forward ^ side).normal()
    side = (up ^ forward).normal()

    # construct matrix
    return math.channels_to_matrix_list(side, up, forward, pos)


def matrix_from_surface_point_selection():
    """
    Get the transformation matrix in world space based on a 1 point vertex
    selection. The normal of the mesh will be used to rotation values of
    the matrix.

    :return: Matrix
    :rtype: list
    """
    # get vertices from selection
    sel = cmds.ls(sl=True, fl=True)
    _, uvs = selection.filter_objects_from_components(sel, component=".uv")

    # validate selection
    if not uvs:
        raise RuntimeError("Make a surface selection!")

    # split component
    surface, component, values = path.split_component(uvs[0])
    return matrix_from_surface_point(surface, *values)
