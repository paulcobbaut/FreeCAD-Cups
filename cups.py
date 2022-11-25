"""
cups.py
Paul Cobbaut, 2022-11-25
Some FreeCAD scripting
The goal is to make measuring cups
"""

import FreeCAD
from FreeCAD import Base, Vector
#import Arch
#import Draft
import Part
import Sketcher
#import importSVG
#import BOPTools
#import BOPTools.JoinFeatures
import math

# FreeCAD document
doc = FreeCAD.newDocument("Cups")
obj = doc.addObject("PartDesign::Body", "Body")

# create a sketch with dovetails and pockets that will be padded later
sketch_inner = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_inner")
sketch_outer = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_outer")

# thickness of the solid part of the cups
wall = 4

# 1000ml cup
radius = 10 * math.pow(1000/(2*math.pi),1/3)
height = 2 * radius
doc.getObject('sketch_inner').addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),radius),False)
cup_inner = doc.getObject('Body').newObject("PartDesign::Pad", "cup_inner")
cup_inner.Profile = doc.getObject("sketch_inner")
cup_inner.Length = height

radius = radius + wall
height = height + wall
doc.getObject('sketch_outer').addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),radius),False)
cup_outer = doc.getObject('Body').newObject("PartDesign::Pad", "cup_outer")
cup_outer.Profile = doc.getObject("sketch_outer")
cup_outer.Length = height

cup = doc.addObject('Part::Cut', "cup")
cup.Base = cup_outer
cup.Tool = cup_inner
cup_outer.ViewObject.hide()
cup_inner.ViewObject.hide()


doc.recompute()

FreeCADGui.ActiveDocument.ActiveView.fitAll()
