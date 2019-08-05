from maya import OpenMaya


__all__ = [
    "to_mobject",
    "to_mdag_path"
]


def to_mobject(node):
    """
    :param str node:
    :return: toMObject
    :rtype: OpenMaya.toMObject
    """
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(node)
    obj = OpenMaya.MObject()
    selection_list.getDependNode(0, obj)

    return obj


def to_mdag_path(node):
    """
    :param str node:
    :return: MDagPath
    :rtype: OpenMaya.MDagPath
    """
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(node)
    dag = OpenMaya.MDagPath()
    selection_list.getDagPath(0, dag)

    return dag


