import scriptcontext as sc
import math
import System
import System.Collections.Generic
import Rhino
import clr
import rhinoscriptsyntax as rs
import measures


clr.AddReference("NorthernFlicker")
from NorthernFlicker.MVVM.Model import TimberElement

Attributes_of_TimberElement = [
    'ABox', 'ABoxDiagonal', 'Axes', 'BBoxVolume', 'Copy', 'Depth', 'Description',
    'Dispose', 'Duplicate', 'ElementSubType', 'ElementType', 'End', 'Equals', 'Extract',
    'FacesArea', 'FromJson', 'GetHashCode', 'GetType', 'InvalidLog', 'Length',
    'MemberwiseClone', 'MoveUserDataFrom', 'MoveUserDataTo', 'Name', 'NeedsUpdate',
    'OnDuplicate', 'OnPropertyChanged', 'OnTransform', 'Origin', 'OriginalLayerName',
    'PropertyChanged', 'Read', 'RefSurfaceIndex', 'RefSurfacePlane', 'ReferenceEquals',
    'ShouldWrite', 'ThrowOnInvalidPropertyName', 'ToJson', 'ToString', 'Transform',
    'TrySetBBoxVolume', 'TrySetElementSubType', 'TrySetElementType', 'TrySetEnd',
    'TrySetFacesArea', 'TrySetHeight', 'TrySetLength', 'TrySetOrigin', 'TrySetRefSurfacePlane',
    'TrySetVolume', 'TrySetWidth', 'Volume', 'Width', 'Write', '__class__', '__delattr__',
    '__doc__', '__enter__', '__exit__', '__format__', '__getattribute__', '__hash__',
    '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    '__sizeof__', '__str__', '__subclasshook__']


timber_colors = {
"HorizontalPanel": (255, 127, 0),
"VerticalPanel": (191, 63, 255),
"InclinedPanel": (191, 63, 63),
"Beam": (0, 0, 255),
"InclinedBeam": (0, 255, 0),
"Column": (255, 191, 0)
}


steel_colors = {
    "Beam": (205, 179, 139),
    "Column": (105, 105, 105),
    "InclinedBeam": (0, 105, 105),
    "HorizontalPanel": (205, 112, 84),
    "VerticalPanel": (205, 112, 84),
    "InclinedPanel": (205, 112, 84),
    "Connector": (0, 255, 255),
    "HorizontalPlate": (63, 191, 191),
    "VerticalPlate": (127, 255, 191),
    "InclinedPlate": (255, 0, 255)
}

def try_get_nf_data(rh_obj):
    if rh_obj and rh_obj.Geometry.HasUserData:
        user_data_list = rh_obj.Geometry.UserData
        for user_data in user_data_list:
            if isinstance(user_data, TimberElement):
                # Print all available attributes of TimberElement
                #attributes = dir(user_data)
                #print("Attributes of TimberElement:\n", attributes)
                
                ref_plane = user_data.RefSurfacePlane
                axis_lines = user_data.Axes                
                origin_pt = ref_plane.Origin
                #rs.AddPoint(origin_pt)
                len_pt = origin_pt + ref_plane.XAxis             
                dep_pt = origin_pt + ref_plane.ZAxis
                
                input_str = "{} {} {}".format(origin_pt, len_pt, dep_pt)
                
                rs.UnselectAllObjects()
                rs.SelectObject(obj_id)
                rs.Command("SetCadworkAxes " + input_str)
                rs.UnselectAllObjects()


                
                vo_dict = measures.Measures.VolumeMeasures(obj_id) 
                measure_dict = measures.Measures.LengthMeasures(obj_id)
                

                # Assuming measure_dict and vol_dict are already defined
                for k, v in vo_dict.items():
                    rs.SetUserText(obj_id, str(k), str(v))

                for k, v in measure_dict.items():
                    rs.SetUserText(obj_id, str(k), str(v))
                
                rs.SetUserText(obj_id,"GN_LOD_representation","300")

                if "GLU" in vo_dict["MA_Description"] and "Planar" in str(user_data.ElementType):
                    print ("You are trying to set a linear material on a planar element")
                    #return

                if "CLT" in vo_dict["MA_Description"] and ("Linear" in str(user_data.ElementType)):
                    print ("You are trying to set a planar material on a linear element")
                    #return


                if "STEEL" in vo_dict["MA_Description"]:
                    color = steel_colors.get(str(user_data.ElementSubType))
                    rs.ObjectColor(obj_id,color)
                else:
                    color = timber_colors.get(str(user_data.ElementSubType))
                    rs.ObjectColor(obj_id,color)
                
                
                
                
                rs.SetUserText(obj_id,"KS_SUB_ID",str(user_data.ElementSubType))
                #transform = rs.XformChangeBasis(rs.WorldXYPlane(),ref_plane)
                #rs.TransformObject(obj_id,transform,True)             
                

                

                
                # Assuming `user_data` is an object with attributes Width, Depth, Length, and BBoxVolume
                nf_data =   "ElementSubType : " + str(user_data.ElementSubType) + "\n" + \
                            "ElementType : " + str(user_data.ElementType) + "\n" + \
                            "OriginalLayerName : " + str(user_data.OriginalLayerName) + "\n" + \
                            "Width : " + str(user_data.Width) + "\n" + \
                            "Depth : " + str(user_data.Depth) + "\n" + \
                            "Length : " + str(user_data.Length) + "\n" + \
                            "BBoxVolume : " + str(user_data.BBoxVolume)
                return True, nf_data
    return False, "Failed to retrieve any NF data"

obj_ids = rs.GetObjects("Select objects")

no_data = []
if obj_ids:
    for obj_id in obj_ids:
        rs.SelectObject(obj_id)
        rs.Command("DestroyTimber")
        rs.Command("CreateTimber")
        obj = rs.coercerhinoobject(obj_id)
        if obj:
            success, message = try_get_nf_data(obj)
            if success:
                print(message)
            else:
                no_data.append(obj_id)
else:
    print("No objects selected.")

if no_data:
    rs.SelectObjects(no_data)
    rs.MessageBox("Active objects don't have NF data")
    
    
