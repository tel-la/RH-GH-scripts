import rhinoscriptsyntax as rs
import random

def assign_random_display_colors():
    # Get selected objects
    objs = rs.GetObjects("Select objects to assign random display colors", preselect=True)
    if not objs:
        print("No objects selected.")
        return

    # Ask for confirmation if more than or equal to 100 objects
    if len(objs) >= 50:
        response = rs.MessageBox("You selected {} objects. Do you want to continue?".format(len(objs)), 4 | 32, "Confirm Large Selection")
        if response != 6:  # 6 means 'Yes'
            print("Operation cancelled by user.")
            return

    for obj in objs:
        # Generate random RGB color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)

        # Set object color
        rs.ObjectColor(obj, color)
        rs.ObjectColorSource(obj, 1)  # 1 = color by object

assign_random_display_colors()

