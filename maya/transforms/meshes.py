from maya import cmds, OpenMaya
from .. import api, path, math, selection


__all__ = [
    "matrix_from_mesh_component",
    "matrix_from_mesh_component_selection"
]


def matrix_from_mesh_component(component):
    """
    Get the transformation matrix in world space based on a 1 point component.
    The normal of the mesh will be used to rotation values of the matrix.

    :param str component:
    :return: Matrix
    :rtype: list
    """
    # split vertex
    mesh, _ = component.split(".", 1)

    # get positions
    positions = cmds.xform(component, query=True, ws=True, t=True)
    positions = path.split_list(positions, 3)

    # get average position
    average_position = math.get_average_vector([OpenMaya.MVector(*p) for p in positions])
    average_position = math.vector_to_list(average_position)

    # get normal and up
    up = api.meshes.closest_normal_from_point(mesh, average_position)
    world_up = OpenMaya.MVector(0, 1, 0)

    # get angle
    angle = up.angle(world_up)

    # get side vector
    if 0 < angle < math.pi:
        side = (world_up ^ up).normal()
    else:
        side = OpenMaya.MVector(1, 0, 0)

    # get forward vector
    forward = (side ^ up).normal()

    # construct matrix
    return math.channels_to_matrix_list(side, up, forward, average_position)


def matrix_from_mesh_component_selection():
    """
    Get the transformation matrix in world space based on a 1 point component
    selection. The normal of the mesh will be used to rotation values of
    the matrix.

    :return: Matrix
    :rtype: list
    """
    # get vertices from selection
    sel = cmds.ls(sl=True, fl=True)
    _, components = selection.filter_objects_from_components(sel, component=".")

    # validate selection
    if not components or cmds.nodeType(components[0]) != "mesh":
        raise RuntimeError("Make a mesh component selection!")

    return matrix_from_mesh_component(components[0])
