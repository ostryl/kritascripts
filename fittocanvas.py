import sys
import re
from krita import *
from pathlib import Path
import xml.etree.ElementTree as ET

currentDir = Path(__file__).parent.resolve()

if str(currentDir) not in sys.path:
    sys.path.append(str(currentDir))

application = Krita.instance()
currentDoc = application.activeDocument()
activeLayer = currentDoc.activeNode()
canvasWidth = currentDoc.width()
canvasHeight = currentDoc.height()

def fillCanvas():
    if not currentDoc:
        print("No active document!")
        return
    if not activeLayer or activeLayer.type() != "paintlayer":
        print("Select a paint layer first!")
        return
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
    duplicatedLayer = activeLayer.duplicate()
    duplicatedLayer.setName(activeLayer.name() + " - Copy")
    parentLayer = activeLayer.parentNode()
    parentLayer.addChildNode(duplicatedLayer, activeLayer)

def filterLayerOilpaint():
    oilpaintFilter = application.filter('oilpaint')
    oilpaintFilterConfig = oilpaintFilter.configuration()

    # show available properties you can modify

    # update a couple of the properties
    oilpaintFilterConfig.setProperty('brushsize', 5)
    oilpaintFilterConfig.setProperty('smooth', 30)
    oilpaintFilter.setConfiguration(oilpaintFilterConfig)
    oilpaintFilter.apply(activeLayer, 0, 0, currentDoc.width(), currentDoc.height())


def parseXMLFilter():

    xmlPath = currentDir / "imageedit.xml"
    try:
        tree = ET.parse(str(xmlPath))
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Error: Could not find the file at {xmlPath}")

    for param in root.findall('.//param'):
        
        prop_name = param.get('name')
        
        prop_value = param.text 

        clean_value = re.sub(r'\s+', ' ', prop_value).strip()


        if prop_name and clean_value:
            print(f"halftoneFilterConfig.setProperty('{prop_name}', '{clean_value}')")




fillCanvas()
copyLayer()
filterLayerOilpaint()
parseXMLFilter()