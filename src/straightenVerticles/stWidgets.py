from PySide2 import QtWidgets, QtCore, QtGui

from straightenVerticles import stCore

class PushButton(QtWidgets.QPushButton):

    onHover = QtCore.Signal()
    offHover = QtCore.Signal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def enterEvent(self, event):
        self.onHover.emit()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.offHover.emit()
        super().leaveEvent(event)


class OnHitWidget(QtWidgets.QWidget):

    updateCancelCount = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.previs = False

        self._buildUi()
        self._setupUi()
        self._connectUi()

    def _buildUi(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.rGroupLayout = QtWidgets.QHBoxLayout()

        self.hButton = PushButton('Horizontal')
        self.vButton = PushButton('Vertical')
        self.bridgeButton = PushButton('Bridge')

        self.centerOfSelectionCb = QtWidgets.QRadioButton("Center of selection")
        self.rightCb = QtWidgets.QRadioButton("The rightmost vertex")
        self.leftCb = QtWidgets.QRadioButton("The leftmost vertex")

        self.rGroup = QtWidgets.QGroupBox()

    def _setupUi(self):
        self.rGroupLayout.addWidget(self.centerOfSelectionCb)
        self.rGroupLayout.addWidget(self.rightCb)
        self.rGroupLayout.addWidget(self.leftCb)

        self.mainLayout.addLayout(self.rGroupLayout)

        self.mainLayout.addWidget(self.hButton)
        self.mainLayout.addWidget(self.vButton)
        self.mainLayout.addWidget(self.bridgeButton)

        self.rGroup.setTitle("Straiten on: ")
        self.centerOfSelectionCb.setChecked(True)
        self.centerOfSelectionCb.setChecked(True)

    def _connectUi(self):
        self.hButton.onHover.connect(self.hButtonHover)
        self.hButton.offHover.connect(stCore.deletePrevis)
        self.vButton.onHover.connect(self.vButtonHover)
        self.vButton.offHover.connect(stCore.deletePrevis)
        self.hButton.clicked.connect(self.onHButtonClicked)
        self.vButton.clicked.connect(self.onVButtonClicked)
        self.bridgeButton.clicked.connect(self.onBrigeButtonClicked)

    def onHButtonClicked(self):
        stCore.flattenVerticesH(
            stCore.flattenSelection(),
            self.centerOfSelectionCb.isChecked(),
            self.rightCb.isChecked(),
            self.leftCb.isChecked()
        )
        self.updateCancelCount.emit()

    def onVButtonClicked(self):
        stCore.flattenVerticesV(
            stCore.flattenSelection(),
            self.centerOfSelectionCb.isChecked(),
            self.rightCb.isChecked(),
            self.leftCb.isChecked()
        )
        self.updateCancelCount.emit()

    def hButtonHover(self):
        if not self.previs:
            return

        stCore.previsHorizontal(stCore.flattenSelection(),
                                self.centerOfSelectionCb.isChecked(),
                                self.rightCb.isChecked(),
                                self.leftCb.isChecked()
                                )

    def vButtonHover(self):
        if not self.previs:
            return

        stCore.previsVertical(stCore.flattenSelection(),
                                self.centerOfSelectionCb.isChecked(),
                                self.rightCb.isChecked(),
                                self.leftCb.isChecked()
                                )

    def onBrigeButtonClicked(self):
        stCore.bridgeVertice(
            stCore.flattenSelection()
        )

        self.updateCancelCount.emit()

    def updatePrevis(self, state):
        self.previs = state


class FineTuningWidget(QtWidgets.QWidget):

    updateCancelCount = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.previs = False

        self._buildUi()
        self._setupUi()
        self._connectUi()

    def _buildUi(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # Labels.
        self.horizontalSliderLabel = QtWidgets.QLabel("Horizontal")
        self.verticalSliderLabel = QtWidgets.QLabel("Vertical")
        self.storeVertices = QtWidgets.QPushButton("Select vertices")

        self.horizontalSliderLabel = QtWidgets.QLabel("Horizontal")

        self.verticalSliderLabel = QtWidgets.QLabel("Vertical")
        # Line edit.
        self.verticesLineEdit = QtWidgets.QLineEdit()
        # Sliders.
        self.horizontalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.verticalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

    def _setupUi(self):
        self.mainLayout.addWidget(self.storeVertices)
        self.mainLayout.addWidget(self.verticesLineEdit)
        self.mainLayout.addWidget(self.horizontalSliderLabel)
        self.mainLayout.addWidget(self.horizontalSlider)

        self.mainLayout.addWidget(self.verticalSliderLabel)
        self.mainLayout.addWidget(self.verticalSlider)
        self.verticesLineEdit.setReadOnly(True)


        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(10)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(10)

    def _connectUi(self):
        self.horizontalSlider.valueChanged.connect(self.onHSliderValueChanged)

    @QtCore.Slot(int, None)
    def onHSliderValueChanged(self, value):
        stCore.flattenVerticlesHFine(stCore.flattenSelection(),
                                     self.centerOfSelectionCb.isChecked(),
                                     self.rightCb.isChecked(),
                                     self.leftCb.isChecked(),
                                     value,
                                     stConstants.VERTICLE_MAT_PRE_PROCESS,
                                     )

    def onHSliderReleased(self):
        self.tempMat.clear()