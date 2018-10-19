"""
Copyright (c) 2018 Daniel J. Swearson

"""

__author__= 'Daniel J. Swearson'
__doc__ = 'Filters specific elements in the current view.'
__window__.Close()

from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInCategory, Group, ElementId, Wall, \
                              Dimension
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ISelectionFilter

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

import clr
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReferenceByPartialName('WindowsBase')
import System.Windows

class commandSwitches:
    def __init__(self, switches, message = 'Pick a command option:'):
        # Create window
        self.my_window = System.Windows.Window()
        self.my_window.WindowStyle = System.Windows.WindowStyle.None
        self.my_window.AllowsTransparency = True
        self.my_window.Background = None
        self.my_window.Title = 'Command Options'
        self.my_window.Width = 450
        self.my_window.SizeToContent = System.Windows.SizeToContent.Height
        self.my_window.ResizeMode = System.Windows.ResizeMode.CanMinimize
        self.my_window.WindowStartupLocation = System.Windows.WindowStartupLocation.CenterScreen
        self.my_window.PreviewKeyDown += self.handleEsc
        border = System.Windows.Controls.Border()
        border.CornerRadius  = System.Windows.CornerRadius(15)
        border.Background = System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromArgb(220,55,50,50))
        self.my_window.Content = border

        # Create StackPanel to Layout UI elements
        stack_panel = System.Windows.Controls.StackPanel()
        stack_panel.Margin = System.Windows.Thickness(5)
        border.Child = stack_panel

        label = System.Windows.Controls.Label()
        label.Foreground = System.Windows.Media.Brushes.White
        label.Content = message
        label.Margin = System.Windows.Thickness(2, 0, 0, 0)
        stack_panel.Children.Add(label)

        # Create WrapPanel for command options
        self.button_list = System.Windows.Controls.WrapPanel()
        self.button_list.Margin = System.Windows.Thickness(5)
        stack_panel.Children.Add(self.button_list)

        for switch in switches:
            my_button = System.Windows.Controls.Button()
            my_button.BorderBrush = System.Windows.Media.Brushes.Black
            my_button.BorderThickness = System.Windows.Thickness(0)
            my_button.Content = switch
            my_button.Margin = System.Windows.Thickness(5, 0, 5, 5)
            my_button.Padding = System.Windows.Thickness(5, 0, 5, 0)
            my_button.Click += self.processSwitch
            self.button_list.Children.Add(my_button)


    def handleEsc(self, sender, args):
        if (args.Key == System.Windows.Input.Key.Escape):
            self.my_window.Close()


    def processSwitch(self, sender, args):
        self.my_window.Close()
        global selected_switch
        selected_switch = sender.Content

    def pickCommandSwitch(self):
        self.my_window.ShowDialog()
        
class PickByCategorySelectionFilter(ISelectionFilter):
    def __init__(self, catname):
        self.category = catname

    # standard API override function
    def AllowElement(self, element):
        if self.category in element.Category.Name:
            return True
        else:
            return False

    # standard API override function
    def AllowReference(self, refer, point):
        return False


def pickbycategory(catname):
    try:
        sel = PickByCategorySelectionFilter(catname)
        sellist = uidoc.Selection.PickElementsByRectangle(sel)
        filteredlist = []
        for el in sellist:
            filteredlist.append(el.Id)
        uidoc.Selection.SetElementIds(List[ElementId](filteredlist))
    except:
        pass
    
