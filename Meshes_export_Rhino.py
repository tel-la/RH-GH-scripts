import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import os

def export_selected_as_stl():
    # Step 1: Select objects
    guids = rs.GetObjects("Select geometry to export as STL", preselect=True)
    if not guids:
        print("No geometry selected.")
        return

    # Step 2: Choose export directory
    folder = rs.BrowseForFolder(message="Choose export folder")
    if not folder:
        print("No folder selected.")
        return

    # Step 3: Export each object
    for guid in guids:
        # Deselect all first
        rs.UnselectAllObjects()
        
        # Select current object
        rs.SelectObject(guid)

        # Generate file name from object name or ID
        name = rs.ObjectName(guid)
        if not name:
            name = str(guid)
        filename = os.path.join(folder, "{}.stl".format(name))

        # Prepare the command for STL export
        # -Export requires full path and Enter to accept defaults
        command = '-_Export "{}" _Enter _Enter'.format(filename)
        
        # Run the command in Rhino's context
        rs.Command(command, echo=False)

        print("Exported: {}".format(filename))

    print("Done exporting all selected objects.")

export_selected_as_stl()

