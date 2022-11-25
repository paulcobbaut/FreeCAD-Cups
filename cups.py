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


def create_cup(ml, cup_name):

    # create a sketch with dovetails and pockets that will be padded later
    sketch_inner = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_inner")
    sketch_outer = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_outer")
    
    # thickness of the solid part of the cups
    wall = 4
    
    # 1000ml cup
    radius = 10 * math.pow(ml/(2*math.pi),1/3)
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
    doc.recompute()

    Draft.rotate([doc.cup], 180.0, FreeCAD.Vector(0, 0, 0), axis=FreeCAD.Vector(0, -1, 0), copy=False)

    doc.addObject("Part::Fillet","fillet")
    doc.fillet.Base = cup 
    __fillets__ = []
    __fillets__.append((2,1.00,1.00))
    __fillets__.append((3,1.00,1.00))
    __fillets__.append((4,1.00,1.00))
    doc.fillet.Edges = __fillets__

    doc.recompute()
    export = []
    export.append(doc.getObject("cup"))
    Mesh.export(export, u"/home/paul/FreeCAD models/cups_python/sharp/sharp " + cup_name + ".stl")
    export = []
    export.append(doc.getObject("fillet"))
    Mesh.export(export, u"/home/paul/FreeCAD models/cups_python/rounded/rounded " + cup_name + ".stl")

    doc.removeObject("fillet")
    doc.removeObject("cup")
    doc.removeObject("cup_inner")
    doc.removeObject("cup_outer")
    doc.removeObject("sketch_inner")
    doc.removeObject("sketch_outer")



create_cup(2000, "two liter")
create_cup(1000, "one liter")
create_cup(900, "900 ml")
create_cup(800, "800 ml")
create_cup(750, "750 ml")
create_cup(700, "700 ml")
create_cup(600, "600 ml")
create_cup(500, "500 ml")
create_cup(400, "400 ml")
create_cup(300, "300 ml")
create_cup(250, "250 ml")
create_cup(200, "200 ml")
create_cup(150, "150 ml")
create_cup(100, "100 ml")
create_cup(90, "90 ml")
create_cup(80, "80 ml")
create_cup(75, "75 ml")
create_cup(70, "70 ml")
create_cup(60, "60 ml")
create_cup(50, "50 ml")
create_cup(25, "25 ml")
create_cup(20, "20 ml")
create_cup(10, "10 ml")
create_cup(5, "5 ml")
create_cup(1, "1 ml")




FreeCADGui.ActiveDocument.ActiveView.fitAll()
