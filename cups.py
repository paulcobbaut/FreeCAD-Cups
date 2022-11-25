"""
cups.py
Paul Cobbaut, 2022-11-25
Some FreeCAD scripting
The goal is to make measuring cups
"""

import FreeCAD
from FreeCAD import Base, Vector
import Draft
import Part
import Sketcher
import math

# FreeCAD document
doc = FreeCAD.newDocument("Cups")
obj = doc.addObject("PartDesign::Body", "Body")


def create_cup(ml, cup_name, dir_name):

    # create sketches that will contain the inner and outer circle of the cup
    sketch_inner = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_inner")
    sketch_outer = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_outer")
    
    # thickness of the solid part of the cups
    wall = 4
    
    # create inner cylinder
    radius = 10 * math.pow(ml/(2*math.pi),1/3)
    height = 2 * radius
    doc.getObject('sketch_inner').addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),radius),False)
    cup_inner = doc.getObject('Body').newObject("PartDesign::Pad", "cup_inner")
    cup_inner.Profile = doc.getObject("sketch_inner")
    cup_inner.Length = height
    
    # create outer cylinder
    radius = radius + wall
    height = height + wall
    doc.getObject('sketch_outer').addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),radius),False)
    cup_outer = doc.getObject('Body').newObject("PartDesign::Pad", "cup_outer")
    cup_outer.Profile = doc.getObject("sketch_outer")
    cup_outer.Length = height
    
    # substract inner from outer cylinder
    cup = doc.addObject('Part::Cut', "cup")
    cup.Base = cup_outer
    cup.Tool = cup_inner

    # rotate 180 degrees so open end is on top in slicer
    Draft.rotate([doc.cup], 180.0, FreeCAD.Vector(0, 0, 0), axis=FreeCAD.Vector(0, -1, 0), copy=False)

    # create rounded cup
    doc.addObject("Part::Fillet","fillet")
    doc.fillet.Base = cup 
    __fillets__ = []
    __fillets__.append((2,1.00,1.00))
    __fillets__.append((3,1.00,1.00))
    __fillets__.append((4,1.00,1.00))
    doc.fillet.Edges = __fillets__

    doc.recompute()

    # export .stl files for this cup and this rounded cup
    export = []
    export.append(doc.getObject("cup"))
    Mesh.export(export, u"/home/paul/FreeCAD models/cups_python/" + dir_name + "/sharp measuring cup " + cup_name + ".stl")
    export = []
    export.append(doc.getObject("fillet"))
    Mesh.export(export, u"/home/paul/FreeCAD models/cups_python/" + dir_name + "/rounded measuring cup " + cup_name + ".stl")

    # remove all objects
    doc.removeObject("fillet")
    doc.removeObject("cup")
    doc.removeObject("cup_inner")
    doc.removeObject("cup_outer")
    doc.removeObject("sketch_inner")
    doc.removeObject("sketch_outer")


for i in range(25):
    ml = i + 1
    create_cup(ml       , str(ml) + 'ml' + '=' + str(ml)        + 'ml', 'millilitre')
    create_cup(ml * 10  , str(ml) + 'cl' + '=' + str(ml * 10)   + 'ml', 'centilitre')
    create_cup(ml * 100 , str(ml) + 'dl' + '=' + str(ml * 100)  + 'ml', 'decilitre')
    create_cup(ml * 1000, str(ml) + 'l'  + '=' + str(ml * 1000) + 'ml', 'litre')


FreeCADGui.ActiveDocument.ActiveView.fitAll()