class CommandSwitchWindow:
    def __init__(self, switches, message='Pick a command option:'):
        self.Parent = self
        self.selected_switch = ''
        # Create window
        self.my_window = System.Windows.Window()
        self.my_window.WindowStyle = System.Windows.WindowStyle.None
        self.my_window.AllowsTransparency = True
        self.my_window.Background = None
        self.my_window.Title = 'Command Options'
        self.my_window.Width = 450
        self.my_window.SizeToContent = System.Windows.SizeToContent.Height
        self.my_window.ResizeMode = System.Windows.ResizeMode.CanMinimize
        self.my_window.WindowStartupLocation = System.Windows.WindowStartupLocation.CenterScreen
        self.my_window.PreviewKeyDown += self.handle_esc_key
        self.my_window.MouseUp += self.handle_click
        border = System.Windows.Controls.Border()
        border.CornerRadius = System.Windows.CornerRadius(15)
        border.Background = System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromArgb(220, 55, 50, 50))
        self.my_window.Content = border

        # Create StackPanel to Layout UI elements
        stack_panel = System.Windows.Controls.StackPanel()
        stack_panel.Margin = System.Windows.Thickness(5)
        border.Child = stack_panel

        label = System.Windows.Controls.Label()
        label.Foreground = System.Windows.Media.Brushes.White
        label.Content = message
        label.Margin = System.Windows.Thickness(2, 0, 0, 0)
        stack_panel.Children.Add(label)

        # Create WrapPanel for command options
        self.button_list = System.Windows.Controls.WrapPanel()
        self.button_list.Margin = System.Windows.Thickness(5)
        stack_panel.Children.Add(self.button_list)

        for switch in switches:
            my_button = System.Windows.Controls.Button()
            my_button.BorderBrush = System.Windows.Media.Brushes.Black
            my_button.BorderThickness = System.Windows.Thickness(0)
            my_button.Content = switch
            my_button.Margin = System.Windows.Thickness(5, 0, 5, 5)
            my_button.Padding = System.Windows.Thickness(5, 0, 5, 0)
            my_button.Click += self.process_switch
            self.button_list.Children.Add(my_button)

    # noinspection PyUnusedLocal
    def handle_click(self, sender, args):
        self.my_window.Close()

    # noinspection PyUnusedLocal+-
    def handle_esc_key(self, sender, args):
        if args.Key == System.Windows.Input.Key.Escape:
            self.my_window.Close()

    # noinspection PyUnusedLocal
    def process_switch(self, sender, args):
        self.my_window.Close()
        self.selected_switch = sender.Content

    def pick_cmd_switch(self):
        self.my_window.ShowDialog()
        return self.selected_switch

# Replace element type with preferred System Category Names

