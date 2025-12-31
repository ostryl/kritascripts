
import sys
from krita import *
from imagefilter import *
from pathlib import Path

currentDir = Path(__file__).parent.resolve()

if str(currentDir) not in sys.path:
    sys.path.append(str(currentDir))

application = Krita.instance()
currentDoc = application.activeDocument()
activeLayer = currentDoc.activeNode()

def musicFilter():
    if not currentDoc:
        print("No active document!")
        return
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

def copyLayer():
    duplicateLayer = activeLayer.duplicate()
    parentLayer = activeLayer.parentNode()
    parentLayer.addChildNode(duplicateLayer, activeLayer)


musicFilter()
copyLayer()
filterLayer()