from PySide2 import QtWidgets

from shiboken2 import wrapInstance
import maya.OpenMaya
from maya import cmds

from straightenVerticles import stConstants


def getMayaMainWindow():
    """
        Return the Maya main window widget as a Python object
    """
    main_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()

    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def storeMatrix(func):
    def wrapper(*args, **kwargs):
        sel = cmds.ls(selection=True, flatten=True)
        matrix = []
        for v in sel:
            matrix.append({v: cmds.xform(v, query=True, translation=True, worldSpace=True)})
        vmConstants.VERTICLE_MAT.append(matrix)

        result = func(*args, **kwargs)

        return result
    return wrapper


def storeMatPreProcess(func):
    def wrapper(*args, **kwargs):
        vmConstants.VERTICLE_MAT_PRE_PROCESS.clear()
        sel = cmds.ls(selection=True, flatten=True)
        for v in sel:
            vmConstants.VERTICLE_MAT_PRE_PROCESS[v] =  cmds.xform(v, query=True, translation=True, worldSpace=True)

        result = func(*args, **kwargs)

        return result
    return wrapper
