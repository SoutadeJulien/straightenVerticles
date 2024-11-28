from maya import cmds

from straightenVerticles import stUtils


def queryTranslates(sel):
    return cmds.xform(sel, query=True, translation=True, worldSpace=True)

def flattenSelection():
    return cmds.ls(selection=True, flatten=True)

def getActiveCamera():
    # Get the active model panel (the viewport that is active)
    active_panel = cmds.getPanel(visiblePanels=True)

    # Check if the panel is a model panel (i.e., a viewport)
    for panel in active_panel:
        if 'modelPanel' in panel:
            # Get the camera associated with the active viewport
            return cmds.modelPanel(panel, query=True, camera=True)
    else:
        return None


def resetLastOperation(verticleMat):
    if not verticleMat:
        return

    cmds.select(clear=True)

    for verticle in verticleMat:
        for vtx, coor in verticle.items():
            cmds.xform(vtx, translation=coor, worldSpace=True)

            cmds.select(vtx, add=True)


def getReferenceVtx(selection, refCenterOfSelection, refRightMostVtx, refLeftMostVtx):
    referenceVtx = None
    if refCenterOfSelection:
        referenceVtx = centerOfSelection(selection)

    if refRightMostVtx:
        referenceVtx = getRightmostVtx(selection)

    if refLeftMostVtx:
        referenceVtx = getLeftmostVtx(selection)

    return referenceVtx


