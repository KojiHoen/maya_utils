from maya import OpenMaya
from . import vectors


__all__ = [
    "channels_to_matrix_list",
    "list_to_matrix",
    "matrix_to_list"
]


def channels_to_matrix_list(x=None, y=None, z=None, t=None):
    """
    :param list/OpenMaya.MVector/None x: X-vector
    :param list/OpenMaya.MVector/None y: Y-vector
    :param list/OpenMaya.MVector/None z: Z-vector
    :param list/OpenMaya.MPoint/None t: Translation
    :return: Matrix
    :rtype: list
    """
    # define lists if not provided
    if not x:
        x = [1, 0, 0]
    if not y:
        y = [0, 1, 0]
    if not z:
        z = [0, 0, 1]
    if not t:
        t = [0, 0, 0]

    # convert maya type to list
    if type(x) != list:
        x = vectors.vector_to_list(x)
    if type(y) != list:
        y = vectors.vector_to_list(y)
    if type(z) != list:
        z = vectors.vector_to_list(z)
    if type(t) != list:
        t = vectors.vector_to_list(t)

    # construct matrix
    return x + [0] + y + [0] + z + [0] + t + [1]


def list_to_matrix(l):
    """
    :param list l:
    :return: Matrix
    :rtype: OpenMaya.MMatrix
    """
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil().createMatrixFromList(l, matrix)

    return matrix


def matrix_to_list(matrix):
    """
    :param OpenMaya.MMatrix matrix:
    :return: Matrix as list
    :rtype: list
    """
    return [
        matrix(i, j)
        for i in range(4)
        for j in range(4)
    ]
