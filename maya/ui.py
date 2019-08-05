import os
from maya import OpenMayaUI
from Qt import QtWidgets, QtCompat


def get_maya_main_window():
    """
    Find Maya's main Window
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = QtCompat.wrapInstance(long(window), QtWidgets.QMainWindow)

    return window


def get_icon_path(name):
    """
    Get an icon path based on file name. All paths in the XBMLANGPATH variable
    processed to see if the provided icon can be found.

    :param str name:
    :return: Icon path
    :rtype: str/None
    """
    # get paths
    paths = os.environ.get("XBMLANGPATH")

    # validate paths
    if not paths:
        return

    # loop paths
    for path in paths.split(os.pathsep):
        icon_path = os.path.join(path, name)
        if os.path.exists(icon_path):
            return icon_path.replace("\\", "/")
