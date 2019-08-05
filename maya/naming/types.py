from maya import cmds
from . import order


# ----------------------------------------------------------------------------


TYPE_MAPPER = {
    "transform": "grp",
    "mesh": "mesh",
    "nurbsCurve": "crv",
    "deformBend": "bend",
    "deformFlare": "flare",
    "deformSine": "sine",
    "deformSquash": "squash",
    "deformTwist": "twist",
    "deformWave": "wave",
    "softModHandle": "sm",
    "locator": "loc",
    "textureDeformerHandle": "tex_def",
    "clusterHandle": "cls",
    "lattice": "lattice",
    "baseLattice": "lattice_base",
    "camera": "cam",
    "sculpt": "sculpt",
    "implicitSphere": "implicit_sphere",
}

TAG_MAPPER = {
    "isControl": "ctrl"
}

TAG_KEYS = set(TAG_MAPPER.keys())
PROTECTED_KEYS = set(
    [
        "setup",
        "skeleton",
        "controls",
        "rig",
        "untouchables",
        "geometry",
        "geo",
        "proxy"
    ]
)


# ----------------------------------------------------------------------------


def get_type(node, sections):
    """
    Get the node type of an node based on pre-defined protected keys,
    attributes on the node and lastly fall back on the node type of the
    object. Assembly nodes are handled differently to not have to deal
    with specific contexts.

    :param str node:
    :param list sections:
    :return: Node type
    :rtype: str/None
    """
    # match protected keys
    match = PROTECTED_KEYS & set(sections)

    # return protected type
    if match:
        return match.pop()

    # deal with assembly nodes
    # assembly nodes depend on the context, if you are modelling or rigging.
    # for this script not to become to complicated we rely on the user to
    # define these by hand before hand and have them part of the protected
    # keys.
    parent = cmds.listRelatives(node, parent=True)
    if not parent:
        return

    # match tags types
    # get user defined attributes
    attributes = set(cmds.listAttr(node, userDefined=True) or [])

    # find match between known tags
    match = TAG_KEYS & attributes
    match.add(None)

    # get tag type
    tag_type = TAG_MAPPER.get(match.pop())

    # return tag type
    if tag_type:
        return tag_type

    # get node types
    shapes = cmds.listRelatives(node, shapes=True, f=True) or []
    shapes.append(node)

    node_type = cmds.nodeType(shapes[0])
    node_type = TYPE_MAPPER.get(node_type, node_type)

    return node_type


def add_type(node, sections):
    """
    Add the node type to the sections list. It is checked to see if that
    node type string is already part of the section and if that is the case
    it will be moved to the back. If not it will simply be appended.
    :param node:
    :param sections:
    :return:
    """
    # get node type
    t = get_type(node, sections)

    # validate node type
    if not t:
        return sections

    # add node type to sections
    if t in sections:
        order.move_to_last(t, sections)
    else:
        sections.append(t)

    return sections