"""Adaptive Points
Air Terminal Tags
Air Terminals
Analysis Display Style
Analysis Results
Analytical Beam Tags
Analytical Beams
Analytical Brace Tags
Analytical Braces
Analytical Column Tags
Analytical Columns
Analytical Floor Tags
Analytical Floors
Analytical Foundation Slabs
Analytical Isolated Foundation Tags
Analytical Isolated Foundations
Analytical Link Tags
Analytical Links
Analytical Node Tags
Analytical Nodes
Analytical Slab Foundation Tags
Analytical Spaces
Analytical Surfaces
Analytical Wall Foundation Tags
Analytical Wall Foundations
Analytical Wall Tags
Analytical Walls
Annotation Crop Boundary
Area Load Tags
Area Tags
Areas
Assemblies
Assembly Tags
Boundary Conditions
Brace in Plan View Symbols
Cable Tray Fitting Tags
Cable Tray Fittings
Cable Tray Runs
Cable Tray Tags
Cable Trays
Callout Boundary
Callout Heads
Callouts
Cameras
Casework
Casework Tags
Ceiling Tags
Ceilings
Color Fill Legends
Columns
Communication Device Tags
Communication Devices
Conduit Fitting Tags
Conduit Fittings
Conduit Runs
Conduit Tags
Conduits
Connection Symbols
Contour Labels
Crop Boundaries
Curtain Grids
Curtain Panel Tags
Curtain Panels
Curtain System Tags
Curtain Systems
Curtain Wall Mullions
Data Device Tags
Data Devices
Detail Item Tags
Detail Items
Dimensions
Displacement Path
Door Tags
Doors
Duct Accessories
Duct Accessory Tags
Duct Color Fill
Duct Color Fill Legends
Duct Fitting Tags
Duct Fittings
Duct Insulation Tags
Duct Insulations
Duct Lining Tags
Duct Linings
Duct Placeholders
Duct Systems
Duct Tags
Ducts
Electrical Circuits
Electrical Equipment
Electrical Equipment Tags
Electrical Fixture Tags
Electrical Fixtures
Electrical Spare/Space Circuits
Elevation Marks
Elevations
Entourage
Filled region
Fire Alarm Device Tags
Fire Alarm Devices
Flex Duct Tags
Flex Ducts
Flex Pipe Tags
Flex Pipes
Floor Tags
Floors
Foundation Span Direction Symbol
Furniture
Furniture System Tags
Furniture Systems
Furniture Tags
Generic Annotations
Generic Model Tags
Generic Models
Grid Heads
Grids
Guide Grid
HVAC Zones
Imports in Families
Internal Area Load Tags
Internal Line Load Tags
Internal Point Load Tags
Keynote Tags
Level Heads
Levels
Lighting Device Tags
Lighting Devices
Lighting Fixture Tags
Lighting Fixtures
Line Load Tags
Lines
Masking Region
Mass
Mass Floor Tags
Mass Tags
Matchline
Material Tags
Materials
Mechanical Equipment
Mechanical Equipment Tags
MEP Fabrication Containment
MEP Fabrication Containment Tags
MEP Fabrication Ductwork
MEP Fabrication Ductwork Tags
MEP Fabrication Hanger Tags
MEP Fabrication Hangers
MEP Fabrication Pipework
MEP Fabrication Pipework Tags
Multi-Category Tags
Multi-Rebar Annotations
Nurse Call Device Tags
Nurse Call Devices
Panel Schedule Graphics
Parking
Parking Tags
Part Tags
Parts
Pipe Accessories
Pipe Accessory Tags
Pipe Color Fill
Pipe Color Fill Legends
Pipe Fitting Tags
Pipe Fittings
Pipe Insulation Tags
Pipe Insulations
Pipe Placeholders
Pipe Segments
Pipe Tags
Pipes
Piping Systems
Plan Region
Planting
Planting Tags
Plumbing Fixture Tags
Plumbing Fixtures
Point Clouds
Point Load Tags
Project Information
Property Line Segment Tags
Property Tags
Railing Tags
Railings
Ramps
Raster Images
Rebar Cover References
Rebar Set Toggle
Rebar Shape
Reference Lines
Reference Planes
Reference Points
Render Regions
Revision Cloud Tags
Revision Clouds
Roads
Roof Tags
Roofs
Room Tags
Rooms
Routing Preferences
Schedule Graphics
Scope Boxes
Section Boxes
Section Line
Section Marks
Sections
Security Device Tags
Security Devices
Shaft Openings
Sheets
Site
Site Tags
Space Tags
Spaces
Span Direction Symbol
Specialty Equipment
Specialty Equipment Tags
Spot Coordinates
Spot Elevation Symbols
Spot Elevations
Spot Slopes
Sprinkler Tags
Sprinklers
Stair Landing Tags
Stair Paths
Stair Run Tags
Stair Support Tags
Stair Tags
Stair Tread/Riser Numbers
Stairs
Structural Annotations
Structural Area Reinforcement
Structural Area Reinforcement Symbols
Structural Area Reinforcement Tags
Structural Beam System Tags
Structural Beam Systems
Structural Column Tags
Structural Columns
Structural Connection Tags
Structural Connections
Structural Fabric Areas
Structural Fabric Reinforcement
Structural Fabric Reinforcement Symbols
Structural Fabric Reinforcement Tags
Structural Foundation Tags
Structural Foundations
Structural Framing
Structural Framing Tags
Structural Internal Loads
Structural Load Cases
Structural Loads
Structural Path Reinforcement
Structural Path Reinforcement Symbols
Structural Path Reinforcement Tags
Structural Rebar
Structural Rebar Coupler Tags
Structural Rebar Couplers
Structural Rebar Tags
Structural Stiffener Tags
Structural Stiffeners
Structural Truss Tags
Structural Trusses
Switch System
Telephone Device Tags
Telephone Devices
Text Notes
Title Blocks
Topography
View Reference
View Titles
Viewports
Views
Wall Tags
Walls
Window Tags
Windows
Wire Tags
Wires
Zone Tags
"""

selected_switch = CommandSwitchWindow(sorted(['Structural Columns',
                                              'Structural Framing',
                                              'Structural Beam Systems',
                                              'Structural Foundations',
                                              'Stairs',
                                              'Railings',
                                              'Floors',
                                              'Roofs',
                                              'Walls', ]), 'Select element type:').pick_cmd_switch()

if selected_switch is not '':
    pickbycategory(selected_switch)

    t = Transaction(doc, 'Isolate {}'.format(selected_switch))
    t.Start()

    t.Commit()
