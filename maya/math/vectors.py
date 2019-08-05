from maya import OpenMaya


__all__ = [
    "vector_to_list",
    "list_to_vector",
    "get_signed_angle",
    "get_average_vector"
]


def vector_to_list(vector):
    """
    :param MVector vector:
    :return: Vector values as list
    :rtype: list
    """
    return [vector.x, vector.y, vector.z]


def list_to_vector(l):
    """
    :param list l:
    :return: OpenMaya.MVector
    """
    return OpenMaya.MVector(*l)


def get_signed_angle(v1, v2):
    """
    Get the signed angle between two vectors

    :param OpenMaya.MVector v1:
    :param OpenMaya.MVector v2:
    :return: Signed angle
    :rtype: float
    """
    angle = v1.angle(v2)
    cross = v1 ^ v2

    if cross.z < 0:
        angle *= -1

    return angle


def get_average_vector(vectors):
    """
    Get the average of the provided vectors

    :param list vectors:
    :return: Average vector
    :rtype: OpenMaya.MVector
    """
    average_vector = OpenMaya.MVector()

    for vector in vectors:
        average_vector += vector

    average_vector /= len(vectors)
    return average_vector
