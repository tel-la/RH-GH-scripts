import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import System

inputAll = rs.GetObjects(message="Select objects...",preselect=True,select=False)

Names = []

def get_centroid(geometry):
    # Use different logic based on geometry type
    if isinstance(geometry, (Rhino.Geometry.Curve, Rhino.Geometry.PolyCurve, Rhino.Geometry.LineCurve)):
        amp = Rhino.Geometry.AreaMassProperties.Compute(geometry)
        if amp != None:
            return amp.Centroid
        else:
            a = "ERROR1_curve+Polyc+LineC centroid calculation failed"
            return a


    elif isinstance(geometry, (Rhino.Geometry.Brep, Rhino.Geometry.Extrusion)):
        # First try volume centroid
        tmp = Rhino.Geometry.Brep.TryConvertBrep(geometry)
        vmp = Rhino.Geometry.VolumeMassProperties.Compute(tmp)
        if vmp != None:
            return vmp.Centroid
        else:
            # If volume fails, fall back to area
            amp = Rhino.Geometry.AreaMassProperties.Compute(geometry)
            if amp != None:
                return amp.Centroid
            else:
                a = "ERROR2_brep Centroid Calculation failed"
                return a

    # Optional: handle other types like Mesh, Surface, etc.
    elif isinstance(geometry, Rhino.Geometry.Mesh):
        amp = Rhino.Geometry.AreaMassProperties.Compute(geometry)
        if amp != None:
            return amp.Centroid
        else:
            a = "ERROR3_Mesh Centroid Calculation failed"
            return a
    
    return None

def GetObjectColor(obj_id):
    rhobj = sc.doc.Objects.Find(obj_id)
    if rhobj:
        attr = rhobj.Attributes
        if attr.ColorSource == Rhino.DocObjects.ObjectColorSource.ColorFromObject:
            return attr.ObjectColor
        elif attr.ColorSource == Rhino.DocObjects.ObjectColorSource.ColorFromLayer:
            layer = sc.doc.Layers[attr.LayerIndex]
            if layer: return layer.Color
    return System.Drawing.Color.Black  # Default fallback

if inputAll:
    sc.doc.Views.RedrawEnabled = False
    for i in inputAll:
        nn = rs.ObjectName(i)
        Names.append(nn)
        
        rhobj = sc.doc.Objects.Find(i)
        if not rhobj:
            continue

        geo = rhobj.Geometry
        centroid = get_centroid(geo)

        if type(centroid) == Rhino.Geometry.Point3d:
            color = GetObjectColor(i)
            text_dot = Rhino.Geometry.TextDot(nn, centroid)

            attr = Rhino.DocObjects.ObjectAttributes()
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            attr.ObjectColor = color
            attr.LayerIndex = sc.doc.Layers.CurrentLayerIndex

            sc.doc.Objects.Add(text_dot, attr)
        else:
            print("Could not compute centroid for object: {}".format(nn))
            print("ERROR! = {}".format(centroid))
            
    sc.doc.Views.RedrawEnabled = True
    sc.doc.Views.Redraw()

    print("Added {} tags.".format(len(Names)))
    print("These are the tags added: {}".format(Names))
else:
    print("Nothing Done! No object selected!")

