from maya import cmds
from . import path


ATTRIBUTE_MAPPER = {
    "show": {"cb": True},
    "hide": {"cb": False, "k": False},
    "lock": {"lock": True},
    "unlock": {"lock": False},
    "animatable": {"k": True},
    "not-animatable": {"k": False}
}


DISPLAY_MAPPER = {
    "normal": 0,
    "template": 1,
    "reference": 2
}


def validate_attribute(node, attr):
    """
    :param str node:
    :param str attr:
    :return: Plug
    :rtype: str/None
    """
    plug = "{}.{}".format(node, attr)
    return plug if cmds.objExists(plug) else None


def edit_attributes(node, attr=None, mode=None):
    """
    Adjust attribute values and display attributes on a node. Attributes can
    be added as a group and the X, Y, Z channels will automatically be added.
    
    Valid groups:
    * translate
    * rotate
    * scale
    
    Valid modes ( modify attributes ):
    * lock
    * unlock
    * hide
    * show
    * animatable
    * not-animatable
    
    Valid modes ( modify display ):
    * normal
    * template
    * reference
    
    :param str node:
    :param str/list attr:
    :param str/list mode:
    """
    # force list
    attr = path.as_list(attr)
    mode = path.as_list(mode)

    # add channels to attribute list if children are present
    for a in attr[:]:
        children = cmds.attributeQuery(a, node=node, listChildren=True)
        if children:
            attr.remove(a)
            attr.extend(children)

    for m in mode:
        # edit attributes
        if m in ATTRIBUTE_MAPPER.keys():
            for a in attr:
                cmds.setAttr(
                    "{0}.{1}".format(node, a), 
                    **ATTRIBUTE_MAPPER.get(m)
                )

        # edit display
        if m in DISPLAY_MAPPER.keys():
            cmds.setAttr("{0}.overrideEnabled".format(node), 1)
            cmds.setAttr(
                "{0}.overrideDisplayType".format(node), 
                DISPLAY_MAPPER.get(m)
            )
