from functools import partial

from PySide2 import QtWidgets, QtCore

from straightenVerticles import stWidgets
from straightenVerticles import stCore
from straightenVerticles import stConstants
from straightenVerticles import stUtils


class Main(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.verticleMat = []
        self.referenceVtx = None
        self.tempMat = {}

        self._buildUi()
        self._setupUi()
        self._connectUi()

    def _buildUi(self):
        # Buttons.
        self.resetButton = QtWidgets.QPushButton("Reset last operation [{}]".format(len(stConstants.VERTICLE_MAT)))
        self.storeVertices = QtWidgets.QPushButton("Select vertices")

        # CheckBoxes.
        self.previsCheck = QtWidgets.QCheckBox("Visualisation")
        self.onHitCheck = QtWidgets.QCheckBox("On hit")

        # Layouts.
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # Widgets.
        self.onHitWidget = stWidgets.OnHitWidget()

    def _setupUi(self):
        self.setWindowTitle('Straighten verticles')
        self.mainLayout.addWidget(self.previsCheck)
        self.mainLayout.addWidget(self.onHitCheck)

        self.mainLayout.addWidget(self.onHitWidget)

        self.mainLayout.addWidget(self.resetButton)

        self.resetButton.setStyleSheet("color: black; background-color: rgb(240, 50, 50);")

        self.onHitCheck.setChecked(True)

        self.resize(200, 100)

    def _connectUi(self):
        self.onHitCheck.stateChanged.connect(self.updateOnHitEnabled)
        self.previsCheck.stateChanged.connect(self.onHitWidget.updatePrevis)
        self.storeVertices.clicked.connect(self.onStoreVerticesClicked)
        self.resetButton.clicked.connect(self.resetLastOperation)
        self.onHitWidget.updateCancelCount.connect(self.updateCancelCount)

    @stUtils.storeMatPreProcess
    def onStoreVerticesClicked(self):
        self.verticesLineEdit.setText(' | '.join(stCore.flattenSelection()))

    def updateOnHitEnabled(self, state):
        self.onHitWidget.setEnabled(state)

    @QtCore.Slot(None)
    def updateCancelCount(self):
        self.resetButton.setText("Reset last operation [{}]".format(len(stConstants.VERTICLE_MAT)))

    def resetLastOperation(self):
        if not stConstants.VERTICLE_MAT:
            return
        stCore.resetLastOperation(stConstants.VERTICLE_MAT.pop(-1))
        self.updateCancelCount()