def getRightmostVtx(selection):
    cam = getActiveCamera()

    rightmostVtx = []

    if cam == 'front' or cam == 'top' or cam == 'bottom':
        rightmostVtxX = float('-inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)
            if trans[0] > rightmostVtxX:
                rightmostVtxX = trans[0]
                rightmostVtx = trans

        return rightmostVtx

    elif cam == 'back':
        rightmostVtxX = float('+inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)
            if trans[0] < rightmostVtxX:
                rightmostVtxX = trans[0]
                rightmostVtx = trans

        return rightmostVtx

    elif cam == 'side':
        rightmostVtxX = float('+inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)
            if trans[2] < rightmostVtxX:
                rightmostVtxX = trans[2]
                rightmostVtx = trans

        return rightmostVtx

    else:
        rightmostVtxX = float('-inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)
            if trans[2] > rightmostVtxX:
                rightmostVtxX = trans[2]
                rightmostVtx = trans

        return rightmostVtx



def getLeftmostVtx(selection):
    cam = getActiveCamera()

    if cam == 'front' or cam == 'top' or cam == 'bottom':
        leftmostVtxX = float('+inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)

            if trans[0] < leftmostVtxX:
                leftmostVtxX = trans[0]
                leftmostVtx = trans

        return leftmostVtx

    elif cam == 'back':
        leftmostVtxX = float('-inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)

            if trans[0] > leftmostVtxX:
                leftmostVtxX = trans[0]
                leftmostVtx = trans

        return leftmostVtx

    elif cam == 'side':
        leftmostVtxX = float('-inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)

            if trans[-1] > leftmostVtxX:
                leftmostVtxX = trans[-1]
                leftmostVtx = trans

        return leftmostVtx

    else:
        leftmostVtxX = float('+inf')

        for vtx in selection:
            trans = cmds.xform(vtx, query=True, translation=True, worldSpace=True)

            if trans[2] < leftmostVtxX:
                leftmostVtxX = trans[2]
                leftmostVtx = trans

        return leftmostVtx




def centerOfSelection(sel):
    coor = {}
    for v in sel:
        coor[v] = cmds.xform(v, query=True, translation=True, worldSpace=True)
    numberOfVtx = len(sel)
    x = 0
    y = 0
    z = 0
    for i, trans in coor.items():
        x = x + trans[0]
        y = y + trans[1]
        z = z + trans[2]

    return x / numberOfVtx, y / numberOfVtx, z / numberOfVtx


def createPrevisCurve(spans):
    previsCurve = cmds.curve(name="flattenPrevisCurve", d=1, p=spans)
    cmds.setAttr(previsCurve + '.overrideEnabled', 1)
    cmds.setAttr(previsCurve + '.overrideColor', 14)
    cmds.setAttr(cmds.listRelatives(previsCurve, shapes=True)[0] + '.lineWidth', 5)

    return previsCurve


def deletePrevis():
    if cmds.objExists('flattenGroup') :
        cmds.delete('flattenGroup')


@stUtils.storeMatrix
def flattenVerticesH(selection, refCenterOfSelection, refRightVtx, refLeftVtx):
    if not selection:
        return

    cam = getActiveCamera()
    sel = flattenSelection()
    referenceVtx = getReferenceVtx(selection, refCenterOfSelection, refRightVtx, refLeftVtx)
    print(referenceVtx)

    if cam == 'top' or cam == 'bottom':
        for i in sel:
            oldTrans = queryTranslates(i)
            cmds.select(i)
            cmds.move(oldTrans[0], oldTrans[1], referenceVtx[-1], worldSpace=True)
            cmds.select(clear=True)

    elif cam == 'left' or cam == 'front' or cam == 'side' or cam == 'back':
        for i in sel:
            oldTrans = cmds.xform(i, query=True, translation=True, worldSpace=True)
            cmds.select(i)
            cmds.move(oldTrans[0], referenceVtx[1], oldTrans[-1], worldSpace=True)
            cmds.select(clear=True)
    else:

        print("This tool doesn't work with perspective camera")

    cmds.select(sel)


@stUtils.storeMatrix
def flattenVerticesV(sel, refCenterOfSelection, refRightVtx, refLeftVtx):
    if not sel:
        return

    cam = getActiveCamera()
    referenceVtx = getReferenceVtx(sel, refCenterOfSelection, refRightVtx, refLeftVtx)

    if cam == 'top' or cam == 'front':
        for i in sel:
            oldTrans = queryTranslates(i)
            cmds.select(i)
            cmds.move(referenceVtx[0], oldTrans[1], oldTrans[-1], worldSpace=True)
            cmds.select(clear=True)

    elif cam == 'left' or cam == 'front' or cam == 'side':
        for i in sel:
            oldTrans = queryTranslates(i)
            cmds.select(i)
            cmds.move(oldTrans[0], oldTrans[1], referenceVtx[-1], worldSpace=True)
            cmds.select(clear=True)
    else:
        print("This tool doesn't work with persp camera")

    cmds.select(sel)


def previsHorizontal(selection, refCenterOfSelection, refRightVtx, refLeftVtx):
    if not selection:
        return

    cam = getActiveCamera()

    referenceVtx = getReferenceVtx(selection, refCenterOfSelection, refRightVtx, refLeftVtx)

    allGroup = cmds.createNode('transform', name='flattenGroup')
    spanCoor = []

    if cam == 'top' or cam == 'bottom':
        for i in selection:
            oldTrans = queryTranslates(i)
            spanCoor.append((oldTrans[0], oldTrans[1], referenceVtx[-1]))

    elif cam == 'left' or cam == 'front' or cam == 'side' or cam == 'back':
        for i in selection:
            oldTrans = queryTranslates(i)
            spanCoor.append((oldTrans[0], referenceVtx[1], oldTrans[-1]))

    previsCurve = createPrevisCurve([span for span in spanCoor])
    cmds.parent(previsCurve, allGroup)

    cmds.select(clear=True)
    cmds.select(selection)


def previsVertical(selection, refCenterOfSelection, refRightVtx, refLeftVtx):
    if not selection:
        return

    cam = getActiveCamera()

    referenceVtx = getReferenceVtx(selection, refCenterOfSelection, refRightVtx, refLeftVtx)

    allGroup = cmds.createNode('transform', name='flattenGroup')
    spanCoor = []

    if cam == 'front'or cam == 'back' or cam == 'top' or cam == 'bottom':
        for i in selection:
            oldTrans = queryTranslates(i)
            spanCoor.append((referenceVtx[0], oldTrans[1], oldTrans[-1]))

    elif cam == 'side' or cam == 'left':
        for i in selection:
            oldTrans = queryTranslates(i)
            spanCoor.append((oldTrans[0], oldTrans[1], referenceVtx[-1]))

    previsCurve = createPrevisCurve([span for span in spanCoor])
    cmds.parent(previsCurve, allGroup)

    cmds.select(clear=True)
    cmds.select(selection)


def flattenVerticlesHFine(self, selection, refCenterOfSelection, refRightVtx, refLeftVtx, sliderValue, preProcessMatrix):
    cam = getActiveCamera()

    referenceVtx = getReferenceVtx(selection, refCenterOfSelection, refRightVtx, refLeftVtx)

    if cam == 'top' or cam == 'bottom':
        for vtx, trans in self.tempMat.items():
            cmds.select(vtx)
            range = self.referenceVtx[-1] - trans[-1]
            cmds.move(trans[0], trans[1], trans[-1]+(range/value), worldSpace=True)
            cmds.select(clear=True)

    elif cam == 'left' or cam == 'front' or cam == 'side' or cam == 'back':
        for vtx in selection:
            oldTranslates = preProcessMatrix.get(vtx, None)

            yRange = referenceVtx[1] - oldTranslates[1]
            cmds.select(vtx)
            cmds.move(oldTranslates[0], yRange/(sliderValue/10), oldTranslates[-1], worldSpace=True)
            cmds.select(clear=True)

    else:
        print("This tool doesn't work with persp camera")

    cmds.select(selection)

@stUtils.storeMatrix
def bridgeVertice(selection):
    cam = getActiveCamera()

    u, v = getUvIndex()

    for vtx in selection:
        a = getLeftmostVtx(selection)
        b = getRightmostVtx(selection)

        # Get the coordinates before the vertex has moved.
        p = cmds.xform(vtx, query=True, translation=True, worldSpace=True)

        # Calculate the slope.
        m = (b[v] - a[v]) / (b[u] - a[u])

        # Calculate h, which is the coordinate that the vtx cuts the y coordinate.
        h = a[v] - m * a[u]

        # Calculate the vtx y coordinate.
        axeToMove = m * p[u] + h

        if cam == 'front' or cam == 'side' or cam == 'left':
            cmds.xform(vtx, translation=(p[0], axeToMove, p[2]), worldSpace=True)

        elif cam == 'bottom' or cam == 'top':
            cmds.xform(vtx, translation=(p[0], p[1], axeToMove), worldSpace=True)


def getUvIndex():
    cam = getActiveCamera()

    u = 0
    v = 0

    if cam == 'front':
        u = 0
        v = 1

    elif cam == 'side' or cam == 'left':
        u = 2
        v = 1

    elif cam == 'bottom' or cam == 'top':
        u = 0
        v = 2

    return u, v


def fromLeftToRight(verticleDict):
    cam = getActiveCamera()
    if cam == 'front' or cam == 'top' or cam == 'bottom':
        return dict(sorted(verticleDict.items(), key=lambda item: item[1][0]))

    elif cam == 'back':
        return dict(sorted(verticleDict.items(), key=lambda item: item[1][0]), reverse=True)

    elif cam == 'side':
        return dict(sorted(verticleDict.items(), key=lambda item: item[1][-1]))

    else:
        return dict(sorted(verticleDict.items(), key=lambda item: item[1][2]))


# sel = cmds.ls(selection=True, flatten=True)

# curveCoordinate = {}

# for vtx in sel:
#     curveCoordinate[vtx] = cmds.xform(vtx, query=True, translation=True, worldSpace=True)

# sortedDict = fromLeftToRight(curveCoordinate)

# curve = cmds.curve(name="flattenPrevisCurve", d=3, p=[value for value in sortedDict.values()], bezier=False)
# curveShape = cmds.listRelatives(curve, shapes=True)

# cmds.setAttr(curve + '.overrideEnabled', 1)
# cmds.setAttr(curve + '.overrideColor', 14)

# cmds.select(clear=True)

# allGrp = cmds.createNode('transform', name='ALLGRP_grp'.format(curve))

# rangePercent = (100 / len(sortedDict.keys()) + 1) / 100
# currentPercent = 0

# for index in range(len(sortedDict.keys())):
#     cluster = cmds.cluster(list(sortedDict.keys())[index], name='cvCluster_{}'.format(index))
#     clusterGrp = cmds.createNode('transform', name='clusterGrp_{}'.format(index))
#     cmds.matchTransform(clusterGrp, cluster)
#     cmds.parent(cluster[1], clusterGrp)

#     locator = cmds.createNode('transform', name='vertexLocator_{}'.format(index))

#     pointOnCurve = cmds.createNode('pointOnCurveInfo', name='pointOfCurve_{}'.format(index))
#     cmds.setAttr('{}.turnOnPercentage'.format(pointOnCurve), 1)
#     cmds.connectAttr('{}.worldSpace'.format(curve), '{}.inputCurve'.format(pointOnCurve))
#     cmds.setAttr('{}.parameter'.format(pointOnCurve), currentPercent)
#     cmds.connectAttr('{}.position'.format(pointOnCurve), '{}.translate'.format(locator))

#     cmds.pointConstraint(locator, '{}Handle'.format(cluster[0]), maintainOffset=True)

#     ctrl = cmds.circle(name='{}_{}_ctrl'.format(curve, index))
#     ctrlGroup = cmds.createNode('transform', name='{}_grp'.format(curve))

#     cmds.select(clear=True)
#     cmds.parent(ctrl[0], ctrlGroup)

#     cmds.xform(ctrlGroup, translation=sortedDict[list(sortedDict.keys())[index]], worldSpace=True)
#     cmds.select(clear=True)

#     decomposeMat = cmds.createNode('decomposeMatrix', name='ctrlMat_{}'.format(index))
#     cmds.connectAttr('{}.worldMatrix'.format(ctrl[0]), '{}.inputMatrix'.format(decomposeMat))
#     cmds.connectAttr('{}.outputTranslate'.format(decomposeMat), '{}.controlPoints[{}]'.format(curveShape[0], index))

#     cmds.parent(clusterGrp, allGrp)
#     cmds.parent(locator, allGrp)
#     cmds.parent(ctrlGroup, allGrp)

#     currentPercent = currentPercent + rangePercent
