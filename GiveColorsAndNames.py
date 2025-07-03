import Rhino
import rhinoscriptsyntax as rs
import random

obj = rs.GetObjects("Select Objects...", preselect=True, select=True,)

user_input = rs.GetString("Enter a name for the object family:")
if user_input:
    print("You entered:", user_input)
else:
    print("User canceled input.")

def random_color(objects):
    minim = 0
    maxim = 255
    l = len(objects)
    colors = []
    for el in range(l+1):
        R = random.randint(minim,maxim)
        G = random.randint(minim,maxim)
        B = random.randint(minim,maxim)
        el = (R,G,B)
        colors.append(el)
    return colors

colors = random_color(obj)

for o, c in zip(obj, colors):
    rs.ObjectColor(o, color=c)

count = 0
for o in obj:
    rs.ObjectName(o, user_input+str(count))
    count += 1
