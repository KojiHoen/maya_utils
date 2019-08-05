from maya import cmds
from . import generic, meshes, surfaces, curves
from .. import selection


__all__ = [
    "generic",
    "meshes",
    "surfaces",
    "curves",
    "matrix_from_selection"
]


def matrix_from_selection():
    """
    A wrapper function that will try to find the correct matrix query
    function based on the current selection type and number of items
    selected.

    :return: Matrix
    :rtype: list/None
    :raise RuntimeError: When no selection is made
    :raise RuntimeError: When the selection type is not supported
    """
    # get selection
    sel = cmds.ls(sl=True, fl=True) or []

    # validate selection
    if not sel:
        raise RuntimeError("No selection made!")

    # get query based on selection length
    if len(sel) >= 2:
        return generic.matrix_from_3_points_selection()

    # filter selection
    _, components = selection.filter_objects_from_components(sel)

    # validate components
    if not components:
        raise RuntimeError("Selection not supported!")

    # get query based on type
    component = components[0]
    if cmds.nodeType(component) == "mesh":
        return meshes.matrix_from_mesh_component_selection()
    elif component.count(".uv") and cmds.nodeType(component) == "nurbsSurface":
        return surfaces.matrix_from_surface_point_selection()
    elif component.count('.u') and cmds.nodeType(component) == "nurbsCurve":
        return curves.matrix_from_curve_point_selection()
    else:
        raise RuntimeError("Selection not supported!")
