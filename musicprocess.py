from krita import *


def musicFilter():
    application = Krita.instance()
    currentDoc = application.activeDocument()
    if not currentDoc:
        print("No active document!")
        return

    activeLayer = currentDoc.activeNode()
    if not activeLayer or activeLayer.type() != "paintlayer":
        print("Select a paint layer first!")
        return

    canvasWidth = currentDoc.width()
    canvasHeight = currentDoc.height()
    activeLayer.scaleNode(QPoint(0,0), canvasWidth, canvasHeight, "Bicubic")
    layerBounds = currentDoc.activeNode()
    layerX = activeLayer.position().x()
    layerY = activeLayer.position().y()
    realBounds = layerBounds.bounds()
    absoluteX = realBounds.x()
    absoluteY = realBounds.y()
    movementX = (-1 * (absoluteX)) + (layerX)
    movementY = (-1 * (absoluteY)) + (layerY)
    activeLayer.move(movementX,movementY)
    currentDoc.activeNode()
    currentDoc.refreshProjection()
musicFilter()