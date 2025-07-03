#! python3

import System
import System.Collections.Generic

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import os

def export_selected_as_dxf():
    # Step 1: Select objects
    guids = rs.GetObjects("Select geometry to export as DXF", preselect=True)
    if not guids:
        print("No geometry selected.")
        return

    # Step 2: Choose export directory
    folder = rs.BrowseForFolder(message="Choose export folder")
    if not folder:
        print("No folder selected.")
        return

    # Step 3: Specify the DXF export scheme name
    # This name must match a saved scheme from Rhino's DXF export options
    dxf_scheme = "R12 Natural"  # Replace with your desired scheme name

    # Step 4: Export each object
    for guid in guids:
        rs.UnselectAllObjects()
        rs.SelectObject(guid)

        name = rs.ObjectName(guid)
        if not name:
            name = str(guid)
        filename = os.path.join(folder, "{}.dxf".format(name))

        # Use the DXF scheme in the command
        command = '-_Export "{}" _Scheme "{}" _Enter'.format(filename, dxf_scheme)

        rs.Command(command, echo=False)
        print("Exported: {}".format(filename))

    print("Done exporting all selected objects.")

export_selected_as_dxf()

