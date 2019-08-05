from maya import cmds
from functools import wraps


def preserve_selection(func):
    """
    The preserve selection decorator will store the maya selection before the
    function is called. There are many functions to Maya's native cmds that
    alter the selection. After the function is called the original selection
    shall be made.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # store selection
        sel = cmds.ls(sl=True)

        # call function
        ret = func(*args, **kwargs)

        # redo selection
        if sel:
            cmds.select(sel)
        else:
            cmds.select(clear=True)

        return ret

    return wrapper
