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

    # font file location
    # adjust this path according to the location of this font on your PC
    my_font_file = '/home/paul/FreeCAD models/cups_python/Vera.ttf'

    # export files location
    # this directory should contain four subdirectories named litre, decilitre, centilitre, millilitre
    my_export_dir = u"/home/paul/FreeCAD models/cups_python/"

    # create sketches that will contain the inner and outer circle of the cup
    # the inner circle will form a cylinder with the exact millilitre contents
    # the inner cylinder is later substracted from the outer cylinder to form a cup
    sketch_inner = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_inner")
    sketch_outer = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_outer")
    
    # wall thickness of the solid part of the cups
    if ml < 200:
        wall = 3
    elif ml < 1000:
        wall = 4
    else:
        wall = 5
    
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
    
    # substract inner from outer cylinder, we now have an exact ml cup
    cup = doc.addObject('Part::Cut', "cup")
    cup.Base = cup_outer
    cup.Tool = cup_inner

    # rotate 180 degrees so open end is on top in slicer
    Draft.rotate([doc.cup], 180.0, FreeCAD.Vector(0, 0, 0), axis=FreeCAD.Vector(0, -1, 0), copy=False)

    # Create Shapestring that contains the number of millilitre
    # fontsize is set to half the radius, most numbers will fit the bottom of the cup
    ss=Draft.makeShapeString(String=str(ml),FontFile=my_font_file,Size=(radius/2),Tracking=0.0)
    # Place at the bottom
    # The X-value here is a weak attempt to center the shapestring on the bottom
    # +5 is only significant for the very small cups
    # -radius/1.1 is reasonable for large cups
    ss.Placement = App.Placement(App.Vector(5-(radius/1.1),0,-height),App.Rotation(App.Vector(1,0,0),0))
    ss.Support=None
    Draft.autogroup(ss)

    # Extrude the ShapeString
    # Later this extrude is subtracted from the cup
    # Yes this means the contents is no longer exact, so don't fill the top 0.02mm or something :)
    extrude=doc.addObject('Part::Extrusion','extrude')
    extrude.Base = doc.getObject('ShapeString')
    extrude.LengthFwd = 0.5
    extrude.Placement = App.Placement(App.Vector(0,0,wall-0.5),App.Rotation(App.Vector(1,0,0),0))
    doc.getObject('ShapeString').Visibility = False

    # substract extrude from cup
    mcup = doc.addObject('Part::Cut', "mcup")
    mcup.Base = cup
    mcup.Tool = extrude

    # create rounded cup
    # each cup exists in two versions:
    # 1. mcup with sharp edges
    # 2. fillet with rounded edges
    # the bottom inside is NOT rounded
    doc.addObject("Part::Fillet","fillet")
    doc.fillet.Base = mcup
    __fillets__ = []
    __fillets__.append((2,1.00,1.00))
    __fillets__.append((3,1.00,1.00))
    __fillets__.append((4,1.00,1.00))
    doc.fillet.Edges = __fillets__

    doc.recompute()

    # export .stl files for this sharp mcup and this rounded fillet
    export = []
    export.append(doc.getObject("mcup"))
    Mesh.export(export, my_export_dir + dir_name + "/sharp measuring cup " + cup_name + ".stl")
    export = []
    export.append(doc.getObject("fillet"))
    Mesh.export(export, my_export_dir + dir_name + "/rounded measuring cup " + cup_name + ".stl")

    # remove all objects before the next for loop
    # FreeCAD should be almost empty when this script finishes
    # all cups are saved as .stl files
    doc.removeObject("extrude")
    doc.removeObject("ShapeString")
    doc.removeObject("fillet")
    doc.removeObject("mcup")
    doc.removeObject("cup")
    doc.removeObject("cup_inner")
    doc.removeObject("cup_outer")
    doc.removeObject("sketch_inner")
    doc.removeObject("sketch_outer")

for i in range(25):
    ml = i + 1
    create_cup(ml       , str(ml) + 'ml'                              , 'millilitre')
    create_cup(ml * 10  , str(ml) + 'cl' + '=' + str(ml * 10)   + 'ml', 'centilitre')
    create_cup(ml * 100 , str(ml) + 'dl' + '=' + str(ml * 100)  + 'ml', 'decilitre')
    create_cup(ml * 1000, str(ml) + 'l'  + '=' + str(ml * 1000) + 'ml', 'litre')

# for testing individual cup creation
#create_cup(42, "42ml", "millilitre")

FreeCADGui.ActiveDocument.ActiveView.fitAll()
